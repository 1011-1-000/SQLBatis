import unittest

from tests.basic_test import BasicTestCase, db
from tests.crud import *


class PropagationTestCase(BasicTestCase):

    def test_1_required_inner(self):
        try:
            transaction_outer_for_inner_exception()
        except Exception as e:
            pass
        result = count().scalar()
        self.assertEqual(result, 0)

    def test_2_required_outer(self):
        try:
            transaction_outer_for_outer_exception()
        except Exception as e:
            pass
        result = count().scalar()
        self.assertEqual(result, 0)


@db.transactional()
def transaction_outer_for_inner_exception():
    create(user)
    create(user)
    transaction_inner_for_inner_exception()


@db.transactional()
def transaction_inner_for_inner_exception():
    create(user)
    raise Exception('transaction error')


@db.transactional()
def transaction_outer_for_outer_exception():
    create(user)
    transaction_inner_for_outer_exception()
    raise Exception('transaction error')
    create(user)


@db.transactional()
def transaction_inner_for_outer_exception():
    create(user)


if __name__ == '__main__':
    unittest.main()
