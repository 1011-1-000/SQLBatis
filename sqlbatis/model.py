from .sqlbatis import Table
from .utils import camel_to_snake_case


class Model:
    """Basic Model in the SQLBatis, all the defined model should inherit this class,
    it will automaticlly interact with SQLAlchemy Core functions:
    """

    @classmethod
    def _get_columns(cls):
        """Retrieve all the columns that defined in the model class,
        which according to the rule that not start with the '_'

        :return: A group that contain all the columns defined in the class
        :rtype: list[SQLAlchemy Column]
        """
        columns = []
        for attr in cls.__dict__.keys():
            if not attr.startswith('_'):
                column = getattr(cls, attr)

                # add name to the Column object
                column.name = attr
                columns.append(column)
        return columns

    @classmethod
    def _create_table_instance(cls, metadata):
        """Create a table object in SQLAlchemy style, and add it to the metadata.
        Also, it will generate a table name if not a __tablename__ provided
        """
        if not getattr(cls, '__tablename__', None):
            cls.__tablename__ = camel_to_snake_case(cls.__name__)
        columns = cls._get_columns()
        table = metadata.tables.get(cls.__tablename__, None)
        if table is not None:
            metadata.remove(table)
        Table(cls.__tablename__, metadata, *columns)
