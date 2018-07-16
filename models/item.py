from db import db

class ItemModel(db.Model):

    # tell SQLAlchemy that which table and columns this class is going to map onto
    __tablename__ = 'items'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    price = db.Column(db.Float(precision=2))

    store_id = db.Column(db.Integer, db.ForeignKey('stores.id'))

    store = db.relationship('StoreModel')   # let 'items' join the table 'stores' with store_id to get the store


    def __init__(self, name, price, store_id):
        self.name = name
        self.price = price
        self.store_id = store_id

    def json(self):
        return {'name': self.name, 'price': self.price, 'store_id': self.store_id}


    # with SQLAlchemy, we no longer need connection, cursor ... blah blah
    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(name=name).first()    # SELECT * FROM items WHERE name=name LIMIT 1
        # the line above return an ItemModel object with self.name and self.price

        # we can even do multiple filtering -
        # ItemModel.query.filter_by(name=name, id=num)
        # or: ItemModel.query.filter_by(name=name).filter_by(id=num)


    def save_to_db(self):
        db.session.add(self)    # SQLAlchemy allows us to directly add the object to the database
        db.session.commit()     # we can have multiple lines of db.session.add(obj), and then commit() once. Here we only have one obj


    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

