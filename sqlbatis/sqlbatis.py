from sqlalchemy import *
from functools import wraps

from ._internals import _parse_signature, _parse_signature_for_bulk_query
from .errors import ConnectionException, QueryException, TransactionException
from .connection import Connection
from .container import SQLBatisMetaClass, entity, SQLBatisContainer
from .page_query_builder import PageQueryBuilder


@entity
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
        self.metadata = MetaData(self.engine)
        self.metadata.reflect()

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
        local = SQLBatisContainer.__local__

        if hasattr(local, 'connection'):
            return local.connection
        else:
            if not self.open:
                raise ConnectionException('Database connection closed')
            conn = self.engine.connect()
            local.connection = Connection(conn)
            return local.connection

    def query(self, sql, fetch_all=False):
        """The decorator that using for the raw sql query, the simple example for usage is like::

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
                try:
                    parameters = _parse_signature(func, *args, **kwargs)
                    with self.get_connection() as conn:
                        results = conn.query(sql, fetch_all, **parameters)
                        return results
                except Exception as e:
                    raise QueryException(
                        'Query Exception in func [{}]'.format(func.__name__)) from e

            return wrapper

        return db_query

    def bulk_query(self, sql):
        """Bulk update or insert with this decorator, it has the similar usage like the query
        it also have the requirements for the inner function, which means the paramters should be
        the list of the object that we want to do update or insert

        :param sql: the raw sql that you want to execute
        :type sql: str
        """
        def db_bulk_query(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                try:
                    parameters = _parse_signature_for_bulk_query(
                        func, *args, **kwargs)
                    with self.get_connection() as conn:
                        results = conn.bulk_query(sql, *parameters)
                        return results
                except Exception as e:
                    raise QueryException(
                        'Query Exception in func [{}]'.format(func.__name__)) from e

            return wrapper

        return db_bulk_query

    def query_by_page(self, sql, page=1, page_size=10, fetch_all=True):
        """Get the rows by page number and page size

        :param sql: The raw SQL that you want to execute
        :type sql: str
        :param page: page number, defaults to 1
        :type page: int, optional
        :param page_size: number of rows per page, defaults to 10
        :type page_size: int, optional
        :param fetch_all: ignore lazy loading or not, defaults to True
        :type fetch_all: bool, optional
        """
        def db_query_by_page(func):
            @wraps(func)
            def wrapper(*args, **kwargs):

                # assemble the arguments
                try:
                    parameters = _parse_signature(func, *args, **kwargs)
                    page_query_builder = PageQueryBuilder(
                        sql, parameters, page, page_size, fetch_all)
                    results = page_query_builder.query()
                    return results
                except Exception as e:
                    raise QueryException(
                        'Query Exception in func [{}]'.format(func.__name__)) from e

            return wrapper

        return db_query_by_page

    def transactional(self):
        """The decorator that for do the transaction, the useage of this is::

            @db.transactional()
            def transaction_needed_func():
                do(1)
                do(2)

        any error occurred, the changes will be rolled back.

        also include the nested transaction, consider the scenario like this::

            @db.transactional():
            def transaction_func_1():
                do(1)
                transaction_func_2()

            @db.transactional()
            def transaction_func_2():
                do(2) 

        if the transaction_func_2 is failed, the result of the do(1) also will rolled back
        """

        def _transactional(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                with self.get_connection().begin() as t:
                    try:
                        results = func(*args, **kwargs)
                        return results
                    except Exception as e:
                        t.rollback()
                        raise QueryException(
                            'Query Exception in func [{}]'.format(func.__name__)) from e
            return wrapper
        return _transactional

    def __enter__(self):
        return self

    def __exit__(self, exc, val, traceback):
        self.close()

    def __repr__(self):
        return '<Database open={}>'.format(self.open)
