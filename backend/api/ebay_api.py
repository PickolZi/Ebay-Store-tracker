# Anything that calls the ebay API will be held in this file.
import requests
import json

from xmlToJson import xmlToJsonParser


# Load ebay API keys from SECRETS.json
with open("../SECRETS.json", "r") as f:
    cred = json.load(f)

EBAY_GET_ITEMS_ENDPOINT = "https://svcs.ebay.com/services/search/FindingService/v1"  # Returns in XML format because using old finding API.
EBAY_SHOPPING_GET_ITEMS_ENDPOINT = "https://open.api.ebay.com/shopping"
headers = {
        "X-EBAY-SOA-SECURITY-APPNAME": cred['appid'],
        "X-EBAY-SOA-OPERATION-NAME": None
    }


def pretty_print_json(json_data):
    print(json.dumps(json_data, indent=5))


def getAllEbayDataFromStores(store, page=1, output=[], minPrice=None, maxPrice=None):
    # Gets all items an ebay store seller has.
    # params: store => ebay store name.
    # Returns list of json of ebay item data

    if page==1:
        output.clear()

    if not isValidStore(store):
        return False

    headers["X-EBAY-SOA-OPERATION-NAME"] = "findItemsIneBayStores"

    body = f"""<?xml version="1.0" encoding="UTF-8"?>
    <findItemsIneBayStoresRequest xmlns="http://www.ebay.com/marketplace/search/v1/services">
        <storeName>{store}</storeName>
        <outputSelector>StoreInfo</outputSelector>"""
    
    if minPrice:
        body += f"""
        <itemFilter>
            <name>MinPrice</name>
            <value>{minPrice}</value>
            <paramName>Currency</paramName>
            <paramValue>USD</paramValue>
        </itemFilter>
        """

    if maxPrice:
        body += f"""
        <itemFilter>
            <name>MaxPrice</name>
            <value>{maxPrice}</value>
            <paramName>Currency</paramName>
            <paramValue>USD</paramValue>
        </itemFilter>
        """

    body += f"""<paginationInput>
            <entriesPerPage>100</entriesPerPage>
            <pageNumber>{page}</pageNumber>
        </paginationInput>
    </findItemsIneBayStoresRequest>
    """
    response = requests.post(EBAY_GET_ITEMS_ENDPOINT, data=body, headers=headers)
    json_data = xmlToJsonParser(response.text)

    num_of_pages = int(json_data['findItemsIneBayStoresResponse']['paginationOutput']['totalPages'])

    try:
        ebay_items = json_data['findItemsIneBayStoresResponse']['searchResult']['item']
        for item in ebay_items:
            item_id = item['itemId']
            title = item['title'].replace("'", "")
            listed_date = item['listingInfo']['startTime'].replace("T", " ")[:-1]
            price = item['sellingStatus']['currentPrice']['#text']
            item_url = item['viewItemURL']
            image_url = item['galleryURL'].replace('l140', 'l1600')
            location = item['location'].replace("'", "")
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
        print(f"Got page {page} / {num_of_pages} from ebay API")
    except TypeError:
        print(json_data)
        print("Error with the response from ebay api?")
        input("Pausing....")


    if page == num_of_pages or page == 100:
        return output

    getAllEbayDataFromStores(store, page=page+1, output=output, minPrice=minPrice, maxPrice=maxPrice)
    return output[:]

def areSoldItems(total_ebay_ids):
    # Given the ebay item ids, return if the item has been sold/completed.
    # params: ebay_id => [int]
    # returns: dictionary with the key being the ids and values being booleans.
    results = {}

    # API request
    headers["X-EBAY-API-IAF-TOKEN"] = f"Bearer {cred['userToken']}"
    headers["X-EBAY-API-SITE-ID"] = "0"
    headers["X-EBAY-API-CALL-NAME"] = "GetItemStatus"
    headers["X-EBAY-API-VERSION"] = "863"
    headers["X-EBAY-API-REQUEST-ENCODING"] = "xml"

    quotient = len(total_ebay_ids) // 20
    remainder = len(total_ebay_ids) % 20
    print(f"Calling API {quotient+1} times to see which items need to be removed...")
    for i in range(quotient+1):
        ebay_ids = total_ebay_ids[i*20:(i+1)*20]  # Can only do API calls in batches of 20
        if i == quotient:
            ebay_ids = total_ebay_ids[i*20:]

        body = f"""<?xml version="1.0" encoding="utf-8"?>
        <GetItemStatusRequest xmlns="urn:ebay:apis:eBLBaseComponents">"""

        for ebay_id in ebay_ids:
            body+= f"<ItemID>{ebay_id}</ItemID>"

        body += "</GetItemStatusRequest>"

        response = requests.post(EBAY_SHOPPING_GET_ITEMS_ENDPOINT, data=body, headers=headers)
        json_data = xmlToJsonParser(response.text)["GetItemStatusResponse"]
        # Handling Errors
        RESPONSE_CODES = ["Success", "PartialFailure", "Failure"]
        SERVER_RESPONSE_CODE = json_data["Ack"]

        if SERVER_RESPONSE_CODE == RESPONSE_CODES[2]:
            print("Failed to retrieve any sold ebay items.")
            return False
        elif SERVER_RESPONSE_CODE == RESPONSE_CODES[1]:
            error_items = json_data["Errors"]["ErrorParameters"]["Value"].split(",")
            results["Failures"] = error_items
            print("Error when trying to find these ebay items:", error_items)

        ebay_items = json_data["Item"]
        if type(ebay_items) == dict:
            ebay_items = [ebay_items]

        # Key, Value: ebay id, boolean
        for ebay_item in ebay_items:
            item_id = ebay_item['ItemID']
            status = ebay_item['ListingStatus']

            results[item_id] = (status != "Active")

    return results


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
    # ebayItems = getAllEbayDataFromStores("Basset Auto Wreckers", minPrice=50)

    x = [295778007334, 293691222982, 295705847685, 293582067774, 295459132336, 295464479330, 295478218835, 292727410224, 304804608243, 295791717743, 293120981956, 292713027082, 304500674113, 305214724014, 295705848289, 295329815173, 303477230115, 292713029569, 305124992789, 304792061331, 294279016350, 305078758459, 293567361848, 293792614665, 294749552524, 303968684831, 304973884654, 303908610702, 295025220445, 292745732411, 304902130710, 295646269195, 302871738062, 303561012266, 304129675761, 303795842298, 304903784487, 295961818315, 294227051986, 304201244737, 304736576101, 304379008928, 295453761114, 304698535151, 295704837569, 304834615878, 295900176773, 292732126285, 303252154280, 295089282585, 305004819413, 304924057588, 304229165193, 294029830457, 304829658454, 293957015254, 295555457840, 304897053580, 295743731292, 304944751849, 292943552901, 295567199095, 304758480640, 304914935097, 304813455855, 302932605797, 302883362428, 293721343139, 293995676248, 295038220376, 304959603170, 304555601837, 304140435740, 295769749473]

    pretty_print_json(areSoldItems(x))

    # print(isValidStore("PARTS THAT FIT LLC"))
    # for ebayItem in ebayItems:
    #     pretty_print_json(ebayItem)
    # print("Total Items:", len(ebayItems))
    pass
