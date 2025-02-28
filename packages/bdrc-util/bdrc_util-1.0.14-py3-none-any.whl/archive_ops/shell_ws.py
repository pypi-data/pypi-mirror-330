"""
Was Callable front-end to remote web service locators
Is now statically bound
"""
import argparse


from util_lib.version import ver_check
from archive_ops.Resolvers import Resolvers
from archive_ops.locators import *



# map of Operation id to field in the return json
Resolvers_map = {
    Resolvers.DEFAULT: r_divmod_nb_b_2,
    Resolvers.NULL: r_null,
    Resolvers.S3_BUCKET: r_s3,
    Resolvers.TWO: r_divmod_nb_b_2
}


def get_mappings(root: str, archive: str, resolver: Resolvers) -> str:
    """
    Calls the service
    :param resolver:
    :param root: parent of mapped site
    :param archive: archive name
    :param resolver: path resolution strategy
    :return: resolved path
    """
    return Resolvers_map.get(resolver)(root, archive)


def resolve_arguments(arg_obj: object) -> Resolvers:
    """
    Modifies internal arguments - if no default resolution mapping was requested, set resolution_type
    to default
    :param arg_obj: parseargs
    :return: modified arg_obj
    """

    # if they asked for default, use it, otherwise if they didn't ask for anything else
    # return the default
    if not arg_obj.default:
        arg_obj.default = not (arg_obj.two or arg_obj.s3 or arg_obj.null)

    if arg_obj.default:
        return Resolvers.DEFAULT
    if arg_obj.two:
        return Resolvers.TWO
    if arg_obj.s3:
        return Resolvers.S3_BUCKET
    if arg_obj.null:
        return Resolvers.NULL


def locate_archive():
    ver_check()
    parser = argparse.ArgumentParser(description="Provides mapping of archive names to paths")
    group = parser.add_mutually_exclusive_group(required=False)
    group.add_argument("-s", "--s3", action="store_true", help="Map to ENCODE_S3 storage (hexdigest[:2])")
    group.add_argument("-t", "--two", action="store_true",
                       help="Derive from last two characters of archive")
    group.add_argument("-n", "--null", action="store_true", help="No Derivation - return input as path")
    group.add_argument("-d", "--default", action="store_true", help="return Web Service default")
    parser.add_argument("root", type=str, help="parent of archive trees")
    parser.add_argument("archive", type=str, help="the name of the work")

    arg_obj: object = parser.parse_args()

    resolver: Resolvers = resolve_arguments(arg_obj)
    print(get_mappings(arg_obj.root, arg_obj.archive, resolver))


if __name__ == '__main__':
    locate_archive()
