# Functions used to propogate database using ebay's api calls will be called here
import sqlite3
from datetime import datetime, timedelta

from ebay_api import getAllEbayDataFromStores, isValidStore, pretty_print_json

DATABASE = "../instance/db.sqlite3"

def getIdFromStoreName(store):
    # Find the store id given the store name
    # params: store => string from stores database
    # returns: int => id from database.
    sql_query = f"""
    SELECT id from stores where name="{store}";
    """

    if not isValidStore(store):
        return -1

    con = sqlite3.connect(DATABASE)
    cur = con.cursor()

    res = cur.execute(sql_query)
    id = res.fetchone()[0]

    con.close()
    return id

def dailyUpdateDatabaseFromEbay(store):
    # Will be ran once a day.
    # Calls getAllEbayDataFromStores() and gets every ebay item from a store and updates it to current database. If item already exists or there's a new item being added, the 'date_last_updated' date will be updated. However, this means, old items that aren't coming from the api call will not be updated. This mean the item was taken down or sold.
    # params: store => String of ebay store id. From stores table.
    # Returns: Nothing. Updates database.

    if not isValidStore(store):
        return -1

    ebay_items = getAllEbayDataFromStores(store)
    store_id = getIdFromStoreName(store)

    # Connecting to database.
    con = sqlite3.connect(DATABASE)
    cur = con.cursor()

    cur_updated_time = datetime.now() - timedelta(minutes=10)

    for index, ebay_item in enumerate(ebay_items):
        item_id = ebay_item['item_id']
        title = ebay_item['title'].replace("'", "")
        listed_date = ebay_item['listed_date']
        price = ebay_item['price']
        item_url = ebay_item['item_url']
        image_url = ebay_item['image_url']
        location = ebay_item['location'].replace("'", "")
        status = ebay_item['status']

        # Deletes ebay item if exists
        cur.execute(f"""
        DELETE FROM items WHERE item_id={item_id}
        """)

        sql_query = f"""
        INSERT INTO items
VALUES ({item_id}, '{title}', '{listed_date}', '{datetime.now()}', {price}, '{item_url}', '{image_url}', '{location}', '{status}', {store_id});
        """
        cur.execute(sql_query)
        print(f"Inserted {index+1} / {len(ebay_items)} into items database. item id: {item_id}")
        # print(sql_query)  # For debugging 
        # print()  
    print(f"Finished inserting {len(ebay_items)} into database.")  

    # Update items that weren't updated recently, into "sold" status.
    cur.execute(f"""
    UPDATE items 
    SET status="Sold"
    WHERE date_last_updated<'{cur_updated_time} and store={store_id}'
    """)

    con.commit()
    con.close()

def updateSpecificPartFromEbayItems(store, attributes=[]):
    # Calls getAllEbayDataFromStores() and will update attributes of the ebay item provided by the arguments. Will not update date_last_updated unless specified.
    # params: [Strings] list of strings. Strings will be the attribute name of the items table to be updated.
    # Return nothing. Updated database. 

    sample_attributes = ['item_id', 'title', 'listed_date', 'date_last_updated', 'price', 'item_url', 'image_url', 'location', 'status', 'store_id']

    if attributes == []:  # If empty, return.
        print("empty attributes, please add database items attributes to attributes list.")
        return -1

    for attribute in attributes:  # If any of the arguments are not in the verified sample attributes, exit.
        if attribute not in sample_attributes:
            print(f"Attribute: {attribute} not in sample_attributes list.")
            return -1

    # Connecting to database.
    con = sqlite3.connect(DATABASE)
    cur = con.cursor()

    ebay_items = getAllEbayDataFromStores(store)

    for index, ebay_item in enumerate(ebay_items):
        item_id = ebay_item['item_id']
        title = ebay_item['title']
        listed_date = ebay_item['listed_date']
        price = ebay_item['price']
        item_url = ebay_item['item_url']
        image_url = ebay_item['image_url']
        location = ebay_item['location']
        status = ebay_item['status']

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