# Functions used to propogate database using ebay's api calls will be called here
import sqlite3
from datetime import datetime, timedelta

from ebay_api import getAllEbayDataFromStores, isValidStore, areSoldItems, pretty_print_json

DATABASE = "../instance/db.sqlite3"

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
    ebay_items = []
    ebay_items.extend(getAllEbayDataFromStores(store, maxPrice=49.99))
    ebay_items.extend(getAllEbayDataFromStores(store, minPrice=50))

    # Connecting to database.
    con = sqlite3.connect(DATABASE)
    cur = con.cursor()

    cur_updated_time = datetime.now() - timedelta(minutes=2)

    for index, ebay_item in enumerate(ebay_items):
        item_id = ebay_item['item_id']
        title = ebay_item['title']
        listed_date = ebay_item['listed_date']
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
        INSERT INTO items VALUES ({item_id}, '{title}', '{listed_date}', '{datetime.now()}', {price}, '{item_url}', '{image_url}', '{location}', '{status}', {store_id});
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
                cur.execute(f"""
                UPDATE items 
                SET status="Sold"
                WHERE item_id={ebay_id} and store_id={store_id}
                """)

    con.commit()
    con.close()

def updateSpecificPartFromEbayItems(store, attributes=[]):
    # Calls getAllEbayDataFromStores() and will update attributes of the ebay item provided by the arguments. Will not update date_last_updated unless specified.
    # params: attributes => [Strings] list of strings. Strings will be the attribute name of the items table to be updated.
    # Return nothing. Updates database. 

    sample_attributes = ['item_id', 'title', 'listed_date', 'date_last_updated', 'price', 'item_url', 'image_url', 'location', 'status', 'store_id']

    if not attributes:
        print("empty attributes, please add database items attributes to attributes list.")
        return False

    for attribute in attributes:
        if attribute not in sample_attributes:
            print(f"Attribute: {attribute} not in sample_attributes list.")
            return False

    # Connecting to database.
    con = sqlite3.connect(DATABASE)
    cur = con.cursor()

    ebay_items = getAllEbayDataFromStores(store)

    for index, ebay_item in enumerate(ebay_items):
        sql_query = "UPDATE items SET "

        for attribute in attributes:
            if attribute in ['title', 'listed_date', 'item_url', 'image_url', 'location', 'status']:  # If datatype is string, add quotes around.
                sql_query += f"{attribute}='{ebay_item[attribute]}' "
            else:
                sql_query += f"{attribute}={ebay_item[attribute]} "
            
        sql_query += f"WHERE item_id={item_id}"
        cur.execute(sql_query)
        print(f"Updated item {index+1} / {len(ebay_items)}. Item ID: {item_id}")

    con.commit()
    con.close()
    print(f"Finished updating {len(ebay_items)} items.")


if __name__ == "__main__":
    dailyUpdateDatabaseFromEbay("PARTS THAT FIT LLC")
    # dailyUpdateDatabaseFromEbay("Basset Auto Wreckers")
    # print(getIdFromStoreName("PARTS THAT FIT LLC"))
    # updateSpecificPartFromEbayItems("Basset Auto Wreckers", ['item_url'])
    # print(datetime.now())
    # pass