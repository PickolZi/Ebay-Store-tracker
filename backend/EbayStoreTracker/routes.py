from flask import Blueprint, jsonify

from . import db
from .models import Stores, Items

main = Blueprint("main", __name__)

@main.route("/")
def index():
    return "Ebay Store Tracker Development Site"

# End points
@main.route("/api/getAllStores")
def getAllStores():
    store = Stores.query.all()
    store_json = {}

    for item in store:
        name = item.name
        id = item.id

        store_json[name] = id

    return jsonify({
        "stores": store_json,
        "numOfStores": len(store_json)
    })

@main.route("/api/getAllActiveItems/store/<int:store_id>")
def getAllActiveItems(store_id):
    items = Items.query.filter_by(store_id=store_id, status="Active").order_by("date_last_updated").all()
    active_items_list = []

    for item in items:
        active_items_list.append({
            "item_id": item.item_id,
            "title": item.title,
            "listed_date": item.listed_date,
            "date_last_updated": item.date_last_updated,
            "price": item.price,
            "item_url": item.item_url,
            "image_url": item.image_url,
            "location": item.location,
            "status": item.status,
            "store_id": item.store_id
        })
    
    return jsonify({
        "data": active_items_list,
        "numOfItems": len(active_items_list),
        "totalWorth": sum([item["price"] for item in active_items_list])
    })

@main.route("/api/getAllSoldItems/store/<int:store_id>")
def getAllSoldItems(store_id):
    items = Items.query.filter_by(store_id=store_id, status="Sold").order_by("date_last_updated").all()
    active_items_list = []

    for item in items:
        active_items_list.append({
            "item_id": item.item_id,
            "title": item.title,
            "listed_date": item.listed_date,
            "date_last_updated": item.date_last_updated,
            "date_sold": item.date_sold,
            "price": item.price,
            "item_url": item.item_url,
            "image_url": item.image_url,
            "location": item.location,
            "status": item.status,
            "store_id": item.store_id
        })
    
    return jsonify({
        "data": active_items_list,
        "numOfItems": len(active_items_list),
        "totalWorth": sum([item["price"] for item in active_items_list])
    })
    
        
        

