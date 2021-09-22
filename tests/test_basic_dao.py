import unittest

from tests.basic_test import BasicTestCase, db
from tests.crud import *
from sqlbatis.sqlbatis_dao import SQLBatisDao


class UserDao(SQLBatisDao):

    def __init__(self):
        super(UserDao, self).__init__()


class BasicDaoTestCase(BasicTestCase):

    def test_1_dao_create_and_retrieve_by_id(self):

        user_dao = UserDao()

        _id = user_dao.create(user)
        self.assertEqual(_id, 1)
        _id = user_dao.create(extra_user)
        self.assertEqual(_id, 2)
        results = user_dao.retrieve_by_id(2)
        self.assertEqual(results.name, 'libra')

    def test_2_update(self):
        user_dao = UserDao()
        user_dao.update_by_id(2,
                              {'name': 'Huang', 'full_name': 'Leo.Huang'})
        results = user_dao.retrieve_by_id(2)
        self.assertEqual(results.name, 'Huang')
        self.assertEqual(results.full_name, 'Leo.Huang')

    def test_3_retrieve_all(self):
        user_dao = UserDao()
        user_dao.create(user)
        results = user_dao.retrieve_all().all()
        self.assertEqual(len(results), 3)

    def test_4_delete_by_id(self):
        user_dao = UserDao()
        user_dao.delete_by_id(1)
        results = user_dao.retrieve_all().all()
        self.assertEqual(len(results), 2)
        self.assertEqual(results[0].name, 'Huang')

    def test_5_bulk_insert(self):
        user_dao = UserDao()
        r = user_dao.retrieve_all()
        user_dao.bulk_insert(users)
        results = user_dao.retrieve_all().all()
        self.assertEqual(len(results), 4)
        assert len(results) == 4


if __name__ == '__main__':
    unittest.main()
