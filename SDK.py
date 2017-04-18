import requests
from requests.auth import HTTPBasicAuth
import json
import csv
from multiprocessing.pool import ThreadPool

def getJSONDetail(url):
    try:
        r = requests.get(url, auth=HTTPBasicAuth('user', 'craigslist'))
        print url
        return json.loads(r.content)
    except Exception as e:
        print str(e)
        print("Something went wrong. You sure you did it right?")


def getCl_Item_IDList(url):
    r = requests.get(url, auth=HTTPBasicAuth('user', 'craigslist'))
    return json.loads(r.content)

# def rehydrateListing(CL_Item_ID):
#     r = requests.get('http://108.59.217.3:54321/api/listings/?CL')

def getAllIDs(url = 'http://108.59.217.3:54321/api/listings/idlist'):
    CL_Item_IDs = getCl_Item_IDList(url)
    IDs =[]
    while url != None:
        CL_Item_IDs = getCl_Item_IDList(url)
        IDs.append(CL_Item_IDs['results'])
        url = CL_Item_IDs['next']
    return IDs

def getAllDetails(url):
    count = getCount(url)

    # Create list of URLs to query
    URL_list = []
    # for i in range(1, count/100):
    for i in range(1, 5):
        url = 'http://108.59.217.3:54321/api/listings/?format=json&limit=100&offset=' + str(i * 100)
        URL_list.append(url)

   # Iterate through URL list
    pool = ThreadPool(40)
    pool.map(getJSONDetail, URL_list)
    Items = []
    while url != None:
        JSON_Results = getJSONDetail(url)
        Items.append(JSON_Results['results'])
        url = JSON_Results['next']

    return Items

def getCount(url):
    JSON_Results = getJSONDetail(url)
    count = JSON_Results['count']
    return count

# json_data = getJSONDetail()
# print(json_data)
url = 'http://108.59.217.3:54321/api/listings/?format=json&limit=100'
results = getAllDetails(url)
saveFilePath = raw_input("Where would you like to save the file? (Include full file path. File name will be CraigslistPosting.csv) \n")
fullPath = saveFilePath + '/CraigslistPosting.csv'
with open(fullPath, 'wb') as csvfile:
    writer = csv.writer(csvfile, delimiter=',',
                            quotechar='|', quoting=csv.QUOTE_MINIMAL)
print results







