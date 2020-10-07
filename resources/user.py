import sqlite3
from flask_restful import Resource, reqparse
import uuid
from models.user import UserModel as User
from global_functions import Hashing_Password

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
