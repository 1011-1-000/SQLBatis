from tests.basic_test import BasicTestCase
from tests.crud import *


class ProxyTestCase(BasicTestCase):

    def test_1_bulk_create_rowcount(self):
        _users = bulk_create(users)
        self.assertEqual(_users.proxy.rowcount, 2)

    def test_2_not_allowed_attr(self):
        _users = bulk_create(users)

        def get_not_allowed_attr():
            return _users.proxy.lastrowid

        self.assertRaises(AttributeError, get_not_allowed_attr)


if __name__ == '__main__':
    unittest.main()
