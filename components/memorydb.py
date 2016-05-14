import threading
from utils import Singleton

class InMemoryDatabase(object):
    """ Very simple in memory database implementation. """

    def __init__(self):
        self.data = {'123' : 'dummy user'}

    def save(self, key, value): 
        self.data[key] = value

    def find(self, key): 
        if key in self.data:
            return self.data[key]

    def exists(self, key): 
        return key in self.data

    def delete(self, key): 
        if key in self.data:
            del self.data[key]

class InMemoryDatabaseThreadSafe(InMemoryDatabase):
    """ Thread-safe version of the simple in memory database class. """

    def __init__(self, lock):
        super(InMemoryDatabaseThreadSafe, self).__init__()
        self.lock = lock

    def save(self, key, value): 
        with self.lock:
            super(InMemoryDatabaseThreadSafe, self).save(key, value)

    def find(self, key): 
        with self.lock:
            return super(InMemoryDatabaseThreadSafe, self).find(key)

    def exists(self, key): 
        with self.lock:
            return super(InMemoryDatabaseThreadSafe, self).exists(key)

    def delete(self, key): 
        with self.lock:
            super(InMemoryDatabaseThreadSafe, self).delete(key)

    @classmethod
    def factory(cls):
        lock = threading.Lock()
        return cls(lock)
