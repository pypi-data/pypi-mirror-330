"""
Module use to import data into an existing xplordb database

Module use to import data into an existing xplordb database


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

import psycopg2
import sqlalchemy

from xplordb.datamodel.collar import Collar
from xplordb.datamodel.metadata import RawCollarMetadata, create_collar_metadata
from xplordb.sqlalchemy.dh.metadata import create_xplordbcollarmetadataTable
from xplordb.datamodel.dataset import Dataset
from xplordb.datamodel.lith import Lith, LithCode
from xplordb.datamodel.person import Person
from xplordb.datamodel.survey import Survey

from xplordb.sqlalchemy.dh.collar import XplordbCollarTable
from xplordb.sqlalchemy.dh.lith import XplordbLithTable
from xplordb.sqlalchemy.dh.survey import XplordbSurveyTable
from xplordb.sqlalchemy.ref.person import XplordbPersonTable
from xplordb.sqlalchemy.ref.dataset import XplordbDatasetTable
from xplordb.sqlalchemy.ref.lithcode import XplordbLithCodeTable


class ImportData:
    class ImportException(Exception):
        pass

    class InvalidSchema(psycopg2.Error):
        def __init__(self, table_name: str):
            super().__init__(f'Table "{table_name}" does not exist. Check if xplordb is installed.')

    def __init__(self, db_session):
        """
        A class used to import data into a xplordb database

        Example:
            import_data = ImportData(session)
            person = Person('xdb')
            import_data.import_persons_array([person])

        :param db_session: pyscog2 session
        """
        self._db_session = db_session

    def commit(self) -> None:
        """
        Commit current changes

        raises ImportException in case of error

        """

        try:
            self._db_session.commit()
        except sqlalchemy.exc.IntegrityError as exc:
            self._db_session.rollback()
            raise ImportData.ImportException(exc)

    def get_available_person_codes(self) -> [str]:
        """
        Get list af available person codes in xplordb

        Returns: list of available persons
        """
        persons = self._db_session.query(XplordbPersonTable.code).all()
        return [person.code for person in persons]

    def import_persons_array(self, persons: [Person]):
        """
        Import persons into xplordb.

        :param persons: Persons array
        """
        self._db_session.add_all([XplordbPersonTable(trigram=person.code, full_name=person.full_name,
                                                     active=person.active, type=person.type)
                                  for person in persons])

    def get_available_dataset_names(self) -> [str]:
        """
        Get list af available datasets in xplordb

        Returns: list of available dataset names
        """
        datasets = self._db_session.query(XplordbDatasetTable.name).all()
        return [dataset.name for dataset in datasets]

    def import_datasets_array(self, datasets: [Dataset]):
        """
        Import datasets into xplordb.

        :param datasets: Dataset array
        """
        self._db_session.add_all(
            [XplordbDatasetTable(name=dataset.name, full_name=dataset.full_name, loaded_by=dataset.loaded_by)
             for dataset in datasets])

    def import_collars_array(self, collars: [Collar]):
        """
        Import collars into xplordb.

        :param collars: Collar array
        """
        self._db_session.add_all(
            [XplordbCollarTable(hole_id=collar.hole_id, data_set=collar.data_set, loaded_by=collar.loaded_by,
                                x=collar.x, y=collar.y, z=collar.z, srid=collar.srid, project_srid = collar.project_srid, eoh=collar.eoh,
                                planned_x=collar.planned_x, planned_y=collar.planned_y, planned_z=collar.planned_z,planned_eoh=collar.planned_eoh, dip = collar.dip, azimuth = collar.azimuth,
                                survey_date=collar.survey_date)
             for collar in collars])
        
    def import_metadatas_array(self, metadatas: [RawCollarMetadata]):
        """
        Import metadata in xplordb.  
        Table is altered first, then values are updated.  
        """

        # add column if dont exists in database

        extra_cols = {}
        for m in metadatas:
            for col_name, value in m.extra_cols.items():
                sql_type = (
                "FLOAT" if type(value) != str else "VARCHAR"
            )
                extra_cols[col_name] = sql_type

        q = """
            SELECT column_name
            FROM information_schema.columns
            WHERE table_schema = 'dh'
            AND table_name   = 'metadata';
            """
        col_base = [r[0] for r in self._db_session.execute(q).fetchall()]

        for col_name, col_type in extra_cols.items():
             
            if col_name not in col_base:
                q = f"ALTER TABLE dh.metadata ADD COLUMN {col_name} {col_type} ;"
                self._db_session.execute(q)
                self.commit()


        # update data
        for metadata in metadatas:
            # generate a updated XplordbCollarMetadataTable definitio with extra columns
            _, cls = create_xplordbcollarmetadataTable(metadata)
            obj = self._db_session.query(cls).get(metadata.hole_id)
            for col_name, value in metadata.extra_cols.items():
                setattr(obj, col_name, value)

                self._db_session.commit()


    def import_surveys_array(self, surveys: [Survey]):
        """
        Import surveys into xplordb.

        :param surveys: Survey array
        """
        self._db_session.add_all(
            [XplordbSurveyTable(hole_id=survey.hole_id, data_set=survey.data_set, loaded_by=survey.loaded_by,
                                depth=survey.depth, dip=survey.dip, azimuth=survey.azimuth)
             for survey in surveys])

    def import_liths_array(self, liths: [Lith]):
        """
        Import liths into xplordb.

        :param liths: lith array
        """

        # Insert lith_code into database if not available
        unavailable_lith_code_tuple = [(lith.lith_code, lith.loaded_by) for lith in liths
                                       if not self._lith_code_available(lith.lith_code)]
        # Remove duplicates
        unavailable_lith_code_tuple = set(unavailable_lith_code_tuple)
        unavailable_lith_code_array = [LithCode(lith[0], lith[1]) for lith in unavailable_lith_code_tuple]

        self.import_lithology_codes_array(unavailable_lith_code_array)
        self._db_session.flush()
        self._db_session.add_all(
            [XplordbLithTable(data_set=lith.data_set, hole_id=lith.hole_id, loaded_by=lith.loaded_by,
                              lith_code=lith.lith_code,
                              from_m=lith.from_m, to_m=lith.to_m,
                              logged_by=lith.logged_by)
             for lith in liths])

    def _lith_code_available(self, lith_code: str):
        try:
            val = self._db_session.execute(f"SELECT COUNT(code) FROM ref.lithology WHERE code='{lith_code}'").first()
            return val[0] != 0
        except psycopg2.errors.UndefinedTable:
            raise ImportData.InvalidSchema('ref.lithology')

    def import_lithology_codes_array(self, lith_codes: [LithCode]):
        """
        Import lithology codes into xplordb.

        :param lith_codes: Lithology code array
        """
        self._db_session.add_all(
            [XplordbLithCodeTable(code=lith_code.code, description=lith_code.description, loaded_by=lith_code.loaded_by)
             for lith_code in lith_codes])
