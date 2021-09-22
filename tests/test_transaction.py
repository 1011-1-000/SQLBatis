import unittest

from sqlbatis.errors import QueryException

from tests.basic_test import BasicTestCase
from tests.crud import *


@db.transactional()
def transaction_test():
    create(user)
    raise Exception('transaction error')
    create(user)


@db.transactional()
def transaction_test_file_not_found():
    create(user)
    with open('a.txt', 'r') as f:
        r.read()
    create(user)


class TransactionTestCase(BasicTestCase):

    def test_1_transaction(self):
        try:
            transaction_test()
        except Exception as e:
            pass
        result = count().scalar()
        self.assertEqual(result, 0)
        assert result == 0

    def test_2_transaction_message(self):
        self.assertRaises(QueryException, transaction_test_file_not_found)
        # transaction_test_file_not_found()


if __name__ == '__main__':
    unittest.main()
