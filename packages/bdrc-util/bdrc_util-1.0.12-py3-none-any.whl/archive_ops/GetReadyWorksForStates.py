"""

"""
import argparse
from pathlib import Path

import sys
from BdrcDbLib.DbAppParser import DbArgNamespace, DbAppParser
from BdrcDbLib.DbApp import DbApp


from util_lib.utils import reallypath
from util_lib.version import ver_check


class GetReadyWorks(DbApp):
    """
    Records the migration of a volume
    """

    def __init__(self, db_config: str, state_text: str) -> None:
        """
        Constructor
        :param db_config: string describing section and config file location
        """
        super().__init__(db_config)
        self.state_text = state_text

    def get_works(self) -> []:
        """
        Fetch and package the list of works
        :return:
        """
        # Cough. Don't use the `drs` qualifier
        return self.CallAnySproc("GetDIPActivityCandidates", self.state_text)
        # eligible_works: [] = []
        # try:
        #     eligible_works = self.CallAnySproc("drs.GetDIPActivityCandidates", self.state_text)
        # except pymysql.Error:
        #     # CallAnySproc logs the error already, and raises it. Nothing to do here
        #     raise
        #
        # return eligible_works


class FullyQualifiedFileType(argparse.FileType):
    """
    Extends argparse.FileType. thanks to
    https://stackoverflow.com/questions/20934424/specify-file-extension-with-argparse/20940391#20940391
    """

    def __init__(self, mode='r', bufsize=-1):
        super(FullyQualifiedFileType, self).__init__(mode, bufsize)

    def __call__(self, string):
        if string != '-':
            string = str(reallypath(string))

        return super(FullyQualifiedFileType, self).__call__(string)


class GetReadyWorksParser(DbAppParser):
    """
    Parser for the Get Ready Works class
    Returns a structure containing fields:
    .drsDbConfig: str (from base class DBAppArgs)
    .next_state
    """

    def __init__(self, description: str, usage: str):
        """
        Constructor. Sets up the arguments for
        """
        super().__init__(description, usage)

        self._parser.add_argument("-a", "--activity_type", help="Next operation",
                                  choices=['DRS', 'IA', 'BUDA', 'DEEP_ARCHIVE', 'ARCHIVE', 'SINGLE_ARCHIVE',
                                           'SINGLE_ARCHIVE_REMOVED', 'GOOGLE_BOOKS'], required=True)

        self._parser.add_argument("-o", "--output", help="Optional output file name - default is stdout",
                                  required=False,
                                  type=FullyQualifiedFileType(mode='w'), default=sys.stdout)


def output(works_list: [], p_output: Path) -> None:
    """
    Prints the output to a csv file
    :param works_list: list of (work, path) tuples
    :param p_output: TextIOWrapper - stdout or a writable file
    :return: Nothing
    """
    import csv
    with p_output as csvfile:
        # Use the keys of the first dictionary as the headers
        d1: dict = works_list[0]
        fieldnames = d1.keys()
        _writer = csv.DictWriter(csvfile, fieldnames=fieldnames, lineterminator='\n')
        _writer.writeheader()
        for row in works_list:
            _writer.writerow(row)


def get_works_states_shell() -> int:
    """
    shell to get and parse arguments and return the list of works eligible for the state
    :return:
    """
    ver_check()
    sys.tracebacklimit = 0
    args: DbArgNamespace = GetReadyWorksParser("fetches works eligible for an operation", "").parsedArgs
    # aol = AOLogger.AOLogger("get_works_states_shell", args.log_level, Path(os.getcwd()))

    rc: int = 0  # hasn't failed yet
    # noinspection PyBroadException
    try:
        work_list: [] = GetReadyWorks(args.drsDbConfig, args.activity_type).get_works()

        # work_list is a list containing a list, which is the output we want, and a tuple,
        # which we dontcare
        if len(work_list) > 0 and type(work_list[0]) is list and len(work_list[0]) > 0:
            output(work_list[0], args.output)
    except:
        rc = 1
    return rc


if __name__ == "__main__":
    sys.exit(get_works_states_shell())
