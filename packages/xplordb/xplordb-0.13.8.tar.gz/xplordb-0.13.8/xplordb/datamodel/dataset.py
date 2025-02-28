"""
Module define a data set

Module define a data set


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


class Dataset:

    def __init__(self, name: str, loaded_by: str, full_name: str = None):
        """
        Define a data set used to store collar and associated data

        :param name: data set unique identifier
        :param loaded_by: person used to load data set
        :param full_name: full data set name
        """
        self.name = name
        if full_name:
            self.full_name = full_name
        else:
            self.full_name = name

        self.loaded_by = loaded_by
