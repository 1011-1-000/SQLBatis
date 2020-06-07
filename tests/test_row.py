from tests.basic_test import BasicTestCase, db
from tests.crud import *


class RowTestCase(BasicTestCase):

    def test_row_1_create(self):

        create(user)

    def test_row_2_get(self):
        result = select().first()
        assert result.name == 'leo1'
        assert result[1] == 'leo1'


if __name__ == '__main__':
    unittest.main()
