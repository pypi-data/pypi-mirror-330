"""
Module define a lithology and associated lithology code

Module define a lithology and associated lithology code


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


class LithCode:

    def __init__(self, code: str, loaded_by: str, description: str = None):
        """
        Define a lithology code

        :param code: unique lithology code identifier
        :param loaded_by:  person used to load lithology code
        :param description: description of lithology code
        """
        self.code = code
        self.loaded_by = loaded_by
        if description:
            self.description = description
        else:
            self.description = code


class Lith:

    def __init__(self, lith_code: str, data_set: str, hole_id: str, loaded_by: str,
                 from_m: float, to_m: float, logged_by: str = None):
        """
        Define a lithologu

        :param lith_code: lithology code
        :param data_set: data set associated
        :param hole_id: collar used
        :param loaded_by: person loading lithology in database
        :param from_m: start of lithology from collar (meters)
        :param to_m: end of lithology from collar (meters)
        :param logged_by: person who logged lithology
        """
        self.lith_code = lith_code
        self.data_set = data_set
        self.hole_id = hole_id
        self.loaded_by = loaded_by
        self.from_m = from_m
        self.to_m = to_m
        if logged_by:
            self.logged_by = logged_by
        else:
            self.logged_by = loaded_by
