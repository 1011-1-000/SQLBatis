from sqlalchemy.sql import *
from .utils import camel_to_snake_case
from .errors import TableMissingException, PrimaryKeyMissingException
from .container import SQLBatisMetaClass


class SQLBatisDao(metaclass=SQLBatisMetaClass):
    """Basic Dao operations provided by the SQLBatis
    """
    __autowired__ = ('SQLBatis',)

    def __init__(self):
        """Initialization of the Dao
        """
        self.table = self._get_table_in_metadata()

    def _get_table_in_metadata(self):
        """Get the metadata of current dao object

        :raises TableMissingException: will raise the error if the table doesn't exist in the db
        :return: table metadata
        :rtype: Table
        """
        tables = self.SQLBatis.metadata.tables  # or self.db.reflect_tables()
        table_name = self._get_table_name()
        if table_name not in tables:
            raise TableMissingException(
                'No {} in the db'.format(table_name))
        return tables.get(table_name)

    def create(self, attrs):
        """Insert a row of the object to the DB

        :param attrs: the value of the columns
        :type attrs: dict
        :return: the primary key of the inserted record
        :rtype: int
        """
        with self.SQLBatis.get_connection() as conn:
            result = conn.execute(self.table.insert().values(attrs),
                                  inserted_primary_key=True)
            return result

    def retrieve_by_id(self, _id):
        """Get the row by the id

        :param _id: primary key of the row that you want to retrieve
        :type _id: int
        :return: the row which id is _id
        :rtype: Row
        """
        with self.SQLBatis.get_connection() as conn:
            result = conn.execute(self.table.select().where(
                self.table.c.id == _id)).first()
            return result

    def retrieve_all(self):
        """Get all the rows from the database

        :return: all the rows in the database
        :rtype: RowSet
        """
        with self.SQLBatis.get_connection() as conn:
            result = conn.execute(self.table.select())
            return result

    def filter_by(self, where_condition):
        """Get the rows which match the given conditions, if where_condition is empty, will retrieve all rows
        in the table

        :param where_condition: conditions that we need to filter from the table
        :type where_condition: dict
        :return: rows which filtered by the conditions
        :rtype: RowSet
        """
        query = self.table.select()
        for key, value in where_condition.items():
            query = query.where(getattr(self.table.c, key) == value)

        with self.SQLBatis.get_connection() as conn:
            result = conn.execute(query)
            return result

    def delete_by_id(self, _id):
        """Delete the row by the primary key

        :param _id: row primary key
        :type _id: int
        :return: TBI
        :rtype: TBI
        """
        with self.SQLBatis.get_connection() as conn:
            result = conn.execute(
                self.table.delete().where(self.table.c.id == _id))
            return result

    def update_by_id(self, _id, attrs):
        """Update the row in the database by the id and attrs

        :param attrs: the attributes of row and contained the primary key of the row
        :type attrs: dict
        :return: TBI
        :rtype: TBI
        """
        with self.SQLBatis.get_connection() as conn:
            result = conn.execute(
                self.table.update().where(self.table.c.id == _id).values(attrs))
            return result

    def bulk_insert(self, attrs):
        """Bulk insert and update

        :param attrs: the list of the attributes dict
        :type attrs: list[dict]
        :return: TBI
        :rtype: TBI
        """
        with self.SQLBatis.get_connection() as conn:
            result = conn.execute(self.table.insert().values(attrs))
            return result

    def _get_table_name(self):
        """
        Get the table name according to the class name which should be written with CamelCase style.

        if the __tablename__ is specified, will use it as the table name else translate class name
        to table_name
        """
        try:
            table_name = self.__tablename__
        except AttributeError:
            table_name = camel_to_snake_case(
                self.__class__.__name__, ['', 'Dao'])
        except Exception:
            raise Exception('Failed to get the table_name')
        return table_name
