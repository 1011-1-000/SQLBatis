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
        assert _id == 1
        results = user_dao.retrieve_by_id(1)
        assert results.name == 'leo1'

    def test_2_update(self):
        user_dao = UserDao()
        user_dao.update_by_id(
            {'id': 1, 'name': 'Huang', 'full_name': 'Leo.Huang'})
        results = user_dao.retrieve_by_id(1)
        assert results.name == 'Huang'
        assert results.full_name == 'Leo.Huang'

    def test_3_retrieve_all(self):
        user_dao = UserDao()
        user_dao.create(user)
        results = user_dao.retrieve_all().all()
        assert len(results) == 2

    def test_4_delete_by_id(self):
        user_dao = UserDao()
        user_dao.delete_by_id(1)
        results = user_dao.retrieve_all().all()
        assert len(results) == 1

    def test_5_bulk_insert(self):
        user_dao = UserDao()
        r = user_dao.retrieve_all()
        user_dao.bulk_insert(users)
        results = user_dao.retrieve_all().all()
        assert len(results) == 3


if __name__ == '__main__':
    unittest.main()
