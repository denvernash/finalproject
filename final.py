import requests
import json
from bs4 import BeautifulSoup
from secrets import *

CACHE_FNAME = 'dogs.json'
try:
    cache_file = open(CACHE_FNAME, 'r')
    cache_contents = cache_file.read()
    CACHE_DICTION = json.loads(cache_contents)
    cache_file.close()

# if there was no file, no worries. There will be soon!
except:
    CACHE_DICTION = {}

def sorted_search_params(self, baseurl, params, private_keys=["api_key"]):
	sorted_params = sorted(params.keys())
	acc = []
	for item in sorted_params:
        if item not in private_keys:
            acc.append("{}-{}".format(item, params[item]))
	return baseurl + "_".join(acc)


def get_flickr_img(search, amount = 1):
    baseurl = "https://api.flickr.com/services/rest/"
    params= {}
    params["api_key"] = flickr_key
    params["tags"] = search
    params["tag_mode"] = "all"
    params["method"] = "flickr.photos.search"
    params["per_page"] = amount
    params["format"] = 'json'
    uniq_id = params_unique_combination(baseurl, params)


def caching_pattern(search_url):
    if search_url in CACHE_DICTION:
        # print("Returning data from cache file")
        return (CACHE_DICTION[search_url])
    else:
        data = requests.get(search_url).text
        # print("Getting fresh data from UMSI")
        CACHE_DICTION[search_url] = data
        fname = open(CACHE_FNAME, 'w')
        fname.write(json.dumps((CACHE_DICTION), indent=2))
        fname.close()
        return (data)

def get_dog_data():
    baseurl = ''



dog_data = requests.get(baseurl)


print(dog_data.text)
