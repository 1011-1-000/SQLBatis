from tests.basic_test import BasicTestCase, db
from tests.crud import *


class RowSetTestCase(BasicTestCase):

    def test_row_set_1_get_attr(self):

        bulk_create(users)
        results = select()
        assert results.name == ['leo2', 'leo3']


if __name__ == '__main__':
    unittest.main()
