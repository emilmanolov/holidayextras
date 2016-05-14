import unittest

from models.user import User
from persistence.user import UserRepository

class UserRepositoryTest(unittest.TestCase):

    def setUp(self):
        self.user_mapper = self._get_user_mapper()
        self.datetime = self._get_datetime()
        self.user_repo = UserRepository(User,
                                        self.user_mapper,
                                        self.datetime)

    def _get_user_mapper(self):
        class UserMapperStub: pass
        return UserMapperStub()

    def _get_datetime(self):
        class DateTimeStub: pass
        return DateTimeStub()

    def test_create_user(self):

        email = 'user@example.com'
        forename = 'forename'
        surname = 'surname'
        created = '2015-05-14 12:00:00'

        expected_user = User(email, forename, surname)
        expected_user.created = created

        self.datetime.today = lambda: created

        actual_user = self.user_repo.create(email=email,
                                     forename=forename,
                                     surname=surname)

        self.assertEqual(actual_user.__dict__, expected_user.__dict__)
