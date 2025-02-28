"""
Save Work Facts
DBApp application to calculate, for a given path, which is assumed to contain a work:
 - the total number of files
-  the total size of the files
- And save them into the DRS database
"""
import logging
import os
import sys
from BdrcDbLib.DbApp import DbApp
from BdrcDbLib.DbAppParser import DbArgNamespace, DbAppParser
from pathlib import Path
from util_lib.utils import get_work_image_facts
from util_lib.version import ver_check


def existing_dir_path(string):
    if os.path.isdir(string):
        return string
    else:
        raise NotADirectoryError(string)


class SaveWorkFactsParser(DbAppParser):
    """

    """

    def __init__(self, description: str, usage: str):
        """
        Constructor. Sets up the arguments for
        """
        super().__init__(description, usage)
        self._parser.add_argument("source_dir", help="directory to get information and size",
                                  type=existing_dir_path)
        self._parser.add_argument("work_name", help="[opt] work name tag (leaf node of source_dir", nargs='?')

        if self.parsedArgs.work_name is None:
            self.parsedArgs.work_name = Path(self.parsedArgs.source_dir).name


class SaveWorkFacts(DbApp):

    def __init__(self, db_config: str) -> None:
        """
        Constructor
        :param db_config: string describing section and config file location
        """
        super().__init__(db_config)

    def save_work_facts(self, work_name: str, facts: ()) -> None:
        """
        Puts tuple into the database
        :param work_name:
        :param facts:
        [0]: sum of non-images files sizes
        [1]: count of non-images files
        [2]: sum of image files sizes
        [3] count of image files
        :return: none
        """
        #
        # marshal arguments for
        # PROCEDURE `UpdateWorkFacts`(
        # p_work_name varchar(45),
        # p_non_image_total_file_size BIGINT(20),
        # p_non_image_file_count BIGINT(20),
        # p_image_total_file_size BIGINT(20),
        # p_image_file_count BIGINT(20))
        self.CallAnySproc("UpdateWorkFacts", work_name, facts[0], facts[1], facts[2], facts[3])


def save_work_facts_shell() -> int:
    """
    Entry point for save work facts
    :return: 
    """
    ver_check()
    sys.tracebacklimit = 0
    args: DbArgNamespace = SaveWorkFactsParser("Saves the file size and counts for a work", "").parsedArgs

    rc: int = 0  # hasn't failed yet
    # noinspection PyBroadException
    try:
        facts: () = get_work_image_facts(args.source_dir)
        SaveWorkFacts(args.drsDbConfig).save_work_facts(args.work_name, facts)

    except:
        et = sys.exc_info()
        logging.error(f"Exception {et[0]} {et[1]} ")
        rc = 1
    return rc


if __name__ == '__main__':
    sys.exit(save_work_facts_shell())
