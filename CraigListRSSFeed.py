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

# parse = feedparser.parse('https://athensga.craigslist.org/search/cta?auto_bodytype=6&auto_bodytype=7&auto_bodytype=9&auto_cylinders=5&auto_drivetrain=3&format=rss')
#
# for entry in parse['entries']:
#     url = entry['link']
#     print url
#     response = requests.get(url)
#
#     soup = BeautifulSoup(response.content, 'html.parser')
#     # print soup.prettify().encode('utf-8')
#     conditions = soup.find_all('p', class_="attrgroup")
#     for condition in conditions:
#         print condition.get('text')
#     title = soup.find_all('span', id='titletextonly')
#     price = soup.find_all('span', class_='price')
#
#     postingBody = soup.find_all('section', {'class_':'userbody', 'text':True})
#     # postingBody = soup.find_all({class_='userbody', string=True})
#
#     for row in soup.find_all('p', {'class': 'row'}):
#
#         link = row.find('a', {'class': 'hdrlnk'})
#         id = link.attrs['data-id']
#         name = link.text
#         # url = urljoin(self.url, link.attrs['href'])
#
#         time = row.find('time')
#         if time:
#             datetime = time.attrs['datetime']
#         else:
#             pl = row.find('span', {'class': 'pl'})
#             datetime = pl.text.split(':')[0].strip() if pl else None
#         price = row.find('span', {'class': 'price'})
#         where = row.find('small')
#         if where:
#             where = where.text.strip()[1:-1]  # remove ()
#         p_span = row.find('span', {'class': 'p'})
#         p_text = p_span.text if p_span else ''
#
#         result = {'id': id,
#                   'name': name,
#                   'url': url,
#                   'datetime': datetime,
#                   'price': price.text if price else None,
#                   'where': where,
#                   'has_image': 'pic' in p_text,
#                   'has_map': 'map' in p_text,
#                   'geotag': None}
#
#         # if geotagged and result['has_map']:
#         #     self.geotag_result(result)



# """ Library entry point """
# import re, requests
# from bs4 import BeautifulSoup
#
#
# class CLScrape(object):
#     """ Scraper object to hold data """
#     def __init__(self, soup):
#         """ Initialize and scrape """
#         self.soup = soup
#         self.title = self.parse_string('#titletextonly')
#         try:
#             self.price = self.parse_int('.price')
#         except:
#             self.price = 'Unlisted'
#         self.attrs = {}
#         for attrgroup in soup.select('.attrgroup'):
#             for attr in attrgroup('span'):
#                 if attr.b and attr.text != attr.b.text:
#                     self.parse_attr(attr)
#         for attr in soup.select('.bigattr'):
#             self.parse_attr(attr)
#
#     def parse_attr(self, attr):
#         """ Parse a single attribute from the BeautifulSoup tag """
#         name = self.get_text(attr).strip(' :')
#         value = attr.b.text.strip()
#         self.attrs[name] = value
#
#     def parse_string(self, selector):
#         """ Parse first string matching selector """
#         return self.get_text(self.soup.select(selector)[0])
#
#     def parse_int(self, selector):
#         """ Extract one integer element from soup """
#         return int(re.sub('[^0-9]', '', self.parse_string(selector)))
#
#     def get_text(self, item):
#         """ Non-recursively extract text from an item """
#         return item.find(text=True, recursive=False).strip()
#
#
# def scrape_html(html):
#     """ Return meta information about a video """
#     return CLScrape(BeautifulSoup(html, "html.parser"))
#
#
# def scrape_url(url):
#     """ Scrape a given url for information """
#     html = requests.get(url).text
#     return scrape_html(html)
#
#
# parsed = scrape_url('https://athensga.craigslist.org/cto/6001369473.html')
# print parsed.title
# print parsed.attrs
# print parsed.price

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

