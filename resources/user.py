import sqlite3
from flask_restful import Resource, reqparse
import uuid
from models.user import UserModel
from flask_jwt_extended import(
    create_access_token, 
    create_refresh_token, 
    jwt_refresh_token_required, 
    get_jwt_identity,
    jwt_required,
    get_jti,
    get_raw_jwt
)
from global_functions import Hashing_Password, Verify_Password
from libraries import *
from datetime import timedelta

ACCESS_EXPIRES = timedelta(minutes = ACCESS_EXPIRES_m) 
REFRESH_EXPIRES = timedelta(days = REFRESH_EXPIRES_d) 

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
        

class UserLogin(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument('usernameOrEmail',
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
        data = UserLogin.parser.parse_args()

        user = UserModel.find_user(data['usernameOrEmail'])


        # this is what the `authenticate()` function did in securityJWT.py
        if user and Verify_Password(user.password, data['password']):
            # identity= is what the identity() function did in securityJWT.py, now stored in the JWT
            access_token = create_access_token(identity=user.id, fresh=True) 
            refresh_token = create_refresh_token(user.id)

            # Store the tokens in redis with a status of not currently revoked. We
            # can use the `get_jti()` method to get the unique identifier string for
            # each token. We can also set an expires time on these tokens in redis,
            # so they will get automatically removed after they expire. We will set
            # everything to be automatically removed shortly after the token expires
            access_jti = get_jti(encoded_token=access_token) # get the curent id of the access Token
            refresh_jti = get_jti(encoded_token=refresh_token) # get the curent id of the refresh access Token
            revoked_store.set(access_jti, 'false', ACCESS_EXPIRES * 1.2)
            revoked_store.set(refresh_jti, 'false', REFRESH_EXPIRES * 1.2)


            return {
                "username": user.username,
                "email": user.email,
                'access_token': access_token,
                'refresh_token': refresh_token
            }, 200

        return {"message": "Invalid Credentials!"}, 401

class UserLogout(Resource):
    @jwt_required
    def post(self):
        jti = get_raw_jwt()['jti']  # jti is "JWT ID", a unique identifier for a JWT.
        revoked_store.set(jti, 'true', REFRESH_EXPIRES * 1.2)
        return {"message": "Successfully logged out"}, 200


class TokenRefresh(Resource):
    @jwt_refresh_token_required
    def get(self):
        """
        Get a new access token without requiring username and password—only the 'refresh token'
        provided in the /login endpoint.
        Note that refreshed access tokens have a `fresh=False`, which means that the user may have not
        given us their username and password for potentially a long time (if the token has been
        refreshed many times over).
        """
        current_user = get_jwt_identity()
        # fresh is false this token is not like the token in UserLogin class, this token is Less valid
        new_token = create_access_token(identity=current_user, fresh=False) 
        access_jti = get_jti(encoded_token=new_token)
        revoked_store.set(access_jti, 'false', ACCESS_EXPIRES * 1.2)
        return {'access_token': new_token}, 200