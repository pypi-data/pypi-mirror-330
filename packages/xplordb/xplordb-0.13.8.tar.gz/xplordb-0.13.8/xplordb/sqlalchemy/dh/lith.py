from sqlalchemy import Column, String, ForeignKey, Float, Numeric
from xplordb.datamodel.lith import Lith

from xplordb.sqlalchemy.base import Base


class XplordbLithTable(Lith, Base):
    """
    Define Xplordb columns for lith definition
    """
    __tablename__ = "lith"
    __table_args__ = {"schema": 'dh'}

    data_set = Column("data_set", String, ForeignKey('ref.data_sets.data_set'))
    hole_id = Column("hole_id", String, ForeignKey('dh.collar.hole_id'), primary_key=True)

    lith_code = Column('lith_code_1', String, ForeignKey('ref.lithology.code'))

    # Columns defined as Numeric so they can be used as primary keys
    # Values in Lith class defined as float : not used as decimal
    from_m = Column('from_m', Numeric(asdecimal=False), primary_key=True)
    to_m = Column('to_m', Numeric(asdecimal=False), primary_key=True)

    loaded_by = Column(String, ForeignKey('ref.person.code'))
    logged_by = Column(String, ForeignKey('ref.person.code'))
