import unittest

from models.user import UserValidator

class UserValidatorTest(unittest.TestCase):

    def setUp(self):
        self.email_validator = self._get_email_validator()
        self.name_validator = self._get_name_validator()
        self.user = self._get_user()
        self.validator = UserValidator(self.email_validator, self.name_validator)

    def _get_email_validator(self):
        class EmailAddressValidatorStub: pass
        return EmailAddressValidatorStub()

    def _get_name_validator(self):
        class NameValidatorStub: pass
        return NameValidatorStub()

    def _get_user(self):
        class UserStub: pass
        user = UserStub()
        user.email = ''
        user.forename = ''
        user.surname = ''
        return user

    def test_all_valid(self):
        self.email_validator.validate = lambda x: True
        self.name_validator.validate = lambda x: True
        self.assertValidUser(self.user)

    def test_all_invalid(self):
        self.email_validator.validate = lambda x: False
        self.name_validator.validate = lambda x: False
        self.assertInvalidUser(self.user)

    def test_invalid_email(self):
        self.email_validator.validate = lambda x: False
        self.name_validator.validate = lambda x: True
        self.assertInvalidUser(self.user)

    def test_invalid_forename_and_surname(self):
        self.email_validator.validate = lambda x: True
        self.name_validator.validate = lambda x: False
        self.assertInvalidUser(self.user)

    def assertValidUser(self, user):
        self.assertTrue(self.validator.validate(user))

    def assertInvalidUser(self, user):
        self.assertFalse(self.validator.validate(user))
