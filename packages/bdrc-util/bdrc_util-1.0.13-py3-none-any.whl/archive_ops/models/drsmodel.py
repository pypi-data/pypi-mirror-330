# coding: utf-8
from sqlalchemy import BigInteger, Column, DECIMAL, Date, DateTime, ForeignKey, Integer, JSON, String, TIMESTAMP, Table, Text, text
from sqlalchemy.dialects.mysql import BIT, LONGTEXT, VARCHAR
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

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


t_BUDAImageInfos = Table(
    'BUDAImageInfos', metadata,
    Column('WorkName', String(45)),
    Column('WorkImageFileCount', BigInteger, server_default=text("'0'")),
    Column('WorkImageTotalFileSize', BigInteger, server_default=text("'0'")),
    Column('dip_activity_finish', DateTime)
)


class BuildPath(Base):
    __tablename__ = 'BuildPaths'

    buildPathId = Column(Integer, primary_key=True)
    BuildPath = Column(String(255), nullable=False, unique=True)
    create_time = Column(DateTime, server_default=text("CURRENT_TIMESTAMP"))
    update_time = Column(DateTime, server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))
    build_dir = Column(String(45), index=True, comment='basename of buildPath')


class DIPConfig(Base):
    __tablename__ = 'DIP_config'

    idDIP_CONFIG = Column(String(45), primary_key=True, comment='Contains undefined strings representing config values. Sample client is GET_DIP_CONFIG which looks for values and casts them to integers.')
    DIP_CONFIG_DESC = Column(String(255), nullable=False, unique=True)
    DIP_CONFIG_VALUE = Column(String(45), nullable=False)


class DRSCumStatu(Base):
    __tablename__ = 'DRS_cum_status'

    create_time = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP"))
    update_time = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))
    DRS_cum_statusId = Column(Integer, primary_key=True)
    batch_count = Column(Integer, nullable=False)
    object_count = Column(Integer, nullable=False)
    obs_date = Column(Date, nullable=False, unique=True)
    work_count_built_not_uploaded = Column(Integer, nullable=False)
    work_count_partly_uploaded = Column(Integer, nullable=False)
    work_count_complete_upload = Column(Integer, nullable=False)
    uploaded_image_count = Column(Integer, nullable=False)
    uploaded_size_total = Column(BigInteger)


t_Deletions = Table(
    'Deletions', metadata,
    Column('create_time', TIMESTAMP, server_default=text("CURRENT_TIMESTAMP")),
    Column('update_time', TIMESTAMP, server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP")),
    Column('BuildDate', DateTime),
    Column('BuildPath', String(255)),
    Column('Requested', String(45))
)


t_DepositedWorksFacts = Table(
    'DepositedWorksFacts', metadata,
    Column('workId', Integer, server_default=text("'0'")),
    Column('WorkName', String(45)),
    Column('HOLLIS', String(45)),
    Column('create_time', TIMESTAMP, server_default=text("CURRENT_TIMESTAMP")),
    Column('update_time', TIMESTAMP, server_default=text("CURRENT_TIMESTAMP")),
    Column('workVolumes', BigInteger),
    Column('DRSVolumes', BigInteger)
)


t_FPL_Image_Counts_Quarter = Table(
    'FPL_Image_Counts_Quarter', metadata,
    Column('FYQuarter', String(9)),
    Column('QBegin', Date),
    Column('QEnd', Date),
    Column('Work_Count', BigInteger, server_default=text("'0'")),
    Column('Total_Page_Size', DECIMAL(41, 0)),
    Column('Total_Page_Count', DECIMAL(41, 0))
)


t_GB_Activity_Journal = Table(
    'GB_Activity_Journal', metadata,
    Column('date(step_time)', Date),
    Column('Upload_Content', DECIMAL(23, 0)),
    Column('Conversion_Requests', DECIMAL(23, 0)),
    Column('Downloads', DECIMAL(23, 0)),
    Column('Unpack', DECIMAL(23, 0)),
    Column('Distributions', DECIMAL(23, 0))
)


class GBContentState(Base):
    __tablename__ = 'GB_Content_State'

    create_time = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP"))
    update_time = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))
    volume_id = Column(Integer, primary_key=True, nullable=False)
    job_state = Column(String(45), primary_key=True, nullable=False)
    gb_log = Column(LONGTEXT)
    state_date = Column(DateTime, primary_key=True, nullable=False)


t_GB_Content_Work = Table(
    'GB_Content_Work', metadata,
    Column('WorkName', String(45)),
    Column('label', String(45)),
    Column('create_time', TIMESTAMP, server_default=text("CURRENT_TIMESTAMP")),
    Column('update_time', TIMESTAMP, server_default=text("CURRENT_TIMESTAMP")),
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
    Column('create_time', TIMESTAMP, server_default=text("CURRENT_TIMESTAMP")),
    Column('update_time', TIMESTAMP, server_default=text("CURRENT_TIMESTAMP")),
    Column('id', Integer, server_default=text("'0'")),
    Column('work_id', Integer),
    Column('upload_time', DateTime),
    Column('upload_result', Integer)
)


class GBReadyTrack(Base):
    __tablename__ = 'GB_Ready_Track'

    id = Column(Integer, primary_key=True)
    create_time = Column(TIMESTAMP, nullable=False, server_default=text("CURRENT_TIMESTAMP"))
    update_time = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))
    target_id = Column(Integer, comment='Id in specific tabel, varies with activity')
    activity = Column(String(50), comment='Supported activities: download unpack')


class GetReadyLog(Base):
    __tablename__ = 'GetReadyLog'

    create_time = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP"))
    update_time = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))
    getReadyLog_id = Column(Integer, primary_key=True)
    vols_unqueued_pre = Column(Integer, nullable=False, server_default=text("'-1'"))
    vols_unqueued_post = Column(Integer, nullable=False, server_default=text("'-1'"))
    works_unqueued_pre = Column(Integer, nullable=False, server_default=text("'-1'"))
    works_unqueued_post = Column(Integer, nullable=False, server_default=text("'-1'"))
    works_fetched = Column(Integer, nullable=False, server_default=text("'-1'"))
    vols_fetched = Column(Integer, nullable=False, server_default=text("'-1'"))


class HulVol(Base):
    __tablename__ = 'HulVol'

    C1 = Column(String(45), primary_key=True)


t_Image_Counts_Quarter = Table(
    'Image_Counts_Quarter', metadata,
    Column('FYQuarter', String(9)),
    Column('QBegin', Date),
    Column('QEnd', Date),
    Column('Work_Count', BigInteger, server_default=text("'0'")),
    Column('Total_Page_Size', DECIMAL(41, 0)),
    Column('Total_Page_Count', DECIMAL(41, 0))
)


t_NLM_Image_Counts_Quarter = Table(
    'NLM_Image_Counts_Quarter', metadata,
    Column('FYQuarter', String(9)),
    Column('QBegin', Date),
    Column('QEnd', Date),
    Column('Work_Count', BigInteger, server_default=text("'0'")),
    Column('Total_Page_Size', DECIMAL(41, 0)),
    Column('Total_Page_Count', DECIMAL(41, 0))
)


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


t_USAID_Image_Counts_Quarter = Table(
    'USAID_Image_Counts_Quarter', metadata,
    Column('FYQuarter', String(11)),
    Column('QBegin', Date),
    Column('QEnd', Date),
    Column('Work_Count', BigInteger, server_default=text("'0'")),
    Column('Total_Page_Size', DECIMAL(41, 0)),
    Column('Total_Page_Count', DECIMAL(41, 0))
)


t_Volumes_only = Table(
    'Volumes_only', metadata,
    Column('volumeId', Integer, server_default=text("'0'")),
    Column('workId', Integer),
    Column('create_time', TIMESTAMP, server_default=text("CURRENT_TIMESTAMP")),
    Column('update_time', TIMESTAMP, server_default=text("CURRENT_TIMESTAMP")),
    Column('label', String(45)),
    Column('batchBuildId', Integer),
    Column('builtFileSize', BigInteger),
    Column('builtFileCount', Integer),
    Column('Queued', BIT(1), server_default=text("'b''0'''")),
    Column('Queued_time', DateTime)
)


class Work(Base):
    __tablename__ = 'Works'

    workId = Column(Integer, primary_key=True)
    WorkName = Column(String(45), unique=True)
    HOLLIS = Column(String(45))
    create_time = Column(TIMESTAMP, nullable=False, server_default=text("CURRENT_TIMESTAMP"))
    update_time = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))
    WorkSize = Column(BigInteger, server_default=text("'0'"))
    WorkFileCount = Column(Integer, server_default=text("'0'"))
    WorkImageFileCount = Column(BigInteger, server_default=text("'0'"))
    WorkImageTotalFileSize = Column(BigInteger, server_default=text("'0'"))
    WorkNonImageFileCount = Column(BigInteger, server_default=text("'0'"))
    WorkNonImageTotalFileSize = Column(BigInteger, server_default=text("'0'"))


# ?? Work?? class GBMetadataTrack(Work):
class GBMetadataTrack(Base):
    __tablename__ = 'GB_Metadata_Track'

    create_time = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP"))
    update_time = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))
    id = Column(ForeignKey('Works.workId'), primary_key=True)
    work_id = Column(Integer, nullable=False)
    upload_time = Column(DateTime, nullable=False)
    upload_result = Column(Integer)


class UsaidWork(Base):
    __tablename__ = 'usaid_work'
    __table_args__ = {'comment': 'Works ids in USAID'}

    work_id = Column(ForeignKey('Works.workId', ondelete='CASCADE', onupdate='CASCADE'), primary_key=True)


t_d4_new_not_restored_for_sql = Table(
    'd4-new-not-restored-for-sql', metadata,
    Column('WorkName', Text)
)


t_dac_special = Table(
    'dac_special', metadata,
    Column('create_time', TIMESTAMP, server_default=text("CURRENT_TIMESTAMP")),
    Column('update_time', TIMESTAMP, server_default=text("CURRENT_TIMESTAMP")),
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

    create_time = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP"))
    update_time = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))
    dip_activity_type_id = Column(Integer, primary_key=True, nullable=False)
    dip_activity_start = Column(DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP"))
    dip_activity_finish = Column(DateTime)
    dip_activity_result_code = Column(Integer)
    dip_source_path = Column(String(255))
    dip_dest_path = Column(String(255))
    work_id = Column(Integer, primary_key=True, nullable=False)
    dip_external_id = Column(String(45), unique=True)
    dip_comment = Column(LONGTEXT)


t_dip_activity_current_single_archive_workflow = Table(
    'dip_activity_current_single_archive_workflow', metadata,
    Column('create_time', TIMESTAMP, server_default=text("CURRENT_TIMESTAMP")),
    Column('update_time', TIMESTAMP, server_default=text("CURRENT_TIMESTAMP")),
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
    Column('create_time', TIMESTAMP, server_default=text("CURRENT_TIMESTAMP")),
    Column('update_time', TIMESTAMP, server_default=text("CURRENT_TIMESTAMP")),
    Column('dip_activity_type_id', Integer),
    Column('work_id', Integer)
)


class DipActivityType(Base):
    __tablename__ = 'dip_activity_types'

    iddip_activity_types = Column(Integer, primary_key=True)
    dip_activity_types_label = Column(String(45))


t_dip_activity_work = Table(
    'dip_activity_work', metadata,
    Column('workId', Integer, server_default=text("'0'")),
    Column('WorkName', String(45)),
    Column('dip_activity_types_label', String(45)),
    Column('dip_activity_start', DateTime, server_default=text("'CURRENT_TIMESTAMP'")),
    Column('dip_activity_finish', DateTime),
    Column('dip_source_path', String(255)),
    Column('dip_dest_path', String(255)),
    Column('dip_external_id', String(45)),
    Column('dip_comment', LONGTEXT),
    Column('create_time', TIMESTAMP, server_default=text("CURRENT_TIMESTAMP")),
    Column('update_time', TIMESTAMP, server_default=text("CURRENT_TIMESTAMP")),
    Column('dip_activity_type_id', Integer)
)


class GlacierSyncProgres(Base):
    __tablename__ = 'glacier_sync_progress'

    create_time = Column(TIMESTAMP, nullable=False, server_default=text("CURRENT_TIMESTAMP"))
    update_time = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))
    id = Column(Integer, primary_key=True)
    object_name = Column(String(255))
    restore_requested_on = Column(TIMESTAMP)
    restore_complete_on = Column(TIMESTAMP)
    download_complete_on = Column(TIMESTAMP)
    debag_complete_on = Column(TIMESTAMP)
    sync_complete_on = Column(TIMESTAMP)
    user_data = Column(JSON, comment='format:[ {"time_stamp" : <current_time>, "user_data" : provided_user_data object}... ]')


class PmMemberState(Base):
    __tablename__ = 'pm_member_states'

    create_time = Column(TIMESTAMP, nullable=False, server_default=text("CURRENT_TIMESTAMP"))
    update_time = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))
    id = Column(Integer, primary_key=True)
    m_state_name = Column(String(45), nullable=False)
    m_state_desc = Column(LONGTEXT)


class PmMemberType(Base):
    __tablename__ = 'pm_member_types'

    create_time = Column(TIMESTAMP, nullable=False, server_default=text("CURRENT_TIMESTAMP"))
    update_time = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))
    id = Column(Integer, primary_key=True)
    m_type = Column(String(45), nullable=False)


class PmProjectType(Base):
    __tablename__ = 'pm_project_types'

    create_time = Column(TIMESTAMP, nullable=False, server_default=text("CURRENT_TIMESTAMP"))
    update_time = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))
    id = Column(Integer, primary_key=True)
    project_type_name = Column(String(45), nullable=False)
    project_type_desc = Column(LONGTEXT)


t_processing = Table(
    'processing', metadata,
    Column('create_time', TIMESTAMP, server_default=text("CURRENT_TIMESTAMP")),
    Column('update_time', TIMESTAMP, server_default=text("CURRENT_TIMESTAMP")),
    Column('volumeId', Integer),
    Column('activity_date', Date),
    Column('processLogId', Integer, server_default=text("'0'")),
    Column('result', String(45))
)


t_usaid_drs = Table(
    'usaid_drs', metadata,
    Column('workId', Integer, server_default=text("'0'")),
    Column('WorkName', String(45)),
    Column('HOLLIS', String(45)),
    Column('create_time', TIMESTAMP, server_default=text("CURRENT_TIMESTAMP")),
    Column('update_time', TIMESTAMP, server_default=text("CURRENT_TIMESTAMP")),
    Column('WorkSize', BigInteger, server_default=text("'0'")),
    Column('WorkFileCount', Integer, server_default=text("'0'")),
    Column('WorkImageFileCount', BigInteger, server_default=text("'0'")),
    Column('WorkImageTotalFileSize', BigInteger, server_default=text("'0'")),
    Column('WorkNonImageFileCount', BigInteger, server_default=text("'0'")),
    Column('WorkNonImageTotalFileSize', BigInteger, server_default=text("'0'"))
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


class WorksForDrs2023(Base):
    __tablename__ = 'works_for_drs_2023'
    __table_args__ = {'comment': 'Works which must be in DRS'}

    id = Column(Integer, primary_key=True)
    WorkName = Column(String(15))


t_zju_femc_excludes = Table(
    'zju_femc_excludes', metadata,
    Column('WorkName', String(45))
)


class BatchBuild(Base):
    __tablename__ = 'BatchBuilds'

    batchBuildId = Column(Integer, primary_key=True)
    BuildDate = Column(DateTime)
    Result = Column(String(45))
    create_time = Column(DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP"))
    update_time = Column(DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))
    TransferQueuedDate = Column(DateTime)
    TransferCompleteDate = Column(DateTime)
    buildPathId = Column(ForeignKey('BuildPaths.buildPathId', ondelete='SET NULL', onupdate='SET NULL'), unique=True)

    BuildPath = relationship('BuildPath')


class IATrack(Base):
    __tablename__ = 'IATrack'

    idIATrack = Column(Integer, primary_key=True)
    ia_id = Column(String(45), nullable=False, comment='Internet Archive Identifier - bdrc-workRid')
    workId = Column(ForeignKey('Works.workId'), nullable=False, index=True)
    task_id = Column(Integer, server_default=text("'-1'"))
    task_status = Column(String(15))
    task_complete = Column(DateTime)
    log = Column(String(255), comment='Log file location')

    Work = relationship('Work')


class DipActivity(Base):
    __tablename__ = 'dip_activity'

    create_time = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP"))
    update_time = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))
    dip_activity_type_id = Column(ForeignKey('dip_activity_types.iddip_activity_types'), primary_key=True, nullable=False, index=True)
    dip_activity_start = Column(DateTime, primary_key=True, nullable=False, server_default=text("CURRENT_TIMESTAMP"))
    dip_activity_finish = Column(DateTime)
    dip_activity_result_code = Column(Integer)
    dip_source_path = Column(String(255))
    dip_dest_path = Column(String(255))
    work_id = Column(ForeignKey('Works.workId'), primary_key=True, nullable=False, index=True)
    dip_external_id = Column(String(45), unique=True)
    dip_comment = Column(LONGTEXT)

    dip_activity_type = relationship('DipActivityType')
    work = relationship('Work')


class PmProject(Base):
    __tablename__ = 'pm_projects'

    create_time = Column(TIMESTAMP, nullable=False, server_default=text("CURRENT_TIMESTAMP"))
    update_time = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))
    id = Column(Integer, primary_key=True)
    name = Column(String(45))
    description = Column(LONGTEXT)
    project_type_id = Column(ForeignKey('pm_project_types.id'), index=True)
    m_type_id = Column(ForeignKey('pm_member_types.id'), index=True)

    m_type = relationship('PmMemberType')
    project_type = relationship('PmProjectType')


class WorkStatusCount(Base):
    __tablename__ = 'workStatusCount'

    create_time = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP"))
    update_time = Column(TIMESTAMP)
    workStatusCountId = Column(Integer, primary_key=True)
    Volumes = Column(Integer, nullable=False)
    NumberVolumesBatchQueued = Column(Integer, nullable=False)
    NumberVolumesBatchBuilt = Column(Integer, nullable=False)
    NumberVolumesUploadQueued = Column(Integer, nullable=False)
    NumberVolumesUploaded = Column(Integer, nullable=False)
    workId = Column(ForeignKey('Works.workId'), unique=True)
    NumberVolumesDeposited = Column(Integer)

    Work = relationship('Work')


class Volume(Base):
    __tablename__ = 'Volumes'

    volumeId = Column(Integer, primary_key=True, unique=True)
    workId = Column(ForeignKey('Works.workId'), index=True)
    create_time = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP"))
    update_time = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))
    label = Column(String(45), unique=True)
    batchBuildId = Column(ForeignKey('BatchBuilds.batchBuildId', ondelete='SET NULL', onupdate='CASCADE'), index=True)
    builtFileSize = Column(BigInteger)
    builtFileCount = Column(Integer)
    Queued = Column(BIT(1))
    Queued_time = Column(DateTime)

    BatchBuild = relationship('BatchBuild')
    Work = relationship('Work')


class SyncInventory(Base):
    __tablename__ = 'sync_inventory'
    __table_args__ = {'comment': 'Maps an archive sync event to a path containing the sync contents'}

    id = Column(Integer, primary_key=True, comment='key')
    dip_external_id = Column(ForeignKey('dip_activity.dip_external_id'), nullable=False, index=True, comment='dip-activity record')
    inventory_path = Column(VARCHAR(255), nullable=False, comment='Path to the inventory of the referenced sync')

    dip_external = relationship('DipActivity')


class DR(Base):
    __tablename__ = 'DRS'
    __table_args__ = {'comment': 'Corresponds to our data structures and to output/BDRCCun'}

    DRSid = Column(Integer, primary_key=True, unique=True)
    IngestDate = Column(DateTime)
    objectid = Column(String(45), comment='HUL Generated OBJ-ID')
    create_time = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP"))
    update_time = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))
    DRSdir = Column(String(45), index=True)
    objectUrn = Column(String(72))
    filesCount = Column(Integer)
    size = Column(BigInteger)
    OSN = Column(String(45), unique=True)
    volumeId = Column(ForeignKey('Volumes.volumeId'), index=True)

    Volume = relationship('Volume')


class GBContentTrack(Base):
    __tablename__ = 'GB_Content_Track'

    create_time = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP"))
    update_time = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))
    id = Column(Integer, primary_key=True)
    volume_id = Column(ForeignKey('Volumes.volumeId'), nullable=False, index=True)
    job_step = Column(String(45))
    step_time = Column(DateTime, nullable=False)
    step_rc = Column(Integer)
    gb_log = Column(LONGTEXT)

    volume = relationship('Volume')


class GBDistribution(Base):
    __tablename__ = 'GB_Distribution'

    id = Column(Integer, primary_key=True)
    create_time = Column(TIMESTAMP, nullable=False, server_default=text("CURRENT_TIMESTAMP"))
    update_time = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))
    volume_id = Column(ForeignKey('Volumes.volumeId'), index=True)
    dist_time = Column(TIMESTAMP)
    src = Column(String(255))
    dest = Column(String(255))

    volume = relationship('Volume')


class GBDownload(Base):
    __tablename__ = 'GB_Downloads'

    id = Column(Integer, primary_key=True)
    volume_id = Column(ForeignKey('Volumes.volumeId'), index=True)
    download_object_name = Column(String(255))
    download_path = Column(String(255))
    download_time = Column(TIMESTAMP)
    create_time = Column(TIMESTAMP, nullable=False, server_default=text("CURRENT_TIMESTAMP"))
    update_time = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))

    volume = relationship('Volume')


class GBUnpack(Base):
    __tablename__ = 'GB_Unpack'

    id = Column(Integer, primary_key=True)
    create_time = Column(TIMESTAMP, nullable=False, server_default=text("CURRENT_TIMESTAMP"))
    update_time = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))
    volume_id = Column(ForeignKey('Volumes.volumeId'), index=True)
    unpack_object_name = Column(String(255))
    unpacked_path = Column(String(255))
    unpack_time = Column(TIMESTAMP)

    volume = relationship('Volume')


class Outline(Base):
    __tablename__ = 'Outlines'

    volumeId = Column(ForeignKey('Volumes.volumeId', ondelete='CASCADE', onupdate='CASCADE'), nullable=False, unique=True)
    outlineId = Column(Integer, primary_key=True, unique=True)
    create_time = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP"))
    update_time = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))

    Volume = relationship('Volume')


class PrintMaster(Base):
    __tablename__ = 'PrintMasters'

    printMasterId = Column(Integer, primary_key=True, unique=True)
    volumeId = Column(ForeignKey('Volumes.volumeId', ondelete='CASCADE', onupdate='CASCADE'), nullable=False, unique=True)
    create_time = Column(TIMESTAMP, nullable=False, server_default=text("CURRENT_TIMESTAMP"))
    update_time = Column(TIMESTAMP, nullable=False, server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))

    Volume = relationship('Volume')


class PmProjectMember(Base):
    __tablename__ = 'pm_project_members'

    create_time = Column(TIMESTAMP, nullable=False, server_default=text("CURRENT_TIMESTAMP"))
    update_time = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))
    pm_id = Column(Integer, primary_key=True)
    pm_type = Column(ForeignKey('pm_member_types.id'), index=True)
    pm_work_id = Column(ForeignKey('Works.workId'), index=True)
    pm_volume_id = Column(ForeignKey('Volumes.volumeId'), index=True)
    pm_project = Column(ForeignKey('pm_projects.id'), index=True)
    pm_project_state_id = Column(ForeignKey('pm_member_states.id'), index=True)

    pm_project1 = relationship('PmProject')
    pm_project_state = relationship('PmMemberState')
    pm_member_type = relationship('PmMemberType')
    pm_volume = relationship('Volume')
    pm_work = relationship('Work')


class ProcessLog(Base):
    __tablename__ = 'process_log'

    create_time = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP"))
    update_time = Column(TIMESTAMP, nullable=False, server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))
    volumeId = Column(ForeignKey('Volumes.volumeId', ondelete='CASCADE', onupdate='CASCADE'), index=True)
    activity_date = Column(Date, nullable=False)
    processLogId = Column(Integer, primary_key=True)
    result = Column(String(45), nullable=False)

    Volume = relationship('Volume')
