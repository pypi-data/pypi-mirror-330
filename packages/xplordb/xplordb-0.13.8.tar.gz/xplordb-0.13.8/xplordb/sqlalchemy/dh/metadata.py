from geoalchemy2 import Geometry
from sqlalchemy import Column, String, Float

from xplordb.datamodel.metadata import CollarMetadata, RawCollarMetadata
from xplordb.sqlalchemy.base import Base

DEFAULT_SRID = 4326



class XplordbCollarMetadataTable(CollarMetadata, Base):
    """
    Define Xplordb columns for Collar metadata definition
    """
    __tablename__ = "metadata"
    __table_args__ = {"schema": 'dh'}
    hole_id = Column("hole_id", String, primary_key = True)  
  

def create_xplordbcollarmetadataTable(collar_metadata:RawCollarMetadata) -> tuple:
    """
    Function returning updated XplordbCollarMetadataTable class instance for a specific hole_id and table definition
    """
    # we should derive base class to not alter it.
    class tmp(XplordbCollarMetadataTable):
        pass
    metadata_base = tmp

    for col_name, value in collar_metadata.extra_cols.items():
        data_type = String if type(value) == str else Float
        column = Column(col_name, data_type)
        if not hasattr(metadata_base, col_name):
            setattr(metadata_base, col_name, column)

    metadata_base_instance = metadata_base(collar_metadata.hole_id)
    for col_name, value in collar_metadata.extra_cols.items():
        
        setattr(metadata_base_instance, col_name, value)

    return metadata_base_instance, metadata_base