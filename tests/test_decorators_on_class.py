import unittest

from tests.basic_test import BasicTestCase, db
from tests.crud import *
from sqlbatis.sqlbatis_dao import SQLBatisDao

CREATE = 'INSERT INTO user(name) VALUES (:name)'
SELECT = 'SELECT * FROM user'
DELETE = 'DELETE FROM user WHERE id = 1'
UPDATE = 'UPDATE user SET name = :name WHERE id = 1'
COUNT = 'SELECT count(*) FROM user'
SELECT_USER_BY_NAME = 'SELECT * FROM user WHERE name = :name'


class UserDao(SQLBatisDao):

    def __init__(self):
        super(UserDao, self).__init__()

    @db.query(CREATE)
    def create(self, name):
        pass

    @db.query(SELECT)
    def select(self):
        pass

    @staticmethod
    @db.query(SELECT)
    def static_select():
        pass


class QueryOnClassTestCase(BasicTestCase):

    def test_1_class_create(self):

        UserDao().create('leo')

    def test_2_class_select(self):
        user = UserDao().select().first()
        self.assertEqual(user.name, 'leo')

    def test_2_static_select(self):
        user = UserDao.select().first()
        self.assertEqual(user.name, 'leo')


if __name__ == '__main__':
    unittest.main()
