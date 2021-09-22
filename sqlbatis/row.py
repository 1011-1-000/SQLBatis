from collections import OrderedDict
from prettytable import PrettyTable


class SQLAlchemyResultProxy:

    def __init__(self, result_proxy):
        self._proxy = result_proxy

    @property
    def rowcount(self):
        return self._proxy.rowcount

    @property
    def inserted_primary_key(self):
        return self._proxy.inserted_primary_key


class Row:
    """Row objecct which constructed by the Result retrieved by sqlalchemy"""

    __slots__ = ('_columns', '_values')

    def __init__(self, columns, values):
        """Initialize the row with the sqlalchemy result

        :param columns: columns in the result
        :type columns: list
        :param values: values in the result
        :type values: list
        """

        # check the number of the columns equal with the number of values
        assert len(columns) == len(values)
        # To compatible the 1.4+ version sqlalchemy, convert RMKeyView to list
        if isinstance(columns, list):
            self._columns = columns
        else:
            self._columns = list(columns)
        self._values = values

    def columns(self):
        """Columns of result

        :return: all columns
        :rtype: list
        """
        return self._columns

    def values(self):
        """Values of result

        :return: values conrespond to the columns
        :rtype: list
        """
        return self._values

    def get(self, column, default=None):
        """Get the value by the column

        :param column: the column
        :type column: str
        :param default: default value if the column not exist, defaults to None
        :type default: any, optional
        :return: the value conresponding to column
        :rtype: any
        """
        try:
            return self[column]
        except KeyError:
            return default

    def to_dict(self, ordered=False):
        """Return the row as a dictionary, if ordered is True, return an ordereddict

        :param ordered: if need keep order or not, defaults to False
        :type ordered: bool, optional
        :return: the row dictionary
        :rtype: dict
        """
        items = zip(self.columns(), self.values())
        return OrderedDict(items) if ordered else dict(items)

    def __repr__(self):
        table = PrettyTable(self._columns)
        table.add_row(self._values)
        return str(table)

    def __getitem__(self, column):
        """Get the conresponding value of the column, becareful, in py3.5 the columns of the results 
        will random generate, it's not reliable to use the index to get the value,
        please use the column name to get the value if you not sure that is correct

        :param column: the column string or index
        :type column: str or int
        :raises IndexError: if the index out of the range
        :raises KeyError: column string is not contained in the row
        :return: value conresonding to the column
        :rtype: any
        """
        # get the value by the index
        if isinstance(column, int):
            if column < len(self._columns):
                return self._values[column]
            else:
                raise IndexError('Index out of the range')

        # get the value by the column.
        if column in self._columns:
            if self._columns.count(column) > 1:
                raise KeyError(
                    "Multiple columns '{}' in the row".format(column))

            index = self._columns.index(column)
            return self._values[index]

        raise KeyError("No '{}' field is contained".format(column))

    def __getattr__(self, column):
        try:
            return self[column]
        except KeyError as e:
            raise AttributeError(e)

    def __dir__(self):
        _super_dir = dir(super(Row, self))
        return sorted(_super_dir + [str(k) for k in self._columns])


class RowSet:
    """Rows collection"""

    def __init__(self, rows, result_proxy):
        self._rows = rows
        self._all_rows = []
        self.proxy = result_proxy
        self.pending = True

    def columns(self):
        try:
            row = self[0]
            return row.columns()
        except IndexError:
            raise 'No rows contained in the set.'

    @property
    def is_empty(self):
        """if the empty or not

        :return: check the empty or not
        :rtype: boolean 
        """
        return True if len(self._all_rows) == 0 else False

    def all(self, to_dict=False, to_ordered_dict=False):
        """Fetch all the rows that contained in the rowset, and consume the iterator."""

        rows = list(self)

        if to_dict:
            return [r.to_dict() for r in rows]
        elif to_ordered_dict:
            return [r.to_dict(ordered=True) for r in rows]

        return rows

    def to_dict(self, ordered=False):
        return self.all(to_dict=not (ordered), to_ordered_dict=ordered)

    def first(self, default=None, to_dict=False, to_ordered_dict=False):
        """Return the first row in the rowset, and will return the default value if the
        rowset is empty
        """
        try:
            row = self[0]
        except IndexError:
            return default

        if to_dict:
            return row.to_dict()
        elif to_ordered_dict:
            return row.to_dict(ordered=True)
        else:
            return row

    def one(self, default=None, to_dict=False, to_ordered_dict=False):
        """Returns a single row for the RowSet or default value, also we will check
        there is only one row contained in the RowSet"""
        self.all()
        assert len(self) == 1, 'Expects only one row contained'
        return self.first(default=default, to_dict=to_dict, to_ordered_dict=to_ordered_dict)

    def scalar(self, default=None):
        """Returns the first column of the first row, or `default`."""
        row = self.one()
        return row[0] if row else default

    def __repr__(self):
        """Generate the table format of the rowset
        """
        try:
            rows = self.all()
            table = PrettyTable(rows[0].columns())
            for row in self._all_rows:
                table.add_row(row.values())
            return str(table)
        except IndexError:
            return 'empty results'

    def __iter__(self):
        """Iterate over all rows in rowset"""
        i = 0
        while True:
            if i < len(self):
                yield self[i]
            else:
                try:
                    yield next(self)
                except StopIteration:
                    return
            i += 1

    def next(self):
        return self.__next__()

    def __next__(self):
        try:
            nextrow = next(self._rows)
            self._all_rows.append(nextrow)
            return nextrow
        except StopIteration:
            self.pending = False
            raise StopIteration('RowSet contains no more rows.')

    def __getattr__(self, column):
        """Get the column value as list

        :param column: the column name that you want to retrieve
        :type column: str
        :return: the values of the column in each row
        :rtype: list
        """
        rows = self.all()
        values = [r.get(column) for r in rows]
        return values

    def __getitem__(self, key):
        is_int = isinstance(key, int)

        if is_int:
            key = slice(key, key + 1)

        # iterate to the key
        while len(self) < key.stop or key.stop is None:
            try:
                next(self)
            except StopIteration:
                break

        rows = self._all_rows[key]
        if is_int:
            return rows[0]
        else:
            return RowSet(iter(rows))

    def __len__(self):
        return len(self._all_rows)
