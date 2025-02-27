from typing import List, Optional

from sqlalchemy import BigInteger, Column, Date, DateTime, ForeignKeyConstraint, Index, Integer, JSON, String, \
    TIMESTAMP, Table, Text, text
from sqlalchemy.dialects.mysql import BIT, LONGTEXT, VARCHAR
from sqlalchemy.orm import declarative_base, mapped_column, relationship
from sqlalchemy.orm.base import Mapped

Base = declarative_base()
metadata = Base.metadata

t_AllReadyWorks = Table(
    'AllReadyWorks', metadata,
    Column('volumeId', Integer, server_default=text("'0'")),
    Column('Volume', String(45)),
    Column('workId', Integer, server_default=text("'0'")),
    Column('WorkName', String(45)),
    Column('HOLLIS', String(45)),
    Column('OutlineUrn', String(72)),
    Column('PrintMasterUrn', String(72))
)

t_AllReadyWorksOPM = Table(
    'AllReadyWorksOPM', metadata,
    Column('volumeId', Integer, server_default=text("'0'")),
    Column('Volume', String(45)),
    Column('workId', Integer, server_default=text("'0'")),
    Column('WorkName', String(45)),
    Column('HOLLIS', String(45)),
    Column('OutlineUrn', String(72)),
    Column('PrintMasterUrn', String(72))
)


class BuildPaths(Base):
    __tablename__ = 'BuildPaths'
    __table_args__ = (
        Index('BuildPath_IDX', 'BuildPath'),
        Index('BuildPaths_UNIQUE', 'BuildPath', unique=True),
        Index('build_dir_IDX', 'build_dir')
    )

    buildPathId = mapped_column(Integer, primary_key=True)
    BuildPath = mapped_column(String(255), nullable=False)
    create_time = mapped_column(DateTime, server_default=text('CURRENT_TIMESTAMP'))
    update_time = mapped_column(DateTime, server_default=text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'))
    build_dir = mapped_column(String(45), comment='basename of buildPath')

    BatchBuilds: Mapped[List['BatchBuilds']] = relationship('BatchBuilds', uselist=True, back_populates='BuildPaths_')


class DIPConfig(Base):
    __tablename__ = 'DIP_config'
    __table_args__ = (
        Index('DIP_DESC_UNIQUE', 'DIP_CONFIG_DESC', unique=True),
    )

    idDIP_CONFIG = mapped_column(String(45), primary_key=True,
                                 comment='Contains undefined strings representing config values. Sample client is GET_DIP_CONFIG which looks for values and casts them to integers.')
    DIP_CONFIG_DESC = mapped_column(String(255), nullable=False)
    DIP_CONFIG_VALUE = mapped_column(String(45), nullable=False)


class DRSCumStatus(Base):
    __tablename__ = 'DRS_cum_status'
    __table_args__ = (
        Index('obs_date_UNIQUE', 'obs_date', unique=True),
    )

    DRS_cum_statusId = mapped_column(Integer, primary_key=True)
    batch_count = mapped_column(Integer, nullable=False)
    object_count = mapped_column(Integer, nullable=False)
    obs_date = mapped_column(Date, nullable=False)
    work_count_built_not_uploaded = mapped_column(Integer, nullable=False)
    work_count_partly_uploaded = mapped_column(Integer, nullable=False)
    work_count_complete_upload = mapped_column(Integer, nullable=False)
    uploaded_image_count = mapped_column(Integer, nullable=False)
    create_time = mapped_column(TIMESTAMP, server_default=text('CURRENT_TIMESTAMP'))
    update_time = mapped_column(TIMESTAMP, server_default=text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'))
    uploaded_size_total = mapped_column(BigInteger)


t_Deletions = Table(
    'Deletions', metadata,
    Column('create_time', TIMESTAMP, server_default=text('CURRENT_TIMESTAMP')),
    Column('update_time', TIMESTAMP, server_default=text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP')),
    Column('BuildDate', DateTime),
    Column('BuildPath', String(255)),
    Column('Requested', String(45))
)

t_DepositedWorksFacts = Table(
    'DepositedWorksFacts', metadata,
    Column('workId', Integer, server_default=text("'0'")),
    Column('WorkName', String(45)),
    Column('HOLLIS', String(45)),
    Column('create_time', TIMESTAMP, server_default=text('CURRENT_TIMESTAMP')),
    Column('update_time', TIMESTAMP, server_default=text('CURRENT_TIMESTAMP')),
    Column('workVolumes', BigInteger),
    Column('DRSVolumes', BigInteger)
)


class GBContentState(Base):
    __tablename__ = 'GB_Content_State'

    volume_id = mapped_column(Integer, primary_key=True, nullable=False)
    job_state = mapped_column(String(45), primary_key=True, nullable=False)
    state_date = mapped_column(DateTime, primary_key=True, nullable=False)
    create_time = mapped_column(TIMESTAMP, server_default=text('CURRENT_TIMESTAMP'))
    update_time = mapped_column(TIMESTAMP, server_default=text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'))
    gb_log = mapped_column(LONGTEXT)


t_GB_Content_Work = Table(
    'GB_Content_Work', metadata,
    Column('WorkName', String(45)),
    Column('label', String(45)),
    Column('create_time', TIMESTAMP, server_default=text('CURRENT_TIMESTAMP')),
    Column('update_time', TIMESTAMP, server_default=text('CURRENT_TIMESTAMP')),
    Column('id', Integer, server_default=text("'0'")),
    Column('volume_id', Integer),
    Column('job_step', String(45)),
    Column('step_time', DateTime),
    Column('step_rc', Integer),
    Column('gb_log', LONGTEXT)
)

t_GB_Metadata_Works = Table(
    'GB_Metadata_Works', metadata,
    Column('WorkName', String(45)),
    Column('create_time', TIMESTAMP, server_default=text('CURRENT_TIMESTAMP')),
    Column('update_time', TIMESTAMP, server_default=text('CURRENT_TIMESTAMP')),
    Column('id', Integer, server_default=text("'0'")),
    Column('work_id', Integer),
    Column('upload_time', DateTime),
    Column('upload_result', Integer)
)


class GBReadyTrack(Base):
    __tablename__ = 'GB_Ready_Track'

    id = mapped_column(Integer, primary_key=True)
    create_time = mapped_column(TIMESTAMP, nullable=False, server_default=text('CURRENT_TIMESTAMP'))
    update_time = mapped_column(TIMESTAMP, server_default=text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'))
    target_id = mapped_column(Integer, comment='Id in specific tabel, varies with activity')
    activity = mapped_column(String(50), comment='Supported activities: download unpack')


class GetReadyLog(Base):
    __tablename__ = 'GetReadyLog'

    getReadyLog_id = mapped_column(Integer, primary_key=True)
    vols_unqueued_pre = mapped_column(Integer, nullable=False, server_default=text("'-1'"))
    vols_unqueued_post = mapped_column(Integer, nullable=False, server_default=text("'-1'"))
    works_unqueued_pre = mapped_column(Integer, nullable=False, server_default=text("'-1'"))
    works_unqueued_post = mapped_column(Integer, nullable=False, server_default=text("'-1'"))
    works_fetched = mapped_column(Integer, nullable=False, server_default=text("'-1'"))
    vols_fetched = mapped_column(Integer, nullable=False, server_default=text("'-1'"))
    create_time = mapped_column(TIMESTAMP, server_default=text('CURRENT_TIMESTAMP'))
    update_time = mapped_column(TIMESTAMP, server_default=text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'))


class HulVol(Base):
    __tablename__ = 'HulVol'

    C1 = mapped_column(String(45), primary_key=True)


t_RFP_MASTER_Works_List = Table(
    'RFP_MASTER_Works_List', metadata,
    Column('FY2015', Text),
    Column('FY2016', Text),
    Column('FY2017', Text),
    Column('FY2018', Text),
    Column('FY2019', Text),
    Column('FY2020', Text),
    Column('FY2021', Text),
    Column('FY2022', Text)
)

t_ReadyWorksNotDeposited = Table(
    'ReadyWorksNotDeposited', metadata,
    Column('workId', Integer, server_default=text("'0'")),
    Column('Volume', String(45)),
    Column('WorkName', String(45)),
    Column('HOLLIS', String(45)),
    Column('OutlineUrn', String(72)),
    Column('PrintMasterUrn', String(72))
)

t_TextSources = Table(
    'TextSources', metadata,
    Column('create_time', TIMESTAMP, server_default=text('CURRENT_TIMESTAMP')),
    Column('update_time', TIMESTAMP),
    Column('text_source', VARCHAR(255), nullable=False)
)

t_Volumes_only = Table(
    'Volumes_only', metadata,
    Column('volumeId', Integer, server_default=text("'0'")),
    Column('workId', Integer),
    Column('create_time', TIMESTAMP, server_default=text('CURRENT_TIMESTAMP')),
    Column('update_time', TIMESTAMP, server_default=text('CURRENT_TIMESTAMP')),
    Column('label', String(45)),
    Column('batchBuildId', Integer),
    Column('builtFileSize', BigInteger),
    Column('builtFileCount', Integer),
    Column('Queued', BIT(1), server_default=text("'b''0'''")),
    Column('Queued_time', DateTime)
)


class Works(Base):
    __tablename__ = 'Works'
    __table_args__ = (
        Index('work_UNIQUE', 'WorkName', unique=True),
        Index('work_text', 'WorkName')
    )

    workId = mapped_column(Integer, primary_key=True)
    create_time = mapped_column(TIMESTAMP, nullable=False, server_default=text('CURRENT_TIMESTAMP'))
    WorkName = mapped_column(String(45))
    HOLLIS = mapped_column(String(45))
    update_time = mapped_column(TIMESTAMP, server_default=text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'))
    WorkSize = mapped_column(BigInteger, server_default=text("'0'"))
    WorkFileCount = mapped_column(Integer, server_default=text("'0'"))
    WorkImageFileCount = mapped_column(BigInteger, server_default=text("'0'"))
    WorkImageTotalFileSize = mapped_column(BigInteger, server_default=text("'0'"))
    WorkNonImageFileCount = mapped_column(BigInteger, server_default=text("'0'"))
    WorkNonImageTotalFileSize = mapped_column(BigInteger, server_default=text("'0'"))

    GB_To_Do: Mapped[List['GBToDo']] = relationship('GBToDo', uselist=True, back_populates='work')
    IATrack: Mapped[List['IATrack']] = relationship('IATrack', uselist=True, back_populates='Works_')
    OutlinesOrig: Mapped[List['OutlinesOrig']] = relationship('OutlinesOrig', uselist=True, back_populates='Works_')
    dip_activity: Mapped[List['DipActivity']] = relationship('DipActivity', uselist=True, back_populates='work')
    workStatusCount: Mapped[List['WorkStatusCount']] = relationship('WorkStatusCount', uselist=True,
                                                                    back_populates='Works_')
    Volumes: Mapped[List['Volumes']] = relationship('Volumes', uselist=True, back_populates='Works_')
    pm_project_members: Mapped[List['PmProjectMembers']] = relationship('PmProjectMembers', uselist=True,
                                                                        back_populates='pm_work')


t_d4_new_not_restored_for_sql = Table(
    'd4-new-not-restored-for-sql', metadata,
    Column('WorkName', Text)
)

t_dac_special = Table(
    'dac_special', metadata,
    Column('create_time', TIMESTAMP, server_default=text('CURRENT_TIMESTAMP')),
    Column('update_time', TIMESTAMP, server_default=text('CURRENT_TIMESTAMP')),
    Column('dip_activity_type_id', Integer),
    Column('dip_activity_start', DateTime, server_default=text("'CURRENT_TIMESTAMP'")),
    Column('dip_activity_finish', DateTime),
    Column('dip_activity_result_code', Integer),
    Column('dip_source_path', String(255)),
    Column('dip_dest_path', String(255)),
    Column('work_id', Integer),
    Column('dip_external_id', String(45)),
    Column('dip_comment', LONGTEXT)
)

t_deposited_vol_data = Table(
    'deposited_vol_data', metadata,
    Column('label', Text),
    Column('batch_dir', Text),
    Column('import_date', Text),
    Column('n_objects', Integer),
    Column('total_size', BigInteger)
)


class DipActivityCurrent(Base):
    __tablename__ = 'dip_activity_current'
    __table_args__ = (
        Index('dip_external_id_UNIQUE', 'dip_external_id', unique=True),
    )

    dip_activity_type_id = mapped_column(Integer, primary_key=True, nullable=False)
    dip_activity_start = mapped_column(DateTime, nullable=False, server_default=text('CURRENT_TIMESTAMP'))
    work_id = mapped_column(Integer, primary_key=True, nullable=False)
    create_time = mapped_column(TIMESTAMP, server_default=text('CURRENT_TIMESTAMP'))
    update_time = mapped_column(TIMESTAMP, server_default=text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'))
    dip_activity_finish = mapped_column(DateTime)
    dip_activity_result_code = mapped_column(Integer)
    dip_source_path = mapped_column(String(255))
    dip_dest_path = mapped_column(String(255))
    dip_external_id = mapped_column(String(45))
    dip_comment = mapped_column(LONGTEXT)


t_dip_activity_current_single_archive_workflow = Table(
    'dip_activity_current_single_archive_workflow', metadata,
    Column('create_time', TIMESTAMP, server_default=text('CURRENT_TIMESTAMP')),
    Column('update_time', TIMESTAMP, server_default=text('CURRENT_TIMESTAMP')),
    Column('dip_activity_type_id', Integer),
    Column('dip_activity_start', DateTime, server_default=text("'CURRENT_TIMESTAMP'")),
    Column('dip_activity_finish', DateTime),
    Column('dip_activity_result_code', Integer),
    Column('dip_source_path', String(255)),
    Column('dip_dest_path', String(255)),
    Column('work_id', Integer),
    Column('dip_external_id', String(45)),
    Column('dip_comment', LONGTEXT)
)

t_dip_activity_current_work = Table(
    'dip_activity_current_work', metadata,
    Column('WorkName', String(45)),
    Column('dip_activity_types_label', String(45)),
    Column('dip_activity_start', DateTime, server_default=text("'CURRENT_TIMESTAMP'")),
    Column('dip_activity_finish', DateTime),
    Column('dip_activity_result_code', Integer),
    Column('dip_source_path', String(255)),
    Column('dip_dest_path', String(255)),
    Column('dip_external_id', String(45)),
    Column('dip_comment', LONGTEXT),
    Column('create_time', TIMESTAMP, server_default=text('CURRENT_TIMESTAMP')),
    Column('update_time', TIMESTAMP, server_default=text('CURRENT_TIMESTAMP')),
    Column('dip_activity_type_id', Integer),
    Column('work_id', Integer)
)


class DipActivityTypes(Base):
    __tablename__ = 'dip_activity_types'

    iddip_activity_types = mapped_column(Integer, primary_key=True)
    dip_activity_types_label = mapped_column(String(45))

    dip_activity: Mapped[List['DipActivity']] = relationship('DipActivity', uselist=True,
                                                             back_populates='dip_activity_type')
    dip_activity_volume: Mapped[List['DipActivityVolume']] = relationship('DipActivityVolume', uselist=True,
                                                                          back_populates='dip_activity_type')


class DipActivityVolumeCurrent(Base):
    __tablename__ = 'dip_activity_volume_current'
    __table_args__ = (
        Index('dip_external_id_UNIQUE', 'dip_external_id', unique=True),
    )

    dip_activity_type_id = mapped_column(Integer, primary_key=True, nullable=False)
    dip_activity_start = mapped_column(DateTime, nullable=False, server_default=text('CURRENT_TIMESTAMP'))
    volumeId = mapped_column(Integer, primary_key=True, nullable=False)
    create_time = mapped_column(TIMESTAMP, server_default=text('CURRENT_TIMESTAMP'))
    update_time = mapped_column(TIMESTAMP, server_default=text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'))
    dip_activity_finish = mapped_column(DateTime)
    dip_activity_result_code = mapped_column(Integer)
    dip_source_path = mapped_column(String(255))
    dip_dest_path = mapped_column(String(255))
    dip_external_id = mapped_column(String(45))
    dip_comment = mapped_column(LONGTEXT)


t_dip_activity_volume_v = Table(
    'dip_activity_volume_v', metadata,
    Column('workId', Integer, server_default=text("'0'")),
    Column('WorkName', String(45)),
    Column('volumeId', Integer, server_default=text("'0'")),
    Column('VolumeLabel', String(45)),
    Column('dip_activity_types_label', String(45)),
    Column('dip_activity_start', DateTime, server_default=text("'CURRENT_TIMESTAMP'")),
    Column('dip_activity_finish', DateTime),
    Column('dip_activity_result_code', Integer),
    Column('dip_source_path', String(255)),
    Column('dip_dest_path', String(255)),
    Column('dip_external_id', String(45)),
    Column('dip_comment', LONGTEXT),
    Column('create_time', TIMESTAMP, server_default=text('CURRENT_TIMESTAMP')),
    Column('update_time', TIMESTAMP, server_default=text('CURRENT_TIMESTAMP')),
    Column('dip_activity_type_id', Integer)
)

t_dip_activity_work = Table(
    'dip_activity_work', metadata,
    Column('workId', Integer, server_default=text("'0'")),
    Column('WorkName', String(45)),
    Column('dip_activity_types_label', String(45)),
    Column('dip_activity_start', DateTime, server_default=text("'CURRENT_TIMESTAMP'")),
    Column('dip_activity_finish', DateTime),
    Column('dip_activity_result_code', Integer),
    Column('dip_source_path', String(255)),
    Column('dip_dest_path', String(255)),
    Column('dip_external_id', String(45)),
    Column('dip_comment', LONGTEXT),
    Column('create_time', TIMESTAMP, server_default=text('CURRENT_TIMESTAMP')),
    Column('update_time', TIMESTAMP, server_default=text('CURRENT_TIMESTAMP')),
    Column('dip_activity_type_id', Integer)
)


class Drs(Base):
    __tablename__ = 'drs'

    workId = mapped_column(Integer, primary_key=True)


class GlacierSyncProgress(Base):
    __tablename__ = 'glacier_sync_progress'

    create_time = mapped_column(TIMESTAMP, nullable=False, server_default=text('CURRENT_TIMESTAMP'))
    id = mapped_column(Integer, primary_key=True)
    update_time = mapped_column(TIMESTAMP, server_default=text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'))
    object_name = mapped_column(String(255))
    restore_requested_on = mapped_column(TIMESTAMP)
    restore_complete_on = mapped_column(TIMESTAMP)
    download_complete_on = mapped_column(TIMESTAMP)
    debag_complete_on = mapped_column(TIMESTAMP)
    sync_complete_on = mapped_column(TIMESTAMP)
    user_data = mapped_column(JSON,
                              comment='format:[ {"time_stamp" : <current_time>, "user_data" : provided_user_data object}... ]')


class MStates(Base):
    __tablename__ = 'm_states'

    id = mapped_column(Integer, primary_key=True)
    create_time = mapped_column(TIMESTAMP, nullable=False, server_default=text('CURRENT_TIMESTAMP'))
    m_state_name = mapped_column(String(45), nullable=False)
    update_time = mapped_column(TIMESTAMP, server_default=text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'))
    m_state_desc = mapped_column(LONGTEXT)


class PmMemberStates(Base):
    __tablename__ = 'pm_member_states'

    create_time = mapped_column(TIMESTAMP, nullable=False, server_default=text('CURRENT_TIMESTAMP'))
    id = mapped_column(Integer, primary_key=True)
    m_state_name = mapped_column(String(45), nullable=False)
    update_time = mapped_column(TIMESTAMP, server_default=text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'))
    m_state_desc = mapped_column(LONGTEXT)

    pm_project_members: Mapped[List['PmProjectMembers']] = relationship('PmProjectMembers', uselist=True,
                                                                        back_populates='pm_project_state')


class PmMemberTypes(Base):
    __tablename__ = 'pm_member_types'

    create_time = mapped_column(TIMESTAMP, nullable=False, server_default=text('CURRENT_TIMESTAMP'))
    id = mapped_column(Integer, primary_key=True)
    m_type = mapped_column(String(45), nullable=False)
    update_time = mapped_column(TIMESTAMP, server_default=text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'))

    pm_projects: Mapped[List['PmProjects']] = relationship('PmProjects', uselist=True, back_populates='m_type')
    pm_project_members: Mapped[List['PmProjectMembers']] = relationship('PmProjectMembers', uselist=True,
                                                                        back_populates='pm_member_types')


class PmProjectTypes(Base):
    __tablename__ = 'pm_project_types'

    create_time = mapped_column(TIMESTAMP, nullable=False, server_default=text('CURRENT_TIMESTAMP'))
    id = mapped_column(Integer, primary_key=True)
    project_type_name = mapped_column(String(45), nullable=False)
    update_time = mapped_column(TIMESTAMP, server_default=text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'))
    project_type_desc = mapped_column(LONGTEXT)

    pm_projects: Mapped[List['PmProjects']] = relationship('PmProjects', uselist=True, back_populates='project_type')


t_processing = Table(
    'processing', metadata,
    Column('create_time', TIMESTAMP, server_default=text('CURRENT_TIMESTAMP')),
    Column('update_time', TIMESTAMP, server_default=text('CURRENT_TIMESTAMP')),
    Column('volumeId', Integer),
    Column('activity_date', Date),
    Column('processLogId', Integer, server_default=text("'0'")),
    Column('result', String(45))
)

t_sync = Table(
    'sync', metadata,
    Column('create_time', TIMESTAMP, server_default=text('CURRENT_TIMESTAMP')),
    Column('update_time', TIMESTAMP, server_default=text('CURRENT_TIMESTAMP')),
    Column('volumeId', Integer),
    Column('activity_date', Date),
    Column('syncLogId', Integer, server_default=text("'0'")),
    Column('result', String(45))
)

t_vols_no_depo = Table(
    'vols-no-depo', metadata,
    Column('id', Integer),
    Column('label', Text),
    Column('urn', Text),
    Column('depositor', Text),
    Column('owner', Text),
    Column('billing_code', Text),
    Column('load_type', Text),
    Column('something', Text),
    Column('batch_dir', Text),
    Column('something_2', Integer),
    Column('import_date', DateTime),
    Column('batch_id', Text),
    Column('file_count', Integer),
    Column('t1', Text),
    Column('t2', Text),
    Column('t3', Text),
    Column('t4', Text),
    Column('total_size', Integer)
)

t_worksOutlines2 = Table(
    'worksOutlines2', metadata,
    Column('workId', Integer),
    Column('volumeId', Integer, nullable=False, server_default=text("'0'")),
    Column('batchBuildId', Integer)
)

t_zju_femc_excludes = Table(
    'zju_femc_excludes', metadata,
    Column('WorkName', String(45))
)


class BatchBuilds(Base):
    __tablename__ = 'BatchBuilds'
    __table_args__ = (
        ForeignKeyConstraint(['buildPathId'], ['BuildPaths.buildPathId'], ondelete='SET NULL', onupdate='SET NULL',
                             name='BatchBuildPath'),
        Index('BatchBuildPathId', 'buildPathId', unique=True),
        Index('BatchBuildPath_idx', 'buildPathId')
    )

    batchBuildId = mapped_column(Integer, primary_key=True)
    create_time = mapped_column(DateTime, nullable=False, server_default=text('CURRENT_TIMESTAMP'))
    update_time = mapped_column(DateTime, nullable=False,
                                server_default=text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'))
    BuildDate = mapped_column(DateTime)
    Result = mapped_column(String(45))
    TransferQueuedDate = mapped_column(DateTime)
    TransferCompleteDate = mapped_column(DateTime)
    buildPathId = mapped_column(Integer)

    BuildPaths_: Mapped[Optional['BuildPaths']] = relationship('BuildPaths', back_populates='BatchBuilds')
    Volumes: Mapped[List['Volumes']] = relationship('Volumes', uselist=True, back_populates='BatchBuilds_')


# /Users/jimk/dev/archive-ops/bdrc_util/archive_ops/models/drsmodel.py:547: SAWarning: Implicitly combining column Works.create_time with column GB_Metadata_Track.create_time under attribute 'create_time'.  Please configure one or more attributes for these same-named columns explicitly.
# class GBMetadataTrack(Works):
# /Users/jimk/dev/archive-ops/bdrc_util/archive_ops/models/drsmodel.py:547: SAWarning: Implicitly combining column Works.update_time with column GB_Metadata_Track.update_time under attribute 'update_time'.  Please configure one or more attributes for these same-named columns explicitly.
# class GBMetadataTrack(Works):
# /Users/jimk/dev/archive-ops/bdrc_util/archive_ops/models/drsmodel.py:723: SAWarning: Implicitly combining column Works.workId with column gb_metadata_transfers.workId under attribute 'workId'.  Please configure one or more attributes for these same-named columns explicitly.
# class GbMetadataTransfers(Works):

# Why did SqlAlchemy create this as subclass of Works? class GBMetadataTrack(Works)

class GBMetadataTrack(Base):
    __tablename__ = 'GB_Metadata_Track'
    __table_args__ = (
        ForeignKeyConstraint(['id'], ['Works.workId'], name='gb_metadata_work'),
    )

    id = mapped_column(Integer, primary_key=True)
    work_id = mapped_column(Integer, nullable=False)
    upload_time = mapped_column(DateTime, nullable=False)
    create_time = mapped_column(TIMESTAMP, server_default=text('CURRENT_TIMESTAMP'))
    update_time = mapped_column(TIMESTAMP, server_default=text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'))
    upload_result = mapped_column(Integer)


class GBToDo(Base):
    __tablename__ = 'GB_To_Do'
    __table_args__ = (
        ForeignKeyConstraint(['work_id'], ['Works.workId'], name='GB_To_Do_ibfk_1'),
        Index('work_id', 'work_id')
    )

    id = mapped_column(Integer, primary_key=True)
    create_time = mapped_column(TIMESTAMP, nullable=False, server_default=text('CURRENT_TIMESTAMP'))
    update_time = mapped_column(TIMESTAMP, server_default=text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'))
    work_id = mapped_column(Integer)

    work: Mapped[Optional['Works']] = relationship('Works', back_populates='GB_To_Do')


class IATrack(Base):
    __tablename__ = 'IATrack'
    __table_args__ = (
        ForeignKeyConstraint(['workId'], ['Works.workId'], name='IATrack_Work'),
        Index('IATrack_Work_idx', 'workId')
    )

    idIATrack = mapped_column(Integer, primary_key=True)
    ia_id = mapped_column(String(45), nullable=False, comment='Internet Archive Identifier - bdrc-workRid')
    workId = mapped_column(Integer, nullable=False)
    task_id = mapped_column(Integer, server_default=text("'-1'"))
    task_status = mapped_column(String(15))
    task_complete = mapped_column(DateTime)
    log = mapped_column(String(255), comment='Log file location')

    Works_: Mapped['Works'] = relationship('Works', back_populates='IATrack')


class OutlinesOrig(Base):
    __tablename__ = 'OutlinesOrig'
    __table_args__ = (
        ForeignKeyConstraint(['workId'], ['Works.workId'], name='OutlineToWork'),
        Index('OutlineToVolume_idx', 'volumeId'),
        Index('OutlineToWork_idx', 'workId')
    )

    outlineId = mapped_column(Integer, primary_key=True)
    workId = mapped_column(Integer, nullable=False)
    volumeId = mapped_column(Integer, nullable=False)
    create_time = mapped_column(TIMESTAMP, server_default=text('CURRENT_TIMESTAMP'))
    update_time = mapped_column(TIMESTAMP)
    outlineText = mapped_column(VARCHAR(255))

    Works_: Mapped['Works'] = relationship('Works', back_populates='OutlinesOrig')


class DipActivity(Base):
    __tablename__ = 'dip_activity'
    __table_args__ = (
        ForeignKeyConstraint(['dip_activity_type_id'], ['dip_activity_types.iddip_activity_types'],
                             name='FK_activity_activity_type'),
        ForeignKeyConstraint(['work_id'], ['Works.workId'], name='FK_dip_activity_work'),
        Index('FK_activity_activity_type_idx', 'dip_activity_type_id'),
        Index('FK_dip_activity_work_idx', 'work_id'),
        Index('dip_external_id_UNIQUE', 'dip_external_id', unique=True)
    )

    dip_activity_type_id = mapped_column(Integer, primary_key=True, nullable=False)
    dip_activity_start = mapped_column(DateTime, primary_key=True, nullable=False,
                                       server_default=text('CURRENT_TIMESTAMP'))
    work_id = mapped_column(Integer, primary_key=True, nullable=False)
    create_time = mapped_column(TIMESTAMP, server_default=text('CURRENT_TIMESTAMP'))
    update_time = mapped_column(TIMESTAMP, server_default=text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'))
    dip_activity_finish = mapped_column(DateTime)
    dip_activity_result_code = mapped_column(Integer)
    dip_source_path = mapped_column(String(255))
    dip_dest_path = mapped_column(String(255))
    dip_external_id = mapped_column(String(45))
    dip_comment = mapped_column(LONGTEXT)

    dip_activity_type: Mapped['DipActivityTypes'] = relationship('DipActivityTypes', back_populates='dip_activity')
    work: Mapped['Works'] = relationship('Works', back_populates='dip_activity')
    gb_metadata_transfers: Mapped[List['GbMetadataTransfers']] = relationship('GbMetadataTransfers', uselist=True,
                                                                              back_populates='dip_activity')
    sync_inventory: Mapped[List['SyncInventory']] = relationship('SyncInventory', uselist=True,
                                                                 back_populates='dip_external')


class PmProjects(Base):
    __tablename__ = 'pm_projects'
    __table_args__ = (
        ForeignKeyConstraint(['m_type_id'], ['pm_member_types.id'], name='pm_projects_ibfk_2'),
        ForeignKeyConstraint(['project_type_id'], ['pm_project_types.id'], name='pm_projects_ibfk_1'),
        Index('m_type_id', 'm_type_id'),
        Index('project_type_id', 'project_type_id')
    )

    create_time = mapped_column(TIMESTAMP, nullable=False, server_default=text('CURRENT_TIMESTAMP'))
    id = mapped_column(Integer, primary_key=True)
    update_time = mapped_column(TIMESTAMP, server_default=text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'))
    name = mapped_column(String(45))
    description = mapped_column(LONGTEXT)
    project_type_id = mapped_column(Integer)
    m_type_id = mapped_column(Integer)

    m_type: Mapped[Optional['PmMemberTypes']] = relationship('PmMemberTypes', back_populates='pm_projects')
    project_type: Mapped[Optional['PmProjectTypes']] = relationship('PmProjectTypes', back_populates='pm_projects')
    pm_project_members: Mapped[List['PmProjectMembers']] = relationship('PmProjectMembers', uselist=True,
                                                                        back_populates='pm_projects')


class WorkStatusCount(Base):
    __tablename__ = 'workStatusCount'
    __table_args__ = (
        ForeignKeyConstraint(['workId'], ['Works.workId'], name='work'),
        Index('status_work_idx', 'workId'),
        Index('workId', 'workId', unique=True)
    )

    workStatusCountId = mapped_column(Integer, primary_key=True)
    Volumes = mapped_column(Integer, nullable=False)
    NumberVolumesBatchQueued = mapped_column(Integer, nullable=False)
    NumberVolumesBatchBuilt = mapped_column(Integer, nullable=False)
    NumberVolumesUploadQueued = mapped_column(Integer, nullable=False)
    NumberVolumesUploaded = mapped_column(Integer, nullable=False)
    create_time = mapped_column(TIMESTAMP, server_default=text('CURRENT_TIMESTAMP'))
    update_time = mapped_column(TIMESTAMP)
    workId = mapped_column(Integer)
    NumberVolumesDeposited = mapped_column(Integer)

    Works_: Mapped[Optional['Works']] = relationship('Works', back_populates='workStatusCount')


class Volumes(Base):
    __tablename__ = 'Volumes'
    __table_args__ = (
        ForeignKeyConstraint(['batchBuildId'], ['BatchBuilds.batchBuildId'], ondelete='SET NULL', onupdate='CASCADE',
                             name='VolToBatch'),
        ForeignKeyConstraint(['workId'], ['Works.workId'], name='VolToWork'),
        Index('Label_IDX', 'label'),
        Index('VolToBatch_idx', 'batchBuildId'),
        Index('VolToWork_idx', 'workId'),
        Index('label_UNIQUE', 'label', unique=True),
        Index('volumeId_UNIQUE', 'volumeId', unique=True)
    )

    volumeId = mapped_column(Integer, primary_key=True)
    workId = mapped_column(Integer)
    create_time = mapped_column(TIMESTAMP, server_default=text('CURRENT_TIMESTAMP'))
    update_time = mapped_column(TIMESTAMP, server_default=text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'))
    label = mapped_column(String(45))
    batchBuildId = mapped_column(Integer)
    builtFileSize = mapped_column(BigInteger)
    builtFileCount = mapped_column(Integer)
    Queued = mapped_column(BIT(1))
    Queued_time = mapped_column(DateTime)

    BatchBuilds_: Mapped[Optional['BatchBuilds']] = relationship('BatchBuilds', back_populates='Volumes')
    Works_: Mapped[Optional['Works']] = relationship('Works', back_populates='Volumes')
    DRS: Mapped[List['DRS']] = relationship('DRS', uselist=True, back_populates='Volumes_')
    GB_Content_Track: Mapped[List['GBContentTrack']] = relationship('GBContentTrack', uselist=True,
                                                                    back_populates='volume')
    GB_Distribution: Mapped[List['GBDistribution']] = relationship('GBDistribution', uselist=True,
                                                                   back_populates='volume')
    GB_Downloads: Mapped[List['GBDownloads']] = relationship('GBDownloads', uselist=True, back_populates='volume')
    GB_Unpack: Mapped[List['GBUnpack']] = relationship('GBUnpack', uselist=True, back_populates='volume')
    Outlines: Mapped[List['Outlines']] = relationship('Outlines', uselist=True, back_populates='Volumes_')
    PrintMasters: Mapped[List['PrintMasters']] = relationship('PrintMasters', uselist=True, back_populates='Volumes_')
    PrintMastersOrig: Mapped[List['PrintMastersOrig']] = relationship('PrintMastersOrig', uselist=True,
                                                                      back_populates='Volumes_')
    dip_activity_volume: Mapped[List['DipActivityVolume']] = relationship('DipActivityVolume', uselist=True,
                                                                          back_populates='Volumes_')
    pm_project_members: Mapped[List['PmProjectMembers']] = relationship('PmProjectMembers', uselist=True,
                                                                        back_populates='pm_volume')
    process_log: Mapped[List['ProcessLog']] = relationship('ProcessLog', uselist=True, back_populates='Volumes_')
    sync_log: Mapped[List['SyncLog']] = relationship('SyncLog', uselist=True, back_populates='Volumes_')


class GbMetadataTransfers(Base):
    __tablename__ = 'gb_metadata_transfers'
    __table_args__ = (
        ForeignKeyConstraint(['id'], ['Works.workId'], name='gb_metadata_transfers___fk__W'),
        ForeignKeyConstraint(['transfer_log_dip'], ['dip_activity.dip_external_id'], ondelete='CASCADE',
                             onupdate='CASCADE', name='gb_metadata_transfers_dip_activity_dip_external_id_fk'),
        Index('gb_metadata_transfers___fk_vol', 'workId'),
        Index('gb_metadata_transfers_dip_activity_dip_external_id_fk', 'transfer_log_dip'),
        {'comment': 'Track metadata transfers  '}
    )

    id = mapped_column(Integer, primary_key=True)
    workId = mapped_column(Integer, nullable=False)
    transfer_result = mapped_column(Integer, nullable=False, server_default=text("'-1'"), comment='-1 means not set')
    transfer_log_dip = mapped_column(VARCHAR(32))
    transfer_start = mapped_column(DateTime)

    dip_activity: Mapped[Optional['DipActivity']] = relationship('DipActivity', back_populates='gb_metadata_transfers')


class SyncInventory(Base):
    __tablename__ = 'sync_inventory'
    __table_args__ = (
        ForeignKeyConstraint(['dip_external_id'], ['dip_activity.dip_external_id'],
                             name='sync_inventory___dip_activity_fk'),
        Index('sync_inventory___dip_activity_fk', 'dip_external_id'),
        {'comment': 'Maps an archive sync event to a path containing the sync contents'}
    )

    id = mapped_column(Integer, primary_key=True, comment='key')
    dip_external_id = mapped_column(VARCHAR(64), nullable=False, comment='dip-activity record')
    inventory_path = mapped_column(VARCHAR(255), nullable=False, comment='Path to the inventory of the referenced sync')

    dip_external: Mapped['DipActivity'] = relationship('DipActivity', back_populates='sync_inventory')


class DRS(Base):
    __tablename__ = 'DRS'
    __table_args__ = (
        ForeignKeyConstraint(['volumeId'], ['Volumes.volumeId'], name='DRSVolume'),
        Index('DRSVolume_idx', 'volumeId'),
        Index('DRS_DRSid_uindex', 'DRSid', unique=True),
        Index('OSN', 'OSN', unique=True),
        Index('drs_dir_idx', 'DRSdir'),
        {'comment': 'Corresponds to our data structures and to output/BDRCCun'}
    )

    DRSid = mapped_column(Integer, primary_key=True)
    IngestDate = mapped_column(DateTime)
    objectid = mapped_column(String(45), comment='HUL Generated OBJ-ID')
    create_time = mapped_column(TIMESTAMP, server_default=text('CURRENT_TIMESTAMP'))
    update_time = mapped_column(TIMESTAMP, server_default=text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'))
    DRSdir = mapped_column(String(45))
    objectUrn = mapped_column(String(72))
    filesCount = mapped_column(Integer)
    size = mapped_column(BigInteger)
    OSN = mapped_column(String(45))
    volumeId = mapped_column(Integer)

    Volumes_: Mapped[Optional['Volumes']] = relationship('Volumes', back_populates='DRS')


class GBContentTrack(Base):
    __tablename__ = 'GB_Content_Track'
    __table_args__ = (
        ForeignKeyConstraint(['volume_id'], ['Volumes.volumeId'], name='job_step_volume'),
        Index('job_step_volume', 'volume_id')
    )

    id = mapped_column(Integer, primary_key=True)
    volume_id = mapped_column(Integer, nullable=False)
    step_time = mapped_column(DateTime, nullable=False)
    create_time = mapped_column(TIMESTAMP, server_default=text('CURRENT_TIMESTAMP'))
    update_time = mapped_column(TIMESTAMP, server_default=text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'))
    job_step = mapped_column(String(45))
    step_rc = mapped_column(Integer)
    gb_log = mapped_column(LONGTEXT)

    volume: Mapped['Volumes'] = relationship('Volumes', back_populates='GB_Content_Track')


class GBDistribution(Base):
    __tablename__ = 'GB_Distribution'
    __table_args__ = (
        ForeignKeyConstraint(['volume_id'], ['Volumes.volumeId'], name='GB_Distribution_ibfk_1'),
        Index('volume_id', 'volume_id')
    )

    id = mapped_column(Integer, primary_key=True)
    create_time = mapped_column(TIMESTAMP, nullable=False, server_default=text('CURRENT_TIMESTAMP'))
    update_time = mapped_column(TIMESTAMP, server_default=text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'))
    volume_id = mapped_column(Integer)
    dist_time = mapped_column(TIMESTAMP)
    src = mapped_column(String(255))
    dest = mapped_column(String(255))

    volume: Mapped[Optional['Volumes']] = relationship('Volumes', back_populates='GB_Distribution')


class GBDownloads(Base):
    __tablename__ = 'GB_Downloads'
    __table_args__ = (
        ForeignKeyConstraint(['volume_id'], ['Volumes.volumeId'], name='GB_Downloads_ibfk_1'),
        Index('volume_id', 'volume_id')
    )

    id = mapped_column(Integer, primary_key=True)
    create_time = mapped_column(TIMESTAMP, nullable=False, server_default=text('CURRENT_TIMESTAMP'))
    volume_id = mapped_column(Integer)
    download_object_name = mapped_column(String(255))
    download_path = mapped_column(String(255))
    download_time = mapped_column(TIMESTAMP)
    update_time = mapped_column(TIMESTAMP, server_default=text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'))

    volume: Mapped[Optional['Volumes']] = relationship('Volumes', back_populates='GB_Downloads')


class GBUnpack(Base):
    __tablename__ = 'GB_Unpack'
    __table_args__ = (
        ForeignKeyConstraint(['volume_id'], ['Volumes.volumeId'], name='GB_Unpack_ibfk_1'),
        Index('volume_id', 'volume_id')
    )

    id = mapped_column(Integer, primary_key=True)
    create_time = mapped_column(TIMESTAMP, nullable=False, server_default=text('CURRENT_TIMESTAMP'))
    update_time = mapped_column(TIMESTAMP, server_default=text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'))
    volume_id = mapped_column(Integer)
    unpack_object_name = mapped_column(String(255))
    unpacked_path = mapped_column(String(255))
    unpack_time = mapped_column(TIMESTAMP)

    volume: Mapped[Optional['Volumes']] = relationship('Volumes', back_populates='GB_Unpack')


class Outlines(Base):
    __tablename__ = 'Outlines'
    __table_args__ = (
        ForeignKeyConstraint(['volumeId'], ['Volumes.volumeId'], ondelete='CASCADE', onupdate='CASCADE',
                             name='Outline_TO_Vol_FK'),
        Index('Outline_TO_Vol_FK_idx', 'volumeId'),
        Index('Vol_U', 'volumeId', unique=True),
        Index('outlineId_UNIQUE', 'outlineId', unique=True)
    )

    volumeId = mapped_column(Integer, nullable=False)
    outlineId = mapped_column(Integer, primary_key=True)
    create_time = mapped_column(TIMESTAMP, server_default=text('CURRENT_TIMESTAMP'))
    update_time = mapped_column(TIMESTAMP, server_default=text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'))

    Volumes_: Mapped['Volumes'] = relationship('Volumes', back_populates='Outlines')


class PrintMasters(Base):
    __tablename__ = 'PrintMasters'
    __table_args__ = (
        ForeignKeyConstraint(['volumeId'], ['Volumes.volumeId'], ondelete='CASCADE', onupdate='CASCADE',
                             name='PrintMaster_to_Vol_FK'),
        Index('PrintMaster_to_Vol_FK_idx', 'volumeId'),
        Index('printMasterId_UNIQUE', 'printMasterId', unique=True),
        Index('volumeId_UNIQUE', 'volumeId', unique=True)
    )

    printMasterId = mapped_column(Integer, primary_key=True)
    volumeId = mapped_column(Integer, nullable=False)
    create_time = mapped_column(TIMESTAMP, nullable=False, server_default=text('CURRENT_TIMESTAMP'))
    update_time = mapped_column(TIMESTAMP, nullable=False,
                                server_default=text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'))

    Volumes_: Mapped['Volumes'] = relationship('Volumes', back_populates='PrintMasters')


class PrintMastersOrig(Base):
    __tablename__ = 'PrintMastersOrig'
    __table_args__ = (
        ForeignKeyConstraint(['volumeId'], ['Volumes.volumeId'], ondelete='SET NULL', onupdate='SET NULL',
                             name='PrintMasterToVolume'),
        Index('OSN_UNIQUE', 'OSN', unique=True),
        Index('PrintMasterToVolume_idx', 'volumeId'),
        Index('idBatchStatus_idx', 'idBatchStatus')
    )

    PrintMasterId = mapped_column(Integer, primary_key=True)
    create_time = mapped_column(TIMESTAMP, server_default=text('CURRENT_TIMESTAMP'))
    update_time = mapped_column(TIMESTAMP)
    workId = mapped_column(String(45))
    Path = mapped_column(String(255))
    idBatchStatus = mapped_column(Integer)
    OSN = mapped_column(String(45))
    volumeId = mapped_column(Integer)

    Volumes_: Mapped[Optional['Volumes']] = relationship('Volumes', back_populates='PrintMastersOrig')


class DipActivityVolume(Base):
    __tablename__ = 'dip_activity_volume'
    __table_args__ = (
        ForeignKeyConstraint(['dip_activity_type_id'], ['dip_activity_types.iddip_activity_types'],
                             name='FK_activity_activity_type_vol'),
        ForeignKeyConstraint(['volumeId'], ['Volumes.volumeId'], name='FK_dip_activity_volume'),
        Index('FK_activity_activity_type_vol_idx', 'dip_activity_type_id'),
        Index('FK_dip_activity_vol_idx', 'volumeId'),
        Index('dip_external_id_UNIQUE', 'dip_external_id', unique=True)
    )

    dip_activity_type_id = mapped_column(Integer, primary_key=True, nullable=False)
    dip_activity_start = mapped_column(DateTime, primary_key=True, nullable=False,
                                       server_default=text('CURRENT_TIMESTAMP'))
    volumeId = mapped_column(Integer, primary_key=True, nullable=False)
    create_time = mapped_column(TIMESTAMP, server_default=text('CURRENT_TIMESTAMP'))
    update_time = mapped_column(TIMESTAMP, server_default=text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'))
    dip_activity_finish = mapped_column(DateTime)
    dip_activity_result_code = mapped_column(Integer)
    dip_source_path = mapped_column(String(255))
    dip_dest_path = mapped_column(String(255))
    dip_external_id = mapped_column(String(45))
    dip_comment = mapped_column(LONGTEXT)

    dip_activity_type: Mapped['DipActivityTypes'] = relationship('DipActivityTypes',
                                                                 back_populates='dip_activity_volume')
    Volumes_: Mapped['Volumes'] = relationship('Volumes', back_populates='dip_activity_volume')


class PmProjectMembers(Base):
    __tablename__ = 'pm_project_members'
    __table_args__ = (
        ForeignKeyConstraint(['pm_project'], ['pm_projects.id'], name='pm_project_members_ibfk_4'),
        ForeignKeyConstraint(['pm_project_state_id'], ['pm_member_states.id'], name='pm_project_members_ibfk_5'),
        ForeignKeyConstraint(['pm_type'], ['pm_member_types.id'], name='pm_project_members_ibfk_1'),
        ForeignKeyConstraint(['pm_volume_id'], ['Volumes.volumeId'], name='pm_project_members_ibfk_3'),
        ForeignKeyConstraint(['pm_work_id'], ['Works.workId'], name='pm_project_members_ibfk_2'),
        Index('pm_project', 'pm_project'),
        Index('pm_project_state_id', 'pm_project_state_id'),
        Index('pm_type', 'pm_type'),
        Index('pm_volume_id', 'pm_volume_id'),
        Index('pm_work_id', 'pm_work_id')
    )

    create_time = mapped_column(TIMESTAMP, nullable=False, server_default=text('CURRENT_TIMESTAMP'))
    pm_id = mapped_column(Integer, primary_key=True)
    update_time = mapped_column(TIMESTAMP, server_default=text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'))
    pm_type = mapped_column(Integer)
    pm_work_id = mapped_column(Integer)
    pm_volume_id = mapped_column(Integer)
    pm_project = mapped_column(Integer)
    pm_project_state_id = mapped_column(Integer)

    pm_projects: Mapped[Optional['PmProjects']] = relationship('PmProjects', back_populates='pm_project_members')
    pm_project_state: Mapped[Optional['PmMemberStates']] = relationship('PmMemberStates',
                                                                        back_populates='pm_project_members')
    pm_member_types: Mapped[Optional['PmMemberTypes']] = relationship('PmMemberTypes',
                                                                      back_populates='pm_project_members')
    pm_volume: Mapped[Optional['Volumes']] = relationship('Volumes', back_populates='pm_project_members')
    pm_work: Mapped[Optional['Works']] = relationship('Works', back_populates='pm_project_members')


class ProcessLog(Base):
    __tablename__ = 'process_log'
    __table_args__ = (
        ForeignKeyConstraint(['volumeId'], ['Volumes.volumeId'], ondelete='CASCADE', onupdate='CASCADE',
                             name='process_volume'),
        Index('process_volume_idx', 'volumeId')
    )

    update_time = mapped_column(TIMESTAMP, nullable=False,
                                server_default=text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'))
    activity_date = mapped_column(Date, nullable=False)
    processLogId = mapped_column(Integer, primary_key=True)
    result = mapped_column(String(45), nullable=False)
    create_time = mapped_column(TIMESTAMP, server_default=text('CURRENT_TIMESTAMP'))
    volumeId = mapped_column(Integer)

    Volumes_: Mapped[Optional['Volumes']] = relationship('Volumes', back_populates='process_log')


class SyncLog(Base):
    __tablename__ = 'sync_log'
    __table_args__ = (
        ForeignKeyConstraint(['volumeId'], ['Volumes.volumeId'], ondelete='CASCADE', onupdate='CASCADE',
                             name='activity_volume'),
        Index('activity_volume_idx', 'volumeId')
    )

    volumeId = mapped_column(Integer, nullable=False)
    activity_date = mapped_column(Date, nullable=False)
    syncLogId = mapped_column(Integer, primary_key=True)
    result = mapped_column(String(45), nullable=False)
    create_time = mapped_column(TIMESTAMP, server_default=text('CURRENT_TIMESTAMP'))
    update_time = mapped_column(TIMESTAMP, server_default=text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'))

    Volumes_: Mapped['Volumes'] = relationship('Volumes', back_populates='sync_log')
