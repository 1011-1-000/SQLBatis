from .errors import ContainerException
from werkzeug.local import Local

local = Local()


def entity(cls):
    SQLBatisContainer.register(cls.__name__, None)
    return cls


class SQLBatisContainer:
    """The container for the SQLBatis injection, it will hold the instance
    that class which inherit the SQLBatisMetaClass

    :raises ContainerException: will raise exception if no instance is registered
    """
    __local__ = {}

    @staticmethod
    def register(key, instance):
        """Register the instance to the container

        :param key: the key of the instance
        :type key: str
        :param instance: the instance of the cls
        :type instance: cls instance
        """
        SQLBatisContainer.__local__[key] = instance

    @staticmethod
    def get_instance(key):
        """Try to get the instance from the container

        :param key: the key of the instance
        :type key: str
        :raises ContainerException: if no instance is binded with the key, will raise the exception
        :return: the instance
        :rtype: cls instance
        """
        instance = SQLBatisContainer.__local__.get(key)
        if instance:
            return instance
        else:
            raise ContainerException(f'No {key} instance registered')

    @staticmethod
    def has_key(key):
        return key in SQLBatisContainer.__local__


class SQLBatisMetaClass(type):
    """The mataclass which will register the current instance to the container
    be careful: it will just host one instance in the container, the original instance
    will be replaced if a class instance is generated
    """
    def __call__(cls, *args, **kwargs):
        """Register the class instance to the container automatically,and 
        autowired the attributes too.

        :return: cls instance
        :rtype: cls
        """
        obj = cls.__new__(cls, *args, **kwargs)
        if hasattr(obj, '__autowired__'):
            autowired_attrs = getattr(obj, '__autowired__')
            for attr in autowired_attrs:
                setattr(obj, attr, SQLBatisContainer.get_instance(attr))
        obj.__init__(*args, **kwargs)
        key = obj.__class__.__name__
        if key in SQLBatisContainer.__local__:
            SQLBatisContainer.register(key, obj)
        return obj
