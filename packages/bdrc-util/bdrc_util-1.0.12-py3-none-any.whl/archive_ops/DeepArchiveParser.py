#!/usr/bin/env python3
import os
from argparse import Namespace

from BdrcDbLib.DbAppParser import DbAppParser

# override with --bucket in DeepArchive call
DEFAULT_DEEP_ARCHIVE_BUCKET="glacier.archive.bdrc.org"

class DeepArchiveArgs:
    """
    For IDE usage - define the arg namespace, but in a way that allows
    export to other libs: See the DeepArchiveParser class and superclass.
    Any attribute not defined here, and added by the parser can be considered
    as "_private"
    """


    def __init__(self):
        self.log_level = None
        self.log_root = None
        self.input_file = None
        self.drsDbConfig = None
        self.incremental: bool = False
        self.complete: bool = False
        self.bucket = None
        self.in_daemon = False

    def __str__(self):
        return f"DeepArchiveArgs: {self.__dict__}"


class DeepArchiveParser(DbAppParser):
    # noinspection PyTypeChecker
    def __init__(self, description: str, usage: str, log_root: str = os.getcwd()):
        """
        Constructor. Sets up the arguments for DeepArchive(work, path, comment)
        """
        self._da_args = None

        super().__init__(description, usage)
        self._parser.add_argument("-l", "--log-level", dest='log_level', action='store',
                                  choices=['info', 'warning', 'error', 'debug', 'critical'], default='info',
                                  help="choice values are from python logging module")
        self._parser.add_argument("--log-root", dest='log_root', help="Parent of log files", required=False,
                                  default=log_root)
        self._parser.add_argument("-i", "--input-file", help="list of data to upload", required=True)
        level_group = self._parser.add_mutually_exclusive_group()
        level_group.add_argument("-I", "--incremental", action='store_true', help="incremental, use inventory referenced by file dip_external_id")
        level_group.add_argument("-C", "--complete", action='store_true', help="Archive the whole work")
        self._parser.add_argument("-b","--bucket", help="S3 bucket name", required=False, default=DEFAULT_DEEP_ARCHIVE_BUCKET)
        self._parser.add_argument("--in-daemon", help="if in docker or daemon - DO NOT USE ON COMMAND LINE. For api calls only", default=False, action='store_true', required=False)
        self._parser.set_defaults(incremental=True)

    @property
    def parsedArgs(self) -> DeepArchiveArgs:
        """
        Readonly, calc once
        parses the classes arguments, and returns the namespace
        :return:
        """
        # Enforce once only
        if self._da_args is None:
            self._da_args = DeepArchiveArgs()
            # noinspection PyTypeChecker
            xargs = self._parser.parse_args()
            #
            # Stupid hack to have to force mutually exclusive group members to a default
            if xargs.complete:
                xargs.incremental = False

            for attr, value in xargs.__dict__.items():
                setattr(self._da_args, attr, value)

        return self._da_args
