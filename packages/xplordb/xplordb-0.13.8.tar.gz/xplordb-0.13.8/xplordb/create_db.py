from psycopg2 import connect
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

from xplordb.import_ddl import ImportDDL


class CreateDatabase:

    def __init__(self, connection_db: str, user: str, password: str, host: str = 'localhost',
                 port: int = 5432):
        """
        A class used to create xplordb database to an existing server

        Example:
            create_db = CreateDatabase(connection_db='postgres', user='postgres', password='postgres')
            create_db.create_db('xplordb', True, True)

        :param connection_db: database name for connection
        :param user: user for database connection
        :param password: password for database connection
        :param host: host (optional, default 'localhost')
        :param port: port (optional, default 5432)
        """
        self._host = host
        self._port = port
        self._user = user
        self._password = password

        self._conn = connect(
            database=connection_db,
            host=host,
            port=port,
            user=user,
            password=password)

    def __del__(self):
        if self._conn:
            self._conn.close()

    def create_db(self, db: str, import_data: bool = False, full_db: bool = False):
        """
        Create a new xplordb database

        :param db: new database name where xplordb DDL will be imported
        :param import_data: boolean to define if sample dataset must be imported (optional, default False)
        :param full_db: boolean to define if full database DDL must be imported (optional, default False)
        """
        # Create a table in PostgreSQL database
        self._conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cur = self._conn.cursor()
        cur.execute(f'CREATE DATABASE {db}')
        self._conn.commit()

        # Import DDL
        import_ddl = ImportDDL(db=db, user=self._user, password=self._password, host=self._host, port=self._port)
        import_ddl.import_xplordb_schema(import_data, full_db)
