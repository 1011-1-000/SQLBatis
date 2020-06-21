from tests.basic_test import BasicTestCase, db
from tests.crud import *


@db.query_by_page(SELECT, 1, 10, True)
def query_first_page(self):
    pass


@db.query_by_page(SELECT, 4, 10, True)
def query_last_page(self):
    pass


@db.query_by_page(SELECT, 2, 10, True)
def query_middle_page(self):
    pass


@db.query_by_page(SELECT, -1, 10, True)
def query_with_wrong_page_lt(self):
    pass


@db.query_by_page(SELECT, 5, 10, True)
def query_with_wrong_page_gt(self):
    pass


@db.query_by_page(SELECT, 1, 5, True)
def query_with_diff_size_fisrt(self):
    pass


@db.query_by_page(SELECT, 7, 5, True)
def query_with_diff_size_last(self):
    pass


class PageQueryTestCase(BasicTestCase):

    def test_1_page_create(self):
        bulk_create(users_for_paged)

    def test_2_page_first_page(self):

        page = query_first_page()
        assert len(page.results) == 10
        assert page.page == 1
        assert page.page_size == 10
        assert page.total == 35
        assert page.has_next == True
        assert page.has_prev == False

    def test_3_page_last_page(self):
        page = query_last_page()
        assert len(page.results) == 5
        assert page.page == 4
        assert page.page_size == 10
        assert page.total == 35
        assert page.has_next == False
        assert page.has_prev == True

    def test_4_middle_page(self):
        page = query_middle_page()
        assert len(page.results) == 10
        assert page.page == 2
        assert page.page_size == 10
        assert page.total == 35
        assert page.has_next == True
        assert page.has_prev == True

    def test_5_with_wrong_page_number_lt(self):
        page = query_with_wrong_page_lt()
        assert len(page.results) == 10
        assert page.page == 1
        assert page.page_size == 10
        assert page.total == 35
        assert page.has_next == True
        assert page.has_prev == False

    def test_5_with_wrong_page_number_gt(self):
        page = query_with_wrong_page_gt()
        assert len(page.results) == 5
        assert page.page == 4
        assert page.page_size == 10
        assert page.total == 35
        assert page.has_next == False
        assert page.has_prev == True

    def test_6_size_diff_first_page(self):

        page = query_with_diff_size_fisrt()
        assert len(page.results) == 5
        assert page.page == 1
        assert page.page_size == 5
        assert page.total == 35
        assert page.has_next == True
        assert page.has_prev == False

    def test_7_size_diff_last_page(self):
        page = query_with_diff_size_last()
        assert len(page.results) == 5
        assert page.page == 7
        assert page.page_size == 5
        assert page.total == 35
        assert page.has_next == False
        assert page.has_prev == True


if __name__ == '__main__':
    unittest.main()
