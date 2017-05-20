import datetime
from ebaysdk.exception import ConnectionError
from ebaysdk.finding import Connection
import pandas as pd
from multiprocessing import freeze_support
from multiprocessing.pool import ThreadPool
from datetime import datetime, timedelta
import sys
import requests
from requests.auth import HTTPBasicAuth
from collections import OrderedDict
import time
import argparse

def flatten(json_object, container=None, name=''):
    try:
        if container is None:
            container = OrderedDict()
        if isinstance(json_object, dict):
            for key in json_object:
                flatten(json_object[key], container=container, name=name + key + '_')
        elif isinstance(json_object, list):
            for n, item in enumerate(json_object, 1):
                flatten(item, container=container, name=name + str(n) + '_')
        else:
            container[str(name[:-1])] = str(json_object).encode('utf8')
        return container
    except Exception as e:
        print e
        pass

def post_JSON_API(dictionary):
    flat_dict = flatten(dictionary)
    item_ID = flat_dict['itemId'].encode('utf8')
    try:
        for key, value in flat_dict.iteritems():
            print item_ID + "-" + key.encode('utf-8') + ":" + value.encode('utf-8')
            JSON_data = {
            "Cl_Item_ID":str(item_ID),
            "KeyParam": str(key).encode('utf-8'),
            "ValueParam": str(value).encode('utf-8')[0:20000],
            "ScrapedDateTime": str(datetime.now()).encode('utf-8'),
            "RSS_Feed_String": str(search_keywords).encode('utf-8'),
            }

            try:
                r = requests.post('http://108.59.216.215:54321/api/listings/create/', auth=HTTPBasicAuth('user', 'craigslist'), json=JSON_data)
                # r = requests.post('http://192.168.2.2:54321/api/listings/create/', auth=HTTPBasicAuth('user', 'craigslist'), json=JSON_data)

            except Exception as e:
                print e
                print("Could not save via JSON API. Did you check the IP Address and Port Forwarding?")
                pass

        print (item_ID + '-' + flat_dict['title'] + ' Saved to database')
    except Exception as e:
        print e
        pass

def call_Ebay_API(page_num, search_keywords, try_count=1):
    try:
        api = Connection(appid='MattDass-FLCompar-PRD-12442a3e5-6825c4fa', config_file=None)
        response = api.execute('findItemsAdvanced', {'keywords': search_keywords, 'paginationInput': {'pageNumber': page_num}})
        dictstr = api.response.dict()
        df = pd.DataFrame(dictstr)

        # for i in dictstr['searchResult']['item']:
        #     post_JSON_API(i)

        pool = ThreadPool(10)
        pool.map(post_JSON_API, dictstr['searchResult']['item'])

        if page_num <= dictstr['paginationOutput']['totalPages']:
            page_num = page_num + 1
        else:
            page_num = 0
        return page_num
    except Exception as e:
        print e
        if try_count <= 3:
            time.sleep(10)
            try_count +=1
            call_Ebay_API(page_num, try_count)
        else:
            raise ValueError("No luck. Tried connecting 3 times and it still didn't work")

if __name__ == '__main__':
    freeze_support()
    output = pd.DataFrame()

    parser = argparse.ArgumentParser(description='Gather Ebay Postings')
    parser.add_argument('Search_Key', metavar='N', type=str, nargs='+',
                        help='the Ebay search term')

    if len(sys.argv) > 1:
        search_keywords = sys.argv[1]
    else:
        search_keywords = raw_input("What would you like to search for?")
    try:
        page_num = 1
        while page_num !=0:
            page_num = call_Ebay_API(page_num=page_num, search_keywords = search_keywords)


        print ('Finished searching for %s' % search_keywords)
    # except ConnectionError as e:
    except Exception as e:
        pass
        print(e)
       # print(e.response.dict())

