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
__authors__ = ["jmkerloch"]
__contact__ = "geology@oslandia.com"
__date__ = "2022/02/09"
__license__ = "AGPLv3"

from datetime import datetime


class Collar:

    def __init__(self, hole_id: str, data_set: str, loaded_by: str,
                 x: float, y: float, z: float, srid: int, 
                 eoh: float = None, planned_x: float = None, planned_y: float = None, planned_z: float = None,planned_eoh: float = None, survey_date: datetime = None, 
                 project_srid: int = 4326, dip: float = -90, azimuth: float = 0
                 ):
        """
        Define a collar

        :param hole_id: collar name and unique identifier
        :param data_set: data set associated to collar
        :param loaded_by: person used to load collar
        :param x: x coordinate of collar
        :param y: y coordinate of collar
        :param z: z coordinate of collar
        :param srid: srid for coordinate
        :param eoh : (optionnal) end of hole depth
        :param survey_date : (optionnal) date of collar creation
        """
        self.hole_id = hole_id
        self.data_set = data_set
        self.loaded_by = loaded_by
        self.x = x
        self.y = y
        self.z = z
        self.srid = srid
        self.project_srid = project_srid
        self.eoh = eoh
        self.planned_x = planned_x
        self.planned_y = planned_y
        self.planned_z = planned_z
        self.planned_eoh = planned_eoh
        self.dip = dip
        self.azimuth = azimuth
        self.survey_date = survey_date
