"""..."""
import persistence.user
import models.user
from web import Response

class UserFinder(object):

    def __init__(self, response, user_repository):
        self.response = response
        self.user_repository = user_repository

    def find(self, user_id):
        """Find user by ID"""
        user = self.user_repository.find_by_id(user_id)
        if user:
            self.response.body = user.__dict__
        else:
            self.response.status = '404 NOT FOUND'
            self.response.body = 'User not found.'

    @classmethod
    def factory(cls, response):
        user_repository = persistence.user.get_repo()
        return cls(response, user_repository)

class UserCreator(object):

    def __init__(self, request, user_repository):
        self.request = request
        self.user_repository = user_repository

    def create(self):
        """Add a new user to the store """
        user_data = self.request.json
        validator = models.user.UserValidator()
        if not validator.validate(user_data):
            return Response('Data validation failed.', 422)
        user = self.user_repository.save(user_data)
        if user:
            return Response(user.__dict__, 201).redirect('/user/' + str(user.id))
        else:
            return Response('error', 404)

    @classmethod
    def factory(cls, request, response):
        user_repository = persistence.user.get_repo()
        return cls(request, user_repository)

class UserUpdater(object):

    def __init__(self, request, user_repository):
        self.request = request
        self.user_repository = user_repository

    def update(self, user_id):
        """Update an existing user"""
        user_data = self.request.json
        user = user_data
        if user:
            if self.user_repository.save(user):
                return Response(user.__dict__)
            return Response('error', 404)
        return Response('Data validation failed. Please check the response body for detailed error messages.', 422)

    @classmethod
    def factory(cls, request, response):
        user_repository = persistence.user.get_repo()
        return cls(request, user_repository)

class UserDeleter(object):

    def __init__(self, user_repository):
        self.user_repository = user_repository

    def delete(self, user_id):
        """Deletes a user"""
        try:
            self.user_repository.delete(user_id)
            return Response('', 204)
            # The request was handled successfully and the response contains no body content
        except Exception:
            return Response('', 500)

    @classmethod
    def factory(cls, response):
        user_repository = persistence.user.get_repo()
        return cls(user_repository)
