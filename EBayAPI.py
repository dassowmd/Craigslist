import datetime
from ebaysdk.exception import ConnectionError
from ebaysdk.finding import Connection
import pandas as pd
import json
import csv
import responses
from lxml import objectify
from bs4 import BeautifulSoup
import multiprocessing
from multiprocessing import freeze_support
from multiprocessing.pool import ThreadPool
from datetime import datetime, timedelta

import requests
from requests.auth import HTTPBasicAuth
from collections import OrderedDict

def flatten(json_object, container=None, name=''):
    if container is None:
        container = OrderedDict()
    if isinstance(json_object, dict):
        for key in json_object:
            flatten(json_object[key], container=container, name=name + key + '_')
    elif isinstance(json_object, list):
        for n, item in enumerate(json_object, 1):
            flatten(item, container=container, name=name + str(n) + '_')
    else:
        container[str(name[:-1])] = str(json_object)
    return container

def post_JSON_API(dictionary):
    flat_dict = flatten(dictionary)
    item_ID = flat_dict['itemId']
    try:
        for key, value in flat_dict.iteritems():
            print item_ID.encode('utf-8') + "-" + key.encode('utf-8') + ":" + value.encode('utf-8')
            JSON_data = {
            "Cl_Item_ID":str(item_ID).encode('utf-8'),
            "KeyParam": str(key).encode('utf-8'),
            "ValueParam": str(value).encode('utf-8')[0:20000],
            "ScrapedDateTime": str(datetime.now()).encode('utf-8'),
            "RSS_Feed_String": str(search_Keywords).encode('utf-8'),
            }

            try:
                r = requests.post('http://108.59.216.215:54321/api/listings/create/', auth=HTTPBasicAuth('user', 'craigslist'), json=JSON_data)
                if r.status_code != 201:
                    raw_input("pause")
                # r = requests.post('http://192.168.2.2:54321/api/listings/create/', auth=HTTPBasicAuth('user', 'craigslist'), json=JSON_data)

            except Exception as e:
                print e
                # print r.status_code
                print("Could not save via JSON API. Did you check the IP Address and Port Forwarding?")
                pass
    except Exception as e:
        print e
        pass

if __name__ == '__main__':
    freeze_support()
    output = pd.DataFrame()

    search_Keywords = raw_input("What would you like to search for?")
    try:
        api = Connection(appid='MattDass-FLCompar-PRD-12442a3e5-6825c4fa', config_file=None)
        # if pageNum:
        pageNum = 1
        pool = ThreadPool(10)
        # pool = multiprocessing.Pool()
        while pageNum != 0:
            response = api.execute('findItemsAdvanced', {'keywords': search_Keywords, 'paginationInput':{'pageNumber':pageNum}})
            dictstr = api.response.dict()
            df = pd.DataFrame(dictstr)

            pool.map(post_JSON_API, dictstr['searchResult']['item'])
           # for item in dictstr['searchResult']['item']:
           #    print item
              # for k, v in item.iteritems():
              #    print k,":", v

            if pageNum <= dictstr['paginationOutput']['totalPages']:
                pageNum = pageNum + 1
            else:
                pageNum = 0

        print ('Finished searching for %s' % search_Keywords)
    # except ConnectionError as e:
    except:
        pass
        # print(e)
       # print(e.response.dict())

