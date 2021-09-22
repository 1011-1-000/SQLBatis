import unittest

from tests.basic_test import BasicTestCase, db
from tests.crud import *
from sqlbatis.sqlbatis_dao import SQLBatisDao


class UserDao(SQLBatisDao):

    def __init__(self):
        super(UserDao, self).__init__()


class BasicDaoWhereTestCase(BasicTestCase):

    def test_1_where(self):
        user_dao = UserDao()
        user_dao.bulk_insert(users)
        results = user_dao.filter_by({'name': 'leo2'}).all()
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].name, 'leo2')

        assert len(results) == 1
        assert results[0].name == 'leo2'

    def test_2_where_multiple_conditions(self):
        user_dao = UserDao()
        user_dao.bulk_insert(users)
        results = user_dao.filter_by({'name': 'leo2', 'id': 2}).all()
        self.assertEqual(len(results), 0)
        results = user_dao.filter_by({'name': 'leo2', 'id': 3}).all()
        self.assertEqual(len(results), 1)

    def test_3_empty_where(self):
        user_dao = UserDao()
        user_dao.bulk_insert(users)
        results = user_dao.filter_by({}).all()
        self.assertEqual(len(results), 6)

    def test_4_where_multiple_records(self):
        user_dao = UserDao()
        results = user_dao.filter_by({'name': 'leo2'}).all()
        self.assertEqual(len(results), 3)


if __name__ == '__main__':
    unittest.main()
