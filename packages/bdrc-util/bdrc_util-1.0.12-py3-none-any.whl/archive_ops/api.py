"""
Utility facade
"""
from util_lib import GetFromBUDA as ao_buda
from archive_ops.Resolvers import Resolvers
from archive_ops.shell_ws import get_mappings


def get_archive_location(root: str, resource: str, resolver: Resolvers = Resolvers.TWO) -> str:
    """
    Resolves the Archive location of a resource. 
    :param root: parent of mapped resource
    :param resource: RID, typically work RID 
    :param resolver: path resolution strategy. Defaults to local archive. you can
    access S3 resources by:
    from archive_ops.Resolvers import Resolvers
    get_archive_location("Works", "W1FPL2251", Resolvers.S3_BUCKET)
    :return: string of resolved path
    """
    return get_mappings(root, resource, resolver)


def get_s3_location(root: str, resource: str, resolver: Resolvers = Resolvers.S3_BUCKET) -> str:
    """
    Resolves the S3 location of a resource.
    :param root: parent of mapped resource
    :param resource: RID, typically work RID
    :param resolver: path resolution strategy. Defaults to S3
    from archive_ops.Resolvers import Resolvers
    get_archive_location("Works", "W1FPL2251", Resolvers.S3_BUCKET)
    :return: string of resolved path
    """
    return get_mappings(root, resource, resolver)


def get_buda_ig_from_disk(disk_ig_name: str) -> str:
    """
    Returns the BUDA catalog name of a disk image
    :param disk_ig_name: the name of a disk folder containing an archive
    :return:
    """
    return ao_buda.get_buda_ig_from_disk(disk_ig_name)


def get_disk_ig_from_buda(buda_ig_name: str) -> str:
    """
    Returns the disk repository name of a BUDA image group catalog
    :param buda_ig_name: the name of an image group in the BUDA catalog
    :return:
    """
    return ao_buda.get_disk_ig_from_buda(buda_ig_name)


def get_volumes_in_work(work_rid: str, transform_disk: bool = True) -> []:
    """
    BUDA LDS-PDI implementation
    :param: work_rid
    :return: list of dicts of 'vol_seq_in_work, vol_label' entries, where vol_label is the (potentially different)
    disk directory of an image group.
    """
    return ao_buda.get_volumes_in_work(work_rid, transform_disk)

