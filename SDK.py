import requests
from requests.auth import HTTPBasicAuth
import json

def getJSONDetail():
    try:
        r = requests.get('http://108.59.217.3:54321/api/listings/?limit=10', auth=HTTPBasicAuth('user', 'craigslist'))
        return json.loads(r.content)
    except Exception as e:
        print str(e)
        print("Something went wrong. You sure you did it right?")


def getCl_Item_IDList():
    r = requests.get('http://localhost:54321/api/listings/idlist', auth=HTTPBasicAuth('user', 'craigslist'))
    return json.loads(r.content)

def rehydrateListing(CL_Item_ID):
    r = requests.get('http://108.59.217.3:54321/api/listings/?CL')


# json_data = getJSONDetail()
# print(json_data)
CL_Item_IDs = getCl_Item_IDList()
print CL_Item_IDs







