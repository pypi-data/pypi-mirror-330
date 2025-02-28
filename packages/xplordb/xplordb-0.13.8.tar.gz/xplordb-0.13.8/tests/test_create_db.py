import pytest
from psycopg2 import connect


@pytest.fixture()
def new_db():
    return 'test_xplordb'


def test_lite_database_creation(db_creator, new_db, host, port, user, password):
    """
    Test lite database creation

    :param db_creator: fixture to create a database and then remove it from server
    """
    db_creator.create_db(new_db, False, False)
    expected_schema_list = ['assay', 'dh', 'display', 'information_schema', 'pg_catalog', 'pg_toast', 'public', 'ref']
    check_schema_list(expected_schema_list, host, new_db, password, port, user)


def test_full_database_creation(db_creator, new_db, host, port, user, password):
    """
    Test full database creation

    :param db_creator: fixture to create a database and then remove it from server
    """
    db_creator.create_db(new_db, False, True)
    expected_schema_list = ['assay', 'dem', 'dh', 'display','information_schema', 'pg_catalog', 'pg_toast',
                            'public', 'qa', 'ref', 'surf', 'v']
    check_schema_list(expected_schema_list, host, new_db, password, port, user)


def check_schema_list(expected_schema_list, host, new_db, password, port, user):
    with connect(database=new_db,  host=host,  port=port,  user=user, password=password) as session:
        with session.cursor() as cur:
            cur.execute("SELECT nspname FROM pg_catalog.pg_namespace ORDER BY nspname")
            schema_list = [res[0] for res in cur.fetchall()]
    assert expected_schema_list == schema_list
