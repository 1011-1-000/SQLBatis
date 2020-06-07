from functools import wraps
from sqlbatis.sqlbatis import sqlbatis_local


class Propagation:

    REQUIRED = 1
    REQUIRED_NEW = 2
    SUPPORTED = 3
    NOT_SUPPORTED = 4
    NEVER = 5
    MANDATORY = 6
    NESTED = 7


class TransactionManager:

    def __init__(self, db):
        self.db = db

    def transactional(self, propagation=Propagation.REQUIRED):

        def _transaction(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                try:
                    if not hasattr(sqlbatis_local, 'connection'):
                        sqlbatis_local.connection = self.db.get_connection()

                    with sqlbatis_local.connection.begin():
                        results = func(*args, **kwargs)
                        return results
                finally:
                    if hasattr(sqlbatis_local, 'connection'):
                        sqlbatis_local.connection.close()
                    sqlbatis_local.__release_local__()
            return wrapper

        return _transaction
