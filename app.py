from flask import Flask
from flask_restful import Resource, Api
#from flask_jwt import JWT, jwt_required
from flask_jwt_extended import JWTManager, jwt_required, get_jwt_identity, get_jwt_claims
from appsettings import *
from models.user import UserModel
from resources.user import UserRegister, UserLogin
from resources.product import Product, ProductList
from resources.shope import Shope, ShopeList

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['PROPAGATE_EXCEPTIONS'] = True # if False, it will retrun for all errors 500 error

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
api.add_resource(Product, '/product/<string:name>')
api.add_resource(ProductList, '/products')

# add claims to access token
@jwt.user_claims_loader
def add_claims_to_jwt(identity):
    user = UserModel.find_by_id(identity)
    return {
        "username":user.username,
        "email": user.email
    }


class TestAuthentecation(Resource):
    # Get this functionality if the authorization token is validated
    @jwt_required
    def get (self):
        id =get_jwt_identity()
        user = UserModel.find_by_id(get_jwt_identity())# get the identity from access tocken, here is user.id
        claims = get_jwt_claims() 
        return {"message": f" get with Authentecation successfully: {user.username}, {claims['email']}"}, 201

api.add_resource(TestAuthentecation, '/test')



# dockerater
@app.route('/')
def home():
    return "Hello world"


if __name__ == '__main__':
    from db_sql_alchemy import db
    db.init_app(app)
    app.run(port="5000", host="0.0.0.0") # http://localhost:5000