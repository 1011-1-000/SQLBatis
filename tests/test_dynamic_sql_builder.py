import unittest

from tests.basic_test import BasicTestCase, db
from tests.crud import *
from sqlbatis.sqlbatis_dao import SQLBatisDao
from sqlbatis.dynamic_sql_builder import DynamicSQLBuilder


class UserDao(SQLBatisDao):

    def __init__(self):
        super(UserDao, self).__init__()


def select(attrs, default='and'):

    query_clauses = {
        'name': 'name = :name',
        'id': 'id = :id',
    }

    dynamic_sql_builder = DynamicSQLBuilder(
        'select * from user', query_clauses)

    dynamic_sql = dynamic_sql_builder.dynamic_build(
        list(attrs.keys()), default)

    @db.query(dynamic_sql)
    def _select(attrs):
        pass

    return _select(attrs)


class DynamicTestCase(BasicTestCase):

    def test_1_dynamic_sql(self):
        user_dao = UserDao()
        user_dao.bulk_insert(users)
        user_dao.bulk_insert(users)

        results = select({'name': 'leo2'}).all()
        self.assertEqual(len(results), 2)
        self.assertEqual(results[0].name, 'leo2')

        results = select({'name': 'leo2', 'id': 1}).all()
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].name, 'leo2')

        results = select({'name': 'leo2', 'id': 2}, 'or').all()
        self.assertEqual(len(results), 3)


if __name__ == '__main__':
    unittest.main()
