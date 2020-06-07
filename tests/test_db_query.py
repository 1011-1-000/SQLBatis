from tests.basic_test import BasicTestCase, db
from tests.crud import *


class QueryTestCase(BasicTestCase):

    def test_1_create(self):

        create(user)

    def test_2_select(self):

        result = select().first()
        assert result.name == 'leo1'

    def test_3_update(self):
        update('Huang')
        result = select().first()
        assert result.name == 'Huang'

    def test_4_delete(self):
        delete()
        result = select().first()
        assert result == None


if __name__ == '__main__':
    unittest.main()
