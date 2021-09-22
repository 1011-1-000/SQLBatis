import unittest

from tests.basic_test import BasicTestCase, db
from tests.crud import *


class RowTestCase(BasicTestCase):

    def test_row_1_create(self):

        create(user)

    def test_row_2_get(self):
        result = select().first()
        self.assertEqual(result.name, 'leo1')
        self.assertEqual(result.get('name'), 'leo1')

    def test_row_3_to_dict(self):
        result = select().first().to_dict()
        self.assertEqual(isinstance(result, dict), True)
        self.assertEqual(result['name'], 'leo1')


if __name__ == '__main__':
    unittest.main()
