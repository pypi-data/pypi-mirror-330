from sqlalchemy import Column, String, Boolean
from sqlalchemy.orm import relationship

from xplordb.datamodel.person import Person

from xplordb.sqlalchemy.base import Base


class XplordbPersonTable(Person, Base):
    """
    Define Xplordb columns for Person definition
    """
    __tablename__ = "person"
    __table_args__ = {"schema": 'ref'}

    code = Column('code', String, primary_key=True)
    full_name = Column('person', String)
    loaded_by = Column(String)
    type = Column('type', String)
    active = Column('active', Boolean)

    datasets = relationship("XplordbDatasetTable")
    lith_codes = relationship("XplordbLithCodeTable")
