from sqlalchemy import Column, String, ForeignKey, Float, Numeric

from xplordb.datamodel.survey import Survey

from xplordb.sqlalchemy.base import Base


class XplordbSurveyTable(Survey, Base):
    """
    Define Xplordb columns for Survey definition
    """
    __tablename__ = "surv"
    __table_args__ = {"schema": 'dh'}

    data_set = Column("data_set", String, ForeignKey('ref.data_sets.data_set'))
    hole_id = Column("hole_id", String, ForeignKey('dh.collar.hole_id'), primary_key=True)
    loaded_by = Column("loaded_by", String)

    # Column defined as Numeric so they can be used as primary keys
    # Value in Survey class defined as float : not used as decimal
    depth = Column("depth_m", Numeric(asdecimal=False), primary_key=True)
    dip = Column("dip", Float)
    azimuth = Column("azimuth_grid", Float)
