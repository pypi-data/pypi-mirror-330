"""
Module use to import xplordb DDL in an existing database

Module use to import xplordb DDL in an existing database.
Options are available to import full database and example data

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

import os
from pathlib import Path
from typing import List

from xplordb.schema import Schema
from xplordb.sql_utils import connect


class ImportDDL:
    IMPORT_ROOT = Path(os.path.dirname(os.path.abspath(__file__)))

    def __init__(self, db: str, user: str, password: str, host: str = 'localhost', port: int = 5432):
        """
        A class used to import xplordb DDL to an existing database

        Example:
            import_ddl = ImportDDL(db='xplordb', user='postgres', password='postgres')
            import_ddl.import_xplordb_schema()

        :param db: database name where xplordb DDL will be imported
        :param user: user for database connection
        :param password: password for database connection
        :param host: host (optional, default 'localhost')
        :param port: port (optional, default 5432)
        """
        self._host = host
        self._port = port
        self._db = db
        self._user = user
        self._password = password

        self._conn = connect(
            database=db,
            host=host,
            port=port,
            user=user,
            password=password)

    def __del__(self):
        if self._conn:
            self._conn.close()

    @staticmethod
    def xplordb_roles():
        return ['xdb_viewer', 'xdb_logger', 'xdb_admin']

    def import_xplordb_schema(self, import_data: bool = False, full_db: bool = False):
        """
        Import xplordb DDL to database
        :param import_data: boolean to define if sample dataset must be imported (optional, default False)
        :param full_db: boolean to define if full database DDL must be imported (optional, default False)
        """
        self._create_extension()

        self._create_roles()

        # Define schema list depending on full_db option
        schemas = Schema.db_schema_list(full_db)

        # Drop and import all schemas
        for schema in schemas:
            self._drop_and_import_schema(schema)

        # Import data if asked
        if import_data:
            self._import_schemas_data(schemas)

        # Import specific foreign keys and trigger AFTER data import because of some foreign keys and trigger
        for schema in schemas:
            schema.import_fk_creation(self._conn)
            schema.import_trigger(self._conn)

    def _drop_and_import_schema(self, schema: Schema):
        self._drop_schema(schema.name)
        self._import_schema(schema)

    def _drop_schema(self, schema: str):
        with self._conn.cursor() as cur:
            print(f'deleting schema {schema}')
            cur.execute(f'DROP SCHEMA IF EXISTS {schema} CASCADE')
            cur.close()
        self._conn.commit()

    def _import_schema(self, schema: Schema):
        schema.create_schema(self._conn)
        # Function are used in table definition and must be imported before table
        schema.import_pre_table_functions(self._conn)
        schema.import_tables(self._conn)
        # Still there are some function that refers to a table so they must be imported after table
        schema.import_post_table_functions(self._conn)
        schema.import_sequences(self._conn)
        schema.import_views(self._conn)
        # grant permissions
        schema.create_privileges(self._conn)
        # execute dedicated queries
        schema.execute_postcreation_queries(self._conn)

    def _import_schemas_data(self, schemas: List[Schema]):
        for schema in schemas:
            schema.import_tables_data(self._conn)

    def _create_extension(self):
        extensions = ['btree_gist', 'postgis', 'postgis_raster', 'plpgsql']
        with self._conn.cursor() as cur:
            for extension in extensions:
                cur.execute(f"CREATE EXTENSION IF NOT EXISTS {extension}")

    def _create_roles(self):
        for role in self.xplordb_roles():
            self._create_role(role)

    def _create_role(self, role : str):
        if not self._role_exist(role):
            with self._conn.cursor() as cur:
                cur.execute(f"CREATE ROLE {role}")

    def _role_exist(self, role: str):
        exist = False
        with self._conn.cursor() as cur:
            cur.execute(f"SELECT * FROM pg_roles WHERE rolname='{role}'")
            if cur.fetchone():
                exist = True
        return exist
