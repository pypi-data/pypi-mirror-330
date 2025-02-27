"""
SQLAlchemy version of clean up current.
Too risky, but it's at least a skeleton of an API for dip_activity
"""

# Base classes for drs tables
import pprint

from BdrcDbLib.DbOrm.DrsContextBase import DrsDbContextBase
from BdrcDbLib.DbOrm.models.drs import Works

# Import sqlalchemy stuff
# TODO: Trim


from sqlalchemy.orm import declarative_base, relationship, backref, Mapped, mapped_column
from sqlalchemy import Column, DateTime, text, func, select
from sqlalchemy import ForeignKey, String, Integer
from sqlalchemy.dialects.mysql import (
    BIGINT,
    # BINARY,
    # BIT,
    # BLOB,
    # BOOLEAN,
    # CHAR,
    # DATE,
    # DATETIME,
    # DECIMAL,
    # DECIMAL,
    # DOUBLE,
    # ENUM,
    # FLOAT,
    INTEGER,
    # LONGBLOB,
    LONGTEXT,
    # MEDIUMBLOB,
    # MEDIUMINT,
    # MEDIUMTEXT,
    # NCHAR,
    # NUMERIC,
    # NVARCHAR,
    # REAL,
    # SET,
    # SMALLINT,
    # TEXT,
    # TIME,
    TIMESTAMP,
    # TINYBLOB,
    # TINYINT,
    # TINYTEXT,
    # VARBINARY,
    # VARCHAR,
    # YEAR,
)

from BdrcDbLib.DbOrm.models.drs import *

Base = declarative_base()


class DipActivityTypes(Base):
    id: Mapped[int] = mapped_column(name="iddip_activity_types", primary_key=True)
    label: Mapped[str] = mapped_column(name="dip_activity_types_label", primary_key=True)
    __tablename__ = 'dip_activity_types'


class dac(TimestampMixin, Base):
    """
    Two tables share this structure
    """
    dip_activity_type_id = Column(Integer, ForeignKey(DipActivityTypes.id))
    dip_activity_start = Column(TIMESTAMP, nullable=True)
    dip_activity_finish = Column(TIMESTAMP, nullable=True)
    dip_activity_result_code = Column(INTEGER)
    dip_source_path = Column(String(255))
    dip_dest_path = Column(String(255))
    work_id = Column(INTEGER, ForeignKey(Works.workId))
    dip_external_id = Column(String(45), primary_key=True)
    dip_comment = Column(LONGTEXT)
    __tablename__ = "dip_activity_current"

    work = relationship(Works)
    activity = relationship(DipActivityTypes)

    def __repr__(self):
        return f"{self.dip_external_id:2} - w:{self.work.WorkName:10} a: {self.activity.label:15} fin:{self.dip_activity_finish}, dest:{self.dip_dest_path}"


#
# class dac(DipActivityBase):
#     __tablename__ = 'dip_activity_current'


with DrsDbContextBase() as ctx:
    # currents = ctx.session.query(dac).all()
    sq = select(dac.dip_activity_finish, Works.WorkName, dac.dip_dest_path, DipActivityTypes.label, func.count(dac.work_id))\
        .join(Works)\
        .join(DipActivityTypes)\
        .group_by(dac.dip_activity_type_id)\
        .group_by(dac.work_id)\
        .having(func.count(dac.work_id) > 1)
    # .group_by(dac.dip_dest_path)

    print(sq)
    querystmt = ctx.session.execute(sq
       )

    ares = querystmt.all()

    pprint.pprint(ares)
