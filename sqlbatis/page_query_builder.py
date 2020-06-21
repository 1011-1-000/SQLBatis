import math
from .container import SQLBatisMetaClass


class PageResult:

    def __init__(self, page, page_size, total, results):
        self.page = page
        self.page_size = page_size
        self.total = total
        self.results = results

    @property
    def has_next(self):
        return True if self.total > self.page * self.page_size else False

    @property
    def has_prev(self):
        return True if self.page > 1 else False


class PageQueryBuilder(metaclass=SQLBatisMetaClass):

    __autowired__ = ('SQLBatis',)

    def __init__(self, sql, params, page, page_size, fetch_all):
        self.sql = sql
        self.params = params
        self.page = page
        self.limit = self.page_size = page_size
        self.fetch_all = fetch_all

    def query(self):
        self._check_and_calc_page()
        results = self.get_current_page_results()
        return PageResult(self.page, self.page_size, self.total, results)

    def _check_and_calc_page(self):

        self.total = self.get_total_number()

        if self.page_size <= 0:
            self.limit = self.page_size = 10
            print(
                '[WARNING]: page_size is less than 1, the system reset the page size to 10')

        max_page = math.ceil(self.total/self.page_size)

        if self.page <= 0:
            self.page = 1
            print(
                '[WARNING]: page is less than 1, the system reset the page number to 1')

        if self.page > max_page:
            self.page = max_page
            print(
                '[WARNING]: page is greater than the max page, the system reset the page number to max page - {}'.format(max_page))

        self.offset = (self.page - 1) * self.page_size

    def get_total_number(self):
        total_counts = 'SELECT COUNT(1) FROM ({})'.format(self.sql)

        with self.SQLBatis.get_connection() as conn:
            total = conn.query(total_counts, self.fetch_all,
                               **self.params).scalar()
            return total

    def get_current_page_results(self):
        current_page_sql = '{} LIMIT {} OFFSET {}'.format(
            self.sql, self.limit, self.offset)
        with self.SQLBatis.get_connection() as conn:
            results = conn.query(
                current_page_sql, self.fetch_all, **self.params)
            return results
