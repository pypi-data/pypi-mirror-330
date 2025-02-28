"""
Configuration for pytest call

Configuration for pytest call, define database connection

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

import pytest
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from sqlalchemy.orm import Session

from xplordb.create_db import CreateDatabase
from xplordb.import_data import ImportData
from xplordb.import_ddl import ImportDDL
from xplordb.sql_utils import connect
from xplordb.sqlalchemy.base import create_session


def pytest_addoption(parser):
    parser.addoption("--host", action="store",
                     default='localhost')
    parser.addoption("--user", action="store",
                     default='postgres')
    parser.addoption("--password", action="store")
    parser.addoption("--port", action="store", default=5432)
    parser.addoption("--db", action="store")


@pytest.fixture(scope="module")
def host(request):
    return request.config.getoption("--host")


@pytest.fixture(scope="module")
def user(request):
    return request.config.getoption("--user")


@pytest.fixture(scope="module")
def password(request):
    return request.config.getoption("--password")


@pytest.fixture(scope="module")
def db(request):
    return request.config.getoption("--db")


@pytest.fixture(scope="module")
def port(request):
    return request.config.getoption("--port")


@pytest.fixture()
def db_session(host: str, port: int, db: str, user: str, password: str):
    """
    Create a pyscog2 connection with specified parameters
    parameters are defined from pytest call option.

    For example pytest --host localhost --port 5432 --db xplordb_test --user postgres --password postgres

    (default  values are defined in conftest.py)

    :param host: host used for connection
    :param port: port used for connection
    :param db: database name used for connection
    :param user:user used for connection
    :param password:password used for connection
    """
    session = connect(
        database=db,
        host=host,
        port=port,
        user=user,
        password=password)
    yield session
    session.close()


@pytest.fixture()
def sqlalchemy_session(host: str, port: int, db: str, user: str, password: str):
    """
    Create a sql alchemy session with specified parameters
    parameters are defined from pytest call option.

    For example pytest --host localhost --port 5432 --db xplordb_test --user postgres --password postgres

    (default  values are defined in conftest.py)

    :param host: host used for connection
    :param port: port used for connection
    :param db: database name used for connection
    :param user:user used for connection
    :param password:password used for connection
    """
    session = create_session(host, port, db, user, password)

    yield session
    session.close()


@pytest.fixture()
def litedb_no_data(host, user, password, db, port):
    """
    pytest fixture to create a xplordb database with lite schema without sample data
    """
    _import_db(host, user, password, db, port, False, False)


@pytest.fixture()
def litedb_with_data(host, user, password, db, port):
    """
    pytest fixture to create a xplordb database with lite schema and sample data
    """
    _import_db(host, user, password, db, port, True, False)


@pytest.fixture()
def fulldb_with_data(host, user, password, db, port):
    """
    pytest fixture to create a xplordb database with full schema with sample data
    """
    _import_db(host, user, password, db, port, True, True)


@pytest.fixture()
def fulldb_no_data(host, user, password, db, port):
    """
    pytest fixture to create a xplordb database with full schema without sample data
    """
    _import_db(host, user, password, db, port, False, True)


def _import_db(host: str, user: str, password: str, db: str, port: int,
               import_data: bool, full_db: bool):
    import_ddl_ = ImportDDL(host=host, user=user, password=password, db=db, port=port)
    import_ddl_.import_xplordb_schema(import_data=import_data, full_db=full_db)


@pytest.fixture()
def data_importer(sqlalchemy_session):
    importer = ImportData(sqlalchemy_session)
    yield importer


@pytest.fixture()
def db_creator(host, user, password, new_db, port):
    db_creator = CreateDatabase(host=host, user=user, password=password, connection_db='postgres', port=port)
    yield db_creator

    # Delete created database
    session = connect(host=host, port=port, user=user, password=password)
    session.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    cur = session.cursor()
    cur.execute(f"""SELECT pg_terminate_backend(pg_stat_activity.pid)
                    FROM pg_stat_activity
                    WHERE pg_stat_activity.datname = '{new_db}' 
                    AND pid <> pg_backend_pid();
                    """)
    session.commit()
    cur.execute(f'DROP DATABASE {new_db}')
    session.commit()
    session.close()
