import requests
import json
from bs4 import BeautifulSoup


print("***"*20)
print('\n')


CACHE_FNAME = "wiki.json"

try:
    cache_file = open(CACHE_FNAME, 'r')
    cache_contents = cache_file.read()
    CACHE_DICTION = json.loads(cache_contents)
    cache_file.close()

except:
    CACHE_DICTION = {}


def soup_it(nps):
    soup = BeautifulSoup(nps, "html.parser")
    return soup

DUMMY3 = True
DUMMY4 = True
def data_cache(search_url):
    global DUMMY3
    global DUMMY4
    if search_url in CACHE_DICTION:
        data = ((CACHE_DICTION[search_url]))
        if DUMMY3:
            print("Returning data from cache file")
            DUMMY3 = False
        return(soup_it(data))
    else:
        data = requests.get(search_url).text.strip()
        CACHE_DICTION[search_url] = data
        fname = open(CACHE_FNAME, 'w')
        fname.write(json.dumps((CACHE_DICTION), indent=2))
        fname.close()
        if DUMMY4:
            print("Getting fresh data")
            DUMMY4 = False
        return (soup_it(data))

def get_wiki_data(search):
    search_url = 'https://en.wikipedia.org/wiki/{}?action=render'.format(search)
    # search_url = 'https://en.wikipedia.org/w/index.php?action=raw&title={}'.format(search)
    wiki_data = data_cache(search_url)
    return wiki_data




info = get_wiki_data("poodle")
other = info.find_all('Hypoallergenic qualities')

print(other)



print('\n')
print("***"*20)
