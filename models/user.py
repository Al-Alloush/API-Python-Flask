import sqlite3
from db_sql_alchemy import db

'''
API cannot receive data into User class, it is a helper that contains a couple of methods, 
that allow us to easily retrieve User objects from a database, and use to store some data about the User.
'''

class UserModel(db.Model):
    # definition of the table to work with
    # table name.
    __tablename__ = 'users'
    # Table's columns.
    id = db.Column(db.String, primary_key=True)
    username = db.Column(db.String(50), unique=True)
    email = db.Column(db.String(16), unique=True)
    password = db.Column(db.String(80))

    def __init__(self, _id, username, email,  password):
        self.id = _id
        self.username = username
        self.email = email
        self.password = password
    
    @classmethod
    def find_by_username(cls, username):
        return cls.query.filter_by(username=username).first() # SELECT * FROM users WHERE username = username LIMIT 1"
    
    @classmethod
    def find_user(cls, value):
       # check if user email or username exist
        user = cls.query.filter_by(username=value).first() # SELECT * FROM users WHERE username = value LIMIT 1"
        if user is None:
            user = cls.query.filter_by(email=value).first() # SELECT * FROM users WHERE email = value LIMIT 1"
        # return user or None
        return user

    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first() # SELECT * FROM users WHERE id = _id LIMIT 1"
    
    def save_to_db(self):
        # add function work for both the insert and the update, updae if retrive an Id
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()


