from db import db

class StoreModel(db.Model):

    # tell SQLAlchemy that which table and columns this class is going to map onto
    __tablename__ = 'stores'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))

    # [way1] In this way, whenever a store is created, we need to create corresponding item objs for this store, and then save them to 'items' variable -- very tedious and slow
    #items = db.relationship('ItemModel')  # let 'stores' join the table 'items' to get all the items (a list of ItemModel's) in each store

    # [way2] In this way, not until we call json() will the items be created -> lazy=dynamic, making creating the 'stores' table very easy
    items = db.relation('ItemModel', lazy='dynamic')


    # [way1] and [way2] represent a trade-off between the speed of creating 'stores' table
    # and the speed of calling the JSON method -- it's up to us to determine which one is more important

    def __init__(self, name):
        self.name = name


    def json(self):
        # [way1] This way makes self.items in memory and therefore very easy to check (any time!)
        # return {'name': self.name, 'items': [item.json() for item in self.items]}   # or: StoreModel.items is also OK. The class-attribute can be accessed both by the class or the object(instance)

        # [way2] In this way, with lazy='dynamic', self.items is not a list anymore -- it becomes a query, and we need to call self.items.all() to actually go into the 'items' table to find the items -- slow
        return {'name': self.name, 'items': [item.json() for item in self.items.all()]}


    # with SQLAlchemy, we no longer need connection, cursor ... blah blah
    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(name=name).first()    # SELECT * FROM items WHERE name=name LIMIT 1
        # the line above returns an ItemModel object with self.name and self.price

        # we can even do multiple filtering -
        # ItemModel.query.filter_by(name=name, id=num)
        # or: ItemModel.query.filter_by(name=name).filter_by(id=num)


    def save_to_db(self):
        db.session.add(self)    # SQLAlchemy allows us to directly add the object to the database
        db.session.commit()     # we can have multiple lines of db.session.add(obj), and then commit() once. Here we only have one obj


    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

