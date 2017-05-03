import requests
from requests.auth import HTTPBasicAuth
import json
import csv
from multiprocessing.pool import ThreadPool
import pandas as pd
import datetime
from Flatten_Postings import flatten

def getJSONDetail(url):
    try:
        r = requests.get(url, auth=HTTPBasicAuth('user', 'craigslist'))
        print str(datetime.datetime.now()) + url
        return json.loads(r.content)
    except Exception as e:
        print str(e)
        # print("Something went wrong. You sure you did it right?")


def getCl_Item_IDList(url):
    r = requests.get(url, auth=HTTPBasicAuth('user', 'craigslist'))
    return json.loads(r.content)

# def rehydrateListing(CL_Item_ID):
#     r = requests.get('http://108.59.217.3:54321/api/listings/?CL')

def getAllIDs(url = 'http://108.59.216.215:54321/api/listings/idlist'):
    url = 'http://192.168.1.138:54321/api/listings/idlist'
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
    for i in range(1, count/100):
    # for i in range(1, 100):
        url = 'http://108.59.216.215:54321/api/listings/?format=json&limit=100&offset=' + str(i * 100)
        url = 'http://192.168.1.138:54321/api/listings/?format=json&limit=100&offset=' + str(i * 100)
        URL_list.append(url)

   # Iterate through U+
    # RL list
    Items = []
    pool = ThreadPool(40)
    results = pool.map(getJSONDetail, URL_list)
    for i in results:
        for r in i['results']:
            Items.append(r)
    pool.close()
    pool.join()

    Items_df = pd.DataFrame(Items)

    # while url != None:
    #     JSON_Results = getJSONDetail(url)
    #     Items.append(JSON_Results['results'])
    #     url = JSON_Results['next']

    return Items_df

def getCount(url):
    JSON_Results = getJSONDetail(url)
    count = JSON_Results['count']
    return count

# json_data = getJSONDetail()
# print(json_data)
url = 'http://108.59.216.215:54321/api/listings/?format=json&limit=100'
url = 'http://192.168.1.138:54321/api/listings/?format=json&limit=100'

results = getAllDetails(url)
saveFilePath = 'C:\Users\dasso\OneDrive\Documents\GitHub\Craigslist'
fullPath = saveFilePath + '/CraigslistPosting.csv'
print "Saving results to %s" % fullPath
results.to_csv(fullPath, encoding='utf8')
print results







