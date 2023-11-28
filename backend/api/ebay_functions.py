# Functions used to propogate database using ebay's api calls will be called here
import os
import sqlite3
from datetime import datetime, timedelta

from ebay_api import getAllEbayDataFromStores, isValidStore, areSoldItems, pretty_print_json

DATABASE = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "instance/db.sqlite3"))

def getIdFromStoreName(store):
    # Find the store id given the store name
    # params: store => string from stores database
    # returns: int => id from database.
    sql_query = f"""
    SELECT id from stores where name="{store}";
    """

    if not isValidStore(store):
        return False

    con = sqlite3.connect(DATABASE)
    cur = con.cursor()

    res = cur.execute(sql_query)
    id = res.fetchone()[0]

    con.close()
    return id

def dailyUpdateDatabaseFromEbay(store):
    # Will be ran once a day.
    # Calls getAllEbayDataFromStores(), gets every ebay item from a store and updates it to current database. If item already exists or there's a new item being added, the 'date_last_updated' date will be updated. However, this means, old items that aren't coming from the api call will not be updated. This mean the item was taken down or sold.
    # params: store => String of ebay store name. From stores table.
    # Returns: Nothing. Updates database.

    if not isValidStore(store):
        return False

    store_id = getIdFromStoreName(store)

    # For stores with more than 10k parts(100 entries for 100 pages). I can not call pages after 100, so I have to break up api call and filter by price so pages are less than 100.
    ebay_items = getAllEbayDataFromStores(store)
    if not ebay_items:
        print("Error occured when getting items from ebay api.")
        print(f"Stopping daily update for {store}")
        return

    # Connecting to database.
    con = sqlite3.connect(DATABASE)
    cur = con.cursor()

    cur_updated_time = datetime.now() - timedelta(minutes=2)

    for index, ebay_item in enumerate(ebay_items):
        item_id = ebay_item['item_id']
        title = ebay_item['title']
        listed_date = ebay_item['listed_date']
        date_sold = ebay_item['date_sold']
        price = ebay_item['price']
        item_url = ebay_item['item_url']
        image_url = ebay_item['image_url']
        location = ebay_item['location']
        status = ebay_item['status']

        # Deletes ebay item if exists
        cur.execute(f"""
        DELETE FROM items WHERE item_id={item_id}
        """)

        cur.execute(f"""
        INSERT INTO items VALUES ({item_id}, '{title}', '{listed_date}', '{datetime.now()}', NULL, {price}, '{item_url}', '{image_url}', '{location}', '{status}', {store_id});
        """)
        print(f"Inserted {index+1} / {len(ebay_items)} into items database. item id: {item_id}")

    print(f"Finished inserting {len(ebay_items)} into database.")  

    # Ebay glitch where some items aren't updated but they weren't sold. Double check these items to see if they sold or not.
    # areSoldItems() returns a hashMap instead of boolean because I didn't want to waste api calls to ebay api.
    res = cur.execute(f"""
    SELECT item_id FROM items WHERE date_last_updated<'{cur_updated_time}' and store_id={store_id} and status="Active"
    """)
    res = [item_id[0] for item_id in res.fetchall()]
    sold_items_map = areSoldItems(res)
    if sold_items_map:
        for ebay_id, bool_val in sold_items_map.items():
            if bool_val:
                # Update items that weren't updated recently, into "sold" status.
                date_sold = bool_val.replace("Z", "")
                print(f"Ebay Item: {ebay_id} sold on {date_sold}")
                cur.execute(f"""
                UPDATE items 
                SET status="Sold", date_sold="{date_sold}"
                WHERE item_id={ebay_id} and store_id={store_id}
                """)

    con.commit()
    con.close()

def dailyUpdateAllStores():
    # Grabs all stores from database and runs dailyUpdateDatabaseFromEbay() on all stores.
    con = sqlite3.connect(DATABASE)
    cur = con.cursor()
    
    res = cur.execute("""
    SELECT * FROM stores;
    """)

    stores = res.fetchall()

    for store_number, store in stores:
        print(f"{store_number}/{len(stores)}: Running daily update on {store}")
        dailyUpdateDatabaseFromEbay(store)


if __name__ == "__main__":
    dailyUpdateAllStores()
    # dailyUpdateDatabaseFromEbay("Basset Auto Wreckers")
    # dailyUpdateDatabaseFromEbay("PARTS THAT FIT LLC")
    # dailyUpdateDatabaseFromEbay("M&amp;M Auto Parts, Inc.")