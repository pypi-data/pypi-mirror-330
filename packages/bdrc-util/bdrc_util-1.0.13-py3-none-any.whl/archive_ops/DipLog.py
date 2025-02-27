import sys
from datetime import datetime
from typing import Optional

import BdrcDbLib.DbApp
from BdrcDbLib.DbAppParser import DbArgNamespace
from BdrcDbLib.DbApp import DbApp

from archive_ops.DipLogParser import DipLogParser

# SqlAlchemy structure from ao-workflows/airflow-docker/dags/extras.py
from BdrcDbLib.SqlAlchemy_get_or_create import get_or_create

from BdrcDbLib.DbOrm.DrsContextBase import DrsDbContextBase

from archive_ops.models.drsmodel import SyncInventory
# Constants
from util_lib.version import ver_check

DIP_ID_KEY: str = "DIP_ACTIVITY_ID"


class DipLog(DbApp):
    """
    Send a log entry to the database
    """

    def __init__(self, db_config: str):
        super().__init__(db_config)

    def set_dip(self, activity_name: Optional[str],
                begin_t: Optional[datetime],
                end_t: Optional[datetime],
                s_path: Optional[str],
                d_path: Optional[str],
                work_name: Optional[str],
                dip_id: Optional[str],
                ac_result: Optional[int],
                comment: Optional[str],
                inventory: Optional[str]) -> str:
        """
        Call the SQL and retrieve the dip activity ID it generated :param activity_name: the type of activity (e.g.
        BUDA, DEEP_ARCHIVE) :param begin_t: begin time :param end_t: end time or null :param s_path: source path
        :param activity_name: a value in dip_activity_types.dip_activity_types_label
        :param begin_t: begin time
        :param end_t: end time
        :param s_path: source path
        :param d_path: destination path
        :param work_name: workRID
        :param dip_id: NONE to create a new DIP log entry
        if an existing (work_name, start_time, activity_name) is given , the SPROC updates it and returns the
        existing dip_id
        :param ac_result: result of operation, if known.
        :param comment: Any extra text
        :return: The value of DIP_ACTIVITY_ID from the result set returned
        """

        # protect call against SQL 1213 Deadlock found when trying to get lock; try restarting transaction

        query_result_list: list[dict] = self.CallAnySproc('SetWorkDip', work_name, begin_t, end_t, activity_name,
                                                          ac_result, s_path, d_path,
                                                          dip_id, comment)
        # Query result is a list of lists of dictionary entries
        activity_id: str = ""
        for rs_list in query_result_list:
            for ww in rs_list:
                if DIP_ID_KEY in ww.keys():
                    activity_id = ww[DIP_ID_KEY]
                    break
            if len(activity_id) > 0:
                break

        # jimk archive-ops-1087. Put the archive inventory into the database
        if inventory:

            # How awkward. The Base object doesn't retain the string that creates its internal dbconfig object.
            with DrsDbContextBase(db_config_str(self.dbConfig)) as drs:
                sess = drs.get_session()
                si: SyncInventory = get_or_create(sess, SyncInventory, dip_external_id=activity_id,inventory_path=inventory)

        return activity_id


def db_config_str(config: BdrcDbLib.DbApp.DBConfig) -> str:
    """
    Convert a DBConfig into the string that created it. Hack!
    :param config: the DBConfig object
    :return: the string
    """
    return f"{config.db_alias}:{config.config_file_name}"


def dip_log_shell() -> None:
    """
    Intended for use with shell.
    Ex:  bash
    DIP_ID=$(log_dip -d ... -b .... -e ....)
    :return: DIP_ID operated on
    """
    exit_rc = 0
    ver_check()

    try:
        dlp = DipLogParser("Logs a number of different publication strategies",
                           "log_dip [OPTIONS] [dip_source_path] [dip_dest_path]  ")
        dla: DbArgNamespace = dlp.parsedArgs
        dl: DipLog = DipLog(dla.drsDbConfig)

        print(dl.set_dip(dla.activity_type, dla.begin_time, dla.end_time, dla.dip_source_path,
                         dla.dip_dest_path,
                         dla.work_name, dla.dip_id, dla.activity_return_code, dla.comment, dla.inventory))
    except ValueError:
        ei = sys.exc_info()
        print(str(ei[1]))
        exit_rc = 1

    sys.exit(exit_rc)


if __name__ == "__main__":
    dip_log_shell()
