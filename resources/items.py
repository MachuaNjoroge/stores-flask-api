from db import items
from flask import request
from flask_smorest import Blueprint, abort
from flask.views import MethodView


blp = Blueprint("items", __name__, description="items operations")


@blp.route("/add_items")
class AddItems(MethodView):
    def post(self):
        request_data = request.get_json()
        store_items = request_data["items"]
        try:
            storeid = request_data["storeid"]
            if storeid not in items.keys():
                items[storeid] = {}
            # list to hold item names in the specific store
            existing_items = list(items[storeid].keys())
            for name, price in store_items.items():

                #if the name in the items we are trying to add exists, throw an error, since this method add but doesn't update store items
                if name in existing_items:
                    return {"message": "undefined error"}, 401
                else:
                    items[storeid][name] = price
            return items
        except KeyError:
            return {"opps": "oops"}
        
@blp.route("/update_items")
class UpdateItems(MethodView):
    def post(self):
        request_data = request.get_json()
        store_items = request_data["items"]
        try:
            storeid = request_data["storeid"]
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
        

