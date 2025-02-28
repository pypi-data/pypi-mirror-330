import unittest
from decimal import Decimal

from ostium_python_sdk.formulae import GetTakeProfitPrice


class TestGetTradeTpPrice(unittest.TestCase):

    def setUp(self):
        self.test_cases = [
            {
                'openPrice': Decimal('100000'),
                'leverage': Decimal('100'),
                'isLong': True,
                'profit_p': Decimal('900'),
                'expected_tp_price': Decimal('109000')
            },
        ]

    def test_get_trade_tp_price(self):
        for case in self.test_cases:
            with self.subTest(case=case):
                sl_price = GetTakeProfitPrice(
                    case['isLong'],
                    case['openPrice'],
                    case['leverage'],
                    case['isLong'],
                    case['profit_p']
                )
                self.assertAlmostEqual(
                    sl_price,
                    case['expected_tp_price'],
                    places=7,
                    msg=f"Failed for case: {case}"
                )


if __name__ == '__main__':
    unittest.main()
