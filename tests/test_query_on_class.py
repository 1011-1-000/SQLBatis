import unittest

from tests.basic_test import BasicTestCase, db
from tests.crud import *


class QueryOnClassMethod:

    @db.query(CREATE)
    def instance(self, user):
        pass

    @staticmethod
    @db.query(CREATE)
    def static_method(user):
        pass

    @db.bulk_query(CREATE)
    def bulk_query_instance(self, users):
        pass

    @staticmethod
    @db.bulk_query(CREATE)
    def bulk_query_static_method(users):
        pass


class QueryOnClassMethodTestCase(BasicTestCase):

    def test_1_instance(self):
        instance = QueryOnClassMethod()
        instance.instance(user)
        result = select().first()
        self.assertEqual(result.name, 'leo1')

    def test_2_static_method(self):
        QueryOnClassMethod.static_method(user)
        result = select().first()
        self.assertEqual(result.name, 'leo1')

    def test_3_bulk_instance(self):
        instance = QueryOnClassMethod()
        instance.bulk_query_instance(users)
        results = select()
        self.assertEqual(len(results), 4)

    def test_4_bulk_static_method(self):
        QueryOnClassMethod.bulk_query_static_method(users)
        results = select()
        self.assertEqual(len(results), 6)


if __name__ == '__main__':
    unittest.main()
