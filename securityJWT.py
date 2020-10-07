from werkzeug.security import safe_str_cmp # safe string compare
from models.user import UserModel as User
from global_functions import Verify_Password

# in 
def authenticate(username, password):
    # it does not matter if passed username or email to this method
    user = User.find_user(username)
    # compare if password is right
    if user and Verify_Password(user.password, password):
        return user

def identity(payload):
    user_id = payload['identity']
    return User.find_by_id(user_id)