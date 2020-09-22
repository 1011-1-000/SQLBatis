import math
from .container import SQLBatisMetaClass


class PageResults:
    """The class that contain results of the each page

    :attr:`page`: current page number

    :attr:`page_size`: number of the object per page

    :attr:`total`: total number of query objects

    :attr:`results`: the result by page, it is a RowSet object
    """

    def __init__(self, page, page_size, total, results):
        # check if the limit and offset are numbers
        try:
            self.page = int(page)
            self.page_size = int(page_size)
        except TypeError:
            raise TypeError

        self.total = total
        self.results = results

    @property
    def has_next(self):
        """Check if has next page or not

        :return: if has next page or not
        :rtype: bool
        """
        return True if self.total > self.page * self.page_size else False

    @property
    def has_prev(self):
        """Check if has previous page or not

        :return: if has previous page or not
        :rtype: bool
        """
        return True if self.page > 1 else False


class PageQueryBuilder(metaclass=SQLBatisMetaClass):
    """Construct a pagination query according to the params that user passed in
    """
    __autowired__ = ('SQLBatis',)

    def __init__(self, sql, params, page, page_size, fetch_all):
        self.sql = sql
        self.params = params
        self.page = page
        self.limit = self.page_size = page_size
        self.fetch_all = fetch_all

    def query(self):
        """Execute the pagenation query and return the results

        :return: PageResults object
        :rtype: PageResults
        """
        self._check_and_calc_page()
        results = self.get_current_page_results()
        return PageResults(self.page, self.page_size, self.total, results)

    def _check_and_calc_page(self):
        """Check the parameters make sense or not, 
        also calculate the total number of rows according to the query

        In terms of the wrong page or page size, the default process is:
        1. if the page size less than 1, will set the page size to 10
        2. if page less than 1, it means the 0 or negative page number, will set 1
        3. if page greater than max page, will set the page number to the max page number
        """
        self.total = self.get_total_number()

        if self.page_size < 1:
            self.limit = self.page_size = 10
            print(
                '[WARNING]: page_size is less than 1, the system reset the page size to 10')

        max_page = math.ceil(self.total / self.page_size)

        if self.page < 1:
            self.page = 1
            print(
                '[WARNING]: page is less than 1, the system reset the page number to 1')

        if self.page > max_page:
            self.page = max_page
            print(
                '[WARNING]: page is greater than the max page, the system reset the page number to max page - {}'.format(max_page))

        self.offset = (self.page - 1) * self.page_size

    def get_total_number(self):
        """Construct the sql to query the total number of rows, and execute

        :return: the total number of rows
        :rtype: int
        """
        total_counts = 'SELECT COUNT(1) FROM ({})'.format(self.sql)

        with self.SQLBatis.get_connection() as conn:
            total = conn.query(total_counts, self.fetch_all,
                               **self.params).scalar()
            return total

    def get_current_page_results(self):
        """Construct the sql to get the current page results, and execute

        :return: The page results 
        :rtype: Rowsets
        """
        current_page_sql = '{} LIMIT {} OFFSET {}'.format(
            self.sql, self.limit, self.offset)

        with self.SQLBatis.get_connection() as conn:
            results = conn.query(
                current_page_sql, self.fetch_all, **self.params)
            return results
