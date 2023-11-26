# Anything that calls the ebay API will be held in this file.
import requests
import json
import os
import base64

from xmlToJson import xmlToJsonParser


SECRETS_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "SECRETS.json"))
# Load ebay API keys from SECRETS.json
with open(SECRETS_PATH, "r") as f:
    cred = json.load(f)

EBAY_GET_ITEMS_ENDPOINT = "https://svcs.ebay.com/services/search/FindingService/v1" 
EBAY_SHOPPING_GET_ITEMS_ENDPOINT = "https://open.api.ebay.com/shopping"
headers = {
        "X-EBAY-SOA-SECURITY-APPNAME": cred['appid'],
        "X-EBAY-SOA-OPERATION-NAME": None
    }

global_page_counter = 0

def pretty_print_json(json_data):
    print(json.dumps(json_data, indent=5))

def generateBodyForGetEbayDataFromStore(store, minPrice, maxPrice, pageNum=1):
    # Returns body string that will be passed to API request.
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
            <pageNumber>{pageNum}</pageNumber>
        </paginationInput>
    </findItemsIneBayStoresRequest>
    """
    return body

def addEbayItemToList(ebay_items, output_list):
    # Given ebay_items, add each ebay item to the output_list.
    # Params: ebay_items => ebay items from ebay API XML. 
    # Params: output_list => [dict] 
    # return: output_list => [dict] => List of dictionary objects that represents each ebay item along with its attributes.
    for item in ebay_items:
        try:
            item_id = item['itemId']
            title = item['title'].replace("'", "")
            listed_date = item['listingInfo']['startTime'].replace("T", " ")[:-1]
            date_sold = ""
            price = item['sellingStatus']['currentPrice']['#text']
            item_url = item['viewItemURL']
            image_url = item['galleryURL'].replace('l140', 'l1600') if item.get('galleryURL') else "N/A"
            location = item['location'].replace("'", "")
            status = item['sellingStatus']['sellingState']

            output_list.append({
                'item_id': item_id,
                'title': title,
                'listed_date': listed_date,
                'date_sold': date_sold,
                'price': price,
                'item_url': item_url,
                'image_url': image_url,
                'location': location,
                'status': status
            })

        except Exception:
            print("Item failed to be added.")
            continue
    return output_list

def responseFromGettingAllEbayData(store, body, headers):
    # Sends a request to Ebay API and turns the response from XML to JSON.
    response = requests.post(EBAY_GET_ITEMS_ENDPOINT, data=body, headers=headers)
    json_data = xmlToJsonParser(response.text)

    # Error handling.
    if json_data["findItemsIneBayStoresResponse"]["ack"] != "Success":
        print(f"Something went wrong when trying to get all ebay data from store: {store}")
        print("Exiting...")
        print(json_data)
        return False
    return json_data

def loadEbayItemsWithinRange(store, headers, minPrice, maxPrice, output):
    # Loads all ebay items into output list within minPrice and maxPrice
    # Given a minPrice and maxPrice, add all the ebay items within that range to the output list.
    # Returns: output => [dict] => list of ebay item attributes in a dictionary.

    json_data = responseFromGettingAllEbayData(store, generateBodyForGetEbayDataFromStore(store, minPrice, maxPrice, pageNum=1), headers)

    total_entries = int(json_data['findItemsIneBayStoresResponse']['paginationOutput']['totalEntries'])
    cur_page = int(json_data['findItemsIneBayStoresResponse']['paginationOutput']['pageNumber'])
    num_of_pages = int(json_data['findItemsIneBayStoresResponse']['paginationOutput']['totalPages'])
    
    # print(f"minPrice: {minPrice}, maxPrice: {maxPrice}")
    # print(f"total_entries: {total_entries}")
    # print(f"cur_page: {cur_page}")
    # print(f"num_of_pages: {num_of_pages}")
    # return

    for page in range(num_of_pages):
        if page+1 > 100:
            print(f"{store}: Page is greater than 100. Reconfigure EBAY_TOTAL_ITEMS_RANGE to have more ranges. ")
            break
        json_data = responseFromGettingAllEbayData(store, generateBodyForGetEbayDataFromStore(store, minPrice, maxPrice, pageNum=page+1), headers)
        # Calls function that picks apart item attiributes for up to 100 ebay items and adds to output list.
        ebay_items = json_data['findItemsIneBayStoresResponse']['searchResult']['item']
        addEbayItemToList(ebay_items, output)

        global global_page_counter
        global_page_counter += 1
        print(f"Finished loading page #{global_page_counter}")
        
def getAllEbayDataFromStores(store):
    # Gets all items an ebay store seller has.
    # params: store => ebay store name.
    # Returns list of json of ebay item data

    if not isValidStore(store):
        return False

    headers["X-EBAY-SOA-OPERATION-NAME"] = "findItemsIneBayStores"
    body = generateBodyForGetEbayDataFromStore(store, 0, 20000)
    json_data = responseFromGettingAllEbayData(store, body, headers)

    output = []
    total_entries = int(json_data['findItemsIneBayStoresResponse']['paginationOutput']['totalEntries'])
    cur_page = int(json_data['findItemsIneBayStoresResponse']['paginationOutput']['pageNumber'])
    num_of_pages = int(json_data['findItemsIneBayStoresResponse']['paginationOutput']['totalPages'])

    # print(f"total_entries: {total_entries}")
    # print(f"cur_page: {cur_page}")
    # print(f"num_of_pages: {num_of_pages}")
    # return

    # List of tuples. Representing minPrice and maxPrice that loadEbayItemsWithinRange() function will use.
    EBAY_TOTAL_ITEMS_RANGE = {
        # Under 10k items
        "SMALL_RANGE": [(0,20000)],  
        # Under 20k items
        "MEDIUM_RANGE": [(0, 49.99), (50, 99.99), (100, 20000)],
        # Above 20k items
        "LARGE_RANGE": [(0,49.99),(50, 99.99),(100, 149.99),(150, 169.99),(170, 189.99),(190, 199.99),(200, 224.99),(225, 249.99),(250, 299.99),(300, 499.99),(500, 999.99),(1000, 1999.99), (2000, 20000)]
    }
    
    if total_entries < 10000:
        RANGE = EBAY_TOTAL_ITEMS_RANGE["SMALL_RANGE"]
    elif total_entries <= 20000:
        RANGE = EBAY_TOTAL_ITEMS_RANGE["MEDIUM_RANGE"]
    else:
        RANGE = EBAY_TOTAL_ITEMS_RANGE["LARGE_RANGE"]

    for price in RANGE:
        minPrice = price[0]
        maxPrice = price[1]
        loadEbayItemsWithinRange(store, headers, minPrice, maxPrice, output)

    # for ebay_item in output:
    #     pretty_print_json(ebay_item)

    print(f"#of items pulled from ebay api: {len(output)}")
    return output

def areSoldItems(total_ebay_ids):
    # Given a list of ebay item ids, return if the item has been sold/completed.
    # params: total_ebay_ids => [int]
    # returns: dictionary with the key being the ids and values being sold date if True, or False.
    results = {}

    # API request headers
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
            pretty_print_json(json_data)
            SERVER_ERROR_SHORT_MESSAGE = json_data["Errors"]["ShortMessage"]
            if SERVER_ERROR_SHORT_MESSAGE == "Invalid token.":
                print("Token is invalid. Please try using another application token.")
            else:
                print("All ebay item ids were invalid.")
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

            if status != "Active":
                sold_date = ebay_item['EndTime']
                results[item_id] = sold_date    
            else:
                results[item_id] = False

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

def generateApplicationAccessToken():
    # A lot easier than generating a user refresh/access token because doesn't require the user to signin.
    # https://developer.ebay.com/api-docs/static/oauth-client-credentials-grant.html
    # Uses 1) Endpoint 2) Headers 3) Body in order to create a new access token that lasts 2 hours.
    authorization_string = f"{cred['appid']}:{cred['certid']}"  # Gets the client_id:client_secret
    authorization_string = authorization_string.encode("ascii")  # Encodes in ascii
    authorization_string = base64.b64encode(authorization_string)  # Uses base64 to encode 
    authorization_string = authorization_string.decode("ascii")  # Decodes in ascii

    TOKEN_ENDPOINT = "https://api.ebay.com/identity/v1/oauth2/token"
    HEADERS = {
        "Content-Type": "application/x-www-form-urlencoded",
        "Authorization": f"Basic {authorization_string}"
    }
    BODY = {
        "grant_type": "client_credentials",
        "scope": "https://api.ebay.com/oauth/api_scope"
    }
    res = requests.post(TOKEN_ENDPOINT, headers=HEADERS, data=BODY)
    json_data = json.loads(res.text)
    access_token = json_data.get("access_token")

    if access_token:
        cred['userToken'] = access_token
        headers['Authorization'] = access_token
    else:
        print("Failed to get access token. Investigate further...")
        return False


generateApplicationAccessToken()  # Generates application access key.
if __name__ == "__main__":
    # ebayItems = getAllEbayDataFromStores("Basset Auto Wreckers")
    # ebayItems = getAllEbayDataFromStores("PARTS THAT FIT LLC")
    # ebayItems = getAllEbayDataFromStores("M&amp;M Auto Parts, Inc.")
    # print(ebayItems)

    x = [295778007334, 293691222982, 295705847685, 293582067774, 295459132336, 295464479330, 295478218835, 292727410224, 304804608243, 295791717743, 293120981956, 292713027082, 304500674113, 305214724014, 295705848289, 295329815173, 303477230115, 292713029569, 305124992789, 304792061331, 294279016350, 305078758459, 293567361848, 293792614665, 294749552524, 303968684831, 304973884654, 303908610702, 295025220445, 292745732411, 304902130710, 295646269195, 302871738062, 303561012266, 304129675761, 303795842298, 304903784487, 295961818315, 294227051986, 304201244737, 304736576101, 304379008928, 295453761114, 304698535151, 295704837569, 304834615878, 295900176773, 292732126285, 303252154280, 295089282585, 305004819413, 304924057588, 304229165193, 294029830457, 304829658454, 293957015254, 295555457840, 304897053580, 295743731292, 304944751849, 292943552901, 295567199095, 304758480640, 304914935097, 304813455855, 302932605797, 302883362428, 293721343139, 293995676248, 295038220376, 304959603170, 304555601837, 304140435740, 295769749473]

    # True, True, False, False, N/A, N/A
    y = [304758480640, 302932605797, 304959603170, 304555601837, 38290138190, 890458309]
    # pretty_print_json(areSoldItems(x))
    # pretty_print_json(areSoldItems(y))