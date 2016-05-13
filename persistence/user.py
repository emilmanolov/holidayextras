import config
import components.memorydb
import components.sqlitedb
import models.user

def get_repo():
    """ Factory function for creating UserRepository instance. """
    user_mapper = get_user_mapper()
    return UserRepository(user_mapper)

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
    def __init__(self, user_mapper):
        self.user_mapper = user_mapper

    def find_by_id(self, user_id):
        return self.user_mapper.find_by_id(user_id)

    def save(self, user):
        self.user_mapper.save(user)

    def delete(self, user_id):
        self.user_mapper.delete(user_id)


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


class DbUserMapper:
    """ User data mapper using SQLite database for persistence. """

    def __init__(self, db):
        self.db = db

    #def __del__(self):
    #    self.db.close()

    def find_by_id(self, user_id):
        sql = ("SELECT * FROM user WHERE id = ?;")
        row = self.db.execute(sql, (user_id,)).fetchone()
        if not row == None:
            return self._create_user(row)
        return None

    def find_all(self, conditions = []):
        sql = ("SELECT * FROM user;")
        rows = self.db.execute(sql, (id,))
        return self._create_user_collection(rows)

    def save(self, user):
        if user.id == None:
            sql = ("INSERT INTO user (email, forename, surname, created)"
                   "VALUES (:email, :forename, :surname, NOW());")
        else:
            sql = ("UPDATE user"
                   "SET email = :email, forename = :forename, surname = :surname"
                   "WHERE id = :id")
        rows = self.db.execute(sql, {
            'id' : user.id,
            'email' : user.email,
            'forename': user.forename,
            'surname': user.surname,
            'created': user.created,
        }).fetchall()
        #self.db.execute(sql, user.__dict__)
        #self.db.commit()

    def delete(self, user_id):
        cursor = self.db.cursor()
        sql = "DELETE FROM todo WHERE id = ?;"
        cursor.execute(sql, (user_id,))
        self.db.commit()

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
