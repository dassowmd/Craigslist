import requests
from requests.auth import HTTPBasicAuth
import json

def getJSONDetail(url='http://108.59.217.3:54321/api/listings/idlist/?format=json&limit=0&offset=100'):
    try:
        r = requests.get(url, auth=HTTPBasicAuth('user', 'craigslist'))
        return json.loads(r.content)
    except Exception as e:
        print str(e)
        print("Something went wrong. You sure you did it right?")


def getCl_Item_IDList(url):
    r = requests.get(url, auth=HTTPBasicAuth('user', 'craigslist'))
    return json.loads(r.content)

def rehydrateListing(CL_Item_ID):
    r = requests.get('http://108.59.217.3:54321/api/listings/?CL')

def getAllIDs():
    url = 'http://108.59.217.3:54321/api/listings/idlist'
    CL_Item_IDs = getCl_Item_IDList(url)
    IDs =[]
    print CL_Item_IDs['results']
    IDs.append(CL_Item_IDs['results'])
    while CL_Item_IDs['next'] != None:
        url = CL_Item_IDs['next']
        CL_Item_IDs = getCl_Item_IDList(url)
        print CL_Item_IDs['results']
        IDs.append(CL_Item_IDs['results'])
    return IDs

def getAllDetails(url = 'http://108.59.217.3:54321/api/listings/idlist/?format=json&limit=0&offset=100'):
    JSON_Results = getJSONDetail(url)
    Detail_Items = JSON_Results['results']
    Items = []
    Items.append(Detail_Items)
    while url != None:
        JSON_Results = getJSONDetail(url)
        Items.append(Detail_Items)
        Detail_Items = JSON_Results['results']
        url = JSON_Results['next']
    return Items

# json_data = getJSONDetail()
# print(json_data)
url = 'http://108.59.217.3:54321/api/listings/idlist/?format=json&limit=0&offset=100'
results = getAllDetails(url)
print results







