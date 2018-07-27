import os

from flask import Flask
from flask_restful import Api
from flask_jwt import JWT

from security import authenticate, identity

from resources.user import UserRegister

from resources.item import Item, ItemList

from resources.store import Store, StoreList


# note: when import a file (e.g. in another file, we "import app"
# Python will first check each class, and then each method, to make sure that there's no error
# (but will not actually run them)
# However: each single statement in the file will be run!

# In the case of app.py, when we (in another file) import app, app.run() will be run,
# which is NOT what we want. In order to prevent this, we use:
# if __name__ == '__main__'
# (since only the file we run is __main__, if we are not running app.py but, rather, just import it in another file
#  when we run that another file, that file will be __main__, and thus app.run() will not be invoked)


app = Flask(__name__)
#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'  # tell SQLAlchemy where to find data.db

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///data.db')
# use Heroku's postgres. 'DATABASE_URL' is provided by Heroku->Settings->Config Vars
# but we still want to test locally - so providing sqlite:/// as the fallback default value to get()

app.config['SQLALCHEMY_TRACK_MODIFICATION'] = False    # turn off flask's SQLAlchemy tracker in order to use SQLAlchemy's own tracker instead
app.secret_key = 'jose'
api = Api(app)




jwt = JWT(app, authenticate, identity)


# instead of the decorator, with flask_restful, now we can do:
api.add_resource(Item, '/item/<string:name>')  # http://127.0.0.1:5000/student/Rolf
# This URL is used for all http verbs: get, post, delete, put

api.add_resource(ItemList, '/items')

api.add_resource(Store, '/store/<string:name>')
api.add_resource(StoreList, '/stores')

api.add_resource(UserRegister, '/register')



if __name__ == '__main__':
    from db import db
    db.init_app(app)
    app.run(port=5000, debug=True)
