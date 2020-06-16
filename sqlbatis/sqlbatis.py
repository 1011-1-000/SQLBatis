from sqlalchemy import *
from werkzeug.local import Local, LocalStack
from functools import wraps

from ._internals import _parse_signature
from .errors import ConnectionException, QueryException
from .connection import Connection, connections
from .container import SQLBatisMetaClass


class SQLBatis(metaclass=SQLBatisMetaClass):
    """The basic object to do the query with raw sql
    """

    def __init__(self, database_url, **kwargs):
        """Initialize the sqlbatis class

        :param database_url: The database url, which need to interact
        :type database_url: str
        """
        self.database_url = database_url
        self.engine = create_engine(database_url, **kwargs)
        self.open = True

        # will reflect the tables from the local database
        self.metadata = MetaData(self.engine, reflect=True)

    def close(self):
        """Close the sqlbatis, which also mean close the engine of the sqlalchemy
        """
        if self.open:
            self.engine.dispose()
            self.open = False

    def get_connection(self):
        """The function to get the connection, all the connections are in the localstack object

        :raises ConnectionException: if the engine is closed, the connection will be created
        :return: return a connection for query
        :rtype: Connection
        """
        if connections.top:
            return connections.top
        else:
            if not self.open:
                raise ConnectionException('Database connection closed')
            conn = self.engine.connect()
            connections.push(Connection(conn))
            return connections.top

    def query(self, sql, fetch_all=False):
        """The decorator that using for the raw sql query, the simple example for usage is like:

        @db.query("SELECT * FROM user")
        def get_users():
            pass

        then if we try to call the function get_users, the sqlbatis will execute the query
        automatically.

        :param sql: the sql that you want to execute
        :type sql: str
        :param fetch_all: will retrieve all the results instead of lazy loading the data from db, defaults to False
        :type fetch_all: bool, optional
        """
        def db_query(func):
            @wraps(func)
            def wrapper(*args, **kwargs):

                # assemble the arguments
                parameters = _parse_signature(func, *args, **kwargs)
                with self.get_connection() as conn:
                    try:
                        results = conn.query(sql, fetch_all, **parameters)
                        return results
                    except Exception:
                        raise QueryException('Error querying database')

            return wrapper

        return db_query

    def bulk_query(self, sql):
        """Bulk update or insert with this decorator, it has the similar usage like the query
        it also have the requirements for the inner function, which means the paramters should be
        the list of the object that we want to do update or insert

        :param sql: the raw sql that you want to execute
        :type sql: str
        """
        def db_query(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                with self.get_connection() as conn:
                    try:
                        results = conn.bulk_query(sql, *args)
                        return results
                    except Exception:
                        raise Exception('Error querying database')

            return wrapper

        return db_query

    def transactional(self):
        pass

    def __enter__(self):
        return self

    def __exit__(self, exc, val, traceback):
        self.close()

    def __repr__(self):
        return '<Database open={}>'.format(self.open)
