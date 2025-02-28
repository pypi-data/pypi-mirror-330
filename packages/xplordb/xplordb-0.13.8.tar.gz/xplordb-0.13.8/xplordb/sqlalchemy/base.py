from sqlalchemy import create_engine
from sqlalchemy.engine import URL
from sqlalchemy.orm import declarative_base, Session, sessionmaker

Base = declarative_base()


def create_session(host: str, port: int, database: str, user: str, password: str) -> Session:
    """
    Create a sql alchemy session with specified parameters

    :param host: host used for connection
    :param port: port used for connection
    :param database: database name used for connection
    :param user:user used for connection
    :param password:password used for connection
    """
    connection_url = URL.create(
        "postgresql+psycopg2",
        username=user,
        password=password,
        host=host,
        port=port,
        database=database
    )

    engine = create_engine(connection_url)

    xplordb_session = sessionmaker(bind=engine)
    session = xplordb_session()
    return session
