from .errors import ContainerException
from werkzeug.local import Local
from ._internals import _parse_signature


class SQLBatisContainer:

    __local__ = {}

    @staticmethod
    def register(key, instance):
        SQLBatisContainer.__local__[key] = instance

    @staticmethod
    def get_instance(key):
        try:
            return SQLBatisContainer.__local__[key]
        except:
            raise ContainerException(f'No {key} instance registered')


sqlbatis_container = SQLBatisContainer()


class SQLBatisMetaClass(type):

    def __call__(cls, *args, **kwargs):
        obj = cls.__new__(cls, *args, **kwargs)
        obj.__init__(*args, **kwargs)
        sqlbatis_container.register(cls.__name__, obj)
        return obj
