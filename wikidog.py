import requests
import json
from bs4 import BeautifulSoup
from nato import *
from secrets import *
import time


print("***"*20)
print('\n')


CACHE_WFNAME = "wiki.json"

try:
    cache_file = open(CACHE_WFNAME, 'r')
    cache_contents = cache_file.read()
    CACHE_WDICTION = json.loads(cache_contents)
    cache_file.close()

except:
    CACHE_WDICTION = {}



# breed class
class Breed():
    def __init__(self, breed_dict):
        self.kind = ''





def time_delay(number = 15):
    for i in range(number):
        print(number-i)
        time.sleep(1)


def soup_it(nps):
    soup = BeautifulSoup(nps, "html.parser")
    return soup

DUMMY3 = True
DUMMY4 = True
def soup_data_cache(search_url):
    global DUMMY3
    global DUMMY4
    if search_url in CACHE_WDICTION:
        data = ((CACHE_WDICTION[search_url]))
        if DUMMY3:
            print("Returning data from cache file")
            DUMMY3 = False
        return(soup_it(data))
    else:
        data = requests.get(search_url).text.strip()
        CACHE_WDICTION[search_url] = data
        fname = open(CACHE_WFNAME, 'w')
        fname.write(json.dumps((CACHE_WDICTION), indent=2))
        fname.close()
        if DUMMY4:
            print("Getting fresh data")
            DUMMY4 = False
        return (soup_it(data))

def get_wiki_data(search):
    search_url = 'https://en.wikipedia.org/wiki/{}?action=render'.format(search)
    # search_url = 'https://en.wikipedia.org/w/index.php?action=raw&title={}'.format(search)
    wiki_data = soup_data_cache(search_url)
    # wiki_data = requests.get('https://en.wikipedia.org/w/api.php?action=query&titles=poodle&prop=info&imlimit=20&format=jsonfm')
    return wiki_data



# def create_wiki_dict(breed_list):
cells = []
info = get_wiki_data("American Bulldog")
table = info.find('table', attrs = {'class': 'infobox biota'})
rows = table.find_all('tr')
next = False
for row in rows:
    if (type(row.th)) == (type(None)):
        pass
    elif (type(row.td)) == (type(None)):
        pass
    else:
        heading = str(row.th.text.strip('\n').strip().lower())
        texting = str(row.td.text.strip('\n').strip().lower())
        if heading == "origin":
            # print("'{}, {}'".format(heading, texting))
            print('\n')
        elif heading == 'coat':
            # print("'{}, {}'".format(heading, texting))
            print('\n')
        elif heading == 'color':
            # print("'{}, {}'".format(heading, texting))
            print('\n')
        elif heading == 'colour':
            print("yes")
        elif heading == 'life span':
            print("yes")
        elif heading == 'litter size':
            print("yes")
        elif 'litter' in heading:
            print(type(heading[7]))
            print(len(heading[7]))
            print(heading == 'litter size')
            print(heading)
            print('litter size')
        else:
            print('*')
            print(heading)
            print(len(heading))
            print('*')
        # print(len(row.th.text.strip('\n').strip()))

other_info = info.find('table', attrs = {'class': 'infobox collapsible'})
    # if next:
    #     print(row.text)
    #     next = False
    # if row.text == "Origin":
    #     next = True
    # else:
    #     print("not")
    #     print(row.text)
        # print(row.text)
    # for cell in row.find_all('tr'):
    #     try:
    #         print(cell)
    #
    #     # print(cell.th.text)
    #     # try:
    #     #     print(cell.td.text)
    #     except:
    #         print(cell)




#     even = more.find_all('th', attrs= {'scope': 'row'})
#     even_more.append(even)
#
# print(even_more)
# print(other)

print('\n')
print("***"*20)
