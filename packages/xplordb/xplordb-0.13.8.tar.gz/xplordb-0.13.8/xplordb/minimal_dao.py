"""
Minimal data acces object for xplordb test data injection

Minimal data acces object for xplordb test data injection.
With a pyscog2 session, insertion of :
- person
- dataset
- hole type
- collar
- survey



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
__date__ = "2022/02/02"
__license__ = "AGPLv3"

from sqlalchemy import text

from xplordb.datamodel.collar import Collar
from xplordb.datamodel.dataset import Dataset
from xplordb.datamodel.person import Person
from xplordb.datamodel.survey import Survey
from xplordb.import_data import ImportData


class MinimalDao:

    def __init__(self, db_session):
        """
        Simple Data Access Object class to insert some basic data into xplordb database
        :param db_session: psycog2 connection
        """
        self._db_session = db_session
        self._importer = ImportData(db_session)

    def create_person(self, name: str):
        self._importer.import_persons_array([Person(name)])

    def create_dataset(self, name: str, person: str):
        self._importer.import_datasets_array([Dataset(name, person)])

    def create_collar(self, name: str, data_set: str, person: str,
                      x: float = 0.0, y: float = 0.0, z: float = 0.0, srid: int = 3857, eoh: float = None,
                      create_needed_data: bool = True):
        if create_needed_data:
            self.create_person(person)
            self.create_dataset(data_set, person)

        self._importer.import_collars_array([Collar(name, data_set, person, x, y, z, srid, eoh)])

    def create_details(self, from_m: float, to_m: float, colar: str, data_set: str, person: str):
        self._db_session.execute(text(f"INSERT INTO dh.details (data_set,hole_id,loaded_by,from_m,to_m) "
                        f"VALUES ('{data_set}','{colar}','{person}',{from_m},{to_m})"))

    def create_surv(self, depth: float, dip: float, azimuth: float, colar: str, data_set: str, person: str):
        self._importer.import_surveys_array([Survey(colar, data_set, person, depth, dip, azimuth)])

    def create_invalid_surv(self, depth: float, dip: float, azimuth: float, colar: str, data_set: str, person: str):
        self._db_session.execute(text(f"INSERT INTO dh.surv (data_set,hole_id,loaded_by,depth_m,dip,azimuth,azimuth_grid) "
                        f"VALUES ('{data_set}','{colar}','{person}',{depth},{dip},{azimuth},{azimuth})"))
