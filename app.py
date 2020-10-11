from flask import Flask, jsonify
from datetime import timedelta
from flask_restful import Resource, Api
#from flask_jwt import JWT, jwt_required
from flask_jwt_extended import(
    JWTManager, 
    jwt_required, 
    get_jwt_identity, 
    get_jwt_claims, 
    fresh_jwt_required
) 
from appsettings import *
from models.user import UserModel
from resources.user import UserRegister, UserLogin, TokenRefresh, UserLogout
from resources.product import Product, ProductList
from resources.shope import Shope, ShopeList
from libraries import *

app = Flask(__name__)


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['PROPAGATE_EXCEPTIONS'] = True # if False, it will retrun for all errors 500 error
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(minutes = ACCESS_EXPIRES_m) 
app.config['JWT_REFRESH_TOKEN_EXPIRES'] = timedelta(days = REFRESH_EXPIRES_d)  
app.config['JWT_BLACKLIST_ENABLED'] = True # enable blacklist feature
app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access', 'refresh'] # allow blacklisting for access and refresh tokens

'''
flask-SQLAlchemy tracking every change that made to the SQLAlchemy session, and that took some resources. 
And SQLAlchemy the main library itself has its own modification tracker which is a bit better.
this is only changing the flask-SQLAlchemy extensions behaviours not SQLAlchemy. '''
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.secret_key = APP_SECRET_KEY
api = Api(app)

# to create all tables with the first requst in app
@app.before_first_request
def create_tables():
    db.create_all()

# JWT provide an auth endpoint to verify the user, with this login return a token, 
# this token contains the user's Id and authentication code
# jwt = JWT(app, authenticate, identity)
jwt = JWTManager(app)




api.add_resource(Shope, '/shope/<string:name>')
api.add_resource(ShopeList, '/shopes')
api.add_resource(UserRegister, '/register')
api.add_resource(UserLogin, '/login')
api.add_resource(UserLogout, '/logout')
api.add_resource(Product, '/product/<string:name>')
api.add_resource(ProductList, '/products')
api.add_resource(TokenRefresh, '/refresh')

# add claims to access token
@jwt.user_claims_loader
def add_claims_to_jwt(identity):
    user = UserModel.find_by_id(identity)
    return {
        "username":user.username,
        "email": user.email
    }

# configer the message it should send back to the user telling it that their token has expired.
# The following callbacks are used for customizing jwt response/error messages.
# The original ones may not be in a very pretty format (opinionated)
@jwt.expired_token_loader
def expired_token_callback():
    return jsonify({
        'description': 'The token has expired.',
        'error': 'token_expired'
    }), 401

# it's going be called when the token, that sent in the Authorization header is not an actual JWT.
@jwt.invalid_token_loader
def invalid_token_callback(error):  # we have to keep the argument here, since it's passed in by the caller internally
    return jsonify({
        'description': 'Signature verification failed.',
        'error': 'invalid_token'
    }), 401

# it's going to be called when clint don't send an Authorization JWT at all.
@jwt.unauthorized_loader
def missing_token_callback(error):
    return jsonify({
        'description': 'Request does not contain an access token.',
        'error': 'authorization_required'
    }), 401

# functions need a fresh Token, if clint send a non-fresh token call this function.
@jwt.needs_fresh_token_loader
def token_not_fresh_callback():
    return jsonify({
        'description': 'The token is not fresh.',
        'error': 'fresh_token_required'
    }), 401

# This method will check if a token is blacklisted, and will be called automatically when blacklist is enabled
@jwt.token_in_blacklist_loader
def check_if_token_in_blacklist(decrypted_token):
    jti = decrypted_token['jti']
    entry = revoked_store.get(jti)
    if entry is None:
        return True
    return entry == 'true'

# when user log out in token lifetime, set this token is revoked, then clint can't call fuctions with old Token.
@jwt.revoked_token_loader
def revoked_token_callback():
    return jsonify({
        'description': 'The token has been revoked.',
        'error': 'token_revoked'
    }), 401


class TestAuthentecation(Resource):
    # Get this functionality if the authorization token is validated
    # this decorator is for fresh or non-fresh asccess token
    @jwt_required
    def get (self):
        id =get_jwt_identity()
        user = UserModel.find_by_id(get_jwt_identity())# get the identity from access tocken, here is user.id
        claims = get_jwt_claims() 
        return {"message": f" get with Authentecation successfully: {user.username}, {claims['email']}"}, 201

    # this decorator is for just for fresh asccess token, for example to change password we need a 
    @fresh_jwt_required
    def post(slef):
        id =get_jwt_identity()
        user = UserModel.find_by_id(get_jwt_identity())# get the identity from access tocken, here is user.id
        return {"message": f"get inside this post just after login and get a fresh token: {user.username}"}, 201


api.add_resource(TestAuthentecation, '/test')



# dockerater
@app.route('/')
def home():
    return "Hello world"


if __name__ == '__main__':
    from db_sql_alchemy import db
    db.init_app(app)
    app.run(port="5000", host="0.0.0.0") # http://localhost:5000