"""
Module define a person

Module define a person


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


class Person:

    def __init__(self, trigram: str, full_name: str = None, active: bool = True, type: str = 'unknown'):
        """
        Define a person using xplordb database

        :param trigram: unique trigram
        :param full_name: full name of person
        """
        self.code = trigram
        if full_name:
            self.full_name = full_name
        else:
            self.full_name = trigram

        self.type = type
        self.loaded_by = trigram
        self.active = active
