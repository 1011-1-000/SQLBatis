from tests.basic_test import BasicTestCase, db
from tests.crud import *


class PropagationTestCase(BasicTestCase):

    def test_1_required_inner(self):
        try:
            transaction_outer_for_inner_exception()
        except Exception as e:
            pass
        result = count().scalar()
        assert result == 0

    def test_2_required_outer(self):
        try:
            transaction_outer_for_outer_exception()
        except Exception as e:
            pass
        result = count().scalar()
        assert result == 0


if __name__ == '__main__':
    unittest.main()
