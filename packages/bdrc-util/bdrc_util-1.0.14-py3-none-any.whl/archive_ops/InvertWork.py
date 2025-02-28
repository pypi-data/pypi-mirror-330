#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue 16 Apr 2024 jimk
API to invert a work folder from
WorkRid/
+--------- images/
            +------- image_group_1/
                    +------- file_1-*
            +------- image_group_2/
                    +------- file_2-*

+--------- archive/
            +------- image_group_1/
                    +------- file_1-*
            +------- image_group_2/
                    +------- file_2-*
+---------- sources/
            +--- something_else/
                +--- se0001.txt
                +--- se0002.txt
                +--- se0003.txt
...
to
WorkRid/
+--------- image_group_1/
            +------- images/
                    +------- file_1-*
            +------- archive/
                    +------- file_1-*

+--------- image_group_2/
            +------- images/
                    +------- file_1-*
            +------- archive/
                    +------- file_1-*
+---------- sources/
            +--- something_else/
                +--- se0001.txt
                +--- se0002.txt
                +--- se0003.txt

** The folders that contain image groups are discovered at run time, and
are not presumed to have specific names. Folders that do NOT contain folders named after image groups
are not inverted.
"""
import os
from pathlib import Path

import archive_ops.InvertWorkException as IWE


def test_rc_igs(rc_igs: [str], work_path: str) -> None:
    """
    Ensure that each image group name is somewhere under the work_path.
    :param rc_igs:
    :param work_path:
    :return:
    """
    ig_flags: {} = {}
    import os
    for _, dirs, files in os.walk(work_path):
        for ig in rc_igs:
            if ig in dirs:
                ig_flags[ig] = True
    # the rc_igs list must have a 1:1 correspondence with the keys of the ig_flag dict
    if len(ig_flags.keys()) != len(rc_igs):
        raise IWE.InvertWorkException(
            f"image group source is comments: {rc_igs=}, and not all given image groups were found in {work_path}")


def get_igs_for_invert(work_rid: str) -> [str]:
    """
    return a list of comma separated tokens (representing image group names) from BUDA's catalog
    database
    :param work_rid: Work name
    :return: The list of directory names for image groups in the BUDA catalog (should be in AoApi
    """
    import archive_ops.api as AoApi

    rc_igs: [] = []
    # The directory names on disk are {work_rid-image_group_rid}
    rc_igs = [f"{work_rid}-{ig['vol_label']}" for ig in
              AoApi.get_volumes_in_work(work_rid=work_rid, transform_disk=True)]

    return rc_igs


def get_media_splits(search_work: Path, image_groups: [str]) -> ({},[str]):
    """
    :param search_work:
    :param image_groups:
    :return: Two lists of top level directories: 
    - media, meaning a top level directory that has child folders
    - a list of all the other directories under search_path
    """
    #
    # Need uniqueness
    matching_dirs: set = set()
    # iterdir only searches immediate descendants
    for media_dir in search_work.iterdir():
        if not media_dir.is_dir():
            continue
        for ig_dir in media_dir.iterdir():
            if ig_dir.is_dir() and any(s == ig_dir.name for s in image_groups):
                matching_dirs.add(str(search_work / media_dir.name / ig_dir.name))

    # Now, build the list of the deepest directories that are not in the matching_dirs
    non_matching_dirs = get_other_dirs(search_work, matching_dirs)

    # build a dictionary of { 'image_group' :[paths to the image group] }
    # -0GHC - wrote this myself!
    ig_matching_dirs: {} = {ig: [Path(path_to_ig) for path_to_ig in matching_dirs if ig in path_to_ig] for ig in image_groups}
    return ig_matching_dirs, non_matching_dirs


# search a list of strings for a key, and create a dictionary entry that contains the key and the list of strings that contain that key
def get_matching_dirs(search_work: Path, image_groups: [str]) -> {}:
    """
    :param search_work:
    :param image_groups:
    :return: A dictionary of { 'image_group' :[paths to the image group] }
    """
    matching_dirs: {} = {
        ig: [str(search_work / media_dir.name / ig_dir.name) for media_dir in search_work.iterdir() for ig_dir in
             media_dir.iterdir() if ig_dir.is_dir() and ig_dir.name == ig] for ig in image_groups}
    return matching_dirs


def get_non_child_dirs(_all:[str], _refs:[str]) ->[str]:
    """
    Return a list of directories that are not children of any of the directories in _refs
    :param _all: universe
    :param _refs: filter
    :return:  all elements of universe which are not children of _refs
    """
    non_child_dirs = []
    for dir_all in _all:
        if not any(os.path.commonpath([dir_all, dir_ref]) == dir_ref for dir_ref in _refs):
            non_child_dirs.append(dir_all)
    return non_child_dirs


def get_other_dirs(parent_dir: Path, initial_dirs: set) ->[str]:
    """
    :param parent_dir:
    :param initial_dirs:
    :return:
    """
    #
    #     all_dirs = {child for child in parent_dir.iterdir() if child.is_dir()}
    all_dirs = {dir_path for dir_path, _, _ in os.walk(parent_dir)}
    #
    # Need to get rid of parents, or they get put in both image groups and other lists
    all_dirs = set(get_deepest_dirs(all_dirs))
    other_dirs = get_non_child_dirs(list(all_dirs - initial_dirs), list(initial_dirs))
    return get_deepest_dirs(other_dirs)


def get_deepest_dirs(dir_list: [str]) -> [str]:
    """
    Returns the deepest directories in a list of directories
    +5 GHC
    :param dir_list:
    :return:
    """
    deepest_dirs = []
    for dir in dir_list:
        if not any(other_dir != dir and other_dir.startswith(dir) for other_dir in dir_list):
            deepest_dirs.append(dir)
    return deepest_dirs


def invert_image_group_media( output_root: Path, source_dirs: [Path],
                             subject_image_group: str):
    """
    Inverts the media types and image groups in a tree
    :param output_root: Destination. Must exist on call
    :param source_dirs: list full paths that are to be inverted ['/xxx/images/image_group', '/xxx/archive/image_group']
    :param subject_image_group: the image group we're interested in
    :return: A modified folder structure of input_root: Note that 'sources' is unmodified
    because it is not in 'media_types'
    Ex:  src:
    Work_root (input_root)
    +--- images
    |    +--- w1-ig1
    |    |    +--- ig10001.txt
    |    |    +--- ig10002.txt
    |    +--- w1-ig2
    |    |    +--- ig20001.txt
    |    |    +--- ig20002.txt
    +---  archive
    |    +--- w1-ig1
    |    |    +--- ig10001.txt
    |    |    +--- ig10002.txt
    |    +--- w1-ig2
    |    |    +--- ig20001.txt
    |    |    +--- ig20002.txt
    +--- sources
    |    +--- something_else
    |    |    +--- se0001.txt
    |    |    +--- se0002.txt
    |    |    +--- se0003.txt

    Output:
    Work_root
    +--- w1-ig1
    |       +--- images
    |    |    |    +--- ig10001.txt
    |    |    |    +--- ig10002.txt
    |       +--- archive
    |    |    |    +--- ig10001.txt
    |    |    |    +--- ig10002.txt    
    +--- w1-ig2
    |       +--- images
    |    |    |    +--- ig20001.txt
    |    |    |    +--- ig20002.txt
    |       +--- archive
    |    |    |    +--- ig20001.txt
    |    |    |    +--- ig20002.txt

    """
    # ChatGPT +3
    import shutil

    # for each # for each child directory in the input root
    output_root.mkdir(parents=True, exist_ok=True)

    for media_path in source_dirs:
        # this is the inversion
        ig_dest_path: Path = output_root / subject_image_group / media_path.parent.name
        shutil.copytree(media_path, ig_dest_path)
        # for ig_media in os.listdir(media_path):
        #     ig_media_path = os.path.join(media_path, ig_media)

    # for child_dir in os.listdir(input_root):
    #     cdp: Path = Path(child_dir)
    #     if cdp.name in source_dirs:
    #         media_name = cdp.name
    #         # for media in media_types:
    #         media_path = os.path.join(input_root, media_name)
    #         if os.path.exists(media_path):
    #             for item in os.listdir(media_path):
    #                 item_path = os.path.join(media_path, item)
    #                 if os.path.isdir(item_path) and subject_image_group and item in subject_image_group:
    #                     # This is the step that transforms archive/images to images/archive
    #                     new_path = os.path.join(output_root, item, media_name)
    #                     # copytree creates the new path
    #                     shutil.copytree(item_path, new_path)

        # This step was creating multiple copies of non-image groups in each image group
        # else:
        #     # plain old directory
        #     if not filter:
        #         shutil.copytree(os.path.join(input_root, child_dir), os.path.join(output_root, child_dir))
