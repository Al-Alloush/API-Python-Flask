import sqlite3
from flask_restful import Resource, reqparse
import uuid
from models.user import UserModel
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

        # check if username or email not exit.
        user = UserModel.find_user(data['username']) 
        if user is None:
            user = UserModel.find_user(data['email'])
        if user is not None:
            return {"message": "this user is existing"}, 400

        # create an object from UserModel to save this user in database
        user = UserModel(str(uuid.uuid4()), data["username"],data["email"],Hashing_Password(data["password"]))
        
        try:
            user.save_to_db()
            return {"message": "User created successfully."}, 201
        except expression as ex:
            return {"message": "Servir Error"}, 500
        
