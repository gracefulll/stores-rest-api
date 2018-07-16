import sqlite3
from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.item import ItemModel


# Every Resource must be a class

# Resource usually mapped to database

# class Item inherits class Resource
class Item(Resource):

    # Note that parser doesn't have 'self' in front of it, which means that parser belongs to the class Item
    parser = reqparse.RequestParser()
    parser.add_argument('price',  # specify which part of the payload we are going to update
                        type=float,
                        required=True,
                        help="This field cannot be left blank!"
                        )

    parser.add_argument('store_id',  # specify which part of the payload we are going to update
                        type=int,
                        required=True,
                        help="Every item needs a store id."
                        )

    # @app.route('/item/<string:name>') No, we no longer need this
    @jwt_required()   # we need to authenticate before we can call this method
    def get(self, name):
        try:
            item = ItemModel.find_by_name(name)   # Now item is an object of ItemModel rather than a JSON dictionary
        except:
            return {"message": "An error occurred searching the item."}, 500    # 500: internal se

        if item:
            return item.json()   # so we have to jsonify it before returning it
        return {'message': 'Item not found'}, 404


    def post(self, name):

        # error-first approach
        if ItemModel.find_by_name(name):
            return {'message': 'An item with name "{}" already exists.'.format(name)}, 400    # 400: bad request (request's fault)

        requested_data = Item.parser.parse_args()

        # make sure item is NOT a dictionary but a ItemModel object
        #item = {'name': name, 'price': requested_data['price']}  # our return value -- has to be in JSON format

        #item = ItemModel(name, requested_data['price'], requested_data['store_id'])
        item = ItemModel(name, **requested_data)

        try:
            item.save_to_db()
        except:
            return {"message": "An error occurred inserting the item."}, 500    # 500: internal server error  (server's fault)

        # tell the client that we've processed the request -- note that item NOW is an ItemModel object rather than a JSON dictionary
        # so we have to jsonify item before running it
        return item.json(), 201    # 201: server successfully creates something and says everything is OK

        # P.S. 202: means "accepted" - accept client's request to create a long-time-taking object (may takes up to 10 or 20 minutes)
        # it may fail later, but it's out with client's control. 202 just means: server accepts the request and will work on it


    def delete(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            item.delete_from_db()

        return {'message': 'Item deleted'}


    def put(self, name):

        data = Item.parser.parse_args()

        item = ItemModel.find_by_name(name)

        if item is None:   # doesn't exist yet
            #item = ItemModel(name, data['price'], data['store_id'])   # make item a new object of ItemModel
            item = ItemModel(name, **data)
        else:
            item.price = data['price']   # update item's price

        item.save_to_db()     # add item to the database

        return item.json()




class ItemList(Resource):
    def get(self):

        return {'items': [item.json() for item in ItemModel.query.all()]}

        # or:
        # return {'items': list(map(lambda x: x.json(), ItemModel.query.all()))}
        # (use it when working with others in other languages - map, reduce, filter are more stackable)


        # P.S.
        # ItemModel.query.all()    # return all the objects in the database



        

