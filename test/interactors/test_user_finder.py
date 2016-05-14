import unittest

from web import Response
from models.user import User
from interactors import UserFinder

class UserFinderTest(unittest.TestCase):

    def setUp(self):
        self.user_repository = self._get_user_repository()
        self.user_finder = UserFinder(self.user_repository)

    def _get_user_repository(self):
        class UserRepositoryStub: pass
        return UserRepositoryStub()

    def test_user_not_found(self):
        self.user_repository.find_by_id = lambda x: None #User()
        expected_response = Response('User not found.', '404 Not Found')
        self.assertFindUserResponse(expected_response)

    def test_user_found(self):
        self.user_repository.find_by_id = lambda x: User()
        expected_response = Response(User().__dict__, '200 OK')
        self.assertFindUserResponse(expected_response)

    def assertFindUserResponse(self, expected_response):
        actual_response = self.user_finder.find(0)
        self.assertEqualValueObjects(actual_response, expected_response)

    def assertEqualValueObjects(self, actual, expected):
        self.assertEqual(actual.__dict__, expected.__dict__)
