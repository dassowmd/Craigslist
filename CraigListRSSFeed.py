import feedparser
from bs4 import BeautifulSoup
import requests
try:
    from urlparse import urljoin  # PY2
except ImportError:
    from urllib.parse import urljoin  # PY3
import pandas
from time import sleep
import os
import csv
from time import gmtime, strftime
from time import mktime
from datetime import datetime, timedelta
# import pyodbc
import mysql.connector

def writeToDB(dictionary):

    conn = mysql.connector.connect(host="localhost", user="dassowmd",
                                    password="asdfjkl;1", db="Craigslist_Scraper")
    cursor = conn.cursor()
    CL_Item_ID = dictionary['url']
    for key, value in dictionary.iteritems():
        sql = "INSERT INTO RSS_Parsed_Data(CL_Item_ID, KeyParam, ValueParam) VALUES('" + CL_Item_ID + "', '" + key + "', '" + value + "');"
        print sql
        cursor.execute(sql)
        cursor.execute(sql)
        conn.commit()

    conn.close()

def getPostingInfo(soup):
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

def getAttributes(soup):
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

def getPostingBody(soup):
    s = soup.find('section', attrs={'id':'postingbody'}).findAll(text=False, recursive=False)
    bodyString = ''
    for i in s:
        bodyString += str(i.get_text().encode('utf-8'))
    results['body'] = bodyString

def parseRSSFeed(url, daysSinceUpdated = 1):
    parse = feedparser.parse(url)
    for entry in parse['entries']:
        try:
            dateUpdated = convertRSSTime(entry['updated_parsed'])
            if dateUpdated > datetime.now() - timedelta(days=daysSinceUpdated):

                url = entry['link']
                response = requests.get(url)
                soup = BeautifulSoup(response.content, 'html.parser')

                results['url'] = url

                # Parse out Posting Info, Attribute and Body tags
                results.items().append(getPostingInfo(soup))
                results.items().append(getAttributes(soup))
                results.items().append(getPostingBody(soup))

                # Pull RSS information
                results['Publish Date'] = entry['published']
                results['Update Date'] = entry['updated']

                # Pull title and price
                try:
                    results['title'] = soup.find('span', id='titletextonly').get_text()
                    results['price'] = soup.find('span', class_='price').get_text()
                except:
                    continue

                print(results)
                writeToDB(results)

                keys = results.get(keys)
                values = results.get(values)

                global scrapedOutput
                scrapedOutput = scrapedOutput.append(results, ignore_index=True)
        except:
            continue

            sleep(1)

# def clean_text(row):
#     # return the list of decoded cell in the Series instead
#     return [r.decode('unicode_escape').encode('ascii', 'ignore') for r in row]


def convertRSSTime(RSSParsedTime):

    dt = datetime.fromtimestamp(mktime(RSSParsedTime))
    return dt

# sites = ['albany', 'athensga', 'atlanta', 'brunswick', 'columbusga', 'macon', 'nwga', 'savannah', 'statesboro', 'valdosta']
sites = ['akroncanton','albanyga','albany','albuquerque','altoona','amarillo','ames','anchorage','annapolis','annarbor','appleton','asheville','ashtabula','athensga','athensohio','atlanta','auburn','augusta','austin','bakersfield','baltimore','batonrouge','battlecreek','beaumont','bellingham','bemidji','bend','billings','binghamton','bham','bismarck','bloomington','bn','boise','boone','boston','boulder','bgky','bozeman','brainerd','brownsville','brunswick','buffalo','butte','capecod','catskills','cedarrapids','cenla','centralmich','cnj','chambana','charleston','charlestonwv','charlotte','charlottesville','chattanooga','chautauqua','chicago','chico','chillicothe','cincinnati','clarksville','cleveland','clovis','collegestation','cosprings','columbiamo','columbia','columbusga','columbus','cookeville','corpuschristi','corvallis','chambersburg','dallas','danville','daytona','dayton','decatur','nacogdoches','delaware','delrio','denver','desmoines','detroit','dothan','dubuque','duluth','eastco','newlondon','eastky','montana','eastnc','martinsburg','easternshore','eastidaho','eastoregon','eauclaire','elko','elmira','elpaso','erie','eugene','evansville','fairbanks','fargo','farmington','fayar','fayetteville','fingerlakes','flagstaff','flint','shoals','florencesc','keys','fortcollins','fortdodge','fortsmith','fortwayne','frederick','fredericksburg','fresno','fortmyers','gadsden','gainesville','galveston','glensfalls','goldcountry','grandforks','grandisland','grandrapids','greatfalls','greenbay','greensboro','greenville','gulfport','norfolk','hanford','harrisburg','harrisonburg','hartford','hattiesburg','honolulu','cfl','helena','hickory','rockies','hiltonhead','holland','houma','houston','hudsonvalley','humboldt','huntington','huntsville','imperial','indianapolis','inlandempire','iowacity','ithaca','jxn','jackson','jacksontn','jacksonville','onslow','janesville','jerseyshore','jonesboro','joplin','kalamazoo','kalispell','kansascity','kenai','kpr','racine','killeen','kirksville','klamath','knoxville','kokomo','lacrosse','lafayette','tippecanoe','lakecharles','lakeland','loz','lancaster','lansing','laredo','lasalle','lascruces','lasvegas','lawrence','lawton','allentown','lewiston','lexington','limaohio','lincoln','littlerock','logan','longisland','losangeles','louisville','lubbock','lynchburg','macon','madison','maine','ksu','mankato','mansfield','masoncity','mattoon','mcallen','meadville','medford','memphis','mendocino','merced','meridian','milwaukee','minneapolis','missoula','mobile','modesto','mohave','monroe','monroemi','monterey','montgomery','morgantown','moseslake','muncie','muskegon','myrtlebeach','nashville','nh','newhaven','neworleans','blacksburg','newyork','lakecity','nd','nesd','nmi','wheeling','northernwi','newjersey','northmiss','northplatte','nwct','nwga','nwks','enid','ocala','odessa','ogden','okaloosa','oklahomacity','olympic','omaha','oneonta','orangecounty','oregoncoast','orlando','outerbanks','owensboro','palmsprings','panamacity','parkersburg','pensacola','peoria','philadelphia','phoenix','csd','pittsburgh','plattsburgh','poconos','porthuron','portland','potsdam','prescott','provo','pueblo','pullman','quadcities','raleigh','rapidcity','reading','redding','reno','providence','richmondin','richmond','roanoke','rmn','rochester','rockford','roseburg','roswell','sacramento','saginaw','salem','salina','saltlakecity','sanangelo','sanantonio','sandiego','sandusky','slo','sanmarcos','santabarbara','santafe','santamaria','sarasota','savannah','scottsbluff','scranton','seattle','sfbay','sheboygan','showlow','shreveport','sierravista','siouxcity','siouxfalls','siskiyou','skagit','southbend','southcoast','sd','juneau','ottumwa','seks','semo','carbondale','smd','swv','miami','southjersey','swks','swmi','marshall','natchez','bigbend','swva','spacecoast','spokane','springfieldil','springfield','pennstate','statesboro','staugustine','stcloud','stgeorge','stillwater','stjoseph','stlouis','stockton','susanville','syracuse','tallahassee','tampa','terrehaute','texarkana','texoma','thumb','toledo','topeka','treasure','tricities','tucson','tulsa','tuscaloosa','tuscarawas','twinfalls','twintiers','easttexas','up','utica','valdosta','ventura','vermont','victoriatx','visalia','waco','washingtondc','waterloo','watertown','wausau','wenatchee','quincy','westky','westmd','westernmass','westslope','wv','wichitafalls','wichita','williamsport','wilmington','winchester','winstonsalem','worcester','wyoming','yakima','york','youngstown','yubasutter','yuma','zanesville']
# sites = ['athensga']
fp = 'C:\Users\dasso\Desktop\Craigslist\Trucks_' + str(datetime.now()) + '.csv'
results = {}

scrapedOutput = pandas.DataFrame()
daysSinceUpdated = 1
for s in sites:
    print('Searching ' + s)
    # url = 'https://' + s + '.craigslist.org/search/ppa?format=rss&query=washer%20dryer'
    url = 'https://' + s + '.craigslist.org/search/cta?auto_bodytype=6&auto_bodytype=7&auto_bodytype=9&auto_cylinders=5&auto_drivetrain=3&format=rss'
    try:
        parseRSSFeed(url, daysSinceUpdated)
        sleep(60)
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

