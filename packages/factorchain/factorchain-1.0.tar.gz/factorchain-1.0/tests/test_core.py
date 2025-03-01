import unittest
from factorchain.core import Factorchain

class TestFactorchain(unittest.TestCase):
    def test_factorchain(self):
        fc = Factorchain([lambda x: x + 1, lambda x: x * 2])
        self.assertEqual(fc.compute(3), 8)

if __name__ == '__main__':
    unittest.main()
