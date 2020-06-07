from tests.basic_test import BasicTestCase
from tests.crud import *


class TransactionTestCase(BasicTestCase):

    def test_1_transaction(self):
        try:
            transaction_test()
        except Exception as e:
            pass
        result = count().scalar()
        assert result == 0


if __name__ == '__main__':
    unittest.main()
