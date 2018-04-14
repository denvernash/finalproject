import requests
import json

CACHE_FNAME = "wiki.json"

try:
    cache_file = open(CACHE_FNAME, 'r')
    cache_contents = cache_file.read()
    CACHE_DICTION = json.loads(cache_contents)
    cache_file.close()

except:
    CACHE_DICTION = {}



# caching key to ensure cache doesn't store the same information twice
def sorted_search_params(baseurl, params, private_keys=["api_key", 'key']):
    sorted_params = sorted(params.keys())
    acc = []
    for item in sorted_params:
        if item not in private_keys:
            acc.append("{}-{}".format(item, params[item]))
    return baseurl + "_".join(acc)


# setting up caching
DUMMY3 = True
DUMMY4 = True

def get_wiki_data(search):
    baseurl = 'https://en.wikipedia.org/w/api.php'
    params = {}
    params['format'] = 'json'
    params['action'] = 'query'
    params['titles'] = search
    params['prop'] = 'info'
    # params['rvprop'] = 'content'
    uniq_id = sorted_search_params(baseurl, params)
    if uniq_id in CACHE_DICTION:
        if DUMMY3:
            print("Returning data from cache file")
            DUMMY3 = False
        return CACHE_DICTION[uniq_id]
    else:
        resp = requests.get(baseurl, params = params, headers= {'User-Agent': "SI507 (https://github.com/denvernash/finalproject; nashd@umich.edu)"}).text
        data = json.loads(resp)
        CACHE_DICTION[uniq_id] = data
        fname = open(CACHE_FNAME, 'w')
        fname.write(json.dumps((CACHE_DICTION), indent=2))
        fname.close()
        if DUMMY4:
            print("Getting fresh data")
            DUMMY2 = False
        return (data)
    info = json.loads(data)

    print(info.keys())
