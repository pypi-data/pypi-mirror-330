import unittest
from datetime import datetime, timedelta
from uuid import UUID

from BdrcDbLib.DbApp import DbApp

from archive_ops.DipLog import DipLog
from archive_ops.GetReadyWorksForStates import GetReadyWorks

"""
Test scenarios:

The database's retry parameters (DIP_Config) are set to:
* threshold for not adding to ready list: 5
* window for considering fails: 4 hours
- Make a failed activity (begin time, end time, work
- Make three retries of a fail, when getting 
"""


class DIPActivity:
    """
    Container for values. Use the attributes as keywords
    da = DIPActivity(bt = xxx, et= yyy, ext = UUID ...)
    """

    def __init__(self, **kwargs):
        self.bt = None

        self.et = None
        self.ext_id = None
        self.ac = None
        self.rc = None
        self.w = None
        self.sp = None
        self.dp = None
        self.c = None
        for kw in kwargs:
            self.__setattr__(kw, kwargs[kw])


# Use these
bt: datetime  # begin time
et: datetime  # end time
ext_id: UUID  # external id
ac: str  # Restricted values
rc: int  # return code
w: str  # WorkName
sp: str  # source path
dp: str  # dest path
c: str  # comment


class MyTestCase(unittest.TestCase):
    test_db_config: str = 'qa:~/.config/bdrc/db_apps.config'

    def setUp(self) -> None:
        """
        Clean up everything from prior runs. Hope two people aren't running at same time
        """
        db_app = DbApp(self.test_db_config)
        db_app.ExecQuery("truncate table dip_activity_current")
        db_app.ExecQuery("delete from dip_activity where dip_activity.create_time > %s",
                         datetime.now() - timedelta(minutes=20))

    def test_something(self):
        # Create a successful ARCHIVE
        arc: DIPActivity = DIPActivity(bt=datetime.now() - timedelta(minutes=15), ac='ARCHIVE', w='w1',
                                       et=datetime.now() - timedelta(minutes=12), rc=0, sp="source_path",
                                       dp="dest_path")
        dl = DipLog(self.test_db_config)

        sa_a: DIPActivity = DIPActivity(bt=arc.bt + timedelta(minutes=5), ac='SINGLE_ARCHIVE', w='w1',
                                        sp="source_path", dp="dest_path")
        # set up an incomplete SINGLE_ARCHIVE
        sa_a.ext_id = dl.set_dip(sa_a.ac, sa_a.bt, sa_a.et, sa_a.sp, sa_a.dp, sa_a.w, sa_a.ext_id, sa_a.rc, sa_a.c)

        # Should not appear in Ready for IA - it's not complete
        grw_ia = GetReadyWorks(self.test_db_config, state_text='IA')
        ia_readies: [] = grw_ia.get_works()
        self.assertTrue(len(ia_readies[0]) == 0)

        # finish the transaction
        sa_a.et = sa_a.bt + timedelta(minutes=2)
        sa_a.rc = 0
        sa_a.ext_id = dl.set_dip(sa_a.ac, sa_a.bt, sa_a.et, sa_a.sp, sa_a.dp, sa_a.w, sa_a.ext_id, sa_a.rc, sa_a.c)

        # Should be in list (retries < threshold )
        ia_readies: [] = grw_ia.get_works()
        # self.assertTrue(len(ac_list[0]) == 1)

        # Now, fail an IA transaction
        ia_a: DIPActivity = DIPActivity(bt=datetime.now() - timedelta(minutes=10), ac='IA', w='w1',
                                        et=datetime.now() - timedelta(minutes=8), rc=1, sp="dest_path",
                                        dp="ia://KaBoom")
        ia_a.ext_id = dl.set_dip(ia_a.ac, ia_a.bt, ia_a.et, ia_a.sp, ia_a.dp, ia_a.w, ia_a.ext_id, ia_a.rc, ia_a.c)

        # Should still appear in the GetReady - threshold is less
        ia_readies: [] = grw_ia.get_works()
        self.assertTrue(len(ia_readies[0]) == 1)

        # Now pump a bunch of failures at it
        for tries in range(1, 10):
            ia_a.et = ia_a.et + timedelta(seconds=10)
            ia_a.rc += 1
            ia_a.ext_id = dl.set_dip(None, None, ia_a.et, None, None, None, ia_a.ext_id, ia_a.rc, None)

        # Should be gone from the list
        ia_readies: [] = grw_ia.get_works()
        self.assertTrue(len(ia_readies[0]) == 0)

        # But should be ready for DEEP_archive
        grw_da = GetReadyWorks(self.test_db_config, 'DEEP_ARCHIVE')
        da_readies: [] = grw_da.get_works()
        self.assertTrue(len(da_readies[0]) == 1)

        # Now correct the work. Should not appear in the list since the activity we're seeking
        # has been fulfilled
        ia_a.rc = 0
        ia_a.ext_id = dl.set_dip(None, None, ia_a.et, None, None, None, ia_a.ext_id, ia_a.rc, None)

        ia_readies = grw_ia.get_works()
        self.assertTrue(len(ia_readies[0]) == 0)

        # Shouldn't have affected the DEEP_ARCHIVE records
        da_readies = grw_da.get_works()
        self.assertTrue(len(da_readies[0]) == 1)

        # DEEP_ARCHIVE failure
        da_sip: DIPActivity = DIPActivity(bt=datetime.now() - timedelta(minutes=5), ac='DEEP_ARCHIVE', w='w1',
                                          et=datetime.now() - timedelta(minutes=4), rc=1, sp="dest_path",
                                          dp="s3://KaBoom")
        da_sip.ext_id = dl.set_dip(da_sip.ac, da_sip.bt, da_sip.et, da_sip.sp, da_sip.dp, da_sip.w, da_sip.ext_id, da_sip.rc, da_sip.c)

        # Should still be available ( < threshold) 
        da_readies = grw_da.get_works()
        self.assertTrue(len(da_readies[0]) == 1)

        # Now pump a bunch of failures at it
        for tries in range(1, 10):
            da_sip.et = da_sip.et + timedelta(seconds=10)
            da_sip.rc += 1
            da_sip.ext_id = dl.set_dip(None, None, da_sip.et, None, None, None, da_sip.ext_id, da_sip.rc, None)

        # Should be gone from the list
        da_readies = grw_da.get_works()
        self.assertTrue(len(da_readies[0]) == 0)

        # Move finish time for this most recent failure out of the threshold
        da_sip.bt = datetime.now() - timedelta(hours=10)
        da_sip.et = da_sip.bt + timedelta(minutes=5)
        da_sip.ext_id = dl.set_dip(None, da_sip.bt, da_sip.et, None, None, None, da_sip.ext_id, da_sip.rc, None)

        # That should put it back on the list
        da_readies = grw_da.get_works()
        self.assertTrue(len(da_readies[0]) == 1)


if __name__ == '__main__':
    unittest.main()
