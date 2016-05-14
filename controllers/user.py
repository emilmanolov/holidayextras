from interactors import UserFinder, UserCreator, UserUpdater, UserDeleter

class User(object):

    def __init__(self, request):
        self.request = request

    def get(self, user_id):
        user_finder = UserFinder.factory()
        return user_finder.find(user_id)

    def post(self):
        user_creator = UserCreator.factory(self.request)
        return user_creator.create()

    def put(self, user_id):
        user_updater = UserUpdater.factory(self.request)
        return user_updater.update(user_id)

    def delete(self, user_id):
        user_deleter = UserDeleter.factory()
        return user_deleter.delete(user_id)
