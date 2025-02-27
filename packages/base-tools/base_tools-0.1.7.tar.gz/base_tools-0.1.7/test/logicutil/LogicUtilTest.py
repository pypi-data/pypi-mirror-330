import unittest
import random

from src.cjlutils import LogicUtil


class GetGreatestCommonDivisorTest(unittest.TestCase):
    def test_invalid(self):
        self.assertEqual(-1, LogicUtil.get_greatest_common_divisor(-1, 1))
        self.assertEqual(-1, LogicUtil.get_greatest_common_divisor(1, -1))
        self.assertEqual(-1, LogicUtil.get_greatest_common_divisor(-1, -1))

        self.assertEqual(-1, LogicUtil.get_greatest_common_divisor(0, 1))
        self.assertEqual(-1, LogicUtil.get_greatest_common_divisor(1, 0))

    def test_gcd(self):
        self.assertEqual(1, LogicUtil.get_greatest_common_divisor(1, 1))
        self.assertEqual(1, LogicUtil.get_greatest_common_divisor(2, 1))
        self.assertEqual(1, LogicUtil.get_greatest_common_divisor(1, 2))

        self.assertEqual(2, LogicUtil.get_greatest_common_divisor(2, 2))
        self.assertEqual(2, LogicUtil.get_greatest_common_divisor(2, 4))
        self.assertEqual(2, LogicUtil.get_greatest_common_divisor(4, 2))
        self.assertEqual(2, LogicUtil.get_greatest_common_divisor(6, 4))
        self.assertEqual(2, LogicUtil.get_greatest_common_divisor(4, 6))

        self.assertEqual(3, LogicUtil.get_greatest_common_divisor(3, 3))
        self.assertEqual(3, LogicUtil.get_greatest_common_divisor(3, 6))
        self.assertEqual(3, LogicUtil.get_greatest_common_divisor(6, 3))
        self.assertEqual(3, LogicUtil.get_greatest_common_divisor(9, 6))
        self.assertEqual(3, LogicUtil.get_greatest_common_divisor(6, 9))
        self.assertEqual(3, LogicUtil.get_greatest_common_divisor(3, 9))
        self.assertEqual(3, LogicUtil.get_greatest_common_divisor(9, 3))

        self.assertEqual(4, LogicUtil.get_greatest_common_divisor(4, 4))
        self.assertEqual(4, LogicUtil.get_greatest_common_divisor(4, 8))
        self.assertEqual(4, LogicUtil.get_greatest_common_divisor(8, 4))

        for _ in range(100):
            value = random.randint(1, 1000)
            self.assertEqual(value, LogicUtil.get_greatest_common_divisor(value, value))
            self.assertEqual(1, LogicUtil.get_greatest_common_divisor(1, value))
            self.assertEqual(1, LogicUtil.get_greatest_common_divisor(value, 1))

        for _ in range(100):
            value1 = random.randint(1, 1000)
            value2 = random.randint(1, 1000)
            gcd = LogicUtil.get_greatest_common_divisor(value1, value2)
            self.assertEqual(0, value1 % gcd, f'gcd of {value1} and {value2} is {gcd}')
            self.assertEqual(0, value2 % gcd, f'gcd of {value1} and {value2} is {gcd}')
