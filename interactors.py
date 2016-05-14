import persistence.user
import models.user
from web import Response

class UserFinder(object):

    def __init__(self, user_repository):
        self.user_repository = user_repository

    def find(self, user_id):
        """Find user by ID"""
        user = self._find_user(user_id)
        if user:
            return Response(user.__dict__, '200 OK')
        return Response('User not found.', '404 Not Found')

    def _find_user(self, user_id):
        return self.user_repository.find_by_id(user_id)

    @classmethod
    def factory(cls):
        user_repository = persistence.user.get_repo()
        return cls(user_repository)

class UserCreator(object):

    def __init__(self, request, user_repository, user_validator):
        self.request = request
        self.user_repository = user_repository
        self.user_validator = user_validator

    def create(self):
        """Add a new user to the store """
        user_data = self._get_user_data()
        user = self._create_user(user_data)
        if not self._validate(user):
            return Response('Data validation failed.', '422')
        if self._persist(user):
            response = Response(user.__dict__, '201 CREATED')
            response.add_header('Location', "/user/{0}".format(user.id))
            return response

    def _get_user_data(self):
        return self.request.json

    def _create_user(self, user_data):
        return self.user_repository.create(
                user_data['email'],
                user_data['forename'],
                user_data['surname'])

    def _validate(self, user):
        return self.user_validator.validate(user)

    def _persist(self, user):
        return self.user_repository.persist(user)

    @classmethod
    def factory(cls, request):
        user_repository = persistence.user.get_repo()
        user_validator = models.user.UserValidator.factory()
        return cls(request, user_repository, user_validator)

class UserUpdater(object):

    def __init__(self, request, user_repository, user_validator):
        self.request = request
        self.user_repository = user_repository
        self.user_validator = user_validator

    def update(self, user_id):
        """Update an existing user"""
        user_data = self._get_user_data()
        user = self._create_user(user_data)
        if not self._validate(user):
            return Response('Data validation failed.', '422')
        user.id = user_id
        if self._persist(user):
            return Response(user.__dict__)

    def _get_user_data(self):
        return self.request.json

    def _create_user(self, user_data):
        return self.user_repository.create(
                user_data['email'],
                user_data['forename'],
                user_data['surname'])

    def _validate(self, user):
        return self.user_validator.validate(user)

    def _persist(self, user):
        return self.user_repository.persist(user)

    @classmethod
    def factory(cls, request):
        user_repository = persistence.user.get_repo()
        user_validator = models.user.UserValidator.factory()
        return cls(request, user_repository, user_validator)

class UserDeleter(object):

    def __init__(self, user_repository):
        self.user_repository = user_repository

    def delete(self, user_id):
        """Deletes a user"""
        self.user_repository.delete(user_id)
        return Response('', '204 No Content')

    @classmethod
    def factory(cls):
        user_repository = persistence.user.get_repo()
        return cls(user_repository)
