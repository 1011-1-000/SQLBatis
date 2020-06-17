class SQLBatisException(Exception):
    pass


class ConnectionException(SQLBatisException):
    pass


class QueryException(SQLBatisException):
    pass


class TableMissingException(SQLBatisException):
    pass


class PrimaryKeyMissingException(SQLBatisException):
    pass


class PropagationException(SQLBatisException):
    pass


class ContainerException(SQLBatisException):
    pass
