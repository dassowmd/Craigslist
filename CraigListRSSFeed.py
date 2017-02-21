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

sites = ['albany', 'athensga', 'atlanta', 'brunswick', 'columbusga', 'macon', 'nwga', 'savannah', 'statesboro', 'valdosta']
# sites = ['savannah', 'statesboro', 'valdosta']
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

scrapedOutput.to_csv(fp, mode='a', header=True, index=False, encoding='utf-8')
print('Records gathered: ' + str(len(scrapedOutput)))

