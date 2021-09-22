import unittest

from tests.basic_test import BasicTestCase, db
from tests.crud import *


class BulkQueryTestCase(BasicTestCase):

    def test_1_bulk_create(self):

        bulk_create(users)
        results = select()
        self.assertEqual(len(results), 2)


if __name__ == '__main__':
    unittest.main()
