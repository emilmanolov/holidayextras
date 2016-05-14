import unittest
from persistence.user import UserRepository

class UserRepositoryTest(unittest.TestCase):

    def setUp(self):
        self.user_mapper = self._get_user_mapper()
        self.user_class = self._get_user_class()
        self.user_repo = UserRepository(self.user_class, self.user_mapper)

    def _get_user_mapper(self):
        class UserMapperStub: pass
        return UserMapperStub()

    def _get_user_class(self):
        class UserStub: pass
        return UserStub

    def test_create_user(self):
        pass
