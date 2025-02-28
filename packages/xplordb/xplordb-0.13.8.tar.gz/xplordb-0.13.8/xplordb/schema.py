"""
Python class describing an xplordb schema

xplordb schema must be created in specific order, this class define available schema
and specific schema and table import order

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

from xplordb import __version__
from xplordb.sql_utils import import_sql_in_directory, import_all_sql_in_directory, \
    exec_conn_psql, psql_sql_in_directory, psql_all_sql_in_directory


class Schema:
    IMPORT_ROOT = Path(os.path.dirname(os.path.abspath(__file__)))

    def __init__(self, name: str,
                 fk_tables: List[str] = None, function_after_table_import: List[str] = None,
                 extra_files: List[str] = None, fk_views: List[str] = None, full_db: bool = True, postcreation_queries: List[str] = []):
        """
        A class used to define a xplordb schema
        :param name: schema name
        :param fk_tables: list of table .sql files that are used as foreign keys (optional, default None)
        :param function_after_table_import: list of function .sql that must be imported after table import
                                            (optional, default None)
        :param extra_files: list of .sql file that can be removed from full database (optional, default None)
        :param fk_views: list of view .sql that are used in other view (optional, default None)
        :param full_db: boolean to define if full database DDL must be imported (optional, default False)
        :postcreation_queries: list[str] queries to be executed after schema creation (default empty list)
        """
        self.name = name
        if function_after_table_import is None:
            function_after_table_import = []
        if fk_tables is None:
            fk_tables = []
        if extra_files is None:
            extra_files = []
        if fk_views is None:
            fk_views = []
        self.fk_tables = fk_tables
        self.function_after_table_import = function_after_table_import
        self.extra_files = extra_files
        self.fk_views = fk_views
        self.full_db = full_db
        self.postcreation_queries = postcreation_queries

    @staticmethod
    def db_schema_list(full_db: bool = False):
        """
        Get xplordb schema list.
        :param full_db: boolean to define schemas for full database DDL must be created (optional, default False)
        :return: list of xplordb schema
        """
        ref = Schema('ref',
                     fk_tables=['company.sql', 'person.sql', 'data_sets.sql', 'data_source.sql', 'lab.sql',
                                'lab_o_method.sql', 'xplordb.sql'],
                     extra_files=['assay_result_code.sql', 'dh_survey_instrument.sql', 'elements.sql',
                                  'event.sql', 'event_code.sql', 'geomatic_declination.sql',
                                  'geomagnetic_declination.sql', 'lease.sql', 'minerals.sql',
                                  'oxidation.sql', 'preferred.sql', 'qgis_project.sql',
                                  'rl_method.sql', 'sample_class.sql', 'sample_method.sql', 'sample_type.sql',
                                  'sg_method.sql', 'strat_name.sql', 'struc.sql',
                                  'xrf_instrument.sql',
                                  'lab.sql', 'lab_method.sql', 'lab_method_code.sql', 'lab_o_method.sql',
                                  'lab_method_trigger.sql'],
                     full_db=full_db,
                     postcreation_queries=[f"INSERT INTO ref.xplordb VALUES('{__version__}')"])
        dh = Schema('dh',
                    fk_tables=['collar.sql', 'surv.sql', 'details.sql', 'metadata.sql'],
                    function_after_table_import=["get_planar_srid.sql", "dh_trace.sql", "dh_planned_trace.sql"],
                    extra_files=['alteration.sql', 'core_recovery.sql', 'event.sql', 'minerals.sql',
                                 'oxidation.sql', 'petrology.sql', 'sample.sql', 'sample_image.sql',
                                 'sample_quality.sql', 'sample_weight.sql', 'sg.sql', 'struc.sql', 'vein.sql',
                                 'oxidation_trigger.sql', 'sample_quality_trigger.sql',
                                 'sample_trigger.sql'],
                    full_db=full_db)

        assay = Schema('assay',
                       fk_tables=['batch.sql'],
                       extra_files=['assay.sql',  'batch.sql', 'raw.sql', 'intercepts.sql', 'flat_method.sql',
                                    'import.sql', 'flat_ppm.sql', 'structural_types.sql'],
                       fk_views=['assay.sql'],
                       function_after_table_import=['flat_method.sql', 'import.sql', 'flat_ppm.sql', "structural_types.sql"],
                       full_db=full_db)
        
        display = Schema('display',
                         fk_tables=['display_collar.sql'],
                         full_db=full_db)

        schemas = [ref, dh, assay, display]

        if full_db:
            qa = Schema('qa',
                        fk_tables=['qc_type.sql', 'sd_values.sql'])
            surf = Schema('surf')
            v = Schema('v')
            dem = Schema('dem',
                         function_after_table_import=['cap_alos_example.sql', 'alos_cap_update_example.sql'],
                         full_db=full_db)

            schemas += [qa, surf, v, dem]

        return schemas
    
    def execute_postcreation_queries(self, conn):
        """
        Execute all queries contained in self.postcreation_queries.  
        """
        with conn.cursor() as cur:
            for query in self.postcreation_queries:
                cur.execute(query)
        conn.commit()

    def create_privileges(self, conn):
        role_path = self.import_dir() / 'roles'
        self._import_sql_in_directory(conn, role_path, ["grants.sql"])

    def create_schema(self, conn):
        print(f'importing schema: {self.name}')
        exec_conn_psql(conn, self.import_dir() / f'{self.name}.sql')

    def get_mustache_params(self) -> {}:
        params = {}
        if not self.full_db:
            params = {'geom_trace_tables': 'details'}
        return params

    def import_pre_table_functions(self, conn):
        function_list = [x for x in self.function_list()
                         if x not in self.function_after_table_import and x not in self.get_excluded_files()]
        self._import_sql_in_directory(conn, self.function_path(), function_list)

    def import_tables(self, conn):
        table_path = self.import_dir() / 'table'
        fk_tables = [x for x in self.fk_tables
                     if x not in self.get_excluded_files()]
        self._import_sql_in_directory(conn, table_path, fk_tables)
        all_exclusion = self.get_excluded_files() + fk_tables
        self._import_all_sql_in_directory(conn, table_path, all_exclusion)

    def import_post_table_functions(self, conn):
        self._import_sql_in_directory(conn, self.function_path(), self.function_after_table_import)

    def import_sequences(self, conn):
        self._import_all_sql_in_directory(conn, self.import_dir() / 'sequences')

    def import_views(self, conn):
        views_path = self.import_dir() / 'views'
        fk_views = [x for x in self.fk_views
                    if x not in self.get_excluded_files()]
        self._import_sql_in_directory(conn, views_path, fk_views)
        all_exclusion = self.get_excluded_files() + fk_views
        self._import_all_sql_in_directory(conn, views_path, all_exclusion)

    def import_fk_creation(self, conn):
        self._import_all_sql_in_directory(conn, self.import_dir() / 'fk_creation')

    def import_trigger(self, conn):
        excluded_files = self.get_excluded_files()
        self._import_all_sql_in_directory(conn, self.import_dir() / 'trigger', excluded_files)

    def import_tables_data(self, conn):
        table_path = self.import_dir() / 'populate'
        fk_tables = [x for x in self.fk_tables
                     if x not in self.get_excluded_files()]
        psql_sql_in_directory(conn, table_path, fk_tables)
        all_exclusion = self.get_excluded_files() + fk_tables
        psql_all_sql_in_directory(conn, table_path, all_exclusion)

    def get_excluded_files(self):
        excluded_files = []
        if not self.full_db:
            excluded_files = self.extra_files
        return excluded_files

    def import_dir(self):
        return self.IMPORT_ROOT / 'schema' / self.name

    def function_path(self):
        return self.import_dir() / 'functions'

    def function_list(self):
        functions_list = []
        functions_path = self.function_path()
        if functions_path.exists():
            functions_list = os.listdir(functions_path)
        return functions_list

    def _import_all_sql_in_directory(self, conn, directory: Path, excluded_files: List[str] = None):
        import_all_sql_in_directory(conn, directory, excluded_files, self.get_mustache_params())

    def _import_sql_in_directory(self, conn, directory: Path, files: List[str]):
        import_sql_in_directory(conn, directory, files, self.get_mustache_params())
