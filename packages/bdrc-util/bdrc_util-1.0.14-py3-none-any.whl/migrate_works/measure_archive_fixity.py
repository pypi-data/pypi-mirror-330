#!/usr/bin/env python3

#
# Validates a zip of a work against the live contents of the work
#
# Thank you chatGPT
import zipfile
import os
import sys
import argparse
from util_lib.AOLogger import AOLogger
from pathlib import Path
#
# import pydevd_pycharm
#
# pydevd_pycharm.settrace('sattva', port=9535, stdoutToServer=True, stderrToServer=True)


ao_log: AOLogger

# os.getenv key containing log home
RUN_LOG_ENV: str = "ARCHIVE_MIGRATION_LOG_HOME"

# region utils
def must_exist_file(path: str):
    """
    Common utility. Returns if file exists, raise otherwise
    :param path: tested path. Resolved by bdrc lib
    :return:
    """
    from util_lib.utils import reallypath

    full_path = reallypath(path)
    if not os.path.exists(full_path):
        raise argparse.ArgumentTypeError(f"{full_path} not found")
    else:
        return full_path


def build_file_list(src_tree) -> set:
    # get the set of directory files
    directory_files = set()
    for root, dirs, files in os.walk(src_tree):
        for file in files:
            file_path = os.path.join(root, file)
            directory_files.add(os.path.relpath(file_path, src_tree))
        for dir in dirs:
            dir_path = os.path.join(root, dir)
            directory_files.add(os.path.relpath(dir_path, src_tree) + '/')
    return directory_files


# endregion

# region tests


def contents_compare(zip_p: Path, src_tree: Path) -> {}:
    """
    returns tuple of image count status
    :param zip_p:
    :param src_tree:
    :return:
    """

    # create a ZipFile object and get the list of archive files
    zip_archive = zipfile.ZipFile(zip_p)
    archive_files = set(zip_archive.namelist())

    ao_log.debug(f"remote archive {str(zip_p)} has {len(archive_files)} files and folders")

    directory_files = build_file_list(src_tree)

    ao_log.debug(f"local {str(src_tree)}  has {len(directory_files)}")
    # compare the sets of archive and directory files
    extra_files = archive_files - directory_files
    missing_files = directory_files - archive_files

    # print the comparison results
    if extra_files:
        ao_log.error(f'The archive contains {len(extra_files)} extra files:')
        ao_log.error('\n'.join(sorted(extra_files)))

    if missing_files:
        ao_log.error(f'The archive is missing {len(missing_files)} files:')
        ao_log.error('\n'.join(sorted(missing_files)))

    return {'zip content count': len(archive_files),
            'disk content count': len(directory_files),
            'file_set_ok': 'No' if missing_files or extra_files else 'Yes'}


def attr_compare(zip_p: Path, src_tree: Path) -> bool:
    """
    returns if the input zip and the source files all have the same last mod time and size

    :param zip_p:
    :param src_tree:
    :return:
    """

    # create a ZipFile object and get the list of archive files
    zip_archive = zipfile.ZipFile(zip_p)
    archive_files: [zipfile.ZipInfo] = zip_archive.infolist()

    directory_files = list(build_file_list(src_tree))

    for df in directory_files:
        print(archive_files)


# endregion

# region main

def maf_main():
    """
    Shell for running archive integrity check
    :return:
    """
    global ao_log

    # specify the zip archive and directory paths
    ap = argparse.ArgumentParser()
    ap.add_argument("-l", "--log_home", help="Where logs are stored",
                      default=os.getenv(RUN_LOG_ENV))
    ap.add_argument("zip", help="remote zip file to test", type=must_exist_file)
    ap.add_argument("work_tree_path", help="source tree to test", type=must_exist_file)
    arg_ns = ap.parse_args()

    ao_log = AOLogger(Path(__file__).stem, 'info', arg_ns.log_home)
    zip_file_path: Path = Path(arg_ns.zip)
    directory_path: Path = Path(arg_ns.work_tree_path)

    try:
        contents_compare_info: {} = contents_compare(zip_file_path, directory_path)
        ao_log.info(f"zip file:{arg_ns.zip}. Contents comparison: {contents_compare_info}")
        #  attr_compare(zip_file_path, directory_path)
        sys.exit(0 if contents_compare_info['file_set_ok'] else 1)
    except zipfile.BadZipFile as bzf:
        ao_log.exception(f"{arg_ns.zip} is not a valid zip file")
        sys.exit(1)


if __name__ == '__main__':
    maf_main()

# endregion
