import unittest

from models.user import DomainValidator

class DomainValidatorTest(unittest.TestCase):

    def setUp(self):
        self.validator = DomainValidator()

    def test_valid_domain(self):
        self.assert_valid_domain('e.co')
        self.assert_valid_domain('example.co')
        self.assert_valid_domain('EXAMPLE.COM')
        self.assert_valid_domain('e-xample.com')

    def test_empty_domain(self):
        self.assert_invalid_domain('')
        self.assert_invalid_domain(' ')

    def test_too_short_tld(self):
        self.assert_invalid_domain('example.c')

    def test_too_long_domain(self):
        self.assert_invalid_domain('x' * 255 + '.com')

    def test_incomplete_domain(self):
        self.assert_invalid_domain('example')
        self.assert_invalid_domain('example.')

    def test_invalid_domain(self):
        self.assert_invalid_domain(' exa mple . com ')
        self.assert_invalid_domain('-example-.com')
        self.assert_invalid_domain('example.c-om')

    def assert_valid_domain(self, domain):
        self.assertTrue(self.validator.validate(domain))

    def assert_invalid_domain(self, domain):
        self.assertFalse(self.validator.validate(domain))
