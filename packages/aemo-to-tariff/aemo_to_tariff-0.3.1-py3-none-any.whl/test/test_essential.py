import unittest
from datetime import datetime
from zoneinfo import ZoneInfo
import aemo_to_tariff.essential as essential

class TestEssentualPower(unittest.TestCase):
    def test_some_essential_functionality(self):
        interval_time = datetime(2025, 2, 20, 9, 10, tzinfo=ZoneInfo('Australia/Sydney'))
        tariff_code = 'BLNT3AL'
        rrp = -100.0
        expected_price = 3.858878319999999
        price = essential.convert(interval_time, tariff_code, rrp)
        loss_factor = expected_price / price
        self.assertAlmostEqual(price * 1.1678, expected_price, places=1)
