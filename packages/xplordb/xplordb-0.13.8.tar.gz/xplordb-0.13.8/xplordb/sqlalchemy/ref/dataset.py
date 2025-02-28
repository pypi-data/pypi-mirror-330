from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship

from xplordb.datamodel.dataset import Dataset
from xplordb.sqlalchemy.base import Base


class XplordbDatasetTable(Dataset, Base):
    """
    Define spatialite columns for Dataset definition
    """
    __tablename__ = "data_sets"
    __table_args__ = {"schema": 'ref'}

    name = Column('data_set', String, primary_key=True)
    full_name = Column(String)
    loaded_by = Column(String, ForeignKey('ref.person.code'))

    collars = relationship("XplordbCollarTable")
    surveys = relationship("XplordbSurveyTable")
    liths = relationship("XplordbLithTable")


