from tests.basic_test import BasicTestCase, db
from tests.crud import *


@db.query(SELECT_USER_BY_NAME)
def select_user_by_name(name):
    pass


class RowSetTestCase(BasicTestCase):

    def test_row_set_1_is_empty(self):
        results = select()
        print(results)
        assert results.is_empty == True

    def test_row_set_2_get_attr(self):

        bulk_create(users)
        results = select()
        assert results.is_empty == False
        assert results.name == ['leo2', 'leo3']

    def test_row_set_3_scalar(self):
        result = count().scalar()
        assert result == 2

    def test_row_set_4_one(self):
        create(user)
        create(user)
        try:
            result = select_user_by_name('leo1')
            result.one()
        except AssertionError as e:
            assert str(e) == 'Expects only one row contained'

    def test_row_set_5_all(self):
        results = select().all()
        assert len(results) == 4


if __name__ == '__main__':
    unittest.main()
