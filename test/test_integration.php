import unittest

class Test(unittest.TestCase):

    def setUp(self):
        pass

    def test_one(self):
        class ABC: pass
        expected = 1
        self.assertEqual(1, expected)

if __name__ == '__main__':
    unittest.main(verbosity=2)

#python -m unittest -v test.test_zipstream
