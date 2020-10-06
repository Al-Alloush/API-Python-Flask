import sqlite3
from flask_restful import Resource, reqparse
import uuid
from myFunctions import *

connection = sqlite3.connect('data.db')

class User():
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


class UserRegister(Resource):
    TABLE_NAME = 'users'

    parser = reqparse.RequestParser()
    parser.add_argument('username',
                        type=str,
                        required=True,
                        help="This field cannot be left blank!"
                        )
    parser.add_argument('email',
                        type=str,
                        required=True,
                        help="This field cannot be left blank!"
                        )
    parser.add_argument('password',
                        type=str,
                        required=True,
                        help="This field cannot be left blank!"
                        )

    def post(self):
        data = UserRegister.parser.parse_args()

        if User.find_user(data['username']) is not None or User.find_user(data['email']) is not None:
            return {"message": "this user is existing"}, 400

        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        hashed_password = Hashing_Password(data['password'])
        query = "INSERT INTO {table} VALUES (?, ?, ?, ?)".format(table=self.TABLE_NAME)
        cursor.execute(query, (str(uuid.uuid4()), data['username'], data['email'], str(hashed_password)))

        # afetr insert save changes
        connection.commit()
        connection.close()

        return {"message": "User created successfully."}, 201
