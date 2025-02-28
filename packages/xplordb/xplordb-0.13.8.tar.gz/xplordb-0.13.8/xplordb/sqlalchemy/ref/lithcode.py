from sqlalchemy import Column, String, ForeignKey
from xplordb.datamodel.lith import LithCode

from xplordb.sqlalchemy.base import Base


class XplordbLithCodeTable(LithCode, Base):
    """
    Define Xplordb columns for lith code definition
    """
    __tablename__ = "lithology"
    __table_args__ = {"schema": 'ref'}

    code = Column('code', String, primary_key=True)
    description = Column('description', String)
    loaded_by = Column(String, ForeignKey('ref.person.code'))
