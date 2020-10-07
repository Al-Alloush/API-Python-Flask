import sqlite3
'''
API cannot receive data into User class, it is a helper that contains a couple of methods, 
that allow us to easily retrieve User objects from a database, and use to store some data about the User.
'''

class UserModel():
    TABLE_NAME = 'users'

    def __init__(self, _id, username, email,  password):
        self.id = _id
        self.username = username
        self.email = email
        self.password = password
    
    @classmethod
    def find_by_username(cls, username):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "SELECT * FROM users WHERE username=?"
        result = cursor.execute(query,(username,))
        row = result.fetchone()
        if row:
            user = cls(*row)
        else:
            user = None

        connection.close()
        return user
    
    @classmethod
    def find_user(cls, value):

        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "SELECT * FROM users WHERE username=? Or email=?"
        result = cursor.execute(query,(value, value))
        row = result.fetchone()
        if row:
            user = cls(*row)
        else:
            user = None

        connection.close()
        return user

    @classmethod
    def find_by_id(cls, _id):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "SELECT * FROM {table} WHERE id=?".format(table=cls.TABLE_NAME)
        result = cursor.execute(query, (_id,))
        row = result.fetchone()
        if row:
            user = cls(*row)
        else:
            user = None

        connection.close()
        return user

