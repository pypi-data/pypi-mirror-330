from BdrcDbLib.DbAppParser import DbAppParser, str2datetime, DbArgNamespace

from util_lib.utils import reallypath


class DipLogParser(DbAppParser):
    # noinspection PyTypeChecker
    def __init__(self, description: str, usage: str):
        """
        Constructor. Sets up the arguments for
        INSERT INTO `drs`.`dip_activity`
        (
        `dip_activity_type_id`,
        `dip_activity_start`,
        `dip_activity_end`,
        `dip_activity_success`,
        `dip_source_path`,
        `dip_dest_path`,

        `dip_external_id`)

        """

        src_path_help: str = "Source path (optional) - string"
        dest_path_help: str = "Destination path (optional) - string"

        super().__init__(description, usage)
        self._parser.add_argument("-l", "--log-level", dest='log_level', action='store',
                                  choices=['info', 'warning', 'error', 'debug', 'critical'], default='info',
                                  help="choice values are from python logging module")

        self._parser.add_argument("-a", "--activity_type", help="Activity type",

                                  required=False)

        self._parser.add_argument("-w", "--work_name", help="work being distributed", required=False)
        self._parser.add_argument("-i", "--dip_id", help="ID to update", required=False)
        self._parser.add_argument("-r", "--activity_return_code", help="Integer result of operation.", type=int,
                                  required=False)
        self._parser.add_argument("-b", "--begin_time", help="time of beginning - ')"
                                                             "yyyy-mm-dd hh:mm:ss bash format date +\'%%Y-%%m-%%d "
                                                             "%%R:%%S\'",
                                  required=False, type=str2datetime)
        self._parser.add_argument("-e", "--end_time", help="time of end.Default is invocation time. "
                                                           "yyyy-mm-dd hh:mm:ss bash format date + \'%%Y-%%m-%%d "
                                                           "%%R:%%S\'",
                                  required=False, type=str2datetime)
        self._parser.add_argument("-c", "--comment", help="Any text up to 4GB in length", required=False)
        self._parser.add_argument("-s", "--dip_source_path", help=src_path_help, required=False)
        self._parser.add_argument("-t", "--dip_dest_path", help=dest_path_help, required=False)
        self._parser.add_argument("-L", "--resolve-sym-links",
                                  help="True to resolve file paths, false to accept input as is", required=False,
                                  default=False, action='store_true')
        self._parser.add_argument("-n", "--inventory", help="path to inventory (only used for ARCHIVE)", required=False)
        self._parser.add_argument("source_path", help=src_path_help, nargs='?')
        self._parser.add_argument("dest_path", help=dest_path_help, nargs='?')

        self.validate()

        self.adjust_begin()

    def validate(self):
        """
        Test Arguments
        :return: Nothing. Raise ValueError if invalid args
        """
        pa: DbArgNamespace = self.parsedArgs

        # You can refer to the work either by the tuple of (.activity_type, .work_name, .begin_time) OR
        # .dip_id.

        if not pa.dip_id:
            if not pa.begin_time \
                    or not pa.work_name \
                    or not pa.activity_type:
                raise ValueError(
                    "LOG_DIP: When --dip_id is not given, --begin_time, --work_name, and --activity_type must be "
                    "given.")

        if pa.end_time is not None and pa.begin_time is not None and pa.end_time < pa.begin_time:
            raise ValueError("LOG_DIP: end time before begin time")

        # If the positional arguments were given, and the flag arguments were not, copy the positionals
        # into the flag arguments
        # Handle "-s sArgGiven" positionalFileArgGiven --> dest gets positional File Arg

        # archive-ops-1060: For docker, we can't use the hardcoded default db descriptor, we must use the one
        # that the user provides on the command line to get the current set of activities. This stanza moves
        # the arg activities validation here, after the db config is parsed.
        if pa.activity_type:
            rpa = pa.activity_type.upper()
            allowed_activities: [] = [x.upper() for x in self.activities(pa.drsDbConfig)]
            if rpa not in allowed_activities:
                raise ValueError(f"LOG_DIP: activity_type {rpa} must be one of {allowed_activities}")

        if pa.dip_source_path is not None and pa.dip_dest_path is None and pa.dest_path is None:
            pa.dip_dest_path = pa.source_path

        if pa.dip_source_path is None and pa.source_path is not None:
            pa.dip_source_path = pa.source_path
        if pa.dip_dest_path is None and pa.dest_path is not None:
            pa.dip_dest_path = pa.dest_path

        if pa.resolve_sym_links:
            pa.dip_source_path = reallypath(pa.dip_source_path)
            pa.dip_dest_path = reallypath(pa.dip_dest_path)

        # jimk archive-ops-1087. warn if inventory given and op is not BUDA

    def adjust_begin(self):
        """
            Cleanup for beginning and end times. ???
            """
        pa: DbArgNamespace = self.parsedArgs
        has_begin: bool = pa.begin_time is not None
        has_end: bool = pa.end_time is not None
        has_id: bool = pa.dip_id is not None

        # rules:  if begin, don't need end or id.
        # you have to have an id when:
        #   - ending
        #   - no beginning?
        if has_end and not has_begin and not has_id:
            self._parser.error("end time requires begin time or id")

    def activities(self, db_config: str) -> [str]:
        """
        Legal list of activities
        :param db_config: BDRC database configuration
        :return:
        """
        from BdrcDbLib.DbOrm.DrsContextBase import DrsDbContextBase
        from BdrcDbLib.DbOrm.models.drs import DipActivities
        labels: [] = []

        with DrsDbContextBase(db_config) as ctx:
            labels = [x[0] for x in ctx.session.query(DipActivities.label).all()]
        return labels
