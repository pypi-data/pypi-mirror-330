import unittest
from datetime_utils.core import format_date, days_between

class TestDateTimeUtils(unittest.TestCase):
    def test_format_date(self):
        self.assertEqual(format_date('2025-02-28'), '28-02-2025')

    def test_days_between(self):
        self.assertEqual(days_between('2025-02-28', '2025-03-01'), 1)

if __name__ == "__main__":
    unittest.main()

