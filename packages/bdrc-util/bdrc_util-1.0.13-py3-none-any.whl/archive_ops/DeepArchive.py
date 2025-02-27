#!/usr/bin/env python3
"""
Replacement for scripts/glacier/DIP-pump-uploadWorkToGlacier.py

2024 update:
archive-ops-187 wants to only upload all media for any image group that was updated in a given sync process (determined
by the input record's dip_external_id field).
At the same time, this program should have the flexibility to do a complete sync of all image groups and all other contents
of the work. The prior architecture of depending on structure in the 'comments' field is replaced by using an inventory of a sync
whose path is retrieved from the database.

The inventory field

As before, the structure is retained:
- each image group is inverted and uploaded into its own bag.zip
- everything else is assembled into its own bag.zip, which is named after the work_rid
"""
# import sys
# print(sys.path)
# import os
# print(os.environ['PYTHONPATH'])

import datetime
import re
from collections import namedtuple
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import Optional

from s3pathlib import S3Path

import archive_ops.api as AoApi
from archive_ops.DeepArchiveParser import DeepArchiveParser, DeepArchiveArgs
from archive_ops.DipLog import DipLog
from archive_ops.InvertWork import get_igs_for_invert, get_media_splits, invert_image_group_media
from util_lib.AOLogger import AOLogger
from util_lib.utils import *

GLACIER_KEY_ROOT: str = 'Archive'
BAGZIP_SUFFIX: str = '.bag.zip'
INVENTORY_IMAGE_GROUP_PARENTS: [str] = ['archive', 'images']

# -----------------     globals  -------------------
# noinspection PyTypeChecker
_log: AOLogger = None
# noinspection PyTypeChecker
dip_logger: DipLog = None

# This describes the fields in the results of GetDIPActivityCandidates.sql as
# written by get_works_for_activity
# Potential headers are:
# WorkName,path,create_time,update_time,dip_activity_type_id,
# dip_activity_start,dip_activity_finish,dip_activity_result_code,
# dip_source_path,dip_dest_path,work_id,dip_external_id,dip_comment
HEADERS = ['WorkName', 'path', 'dip_comment', 'dip_external_id']
InputDirectiveRow = namedtuple('Todo', HEADERS)  # Create a named tuple type


# -----------------     /globals  -------------------

def do_deep_archive_incremental(work_rid: str, archive_path: Path, inventory_path, bucket: str,
                                in_daemon: bool = False) -> int:
    """
    creates bag zips for all media in any image group mentioned in the manifest whose path
    is referenced in the sync_inventory table by the dip_external_id given
    :param work_rid: tag for work
    :param archive_path: root of media sources
    :param inventory_path: abspath of inventory of files to deep archive
    :param bucket: S3 bucket to upload to
    :param in_daemon: True if running in a daemon or on docker
    :return: 0 if successful, throws exception if not
    """
    work_tag: {} = AOS3WorkTag(work_rid).extra_args_tag

    # The name of the bag zip is the same as the inventory file
    archive_inventory_name: str = inventory_path.name

    # Get the files grouped by image groups, non-image groups from the inventory
    image_groups, non_image_groups = get_image_groups_from_inventory(inventory_path)

    # Get the media splits. For incremental upload, we're disregarding the rest,
    # and using the list of files in non_image_groups, which is the specific content
    # that was sync'd this sync
    media_with_image_group, _ = get_media_splits(archive_path, image_groups)

    # Invert and upload the image groups
    for ig, media_dirs in media_with_image_group.items():
        do_bag_upload(archive_path=archive_path, work_rid=work_rid, work_tag=work_tag, invert_context=(ig, media_dirs),
                      is_complete=False, bucket=bucket, in_daemon=in_daemon)

    # Upload the non-image group media
    # TODO: Copy the loose files into one parent, run do_bag_upload on that.
    # Problem to solve - do_bag_upload needs a distinct file name for an incremental bag

    do_bag_upload(archive_path=archive_path, work_rid=work_rid, work_tag=work_tag, as_is=non_image_groups,
                  is_complete=False, bag_file_name=archive_inventory_name, bucket=bucket,in_daemon=in_daemon)
    return 0


def do_deep_archive_complete(work_rid: str, archive_path: Path, image_groups: [str], bucket: str,
                             in_daemon: bool = False) -> int:
    """
    Splits a work archive
    :param work_rid:
    :param archive_path: data source
    :param image_groups: list of image groups to process
    :param bucket: S3 bucket to upload to
    :param in_daemon: True if running in a daemon or on docker
    :return:
    """
    # Get s3 archive home, under the key. See archive-ops/scripts/glacier/DIP-pump-uploadWorkToGlacier.sh

    work_tag: {} = AOS3WorkTag(work_rid).extra_args_tag

    # Different algorithm. We need to divide the work into two sets: 1 for the image groups which
    # are to be inverted, the other into a set of directories that will be copied as is.
    #
    media_with_image_group, non_image_groups = get_media_splits(archive_path, image_groups)

    for ig, media_dirs in media_with_image_group.items():
        do_bag_upload(archive_path=archive_path, work_rid=work_rid, work_tag=work_tag, invert_context=(ig, media_dirs),
                      bucket=bucket, in_daemon=in_daemon)

    if non_image_groups:
        do_bag_upload(archive_path=archive_path, work_rid=work_rid, work_tag=work_tag, as_is=non_image_groups,
                      bucket=bucket, in_daemon=in_daemon)

    return 0


def get_inventory_path(dip_external_id, db_conf: str) -> Optional[Path]:
    """
    Get the inventory path from the database
    """
    from BdrcDbLib.DbOrm.DrsContextBase import DrsDbContextBase
    from archive_ops.models.drsmodel import SyncInventory
    from sqlalchemy import select
    from sqlalchemy.exc import SQLAlchemyError

    # TODO: Use connection from args
    try:
        with DrsDbContextBase(db_conf) as drs:
            sess = drs.get_session()
            query = select(SyncInventory).where(SyncInventory.dip_external_id == dip_external_id)
            # Let it raise, if error
            result = sess.execute(query).scalar_one_or_none()
            if result:
                return Path(result.inventory_path)
            else:
                return None
    except SQLAlchemyError as e:
        _log.exception(e)
        raise e


def get_image_groups_from_inventory(inventory_path: Path) -> ([], [str]):
    """
    Get the image groups and the non-image group lists from the inventory file
    """
    with open(inventory_path, 'r') as inventory:
        lines = [line.strip() for line in inventory]

    # Get the image groups.
    raw_igs = set([line.split('/')[2] for line in lines])

    # filter in Only subdirs that begin with Workrid-Isomething or Workrid-4digits
    is_ig = lambda x: re.fullmatch(r"W\w+-(\d{4}|I\w+)", x)
    image_groups: [str] = list(filter(is_ig, raw_igs))

    # Now get everything that does not have any image group in its path - meta
    non_ig_elements: [str] = list(filter(lambda x: not any(ig in x for ig in image_groups), lines))

    return image_groups, non_ig_elements


# write a  function that takes a file path and copies it to a new location, preserving the directories in the input path
def copy_file_to_new_location(input_parent: Path, input_file_path: Path, new_location: Path):
    """
    Copy a file to a new location, preserving the directories in the input path
    Ex copy_file_to_new_location(Path('a/b/c'), 'a/b/c/d/e/f.txt', Path('x/y/z')) -> x/y/z/c/d/e/f.txt
    :param input_parent: parent Path of the file  - needed to preserve the directory structure in the output
    :param input_file_path: file to copy, relative to input_parent
    :param new_location: destination directory
    """
    import shutil
    # .parent is the full path to the directory containing the file, relative to its root
    target_dir: Path = new_location / input_file_path.parent
    target_dir.mkdir(parents=True, exist_ok=True)
    shutil.copy(input_parent / input_file_path, target_dir)


def do_bag_upload(archive_path: str,
                  work_rid: str,
                  work_tag: str,
                  bucket: str,
                  invert_context: () = None,
                  as_is: [str] = None,
                  is_complete: bool = True,
                  bag_file_name: str = None,
                  in_daemon: bool = False) -> None:
    """
    create a bag.zip for an image group or a list of files, and upload it to the archive
    :param bucket:
    :param archive_path: Parent of the source
    :param work_rid: Work name
    :param work_tag:
    :param bucket: S3 bucket to upload to
    :param as_is: list of separate files to include in an incremental upload bag
    :param is_complete: True if bagging a complete work, False if an incremental sync
    :param bag_file_name: name of the bag file to create
    :param in_daemon: True if running in a daemon or on docker
    :return:
    """
    import shutil
    from bag.bag_ops import bag

    if invert_context:
        dest_name, media_with_image_group = invert_context
    else:
        dest_name = bag_file_name if bag_file_name else work_rid

    s3_parent: S3Path = S3Path(bucket, AoApi.get_archive_location(GLACIER_KEY_ROOT, work_rid))
    # Make a temporary path for the output:
    exit_e: Exception = None
    with (TemporaryDirectory() as out_buffer):
        dip_id: str = ""
        failed_item_message: str = ""
        had_fail: bool = False
        ig_dest_path: S3Path = s3_parent / f"{dest_name}{BAGZIP_SUFFIX}"
        try:
            dip_id = open_log_dip(work_rid, archive_path, ig_dest_path.arn)
            out_path = Path(out_buffer)
            dest_path: Path = out_path / dest_name
            dest_path.mkdir(parents=True, exist_ok=True)
            bag_path: Path = out_path / "bag" / dest_name
            bag_path.mkdir(parents=True, exist_ok=True)
            bp_str = str(bag_path)

            # Invert the image group into the temp directory's work_folder
            if invert_context:
                invert_image_group_media(dest_path, media_with_image_group, dest_name)
            else:
                if is_complete:
                    # as_is is a list of directories
                    for dir_name in as_is:
                        complete_sub_path = dest_path / children_of(dir_name, work_rid)
                        complete_sub_path.mkdir(parents=True, exist_ok=True)
                        shutil.copytree(dir_name, complete_sub_path, dirs_exist_ok=True)
                else:
                    # as_is is a list of files
                    archive_parent: Path = Path(archive_path).parent
                    for file_name in as_is:
                        copy_file_to_new_location(archive_parent, Path(file_name), dest_path)
            bag(str(dest_path), bp_str, False, in_daemon, False)

            # Upload the inversion(s) to the archive. In this workflow, there should only be one
            for root, dirs, files in os.walk(bag_path):
                for file in files:
                    file_path = os.path.join(root, file)
                    #
                    # Handle subdirs by removing the top of tree
                    s3_object_name = file_path.replace(bp_str, "", 1).lstrip(os.sep)
                    s3_target: S3Path = s3_parent / s3_object_name
                    upload_file_to_s3_with_storage_class(file_path, s3_target.bucket, s3_target.key, 'STANDARD_IA',
                                                         work_tag)
        except Exception as e:
            failed_item_message = f"failed deep_archive {work_rid=} {dest_path=} {e=}"
            _log.exception(e)
            exit_e = e
        finally:
            if dip_id:
                update_log_dip(dip_id, 1 if had_fail else 0, failed_item_message)
            if exit_e:
                complain(f"{work_rid=}, {failed_item_message=}", 1, "do_deep_archive_complete")
                raise exit_e


def children_of(anchor: str, a_path: str) -> Path:
    """
    Returns a path relative to the work_rid in dir_name
    :param a_path:
    :param anchor:
    :return:
    """
    dir_path = Path(anchor)
    _d_parts = dir_path.parts
    _w_sub = _d_parts.index(a_path)
    sub_path = Path(*_d_parts[_w_sub + 1:])
    return sub_path


def upload_file_to_s3_with_storage_class(file_name, bucket, key=None, storage_class='STANDARD',
                                         tag_set: Optional[str] = None):
    """Upload a file to an S3 bucket with a specific storage class

    :param file_name: File to upload
    :param bucket: Bucket to upload to
    :param key: S3 object name. If not specified then file_name is used
    :param storage_class: Storage class to use for the object
    :return: True if file was uploaded, else False
    """

    # If S3 object_name was not specified, use file_name
    if key is None:
        key = file_name

    # Upload the file
    import boto3
    s3_client = boto3.client('s3')
    from botocore.exceptions import ClientError
    try:

        # handy: Can set tagging here:
        # https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html#S3.Client.put_object_tagging
        extra_args: {} = {'StorageClass': storage_class}
        if tag_set:
            # __/|\__ gh copilot
            extra_args.update(tag_set)
        import json
        extra_arg_string = json.dumps(extra_args)
        s3_client.upload_file(file_name, bucket, key, ExtraArgs=extra_args)
    except ClientError as e:
        _log.exception(e)
        complain(f"S3 upload {file_name=}, {bucket=}", 1, "upload_file_to_S3")
        raise e
    return True


def setup(args: DeepArchiveArgs):
    """
    Open resources
    :return: sets logger and dip_log context
    """

    import os
    global _log
    global dip_logger

    if not _log:
        os.makedirs(args.log_root, exist_ok=True)
        _log = AOLogger("Deep_Archive", args.log_level, Path(args.log_root), extra_quiet_loggers=['bagit'])
    if not dip_logger:
        import os
        # Need different path under docker
        db_cfg: [str] = args.drsDbConfig.split(':')

        # Still need to check, in case not run through argparse (i.e. db_config manually populated)
        if len(db_cfg) < 2:
            raise ValueError(f"Invalid db config {args.drsDbConfig} requires section:configFileName")

        # Adjust for running under docker - should be part of DbApps
        db_cfg[1] = '/run/secrets/db_apps' if os.path.exists('/run/secrets') else db_cfg[1]
        args.drsDbConfig = ':'.join(db_cfg)
        dip_logger = DipLog(args.drsDbConfig)


def displayed_comment(displayed, display_length: int = 108, illus_len: int = 20) -> str:
    """
    if displayed is > 108, trim to [1:20]"..."[-20:]
    :param display_length: invocation threshold
    :param illus_len:

    :param displayed:
    :return:
    """
    return f"{displayed[:illus_len]}...{displayed[-illus_len:]}" if len(displayed) > display_length else displayed


def update_log_dip(dip_log_id: str,
                   rc: int,
                   comment: str,
                   src_path: Optional[str] = None,
                   dest_path: Optional[str] = None,
                   ):
    """
    Closes a dip log entry
    :param dip_log_id: Key to locate entry
    :param comment: goes into database
    :param rc: activity return code for log
    :param src_path: source path (shouldn't usually update)
    :param dest_path: output path
    :return:
    """
    log_comment = displayed_comment(comment)
    _log.info(f'closing :{dip_log_id=}\trc:{rc=} {log_comment=}')
    return dip_logger.set_dip(
        # These are table PKs  - you can't update them
        activity_name=None,
        begin_t=None,
        work_name=None,
        # end keys
        # this is the identifying key
        dip_id=dip_log_id,
        # Tell the truth now
        end_t=datetime.datetime.now(),
        # The rest of these are optional
        s_path=src_path,
        d_path=dest_path,
        ac_result=rc,
        comment=f"{comment} log file {_log.log_file_name}",
        inventory=None)


def open_log_dip(work_rid: str, src_path: str, aws_object_path: Optional[str] = None) -> str:
    """
    Opens a dip log entry
    :return:
    :param work_rid: Key to locate entry
    :param src_path: goes into database
    :param aws_object_path: return code to log
    :return: dip_log_id
    """
    global dip_logger
    _log.info(f'opening :{work_rid=}\t{src_path=}\t{aws_object_path=}')

    # set_dip has no optional args:
    return dip_logger.set_dip(activity_name='DEEP_ARCHIVE',
                              begin_t=datetime.datetime.now(),
                              end_t=None,
                              s_path=src_path,
                              d_path=aws_object_path,
                              dip_id=None,
                              work_name=work_rid,
                              ac_result=None,
                              comment=None,
                              inventory=None)


# send a message to an AWS SNS topic
def send_sns(subject: str, message_str):
    """
    Send a message to an AWS SNS topic
    :return:
    """
    import os
    topic: str = os.getenv('AO_AWS_SNS_TOPIC_ARN')
    if topic:
        # Usually configured for default
        import boto3
        sns = boto3.client('sns').publish(TopicArn=topic, Message=message_str,
                                          Subject=subject)
    _log.info(f'{"[sns]" if topic else "[log]"} {subject}, {message_str}')


def complain(object_tag: str, rc: int, operation_tag: str, detail: str = None):
    d4_fstring = f"with {detail=}" if detail else ''""
    sns_fails_message_string = f"""
    The following work could not be uploaded to Glacier:
    {object_tag}
    .
    {operation_tag} returned with exit code {rc} {d4_fstring}.
    
    See log file {_log.log_file_name} for details.
    """

    send_sns("Glacier Upload Failure Report", sns_fails_message_string)


def get_header_indices(header: [str], columns: [str]) -> ():
    return tuple(map(lambda x: header.index(x), columns))


def read_csv(csv_path: Path) -> [InputDirectiveRow]:
    """
    Map a csv file into a list of named tuples.
    Note if the dip_comment field is used, the caller is responsible
    for escaping commas
    """
    import csv
    records: [InputDirectiveRow] = []
    with open(csv_path, 'r') as f:
        reader = csv.reader(f)  # Skip the header
        try:
            header = next(reader)

            h_map = get_header_indices(header, HEADERS)
            records = [InputDirectiveRow(*(row[i] for i in h_map)) for row in reader]
            # noinspection PyTypeChecker
            _log.debug(records)
        except StopIteration:
            _log.info(f"Empty file {csv_path}")

    return records


def deep_archive_shell():
    """
    Command line interface
    :return:
    """
    da_parser: DeepArchiveParser = DeepArchiveParser(usage="%(prog)s -i input_file",
                                                     description="Uploads a series of inverted zip files to backup "
                                                                 "bucket", )

    args: DeepArchiveArgs = da_parser.parsedArgs

    setup(args)
    _log.info(f"Arguments: {str(args)}")

    records: [InputDirectiveRow] = read_csv(args.input_file)
    for record in records:
        inventory_path: Path = None
        try:
            if args.incremental:
                # Get the inventory path from the database. If none, do a complete deep archive
                inventory_path = get_inventory_path(record.dip_external_id, args.drsDbConfig)
                if not inventory_path:
                    args.complete = True
                    args.incremental = False
                    _log.warn(
                        f"No inventory found for {record.WorkName} archive record: {record.dip_external_id[:6]}...  Running complete")

            if args.complete:
                image_group_list = get_igs_for_invert(record.WorkName)
                do_deep_archive_complete(record.WorkName, Path(record.path), image_group_list, args.bucket,
                                         args.in_daemon)
            else:  # args.incremental
                do_deep_archive_incremental(record.WorkName, Path(record.path), inventory_path, args.bucket,
                                            args.in_daemon)
                # image_group_list = get_igs_for_invert(record.WorkName, record.path, record.dip_external_id)

            # if there was a comment, we're only doing the image groups that were designated in the comment.
            # Otherwise, segment the work into:
            # - imagegroup + media tuples to be inverted and zipped separately
            # - everything else
            _log.info(f"Processing {record}")
        except Exception as e:
            dip_id = open_log_dip(record.WorkName, record.path)
            error_string: str = f"Failed to process {record=} {dip_id=} Exception {e=}"
            _log.error(error_string)
            update_log_dip(dip_id, 1, error_string)
            complain(record.WorkName, 1, "deep_archive_shell", error_string)
            raise e


if __name__ == '__main__':
    deep_archive_shell()
