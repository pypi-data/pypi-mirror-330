"""
utilities shared by bdrc_utils
"""

import os
from typing import AnyStr, Any


def reallypath(what_path: AnyStr) ->  Any:
    """
    Resolves everything about the path
    :param what_path: Pathlike object
    :return: fully resolved path
    """
    from os import path

    # jimk #499: detect non-file paths and don't expand
    if what_path is None:
        return None
    # Regex more elegant, but need fast way to say UNCs must be at beginning
    if what_path.find('://') > 0 or what_path.startswith('//') or what_path.startswith('\\'):
        return what_path

    return path.realpath(path.expandvars(path.expanduser(what_path)))


def get_work_facts(a_path: str) -> (int, int):
    """
    Returns the sum of all file sizes and file count in a path
    64 bit python platforms (2 and 3)report sys.maxsize as
    9,223,372,036,854,775,807  or 9 exaBytes.
    """
    size: int = 0
    _count: int = 0
    from os.path import join, getsize
    for root, dirs, files in os.walk(a_path):
        size += sum(getsize(join(root, name)) for name in files)
        _count += len(files)
    return size, _count


def get_work_image_facts(a_path: str, image_folder_name: str = 'images') -> (int, int, int, int):
    """
    Returns a tuple of the:
    - non image total size
    - non image file count
    - images total file size
    - images total file count
    """
    _size: int = 0
    _count: int = 0
    _page_size: int = 0
    _page_count: int = 0
    from os.path import join, getsize
    for root, dirs, files in os.walk(a_path):
        if root.find(image_folder_name) > 0:
            _page_size += sum(getsize(join(root, name)) for name in files)
            _page_count += len(files)
        else:
            _size += sum(getsize(join(root, name)) for name in files)
            _count += len(files)
    return _size, _count, _page_size, _page_count


class VW:
    def __init__(self, token: str, token_sep: str = '-'):
        """
        splits a workgroup directory name into its component parts
        :param token: object to parse
        :param token_sep: separator character
        """
        parts = token.split(token_sep)
        self.work_rid = parts[0]
        self.ig_rid = parts[1]


# Set of AWS tag sets for works - hardwired
# See ~/dev/archive-ops/scripts/glacier/uploadWorkToGlacier.sh
# projectTag=$(work_s3_project $workRID)
# aws_object_info=$(aws s3api put-object-tagging \
#     --bucket "${glacierBucket}" \
#     --key "${aws_object_key}" \
#     --tagging "TagSet=[{Key=project,Value=${projectTag}}]")
# fi
# printf "$(log_date)[${ME}]:dip activity id:%s\n" \

# {'FPL':
#     {'Tagging': {
#         'TagSet': [
#             {
#                 'Key': 'project',
#                 'Value': 'FPL'
#             },
#         ]
#     }
#     }
# }
work_tag_sets: [] = [
    {
        'NLM':
            {
                'Key': 'project',
                'Value': 'NLM'
            },
        # can add other KV pairs if desired
    },
    {
        'FPL':
            {
                'Key': 'project',
                'Value': 'FPL'
            },
        'W8LS':
            {
                'Key': 'project',
                'Value': 'OwdyHay'
            },
    }
]

base_tag: {} = {
    'Tagging': {
        'TagSet': [
            {'Key': 'owner',
             'Value': 'ao'
             }
        ]
    }
}


class AOS3WorkTag:
    """
    Interface to work with tags for S3 objects that AO manages

    """

    def __init__(self, work_rid: str):
        """
        Populate for a work_rid
        :param work_rid:
        """
        self._work_rid = work_rid
        self._tag = self.json_tag()

    @property
    def tag(self) -> {}:
        return self._tag

    def json_tag(self) -> {}:
        """
        return an S3 'Tagging' dictionary for a work (like ~/dev/archive-ops/scripts/syncAnywhere/init_sys.sh)
        :return: dictionary of tags. This is a useful format for 'put_object_tagging'
        Input is work_tag_sets. Output is one or more  dictionaries with keys 'Key' and 'Value'
        """
        import copy
        rc_tag: dict = copy.deepcopy(base_tag)
        for work_tag_item in work_tag_sets:
            for work_tag_key, work_tag_value in work_tag_item.items():
                if work_tag_key in self._work_rid:
                    rc_tag['Tagging']['TagSet'].append(work_tag_value)
        return rc_tag

    @property
    def extra_args_tag(self) -> {}:
        """
        Returns the work tags formatted for use in the upload_object ExtraArgs
        :return:
        """
        td = self.tag['Tagging']['TagSet']

    # result = []
    # for dict_obj in list_of_dicts:
    # return '&'.join(result)
        result:[] = []
        # in
        for t_dict in td:
            key: str = t_dict['Key']
            val: str = t_dict['Value']
            key_value_pairs = [f'{key}={val}']
            result.append('&'.join(key_value_pairs))
        return {'Tagging' : f"{'&'.join(result)}"}


def tag_object(bucket: str, key: str, tag_set: []):
    """
    Add a set of tag to an AWS s3 object
    :param bucket:
    :param key:
    :param tag_set:
    :return:
    """
    import boto3
    s3 = boto3.client('s3')
    s3.put_object_tagging(Bucket=bucket, Key=key, Tagging=tag_set)


def transform_list_of_dicts(list_of_dicts):
    result = []
    for dict_obj in list_of_dicts:
        result.append('&'.join(f'{key}={value}' for key, value in dict_obj.items()))
    return '&'.join(result)
