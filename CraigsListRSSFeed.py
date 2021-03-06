import feedparser
from bs4 import BeautifulSoup
import requests
from urlparse import urljoin  # PY2
import pandas
from time import sleep
import os
import csv
from time import gmtime, strftime
from time import mktime
from datetime import datetime, timedelta
import random
import json
import urllib2
from multiprocessing.pool import ThreadPool
from tqdm import tqdm
import sys
# import pyodbc
# import mysql.connector
from random import shuffle
from requests.auth import HTTPBasicAuth

def post_JSON_Post_Detail(JSON_data):
    try:
        r = requests.post('http://108.59.216.215:54321/api/listings/create/', auth=HTTPBasicAuth('user', 'craigslist'), json=JSON_data)
        # r = requests.post('http://192.168.2.2:54321/api/listings/create/', auth=HTTPBasicAuth('user', 'craigslist'), json=JSON_data)
        if r.status_code == 400:
            raise ValueError('400 error received')

    except Exception as e:
        print e
        # print r.status_code
        print("Could not save via JSON API. Did you check the IP Address?")

def post_JSON_API(dictionary):
    CL_Item_ID = dictionary['url']
    for key, value in tqdm(dictionary.iteritems()):
        JSON_data = {
            "Cl_Item_ID": CL_Item_ID,
            "KeyParam": key,
            "ValueParam": value,
            "ScrapedDateTime": str(datetime.now()),
            "RSS_Feed_String": rssString,
        }
        post_JSON_Post_Detail(JSON_data)

        # JSON_data = [{
        #     "Cl_Item_ID":CL_Item_ID,
        #     "KeyParam": key,
        #     "ValueParam": value,
        #     "ScrapedDateTime": str(datetime.now()),
        #     "RSS_Feed_String": rssString,
        # }]
        # pool.map(post_JSON_Post_Detail, JSON_data)
        # pool.join()

# def write_to_MYSQL_DB(dictionary):
#
#     conn = mysql.connector.connect(host="localhost", user="user",
#                                     password="Need to enter password", db="Craigslist_Scraper")
#     cursor = conn.cursor()
#     CL_Item_ID = dictionary['url']
#     # print "connected to db"
#     for key, value in dictionary.iteritems():
#         time = str(datetime.now())
#         sql = "INSERT INTO CLData_listing(CL_Item_ID, KeyParam, ValueParam, ScrapedDateTime, RSS_Feed_String) VALUES('" + CL_Item_ID + "', '" + key + "', '" + value + "', '" + time + "', '" + rssString + "');"
#
#         # print sql
#         cursor.execute(sql)
#         cursor.execute(sql)
#         conn.commit()
#
#     conn.close()

def getPostingInfo(soup):
    results = {}
    s = soup.findAll('p', attrs={'class': 'postinginfo', 'id':None}, recursive=True)
    for i in s:
        # print i
        temp = i.get_text().encode('utf-8')
        try:
            key = temp[:str(temp).index(":")].strip()
            value = temp[(str(temp).index(":") + 1):].strip()
            results[key] = value
        except:
            continue
    return results

def getAttributes(soup):
    results = {}
    attrgroup = soup.find_all(name = 'p', class_="attrgroup", recursive=True)
    # print attrgroup
    for attr in attrgroup:
        # for i in attr:
        list = attr.get_text().split("\n")
        for l in list:
            try:
                temp = str(l).encode('utf-8')
                key = temp[:str(temp).index(":")].strip()
                value = temp[(str(temp).index(":") + 1):].strip()
                results[key] = value
            except:
                continue
    return results

def getPostingBody(soup):
    results = {}
    s = soup.find('section', attrs={'id':'postingbody'}).findAll(text=False, recursive=False)
    bodyString = ''
    for i in s:
        bodyString += str(i.get_text().encode('utf-8'))
    results['body'] = bodyString
    return results

def parseRSSFeed(url, daysSinceUpdated = 1):
    parse = feedparser.parse(url)
    parse.status
    count = 1
    for entry in parse['entries']:
        results = {}
        try:
            dateUpdated = convertRSSTime(entry['updated_parsed'])
            if dateUpdated > datetime.now() - timedelta(days=daysSinceUpdated):

                # proxies = requests.get('http://proxy.minjja.lt/pac/?type=https&loc=France')
                # proxies = requests.get('https://spinproxies.com/api/v1/protocols=https?proxylist?country_code=US&key=ctklov2d6oy63pa5jysrqn3nxzt0kx')
                # proxy_list = {'https':'https://197.33.180.151:3128'}
                # p = json.loads(proxies.content)

                # response = requests.get(url, proxies=proxy_list)
                url = entry['link']
                response = requests.get(url)
                soup = BeautifulSoup(response.content, 'html.parser')

                wait = random.randint(1,1)
                print("Searched %i items, waiting for %i seconds" %(count, wait))
                count +=1
                sleep(wait)

                results['url'] = url

                # Parse out Posting Info, Attribute and Body tags
                results.update(getPostingInfo(soup))
                results.update(getAttributes(soup))
                results.update(getPostingBody(soup))
                # Pull RSS information
                results['Publish Date'] = entry['published']
                results['Update Date'] = entry['updated']

                # Pull title and price
                try:
                    results['title'] = soup.find('span', id='titletextonly').get_text()
                    results['price'] = soup.find('span', class_='price').get_text()
                except:
                    print "Unable to parse title and price for %s" %url
                    continue


                # print(results)
                post_JSON_API(results)
                print"Success!! %s written to db" %url

                # keys = results.get(keys)
                # values = results.get(values)

                # global scrapedOutput
                # scrapedOutput = scrapedOutput.append(results, ignore_index=True)
            else:
                print"Skipping %s"% entry['id']
        except Exception as e:
            print e
            print "Unable to parse %s" %url
            continue


# def clean_text(row):
#     # return the list of decoded cell in the Series instead
#     return [r.decode('unicode_escape').encode('ascii', 'ignore') for r in row]


def convertRSSTime(RSSParsedTime):

    dt = datetime.fromtimestamp(mktime(RSSParsedTime))
    return dt

# sites = ['albany', 'athensga', 'atlanta', 'brunswick', 'columbusga', 'macon', 'nwga', 'savannah', 'statesboro', 'valdosta']
# sites = ['akroncanton','albanyga','albany','albuquerque','altoona','amarillo','ames','anchorage','annapolis','annarbor','appleton','asheville','ashtabula','athensga','athensohio','atlanta','auburn','augusta','austin','bakersfield','baltimore','batonrouge','battlecreek','beaumont','bellingham','bemidji','bend','billings','binghamton','bham','bismarck','bloomington','bn','boise','boone','boston','boulder','bgky','bozeman','brainerd','brownsville','brunswick','buffalo','butte','capecod','catskills','cedarrapids','cenla','centralmich','cnj','chambana','charleston','charlestonwv','charlotte','charlottesville','chattanooga','chautauqua','chicago','chico','chillicothe','cincinnati','clarksville','cleveland','clovis','collegestation','cosprings','columbiamo','columbia','columbusga','columbus','cookeville','corpuschristi','corvallis','chambersburg','dallas','danville','daytona','dayton','decatur','nacogdoches','delaware','delrio','denver','desmoines','detroit','dothan','dubuque','duluth','eastco','newlondon','eastky','montana','eastnc','martinsburg','easternshore','eastidaho','eastoregon','eauclaire','elko','elmira','elpaso','erie','eugene','evansville','fairbanks','fargo','farmington','fayar','fayetteville','fingerlakes','flagstaff','flint','shoals','florencesc','keys','fortcollins','fortdodge','fortsmith','fortwayne','frederick','fredericksburg','fresno','fortmyers','gadsden','gainesville','galveston','glensfalls','goldcountry','grandforks','grandisland','grandrapids','greatfalls','greenbay','greensboro','greenville','gulfport','norfolk','hanford','harrisburg','harrisonburg','hartford','hattiesburg','honolulu','cfl','helena','hickory','rockies','hiltonhead','holland','houma','houston','hudsonvalley','humboldt','huntington','huntsville','imperial','indianapolis','inlandempire','iowacity','ithaca','jxn','jackson','jacksontn','jacksonville','onslow','janesville','jerseyshore','jonesboro','joplin','kalamazoo','kalispell','kansascity','kenai','kpr','racine','killeen','kirksville','klamath','knoxville','kokomo','lacrosse','lafayette','tippecanoe','lakecharles','lakeland','loz','lancaster','lansing','laredo','lasalle','lascruces','lasvegas','lawrence','lawton','allentown','lewiston','lexington','limaohio','lincoln','littlerock','logan','longisland','losangeles','louisville','lubbock','lynchburg','macon','madison','maine','ksu','mankato','mansfield','masoncity','mattoon','mcallen','meadville','medford','memphis','mendocino','merced','meridian','milwaukee','minneapolis','missoula','mobile','modesto','mohave','monroe','monroemi','monterey','montgomery','morgantown','moseslake','muncie','muskegon','myrtlebeach','nashville','nh','newhaven','neworleans','blacksburg','newyork','lakecity','nd','nesd','nmi','wheeling','northernwi','newjersey','northmiss','northplatte','nwct','nwga','nwks','enid','ocala','odessa','ogden','okaloosa','oklahomacity','olympic','omaha','oneonta','orangecounty','oregoncoast','orlando','outerbanks','owensboro','palmsprings','panamacity','parkersburg','pensacola','peoria','philadelphia','phoenix','csd','pittsburgh','plattsburgh','poconos','porthuron','portland','potsdam','prescott','provo','pueblo','pullman','quadcities','raleigh','rapidcity','reading','redding','reno','providence','richmondin','richmond','roanoke','rmn','rochester','rockford','roseburg','roswell','sacramento','saginaw','salem','salina','saltlakecity','sanangelo','sanantonio','sandiego','sandusky','slo','sanmarcos','santabarbara','santafe','santamaria','sarasota','savannah','scottsbluff','scranton','seattle','sfbay','sheboygan','showlow','shreveport','sierravista','siouxcity','siouxfalls','siskiyou','skagit','southbend','southcoast','sd','juneau','ottumwa','seks','semo','carbondale','smd','swv','miami','southjersey','swks','swmi','marshall','natchez','bigbend','swva','spacecoast','spokane','springfieldil','springfield','pennstate','statesboro','staugustine','stcloud','stgeorge','stillwater','stjoseph','stlouis','stockton','susanville','syracuse','tallahassee','tampa','terrehaute','texarkana','texoma','thumb','toledo','topeka','treasure','tricities','tucson','tulsa','tuscaloosa','tuscarawas','twinfalls','twintiers','easttexas','up','utica','valdosta','ventura','vermont','victoriatx','visalia','waco','washingtondc','waterloo','watertown','wausau','wenatchee','quincy','westky','westmd','westernmass','westslope','wv','wichitafalls','wichita','williamsport','wilmington','winchester','winstonsalem','worcester','wyoming','yakima','york','youngstown','yubasutter','yuma','zanesville']
# sites = ['athensga']
sites = ['appleton','eauclaire', 'duluth', 'greenbay', 'janesville', 'racine', 'lacrosse', 'madison', 'milwaukee', 'northernwi', 'sheboygan', 'wausau']
shuffle(sites)
# Shuffle sites so that I don't always do the same ones first (In case there is an error)
fp = 'C:\Users\dasso\Desktop\Craigslist\Trucks_' + str(datetime.now()) + '.csv'

scrapedOutput = pandas.DataFrame()
daysSinceUpdated = 10
# pool = ThreadPool(40)
if len(sys.argv) > 1:
    rssString = sys.argv[1]
else:
    rssString = raw_input("Please enter the entire RSS feed from craigslist. Or enter 'truck' or 'duplex'\n")

if rssString == 'truck':
    rssString = 'https://athensga.craigslist.org/search/cta?auto_bodytype=6&auto_bodytype=7&auto_bodytype=9&format=rss'
elif rssString == 'duplex':
    rssString = 'https://athensga.craigslist.org/search/apa?format=rss'
rssString = rssString[rssString.find(".craigslist.org"):]
for s in sites:
    print('Searching ' + s)
    # url = 'https://' + s + '.craigslist.org/search/ppa?format=rss&query=washer%20dryer'
    url = 'https://' + s + rssString
    try:
        parseRSSFeed(url, daysSinceUpdated)
        sleep(1)
    except:
        raise


# with open(fp, 'wb') as csvfile:
#     spamwriter = csv.writer(csvfile, delimiter=' ',
#                             quotechar='|', quoting=csv.QUOTE_MINIMAL)
#     for r in scrapedOutput.iterrows():
#         print r
#         spamwriter.writerow(r)

# print scrapedOutput


# scrapedOutput.apply(clean_text)

# scrapedOutput.to_csv(fp, mode='a', header=True, index=False, encoding='utf-8')
print('Records gathered: ' + str(len(scrapedOutput)))

