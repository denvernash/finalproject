import requests
import json
from nato import *
from secrets import *

CACHE_FFNAME = "flickr.json"

try:
    cache_file = open(CACHE_FFNAME, 'r')
    cache_contents = cache_file.read()
    CACHE_FDICTION = json.loads(cache_contents)
    cache_file.close()

except:
    CACHE_FDICTION = {}




############################################################
#
#   FLICKR API
#
#   limit: 30 images per page on application
#   attribution: "This product uses the Flickr API but is not endorsed or certified by Flickr."
#
#
############################################################


# caching key to ensure cache doesn't store the same information twice
def sorted_search_params(baseurl, params, private_keys=["api_key", 'key']):
    sorted_params = sorted(params.keys())
    acc = []
    for item in sorted_params:
        if item not in private_keys:
            acc.append("{}-{}".format(item, params[item]))
    return baseurl + "_".join(acc)

def search_photos_params(search, amount = 1):
    params= {}
    params["api_key"] = flickr_key
    params["tags"] = search
    params["tag_mode"] = "all"
    params["method"] = "flickr.photos.search"
    params["per_page"] = amount
    params["format"] = 'json'
    params['license'] = '4'
    return params

# get flicker image data from seach parameters for dogs
def get_flickr_img(params):
    baseurl = "https://api.flickr.com/services/rest/"

    uniq_id = sorted_search_params(baseurl, params)
    if uniq_id in CACHE_FDICTION:
        return CACHE_FDICTION[uniq_id]
    else:
        flickr_text = requests.get(baseurl, params = params).text
        flickr_text_fixed = flickr_text[14:-1]
        flickr_data = json.loads(flickr_text_fixed)
        fname = open(CACHE_FFNAME, 'w')
        CACHE_FDICTION[uniq_id] = flickr_data
        fname.write(json.dumps((CACHE_FDICTION), indent=2))
        fname.close()
        return flickr_data


# creating the url to the online photo
def get_img_url(search, amount = 1, size=''):
    images =[]
    image_data = get_flickr_img(search_photos_params(search, amount))
    for img in image_data['photos']['photo']:
        farm_id = img['farm']
        server_id = img['server']
        img_id = img['id']
        secret_id = img['secret']
        if len(size) > 0:
            size = '_' + size
        image_url = 'https://farm{}.staticflickr.com/{}/{}_{}{}.jpg'.format(farm_id, server_id, img_id, secret_id, size)
        images.append(image_url)
    return images


img_search = "poodle"
for x in (get_img_url(img_search, amount= 1)):
    print(x)


# baseurl = "https://api.flickr.com/services/rest/"
# pram = {}
# pram['method'] = 'flickr.photos.licenses.getInfo'
# pram["api_key"] = flickr_key
#
#
#
# license = requests.get(baseurl, params= pram)
# print(license.text)
