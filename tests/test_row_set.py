import unittest

from tests.basic_test import BasicTestCase, db
from tests.crud import *
from sqlbatis.row import Row


@db.query(SELECT_USER_BY_NAME)
def select_user_by_name(name):
    pass


class RowSetTestCase(BasicTestCase):

    def test_row_set_1_is_empty(self):
        results = select()
        assert results.is_empty == True

    def test_row_set_2_get_attr(self):
        bulk_create(users)
        results = select()
        self.assertEqual(results.is_empty, False)
        self.assertEqual(results.name, ['leo2', 'leo3'])

    def test_row_set_3_scalar(self):
        result = count().scalar()
        self.assertEqual(result, 2)
        assert result == 2

    def test_row_set_4_one(self):
        result = select_user_by_name('leo2').one()
        self.assertEqual(isinstance(result, Row), True)

        create(user)
        create(user)
        result = select_user_by_name('leo1')
        self.assertRaises(AssertionError, result.one)

    def test_row_set_5_all(self):
        results = select().all()
        self.assertEqual(len(results), 4)
        self.assertEqual(isinstance(results, list), True)
        self.assertEqual(isinstance(results[0], Row), True)

    def test_row_set_6_to_dictionary(self):
        results = select()
        results = results.to_dict()
        self.assertEqual(len(results), 4)
        self.assertEqual(results[0]['name'], 'leo2')
        self.assertEqual(isinstance(results[0], dict), True)

    def test_row_set_7_first(self):
        result = select().first()
        self.assertEqual(result.name, 'leo2')


if __name__ == '__main__':
    unittest.main()
