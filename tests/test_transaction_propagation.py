from tests.basic_test import BasicTestCase, db
from tests.crud import *


class PropagationTestCase(BasicTestCase):

    def test_1_required(self):
        try:
            transaction_outer()
        except Exception as e:
            pass
        result = count().scalar()
        assert result == 0


if __name__ == '__main__':
    unittest.main()
