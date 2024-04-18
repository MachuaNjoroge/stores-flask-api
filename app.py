from flask import Flask, request, abort
from flask_smorest import abort
from sqlalchemy import SQLColumnExpression
from db import stores, items
import uuid 


app = Flask(__name__)


@app.get("/store")
def get_stores():
    return{"stores": stores}, 200

@app.get("/store/<string:name>")
def get_store_id(name):
    store_names = list(stores.values())
    store_keys = list(stores.keys())
    if name in store_names:
        position = store_names.index(name)
        return store_keys[position], 200
    else:
        return {"id": "8bcfdfee0a5d429c9064d796d7f7bb64"}, 404
        #abort(404, message="Store doesn't exit.")


@app.post("/store")
def create_stores():
    request_data = request.get_json()
    store = request_data["name"]
    # if store not in stores.keys() also works
    if store not in stores:
        storeid = uuid.uuid4().hex
        stores[storeid] = store
        return {storeid: stores[storeid] }, 201
    else:
        return {"message": f"store {store} exists created"}, 200

@app.post("/add_items")
def add_items():
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
    
    
@app.put("/update_items")
def update_items():
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

@app.delete("/delete_items")
def delete_items():
    request_data = request.get_json()
    store_id = request_data["storeid"]
    for name,__ in request_data["items"].items():
        del items[store_id][name]
    return {"message": "items deleted"}, 201

@app.get("/storeitems")
def store_items():
    request_data = request.get_json()
    try:
        return items[request_data["uid"]]
    except KeyError:
        abort(404, message="Store doesn't exit.")
   

@app.get("/store/<string:store_uid>")
def storeitems(store_uid):
    suid = int(store_uid)
    try:
        return items[suid]
    except:
        abort(404, message="Store doesn't exist.")
    # for store in stores:
    #     if store["name"] == name:
    #         #return store["items"][0], 200
    #         return store, 200
    return {"error": "Store doesn't exist"}, 404


@app.put("/update_store")
def update_store():
    request_data = request.get_json()
    try:
        stores[request_data["storeID"]] = request_data["name"]
        return {"message": "Updated Succesfully"}
    except KeyError as e:
        abort(404, message="store doesn't exist")

@app.delete("/delete_store")
def delete_store():
    request_data = request.get_json()
    try:
        store_id = request_data["storeid"]
        del stores[store_id]
        return {"message": "items deleted"}, 201
    except KeyError as e:
        abort(404, message="Store doesn't exist")

