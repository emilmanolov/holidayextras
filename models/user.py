import re

class User(object):

    def __init__(self, email='', forename='', surname=''):
        self.id = None
        self.email = email
        self.forename = forename
        self.surname = surname
        self.created = None

    def __str__(self):
        return '<User {0}>'.format(self.id)

    __repr__ = __str__


class UserValidator(object):

    def __init__(self, email_validator, name_validator):
        self.email_validator = email_validator
        self.name_validator = name_validator

    def validate(self, user):
        return (self.validate_email(user.email) and
                self.validate_forename(user.forename) and
                self.validate_surname(user.surname))

    def validate_email(self, email):
        return self.email_validator.validate(email)

    def validate_forename(self, forename):
        return self.name_validator.validate(forename)

    def validate_surname(self, surname):
        return self.name_validator.validate(surname)

    @classmethod
    def factory(cls):
        return cls(EmailAddressValidator(DomainValidator()), NameValidator())


class NameValidator(object):
    def validate(self, name):
        return len(name.strip()) in range(3, 51)


class DomainValidator(object):
    """ Domain names may be formed from the set of alphanumeric ASCII
        characters (a-z, A-Z, 0-9), but characters are case-insensitive.
        In addition the hyphen is permitted if it is surrounded by characters
        or digits, i.e. it is not the start or end of a label. Labels are always
        separated by the full stop (period) character in the textual name representation.
    """
    def validate(self, domain):
        pattern = r'^(([a-z0-9]{1,63}\.)|([a-z0-9][a-z0-9\-]{1,61}[a-z0-9]\.))+[a-z]{2,63}$'
        match = re.search(pattern, domain, re.IGNORECASE)
        return (len(domain) <= 253 and match is not None)


class EmailAddressValidator(object):

    def __init__(self, domain_validator):
        self.domain_validator = domain_validator

    def validate(self, email):
        match = re.search(r'^([a-z0-9.\-_]+)@([a-z0-9.\-]+)$', email, re.IGNORECASE)
        if match:
            return (self.validate_mailbox(match.group(1)) and
                    self.validate_domain(match.group(2)))
        return False

    def validate_domain(self, domain):
        return self.domain_validator.validate(domain)

    def validate_mailbox(self, mailbox):
        return len(mailbox) <= 64
