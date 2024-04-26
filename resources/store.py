import uuid
from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from db import stores 
from schemas import StoreSchema




blp = Blueprint("store", __name__, description="Operations on stores")


@blp.route("/store/<string:store_id>")
class Store(MethodView):
    def get(self, store_id):
        try:
            return stores[store_id]
        except KeyError as e:
            abort(404, message="Store doesn't exist")

    def delete(self, store_id):
        try:
            store = stores[store_id]
            del stores[store_id]
            return {"message": f"store {store} deleted"}, 204
        except KeyError as e:
            abort(404, message="Store doesn't exist")


@blp.route("/store")
class Store(MethodView):
    def get(self):
        return{"stores": stores}, 200

    #@blp.arguments(StoreSchema)
    def post(self):
        store_data = request.get_json()
        store = store_data["name"]
        # if store not in stores.keys() also works
        if store not in stores:
            storeid = uuid.uuid4().hex
            stores[storeid] = store
            return {storeid: stores[storeid] }, 201
        else:
            return {"message": f"store {store} exists"}, 200
        
@blp.route("/update_store")
class StoreUpdate(MethodView):
    def put(self):
        request_data = request.get_json()
        store_id = request_data["storeID"]
        store_name = request_data["name"]
        if store_id in stores.keys():
            stores[store_id] = store_name
            return {"message": "store updated successfully"}, 200
        else:
            abort(404, message="Store doesn't exist")
  