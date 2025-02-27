import unittest

from src.cjlutils import DictUtil


class GetDistributionTest(unittest.TestCase):
    def test_empty(self):
        self.assertEqual(DictUtil.get_distribution({}), {})
        self.assertEqual(DictUtil.get_distribution(None), {})

    def test_single(self):
        self.assertEqual({'1': 1}, DictUtil.get_distribution({'1': [1]}))
        self.assertEqual({'1': 2}, DictUtil.get_distribution({'1': [1, 1]}))
        self.assertEqual({'1': 2}, DictUtil.get_distribution({'1': [1, 2]}))
        self.assertEqual({'1': 3}, DictUtil.get_distribution({'1': [1, 2, 1]}))


if __name__ == '__main__':
    unittest.main()
