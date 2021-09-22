import unittest

from tests.basic_test import BasicTestCase, db
from tests.crud import *


class QueryTestCase(BasicTestCase):

    def test_1_create(self):
        create(user)

    def test_2_select(self):

        result = select().first()
        self.assertEqual(result.name, 'leo1')
        assert result.name == 'leo1'

    def test_3_update(self):
        update('Huang')
        result = select().first()
        self.assertEqual(result.name, 'Huang')
        assert result.name == 'Huang'

    def test_4_delete(self):
        delete()
        result = select().first()
        self.assertEqual(result, None)


if __name__ == '__main__':
    unittest.main()
