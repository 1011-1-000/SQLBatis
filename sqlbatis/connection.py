from sqlalchemy import text
from .row import Row, RowSet, SQLAlchemyResultProxy
from .container import SQLBatisContainer


class Connection:
    """The wrapper of the sqlalchemy raw connection
    """

    def __init__(self, conn):
        self.conn = conn
        self.transaction = None

    def close(self):
        """Close the connection
        """
        local = SQLBatisContainer.__local__
        self.conn.close()
        del local.connection

    @property
    def closed(self):
        """Check the connection status

        :return: the boolean which indicate the connection status
        :rtype: boolean
        """
        return self.conn.closed

    def in_transaction(self):
        """Check if the connection is in transaction

        :return: the status of the connection transaction
        :rtype: boolean
        """
        return self.conn.in_transaction()

    def query(self, sql, fetch_all, **params):
        """The basic query based on the sqlalchemy, it will accept the raw sql, and execute will raw
        sqlalchemy connection

        :param sql: the raw sql that will be executed
        :type sql: str
        :param fetch_all: determine if consume all the iterator immediately instead of lazy loading
        :type fetch_all: bool
        :return: the row or rowset of the sql result
        :rtype: Row or RowSet
        """
        result_proxy = self.conn.execute(text(sql), **params)
        return self._result_proxy_to_rowset(result_proxy, fetch_all)

    def bulk_query(self, sql, *params):
        """Bulk update or insert 

        :param sql: the raw sql that will be executed
        :type sql: str
        :return: the row or rowset of the sql result
        :rtype: Row or RowSet
        """
        result_proxy = self.conn.execute(text(sql), *params)
        return self._result_proxy_to_rowset(result_proxy, False)

    def execute(self, sql, fetch_all=False, inserted_primary_key=False, **params):
        """The raw execute function of the sqlalchemy, and main difference between this func
        with the query is it can accept the sqlalchemy sql expression as the first parameter


        :param sql: the sqlalchemy sql expression need to be executed
        :type sql: sqlalchemy sql expression
        :param fetch_all: determine if consume all the iterator immediately instead of lazy loading, defaults to False
        :type fetch_all: bool, optional
        :param inserted_primary_key: if return the primary key when do the create func, defaults to False
        :type inserted_primary_key: bool, optional
        :return: the result of the query 
        :rtype: Row or RowSet or int(if inserted_primary_key)
        """
        result_proxy = self.conn.execute(sql, **params)
        if inserted_primary_key:
            return result_proxy.inserted_primary_key[0]
        return self._result_proxy_to_rowset(result_proxy, fetch_all)

    def begin(self):
        """Start a transaction

        :return: a transaction
        :rtype: TBI
        """
        self.transaction = self.conn.begin()
        return self.transaction

    def begin_nested(self):
        return self.conn.begin_nested()

    def _result_proxy_to_rowset(self, result_proxy, fetch_all):
        """Convert the ResultProxy object of the query result RowSet which defined in the
        SQLBatis

        :param result_proxy: the query result of the sqlalchemy
        :type result_proxy: ResultProxy
        :param fetch_all: consumen all the iterator
        :type fetch_all: bool
        :return: the rowset of the sql result
        :rtype: RowSet
        """
        if result_proxy.returns_rows:
            keys = result_proxy.keys()
            rows = (Row(keys, values) for values in result_proxy)
            results = RowSet(rows, SQLAlchemyResultProxy(result_proxy))
            if fetch_all:
                results.all()
            return results
        else:
            return RowSet(iter([]), SQLAlchemyResultProxy(result_proxy))

    def __enter__(self):
        return self

    def __exit__(self, exc, val, traceback):
        # if the current connection is in transaction will not close immediately
        if not self.in_transaction():
            self.close()
