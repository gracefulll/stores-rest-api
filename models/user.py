from db import db


class UserModel(db.Model):

    # tell SQLAlchemy that which table and columns this class is going to map onto
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80))
    password = db.Column(db.String(80))


    def __init__(self, username, password):
        self.username = username
        self.password = password

    @classmethod
    def find_by_username(cls, username):    # this method doesn't use 'self', but use 'UserModel' -> make it a classmethod
        return cls.query.filter_by(username=username).first()  # SELECT * FROM users WHERE username=username LIMIT 1


    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()


    def save_to_db(self):
        db.session.add(self)
        db.session.commit()
