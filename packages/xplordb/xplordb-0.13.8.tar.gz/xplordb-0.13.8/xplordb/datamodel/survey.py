"""
Module define a survey

Module define a survey


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


class Survey:

    def __init__(self, hole_id: str, data_set: str, loaded_by: str,
                 depth: float, dip: float, azimuth: float):
        """
        Define a survey

        :param hole_id: collar used
        :param data_set: data set associated
        :param loaded_by: person loading survey in database
        :param depth: survey depth (meters)
        :param dip: survey dip (degrees)
        :param azimuth: survey azimuth (degrees)
        """
        self.data_set = data_set
        self.hole_id = hole_id
        self.loaded_by = loaded_by
        self.depth = depth
        self.dip = dip
        self.azimuth = azimuth
