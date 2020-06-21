from .errors import ContainerException
from werkzeug.local import Local


def entity(cls):
    """Hand over the instance management to the container

    :return: cls object
    :rtype: SQLBatisMetaClass class
    """
    SQLBatisContainer.register(cls.__name__, None)
    return cls


class SQLBatisMetaClass(type):
    """The mataclass which will register the current instance to the container

    **be careful**: it will just host one instance in the container, the original instance
    will be replaced if a class instance is generated
    """
    def __call__(cls, *args, **kwargs):
        """Register the class instance to the container automatically,and 
        autowired the attributes too.

        :return: cls instance
        :rtype: cls
        """
        obj = cls.__new__(cls, *args, **kwargs)

        # autowired the attributes
        if hasattr(obj, '__autowired__'):
            autowired_attrs = getattr(obj, '__autowired__')
            for attr in autowired_attrs:
                setattr(obj, attr, SQLBatisContainer.get(attr))

        obj.__init__(*args, **kwargs)

        key = obj.__class__.__name__

        # register the instance to the container, if we handover the instance management to the container
        if SQLBatisContainer.has_key(key):
            SQLBatisContainer.register(key, obj)
        return obj


class SQLBatisContainer:
    """The container for the SQLBatis injection, it will hold the instance
    that class which inherit the SQLBatisMetaClass

    :raises ContainerException: will raise exception if no instance is registered
    """
    __local__ = Local()

    @staticmethod
    def register(key, instance):
        """Register the instance to the container

        :param key: the key of the instance
        :type key: str
        :param instance: the instance of the cls
        :type instance: cls instance
        """
        setattr(SQLBatisContainer.__local__, key, instance)

    @staticmethod
    def get(key):
        """Try to get the instance from the container

        :param key: the key of the instance
        :type key: str
        :raises ContainerException: if no instance is binded with the key, will raise the exception
        :return: the instance
        :rtype: cls instance
        """
        try:
            instance = getattr(SQLBatisContainer.__local__, key)
            if not instance:
                raise ContainerException(
                    'There is no object bounded with the key {}'.format(key))
            return instance
        except Exception:
            raise ContainerException('No {} instance registered'.format(key))

    @staticmethod
    def has_key(key):
        """Check if the instance exist in the container

        :param key: the instance key
        :type key: str
        :return: True if the instance exists else False
        :rtype: bool
        """
        return hasattr(SQLBatisContainer.__local__, key)
