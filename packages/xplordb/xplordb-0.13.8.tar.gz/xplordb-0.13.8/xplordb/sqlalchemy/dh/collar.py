from geoalchemy2 import Geometry
from sqlalchemy import Column, String, ForeignKey, Float, Integer, DateTime

from xplordb.datamodel.collar import Collar
from xplordb.sqlalchemy.base import Base

DEFAULT_SRID = 4326


class XplordbCollarTable(Collar, Base):
    """
    Define Xplordb columns for Collar definition
    """
    __tablename__ = "collar"
    __table_args__ = {"schema": 'dh'}

    hole_id = Column("hole_id", String, primary_key=True)
    data_set = Column("data_set", String, ForeignKey('ref.data_sets.data_set'))
    x = Column("x", Float)
    y = Column("y", Float)
    z = Column("z", Float)
    srid = Column("srid", Integer)
    project_srid = Column("project_srid", Integer)
    eoh = Column("eoh", Float)
    planned_x = Column("planned_x", Float)
    planned_y = Column("planned_y", Float)
    planned_z = Column("planned_z", Float)
    planned_eoh = Column("planned_eoh", Float)
    dip = Column("dip", Float)
    azimuth = Column("azimuth", Float)
    loaded_by = Column("loaded_by", String)
    survey_date = Column("survey_date", DateTime)
    geom = Column(Geometry(geometry_type='POINT', dimension=3, srid=DEFAULT_SRID))
    planned_loc = Column(Geometry(geometry_type='POINT', dimension=3, srid=DEFAULT_SRID))
    geom_trace = Column(Geometry(geometry_type='LINESTRING', dimension=3, srid=DEFAULT_SRID))
    planned_trace = Column(Geometry(geometry_type='LINESTRING', dimension=3, srid=DEFAULT_SRID))
