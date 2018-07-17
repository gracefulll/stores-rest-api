from app import app
from db import db

db.init_app(app)

# let SQLAlchemy create all the tables for us
@app.before_first_request
def create_tables():
    db.create_all()
