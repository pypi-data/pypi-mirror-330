#!/usr/bin/env python3

"""
Library routine to get volume information from BUDA
"""
import argparse
import logging

import os.path
import re
import requests
import sys
from requests import Response

IG_OLD_HACK_PREFIX = 'I'


def its_a_hack(test_str: str):
    """
    Returns true if the input is 4 digits, false otherwise
    :param test_str:
    :return:
    """
    hack_pattern = re.match('^\d{4}$', test_str)
    return hack_pattern is not None


def get_disk_ig_from_buda(image_group_id: str) -> str:
    """
    Copied from volume-manifest-builder.
    :param image_group_id:
    :type image_group_id: str
    Some old image groups in eXist **and BUDA** are encoded WorkRID-Innn, but their real name on disk is
    WorkRID-nnnn. this detects their cases, and returns the suffix of the disk folder they actually
    exist in. This is a gross hack, we should either fix the archive repository, or have the
    BUDA APIs adjust for this.
    """
    return _disk_ig_from_buda(image_group_id)


def _disk_ig_from_buda(image_group_id: str) -> str:
    """
    Copied from volume-manifest-builder.
    :param image_group_id:
    :type image_group_id: str
    Some old image groups in eXist **and BUDA** are encoded WorkRID-Innn, but their real name on disk is
    WorkRID-nnnn. this detects their cases, and returns the suffix of the disk folder they actually
    exist in. This is a gross hack, we should either fix the archive repository, or have the
    BUDA APIs adjust for this.
    """
    if 0 == len(image_group_id):
        return image_group_id

    pre, rest = image_group_id[0], image_group_id[1:]
    return rest if pre == IG_OLD_HACK_PREFIX and its_a_hack(rest) else image_group_id


def get_buda_ig_from_disk(disk_image_group_name: str):
    """
    Get the catalog image group name from the disk name
    :param disk_image_group_name: path to an image group directory
    :return: the image group reference, without the path, and without the workRID
    """
    return _buda_ig_from_disk(disk_image_group_name)


def _buda_ig_from_disk(disk_image_group_name: str):
    """
    Get the catalog image group name from the disk name
    :param disk_image_group_name: path to an image group directory
    :return: the image group reference, without the path, and without the workRID
    """

    # if there is no hyphen, the whole string is returned the first list position (list[0])
    with_hyphen: [] = disk_image_group_name.split('-')

    # get non-directory part of first segment after *the last* hyphen (or the whole thing if no hyphen at all)
    first_post_hyphen: str = os.path.basename(with_hyphen[len(with_hyphen) - 1])

    return IG_OLD_HACK_PREFIX + first_post_hyphen if its_a_hack(first_post_hyphen) else first_post_hyphen


def get_volumes_in_work(work_rid: str, transform_disk: bool = True) -> []:
    """
    BUDA LDS-PDI implementation
    :param: work_rid
    :return: list of dicts of 'vol_seq_in_work, vol_label' entries, where vol_label is the (potentially different)
    disk directory of an image group.
    """

    vol_info = []

    request_url: str = f'https://purl.bdrc.io/query/table/volumesForInstance'
    request_args = dict(R_RES=f"bdr:{work_rid}", format="json",pageSize=500)

    # pattern from https://www.programcreek.com/python/example/68989/requests.HTTPError
    try:
        buda_vol_resp: Response = requests.get(request_url, request_args)
    except requests.HTTPError as e:
        if e.response.status_code == 404:
            return None
        else:
            raise

    vol_ids = buda_vol_resp.json()
    for vol_id in vol_ids['results']['bindings']:
        _vol_names = vol_id['volid']['value'].split('/')
        _vol_name = _vol_names[len(_vol_names) - 1]
        vol_info.append(dict(vol_seq_in_work=int(vol_id['volnum']['value']),
                             vol_label=_disk_ig_from_buda(_vol_name) if transform_disk else _vol_name))

    return vol_info


def get_ig_folders_from_igs():
    """
    Call this functionality from the command line.
    Usage disk_igs_for_work worknum [anystring]
    If [anystring] is present, the image group is NOT
    processed through the old Innnn hack
    :return:
    """

    # second argument?
    use_old_hack: bool = len(sys.argv) <= 2
    vols = [x['vol_label'] for x in get_volumes_in_work(sys.argv[1], use_old_hack)]
    print('\n'.join(map(str, vols)))


def buda_ig_from_disk():
    """
    Given an image group folder's disk name, derive its image group name
    per the BUDA catalog
    :return:
    """
    # Anything to do?
    if len(sys.argv) == 1:
        return

    print(_buda_ig_from_disk(sys.argv[1]))


def _get_if(_dict: {}, key: str, default: object) -> object:
    return default if key not in _dict.keys() else _dict[key]


def _get_image_count(ig_id: str, bottom: bool = False):
    """
    Gets the image count
    :param ig_id: image group - note. must not be in the disk format
    :return: syncd pages, if any. Disregards count of bdrc header pages.
    """

    # Bzah - using format = json, gets a weird number
    request_url: str = f'https://purl.bdrc.io/query/graph/IIIF_volumeInfoGraph'
    request_args = dict(R_RES=f"bdr:{ig_id}")  # , format="json"

    # pattern from https://www.programcreek.com/python/example/68989/requests.HTTPError
    try:
        buda_vol_resp: Response = requests.get(request_url, request_args)
    except requests.HTTPError as e:
        if e.response.status_code == 404:
            return None
        else:
            raise

    vol_ids = buda_vol_resp.json()

    # Why do only failures contain status?
    # If this failed because the IG wasn't found, try using the Innnn hack
    if 'status' in vol_ids.keys() and vol_ids['status'] == 404:
        if not bottom:
            # the second parm means failure is death
            return _get_image_count(_buda_ig_from_disk(ig_id), True)

    meat = (vol_ids['@graph'][1])
    header_pages = _get_if(meat, 'volumePagesTbrcIntro', 0)
    total_pages = _get_if(meat, 'volumePagesTotal', 0)

    return header_pages + total_pages


def disk_ig_from_buda():
    if len(sys.argv) == 1:
        return
    print(_disk_ig_from_buda(sys.argv[1]))


def get_image_count():
    argp = argparse.ArgumentParser(description="Gets the count of images in an image group.")
    argp.add_argument("ig_id", type=str, help="image group id")
    arg_ns = argp.parse_args()
    print(_get_image_count(arg_ns.ig_id))


if __name__ == "__main__":
    #     disk_ig_from_buda()
    use_old_hack: bool = len(sys.argv) <= 2

    logging.error(get_volumes_in_work('W1PD96185', use_old_hack))
    # print(_disk_ig_from_buda("I0957"))
    # print(_disk_ig_from_buda('I8CZ673'))
    # _get_image_count('0957')
    # _get_image_count('I8CZ673')
