from flask import Flask
from flask_restful import Resource, Api
from flask_jwt import JWT, jwt_required
from appsettings import *

from securityJWT import authenticate, identity
from resources.user import UserRegister

app = Flask(__name__)

app.secret_key = APP_SECRET_KEY
api = Api(app)

# JWT provide an auth endpoint to verify the user, with this login return a token, 
# this token contains the user's Id and authentication code
jwt = JWT(app, authenticate, identity)




api.add_resource(UserRegister, '/register')



class TestAuthentecation(Resource):
    # Get this functionality if the authorization token is validated
    @jwt_required()
    def get (self):
        return {"message": " get with Authentecation successfully."}, 201

api.add_resource(TestAuthentecation, '/test')



# dockerater
@app.route('/')
def home():
    return "Hello world"


if __name__ == '__main__':
    app.run(port="5000", host="0.0.0.0") # http://localhost:5000