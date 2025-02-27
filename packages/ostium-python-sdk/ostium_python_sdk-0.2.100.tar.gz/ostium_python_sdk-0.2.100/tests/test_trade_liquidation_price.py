from ostium_python_sdk.formulae import GetTradeLiquidationPrice
from decimal import Decimal
import pytest


@pytest.fixture
def test_cases():
    return [
        {
            'openPrice': Decimal('92961.71'),
            'isLong': True,
            'collateral': Decimal('98'),
            'leverage': Decimal('20'),
            'rollover_fee': Decimal('0'),
            'current_funding_fee': Decimal('2757.79'),
            'expected_liq_price': Decimal('219578.879081')
        },
    ]


def test_trade_liquidation_price(test_cases):
    for case in test_cases:
        liq_price = GetTradeLiquidationPrice(
            case['openPrice'],
            case['isLong'],
            case['collateral'],
            case['leverage'],
            case['rollover_fee'],
            case['current_funding_fee']
        )
        assert pytest.approx(liq_price, rel=Decimal(1e-7)
                             ) == case['expected_liq_price']
