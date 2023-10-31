from . import db
from datetime import datetime

class Stores(db.Model):
    id = db.Column("id", db.Integer, primary_key=True)
    name = db.Column("name", db.String, unique=True, nullable=False)
    items = db.relationship("Items", backref="items")

    def __repr__(self):
        return f"Store {id}: {self.name}"


class Items(db.Model):
    item_id = db.Column("item_id", db.Integer, primary_key=True)
    title = db.Column("title", db.String)
    listed_date = db.Column("listed_date", db.DateTime)
    date_last_updated = db.Column("date_last_updated", db.DateTime, default=datetime.utcnow)
    price = db.Column("price", db.Float)
    item_url = db.Column("item_url", db.String)
    image_url = db.Column("image_url", db.String)
    location = db.Column("location", db.String)
    status = db.Column("status", db.String)

    store_id = db.Column(db.Integer, db.ForeignKey('stores.id'), nullable=False)

    def __repr__(self):
        return f"Item {item_id}: {title} by: {store_id}"
