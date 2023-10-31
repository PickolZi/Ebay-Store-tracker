# Anything that calls the ebay API will be held in this file.
import requests
import json

from xmlToJson import xmlToJsonParser


# Load ebay API keys from SECRETS.json
with open("../SECRETS.json", "r") as f:
    cred = json.load(f)

all_item_ids = []
EBAY_GET_ITEMS_ENDPOINT = "https://svcs.ebay.com/services/search/FindingService/v1"  # Returns in XML format because using old finding API.
headers = {
        "X-EBAY-SOA-SECURITY-APPNAME": cred['appid'],
        "X-EBAY-SOA-OPERATION-NAME": None
    }


def pretty_print_json(json_data):
    print(json.dumps(json_data, indent=5))


def getAllEbayDataFromStores(store, page=1, output=[]):
    # Gets all items an ebay store seller has.
    # params: store => ebay store name.
    # Returns list of json of ebay item data
    headers["X-EBAY-SOA-OPERATION-NAME"] = "findItemsIneBayStores"

    body = f"""<?xml version="1.0" encoding="UTF-8"?>
    <findItemsIneBayStoresRequest xmlns="http://www.ebay.com/marketplace/search/v1/services">
        <storeName>{store}</storeName>
        <outputSelector>StoreInfo</outputSelector>
        <paginationInput>
            <entriesPerPage>100</entriesPerPage>
            <pageNumber>{page}</pageNumber>
        </paginationInput>
    </findItemsIneBayStoresRequest>
    """
    response = requests.post(EBAY_GET_ITEMS_ENDPOINT, data=body, headers=headers)
    json_data = xmlToJsonParser(response.text)

    num_of_pages = int(json_data['findItemsIneBayStoresResponse']['paginationOutput']['totalPages'])

    if page > num_of_pages:
        return output

    ebay_items = json_data['findItemsIneBayStoresResponse']['searchResult']['item']
    for item in ebay_items:
        item_id = item['itemId']
        title = item['title']
        listed_date = item['listingInfo']['startTime'].replace("T", " ")[:-1]
        price = item['sellingStatus']['currentPrice']['#text']
        item_url = item['viewItemURL']
        image_url = item['galleryURL'].replace('l140', 'l1600')
        location = item['location']
        status = item['sellingStatus']['sellingState']

        output.append({
            'item_id': item_id,
            'title': title,
            'listed_date': listed_date,
            'price': price,
            'item_url': item_url,
            'image_url': image_url,
            'location': location,
            'status': status
        })

    # print(item_url)
    # return
    print(f"Got page {page} / {num_of_pages} from ebay API")

    if page < 100:
        getAllEbayDataFromStores(store, page=page+1, output=output)   

    return output

def isValidStore(store):
    # Given the store name, return if it's a valid store name on ebay or not.
    # params: store => String
    # return: Boolean
    headers["X-EBAY-SOA-OPERATION-NAME"] = "findItemsIneBayStores"

    body = f"""<?xml version="1.0" encoding="UTF-8"?>
    <findItemsIneBayStoresRequest xmlns="http://www.ebay.com/marketplace/search/v1/services">
        <storeName>{store}</storeName>
        <outputSelector>StoreInfo</outputSelector>
        <paginationInput>
            <entriesPerPage>1</entriesPerPage>
        </paginationInput>
    </findItemsIneBayStoresRequest>
    """
    response = requests.post(EBAY_GET_ITEMS_ENDPOINT, data=body, headers=headers)
    json_data = xmlToJsonParser(response.text)

    status = json_data['findItemsIneBayStoresResponse']['ack']
    return status == "Success"



if __name__ == "__main__":
    # ebayItems = getAllEbayDataFromStores("Basset Auto Wreckers")
    print(isValidStore("PARTS THAT FIT LLC"))
    # print(ebayItems)
    # print(len(ebayItems))
    # pass
