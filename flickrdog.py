import requests
import json
from nato import *

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





# get flicker image data from seach parameters for dogs
def get_flickr_img(search, amount = 1):
    baseurl = "https://api.flickr.com/services/rest/"
    params= {}
    params["api_key"] = flickr_key
    params["tags"] = search
    params["tag_mode"] = "all"
    params["method"] = "flickr.photos.search"
    params["per_page"] = amount
    params["format"] = 'json'
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
def get_img_url(search, amount = 1, list_column = 0, size=''):
    image_data = get_flickr_img(search, amount)
    farm_id = image_data['photos']['photo'][list_column]['farm']
    server_id = image_data['photos']['photo'][list_column]['server']
    img_id = image_data['photos']['photo'][list_column]['id']
    secret_id = image_data['photos']['photo'][list_column]['secret']
    if len(size) > 0:
        size = '_' + size
    image_url = 'https://farm{}.staticflickr.com/{}/{}_{}{}.jpg'.format(farm_id, server_id, img_id, secret_id, size)
    return image_url


img_search = "poodle"
print(get_img_url(img_search))
