from resources.user import UserModel

# Here in Section 5, we use database to store user information
# (rather than the in-memory dictionary we used to adopt in Section 4)


# send username, password to the /auth endpoint
def authenticate(username, password):
    user = UserModel.find_by_username(username)
    if user and user.password == password:
        return user

def identity(payload):
    user_id = payload['identity']
    return UserModel.find_by_id(user_id)



