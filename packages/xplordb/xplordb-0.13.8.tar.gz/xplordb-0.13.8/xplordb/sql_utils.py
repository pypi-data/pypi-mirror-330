"""
Utility functions for postgresql database use

Utility functions for postgresql database use :
- psycog2 connection
- sql file import with psql (for data import)
- sql file import with psycog2 (for database definition)

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
import subprocess
import chevron
from pathlib import Path
from typing import List

import psycopg2


class InvalidConnection(Exception):
    pass


def connect(**kwargs):
    """
    creates a connection to PostgreSQL and returns the instance
    """
    try:
        conn = psycopg2.connect(**kwargs)
    except psycopg2.Error as exc:
        raise InvalidConnection(exc)
    return conn


def exec_conn_psql(conn, filename: Path, mustache_params=None):
    """
    Execute psql code from a file with psycog2.
    File can contains mustache parameters such as {{params}}. They will be replace with mustache_params map contents
    :param conn: psycopg2 connection
    :param filename: Path to file
    :param mustache_params: (optional) map with mustache parameters
    """
    with conn.cursor() as cur:
        with open(filename, 'r') as f:
            cur.execute(chevron.render(f, mustache_params))
    conn.commit()


def import_all_sql_in_directory(conn, directory: Path, excluded_files: List[str] = None, mustache_params=None):
    """
    Execute psql code with psycog2 for all files inside a directory.
    File can contains mustache parameters such as {{params}}. They will be replace with mustache_params map contents
    :param conn: psycopg2 connection
    :param directory: directory parsed for files
    :param excluded_files: (optional) list of file that won't be imported
    :param mustache_params: (optional) map with mustache parameters
    """
    if directory.exists():
        for filename in os.listdir(directory):
            if not excluded_files or filename not in excluded_files:
                print(f'importing : {filename}')
                exec_conn_psql(conn, directory / filename, mustache_params)


def import_sql_in_directory(conn, directory: Path, files: List[str], mustache_params=None):
    """
    Execute psql code with psycog2 for specific files inside a directory.
    Warning : if file is not present in directory, an exception is raised
    File can contains mustache parameters such as {{params}}. They will be replace with mustache_params map contents
    :param conn: psycopg2 connection
    :param directory: directory parsed for files
    :param files: list of imported files
    :param mustache_params: (optional) map with mustache parameters
    """
    if files:
        for filename in files:
            print(f'importing : {filename}')
            exec_conn_psql(conn, directory / filename, mustache_params)


def exec_psql(conn, filename: Path):
    """
    Execute psql import with a file
    :param connn: psycopg2 connection used to get connection parameters
    :param filename: file to be imported
    """
    env = {'PGPASSWORD': conn.info.password}
    subprocess.run(['psql',
                    '-h', conn.info.host,
                    '-p', str(conn.info.port),
                    '-U', conn.info.user,
                    '--dbname', conn.info.dbname,
                    '-f', str(filename)],
                   env=env)


def psql_all_sql_in_directory(conn, directory: Path, excluded_files: List[str] = None):
    """
    Execute psql import for all files inside a directory.
    :param conn: psycopg2 connection used to get connection parameters
    :param directory: directory parsed for files
    :param excluded_files: (optional) list of file that won't be imported
    """
    if directory.exists():
        for filename in os.listdir(directory):
            if not excluded_files or filename not in excluded_files:
                print(f'importing : {filename}')
                exec_psql(conn, directory / filename)


def psql_sql_in_directory(conn, directory: Path, files: List[str]):
    """
    Execute psql import for specific files inside a directory.
    Warning : if file is not present in directory, a exception is raised
    :param conn: psycopg2 connection used to get connection parameters
    :param directory: directory parsed for files
    :param files: list of imported files
    """
    if files:
        for filename in files:
            exec_psql(conn, directory / filename)
