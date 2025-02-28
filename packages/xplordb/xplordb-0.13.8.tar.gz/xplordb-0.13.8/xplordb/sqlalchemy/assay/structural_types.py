import json
from sqlalchemy.types import UserDefinedType

class pgAzimuthType(UserDefinedType):
    def get_col_spec(self):
        return "assay.azimuth"
    
class pgDipType(UserDefinedType):
    def get_col_spec(self):
        return "assay.dip"
    
class pgSphericalObjectType(UserDefinedType):
    def get_col_spec(self):
        return "assay.kind"
    
class pgPolarityType(UserDefinedType):
    def get_col_spec(self):
        return "assay.polarity"

class pgSphericalType(UserDefinedType):
    def get_col_spec(self):
        return "assay.spherical_data"
    
    @staticmethod
    def insert(azimuth: float, dip:float, polarity:int = 0, type: str = 'line'):
        res = f'({azimuth},{dip},{int(polarity)},{type.lower()})'
        return res

    @staticmethod
    def insert_from_dict(d: dict):
        return pgSphericalType.insert(**d)
    
    @staticmethod
    def insert_from_json(j: str):
        d = json.loads(j)
        return pgSphericalType.insert_from_dict(d)