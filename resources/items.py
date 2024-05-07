from flask import request
from flask_smorest import Blueprint, abort
from flask.views import MethodView
from sqlalchemy.exc import SQLAlchemyError, IntegrityError

from schemas import ItemUpdateSchema,ItemSchema
from db import db
from models import ItemModel


blp = Blueprint("items", __name__, description="items operations")


@blp.route("/item/<string:item_id>")
class Item(MethodView):

    @blp.response(200, ItemSchema)
    def get(self, item_id):
        item = ItemModel.query.get_or_404(item_id)
        return item
    
    
    @blp.response(204,)
    def delete(self, item_id):
        item = ItemModel.query.get_or_404(item_id)
        db.session.delete(item)
        db.session.commit()
    
    @blp.arguments(ItemUpdateSchema)
    @blp.response(200, ItemSchema)
    def put(self, item_data, item_id):
        try:
            item = ItemModel.query.get(item_id)
            if item:
                item.name = item_data["name"]
                item.price = item_data["price"]

            else:
                item  = ItemModel(id=item_id,**item_data)

            db.session.add(item)
            db.session.commit()
        except SQLAlchemyError:
            abort(500, message="Error while updating item")

        return item


@blp.route("/items")
class AddItems(MethodView):

    @blp.response(200, ItemSchema(many=True))
    def get(self):
        items = ItemModel.query.all()
        return items

    @blp.arguments(ItemSchema)
    @blp.response(200, ItemSchema)
    def post(self, item_data):
        item = ItemModel(**item_data)
        try:
            db.session.add(item)
            db.session.commit()
        except SQLAlchemyError:
            abort(500, message="An error occurred creating the store")
        return item
    

        
@blp.route("/update_items")
class UpdateItems(MethodView):

    #@blp.arguments(ItemUpdateSchema)
    def put(self):
        item_data = request.get_json()
        store_items = item_data["items"]
        try:
            storeid = item_data["storeid"]
            if storeid not in items.keys():
                abort(404, message="store doesn't exist")
            # list to hold item names in the specific store
            existing_items = list(items[storeid].keys())
            for name, price in store_items.items():
                    items[storeid][name] = price
            return items
        except KeyError:
            return {"opps": "oops"}
        


@blp.route("/delete_items")
class DeleteItems(MethodView):
    def delete(self):
        request_data = request.get_json()
        store_id = request_data["storeid"]
        for name,__ in request_data["items"].items():
            del items[store_id][name]
        return {"message": "items deleted"}, 204
        

