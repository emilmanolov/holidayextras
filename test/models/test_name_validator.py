import unittest
from models.user import NameValidator

class UserValidatorTest(unittest.TestCase):

    def setUp(self):
        self.validator = NameValidator()

    def test_valid_name(self):
        self.assertValidName('validname')
        self.assertValidName(' valid name ')
        big_valid_name = 'n' * 50
        self.assertValidName(big_valid_name)
        self.assertValidName(' ' + big_valid_name + ' ')

    def test_empty_name(self):
        self.assertInvalidName('')
        self.assertInvalidName(' ')

    def test_too_short_name(self):
        self.assertInvalidName('n')
        self.assertInvalidName(' n ')

    def test_too_long_name(self):
        self.assertInvalidName('n' * 51)

    def assertValidName(self, name):
        self.assertTrue(self.validator.validate(name))

    def assertInvalidName(self, name):
        self.assertFalse(self.validator.validate(name))
