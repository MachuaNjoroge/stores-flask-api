from flask import Flask, request, abort
from flask_smorest import abort
from sqlalchemy import SQLColumnExpression
from db import stores, items

store_counter = 1


app = Flask(__name__)

# stores = [
#     {
#     "name": "My Store",
#     "items": [
#         {
#             "name": "chir",
#             "price": 120
#         }
#     ]
# }
# ]


@app.get("/store")
def get_stores():
    return{"stores": stores}, 200


@app.post("/store")
def create_stores():
    request_data = request.get_json()
    global store_counter
    store = request_data["name"]
    #new_store  = {"name": request_data["name"], "items": []}
    # if store not in stores.keys() also works
    if store not in stores:
        store_counter += 1
        stores[store] = store_counter
        print(stores)
        return {"message": "store {store} successfully created"}, 201
    else:
        return {"message": "store {store} exists created"}, 200

@app.post("/add_items")
def add_items():
    request_data = request.get_json()
    for store in stores:
        if store["name"] == request_data["name"]:
            # Add a dictionary in which you will add the items as name:value pairs
            if len(store["items"]) == 0:
                store["items"].append({})
            # Request["items"] is a list with one dictionary ie [{"chair":70, "table":70}] , thus we retreive 
            # the dictionary by accessin the first item of the list, then iterate over it 
            for item,price in request_data["items"][0].items():
                # Access the dictionary by accessing the first item of the items list
                print(f"item {item} is {price}")
                store["items"][0][item] = price
            return {store["name"]: store["items"]},201
    return {"error": "store doesn't exist"}, 404


@app.get("/storeitems")
def store_items():
    request_data = request.get_json()
    # for store in stores:
    #     if store["name"] == request_data["name"]:
    #         #return store["items"][0], 200
    #         return store, 200
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

