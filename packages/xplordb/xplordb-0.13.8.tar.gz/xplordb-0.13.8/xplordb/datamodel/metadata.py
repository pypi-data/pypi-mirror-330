"""
Module define a collar

Module define a collar


xplordb

Copyright (C) 2022  Oslandia / OpenLog
This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as published
by the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""
__authors__ = ["vlarmet"]
__contact__ = "vincent.larmet@apeiron.technology"
__date__ = "2024/04/11"
__license__ = "AGPLv3"

from datetime import datetime


class RawCollarMetadata:

    def __init__(self, hole_id: str, extra_cols: dict
                 ):
        """
        Define a raw collar metadata.  
        Metadata are additional collar attributes.

        :param hole_id: collar name and unique identifier
        :param extra_cols
        """
        self.hole_id = hole_id
        self.extra_cols = extra_cols
    
class CollarMetadata:

    def __init__(self, hole_id: str
                 ):
        """
        Define a collar metadata.  
        Metadata are additional collar attributes.

        :param hole_id: collar name and unique identifier
        :param extra_cols
        """
        self.hole_id = hole_id

def create_collar_metadata(raw_collar_metadata: RawCollarMetadata) -> CollarMetadata:

    hole_id = raw_collar_metadata.hole_id
    metadata = CollarMetadata(hole_id=hole_id)
    for col_name, value in raw_collar_metadata.extra_cols.items():
        setattr(metadata, col_name, value)

    return metadata