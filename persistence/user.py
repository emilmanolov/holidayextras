# https://gist.github.com/justanr/aac7bb4576f769c2fecc
# https://gist.github.com/JonathanRaiman/aa0bdfd8e3511c59f3af
import config
import components.memorydb
import components.sqlitedb
import models.user
import datetime

def get_repo():
    """ Factory function for creating UserRepository instance. """
    user_mapper = get_user_mapper()
    return UserRepository(models.user.User, user_mapper, datetime.datetime)

def get_user_mapper():
    """ Factory function for creating UserMapper instance depending on the
        configuration file. """
    if config.PERSISTENCE_TYPE == 'db':
        db = components.sqlitedb.get_db_connection()
        return DbUserMapper(db)
    elif config.PERSISTENCE_TYPE == 'memory':
        memory_database = components.memorydb.InMemoryDatabaseThreadSafe.factory()
        return InMemoryUserMapper(memory_database)


class UserRepository:
    """ Provides an interface for persisting User models.
        Abstracts the persistence layer from different concrete
        data mapper implementations.
    """
    def __init__(self, model_class, user_mapper, datetime):
        self.model_class = model_class
        self.user_mapper = user_mapper
        self.datetime = datetime

    def find_by_id(self, user_id):
        return self.user_mapper.find_by_id(user_id)

    def persist(self, user):
        return self.user_mapper.save(user)

    def delete(self, user_id):
        self.user_mapper.delete(user_id)

    def create(self, email, forename, surname):
        user = self.model_class(email, forename, surname)
        user.created = self._get_timestamp()
        return user

    def _get_timestamp(self):
        return str(self.datetime.today())


class InMemoryUserMapper(object):
    """ User data mapper using InMemoryDatabase for persistence. """

    def __init__(self, mem_db):
        self.mem_db = mem_db

    def find_by_id(self, user_id):
        return self.mem_db.find(user_id)

    def save(self, user):
        if user.user_id == None:
            #self.current_id
            pass
        else:
            self.mem_db.save(user.user_id, user)

    def delete(self, user_id):
        self.mem_db.delete(user_id)

    def create(self, **kwargs):
        #sqlite3.register_adapter()
        #sqlite3.register_converter()
        pass


class DbUserMapper:
    """ User data mapper using SQLite database for persistence. """

    tablename = 'user'

    def __init__(self, db):
        self.db = db

    def _get_cursor(self, sql, params):
        sql = sql.format(table=self.tablename)
        return self.db.execute(sql, params)

    def find_by_id(self, user_id):
        sql = "SELECT * FROM {table} WHERE id = ?"
        cur = self._get_cursor(sql, (user_id,))
        row = cur.fetchone()
        if row:
            return self._create_user(row)

    def save(self, user):
        if user.id == None:
            sql = ("INSERT INTO {table} (email, forename, surname, created) "
                   "VALUES (:email, :forename, :surname, :created)")
        else:
            sql = ("UPDATE {table} "
                   "SET email = :email, forename = :forename, surname = :surname "
                   "WHERE id = :id")
        cur = self._get_cursor(sql, {
            'id' : user.id,
            'email' : user.email,
            'forename': user.forename,
            'surname': user.surname,
            'created': user.created,
        })
        user.id = cur.lastrowid
        return user

    def delete(self, user_id):
        sql = "DELETE FROM {table} WHERE id = ?;"
        cur = self._get_cursor(sql, (user_id,))

    def _create_user(self, row):
        user = models.user.User()
        user.id = row['id']
        user.email = row['email']
        user.forename = row['forename']
        user.surname = row['surname']
        user.created = row['created']
        return user

    def _create_user_collection(self, rows):
        users = []
        for row in rows:
            users[row.user_id] = self._create_user(row)
        return users
