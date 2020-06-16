from functools import wraps
from .errors import PropagationException
from sqlbatis.connection import Connection, connections


class Propagation:

    REQUIRED = 1
    REQUIRED_NEW = 2
    # SUPPORTED = 3
    # NOT_SUPPORTED = 4
    # NEVER = 5
    # MANDATORY = 6
    # NESTED = 7


class TransactionManager:

    def __init__(self, db):
        self.db = db

    def transactional(self, propagation=Propagation.REQUIRED):

        def _transaction(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                try:
                    with self.get_transaction(propagation):
                        results = func(*args, **kwargs)
                        return results

                finally:
                    self.cleanup_transaction(propagation)
            return wrapper

        return _transaction

    def get_transaction(self, propagation):
        connection = connections.top
        if not connection:
            connection = Connection(self.db.engine.connect())
            connections.push(connection)

        return connection.begin()

    def cleanup_transaction(self, propagation):
        connection = connections.top
        if connection.in_transaction():
            pass
        else:
            connection.close()
            connections.pop()
