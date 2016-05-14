import unittest
from models.user import EmailAddressValidator, DomainValidator

class EmailAddressValidatorTest(unittest.TestCase):

    def setUp(self):
        self.domain_validator = DomainValidator()
        self.email_validator = EmailAddressValidator(self.domain_validator)

    def test_valid_mailbox_and_valid_domain(self):
        self.assert_valid_email('user@example.com')
        self.assert_valid_email('user.name@example.com')
        self.assert_valid_email('user-name@example.com')
        self.assert_valid_email('user_name@example.com')

    def test_valid_mailbox_and_invalid_domain(self):
        self.assert_invalid_email('user@example')

    def test_invalid_mailbox_and_valid_domain(self):
        self.assert_invalid_email('')
        self.assert_invalid_email('user-example.com')
        self.assert_invalid_email(' user@example.com')
        self.assert_invalid_email('u ser@example.com')

    def assert_valid_email(self, email):
        self.assertTrue(self.email_validator.validate(email))

    def assert_invalid_email(self, email):
        self.assertFalse(self.email_validator.validate(email))
