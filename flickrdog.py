import requests
import json
from nato import *
from secrets import *
import webbrowser
import time

CACHE_FFNAME = "flickr.json"

try:
    cache_file = open(CACHE_FFNAME, 'r')
    cache_contents = cache_file.read()
    CACHE_FDICTION = json.loads(cache_contents)
    cache_file.close()

except:
    CACHE_FDICTION = {}



LICENSE_URLS = {
  "1" : "https://creativecommons.org/licenses/by-nc-sa/2.0/",
  "2" : "https://creativecommons.org/licenses/by-nc/2.0/",
  "3" : "https://creativecommons.org/licenses/by-nc-nd/2.0/",
  "4" : "https://creativecommons.org/licenses/by/2.0/",
  "5" : "https://creativecommons.org/licenses/by-sa/2.0/",
  "6" : "https://creativecommons.org/licenses/by-nd/2.0/"
}






class Image():
    def __init__(self, img_dict, size= ''):
        self.farm_id = img_dict['farm']
        self.server_id = img_dict['server']
        self.img_id = img_dict['id']
        self.secret_id = img_dict['secret']
        self.size = size
        if len(self.size) > 0:
            self.size = '_' + self.size
        self.image_url = 'https://farm{}.staticflickr.com/{}/{}_{}{}.jpg'.format(self.farm_id, self.server_id, self.img_id, self.secret_id, self.size)
        self.license_code = 'https://creativecommons.org/licenses/by-nc-sa/2.0/legalcode'
        self.content_url = "Flickr URL"
        self.username = 'Name'
    def __str__(self):
        return ("Image at {} by Author {}".format(self.content_url, self.username))
    def get_attribution_data(self):
        attr_data = get_flickr_img(info_photos_params(self.img_id, self.secret_id))
        self.content_url = attr_data['photo']['urls']['url'][0]['_content']
        self.username = attr_data['photo']['owner']['username']
        self.title = attr_data['photo']['title']['_content']
        self.license_id = attr_data['photo']['license']
        self.license_url = LICENSE_URLS[self.license_id]

############################################################
#
#   FLICKR API
#
#   limit: 30 images per page on application
#   attribution: "This product uses the Flickr API but is not endorsed or certified by Flickr."
#   call limit: under 3600 per hour per key
#
#
############################################################


# caching key to ensure cache doesn't store the same information twice
def sorted__params(baseurl, params, private_keys=["api_key", 'key']):
    sorted_params = sorted(params.keys())
    acc = []
    for item in sorted_params:
        if item not in private_keys:
            acc.append("{}-{}".format(item, params[item]))
    return baseurl + "_".join(acc)

def search_photos_params(search, cuttags=True, amount = 1):
    params= {}
    params["api_key"] = flickr_key
    if cuttags:
        params["tags"] = search + ',dog,-finelinerpens,-thehulk,-blancoynegro,-pee,-drawing,-barking,-cat,'
        '-postcardsforthelunchbag,-watercolor,-blackie,-closeup,-nose,-leona,-origami,-glass,-jug,-waterfall,'
        '-confirmation,-berkeley,-groomingtreatment,-fdsflickrtoys,-tillie,-taiwan'
    else:
        params['tags'] = search
    params["tag_mode"] = "all"
    params['sort'] = 'interestingness-desc'
    params['content_type'] = '1'
    params["method"] = "flickr.photos.search"
    params['media'] = 'photos'
    params["per_page"] = amount
    params["format"] = 'json'
    params['license'] = '1,2,3,4,5,6'
    return params

def info_photos_params(photoid, secret):
    params= {}
    params["api_key"] = flickr_key
    params["photo_id"] = photoid
    params["method"] = "flickr.photos.getInfo"
    params["secret"] = secret
    params["format"] = 'json'
    return params


CALL_LIMIT = 0
DUM1 = True
# get flicker image data from seach parameters for dogs
def get_flickr_img(params):
    baseurl = "https://api.flickr.com/services/rest/"
    global DUM1
    global CALL_LIMIT
    uniq_id = sorted__params(baseurl, params)
    if uniq_id in CACHE_FDICTION:
        if DUM1:
            print("Returning cache data")
            DUM1 = False
        return CACHE_FDICTION[uniq_id]
    elif CALL_LIMIT >= 3500:
        sys.exit("You have reached the Flickr call limit per hour")
    else:
        flickr_text = requests.get(baseurl, params = params).text
        CALL_LIMIT += 1
        print(CALL_LIMIT, "Getting fresh data")
        flickr_text_fixed = flickr_text[14:-1]
        flickr_data = json.loads(flickr_text_fixed)
        fname = open(CACHE_FFNAME, 'w')
        CACHE_FDICTION[uniq_id] = flickr_data
        fname.write(json.dumps((CACHE_FDICTION), indent=2))
        fname.close()
        return flickr_data


# creating the url to the online photo
def create_image(search, cuttags=True, amount = 1, size=''):
    list_images =[]
    image_data = get_flickr_img(search_photos_params(search, cuttags, amount))
    for img in image_data['photos']['photo']:
        imagex = Image(img, size)
        imagex.get_attribution_data()
        list_images.append(imagex)
    return list_images

def time_delay(number = 15):
    for i in range(number):
        print(number-i)
        time.sleep(1)



# img_search = "poodle"
# to_test = (create_image(img_search))[0]
# webbrowser.open(to_test.content_url)



def create_dog_images(breed_list, amount = 1, size=''):
    breed_imgs = {}
    global DOG_IMGS_NOT_FOUND
    special_dog_list = [
    "Appenzell Mountain Dog",
    "Black and Tan Coonhound",
    "Cane Corso Mastiff",
    "Caucasian Sheepdog / Caucasian Ovtcharka",
    "Dandi Dinmont Terrier",
    "Galgo Spanish Greyhound",
    "Hamiltonstovare",
    "Kyi Leo",
    "Mountain Cur",
    "Norwegian Lundehund",
    "Podengo Portugueso",
    "Scottish Terrier Scottie",
    "Shetland Sheepdog Sheltie",
    "Tosa Inu",
    "West Highland White Terrier Westie",
    "Yorkshire Terrier Yorkie",
    ]
    not_found = []
    for breed in breed_list:
        if breed not in special_dog_list:
            try:
                dog = breed.split("/")[0].split("(")[0].strip()
                img = create_image(dog, True, amount, size)[0]
                breed_imgs[breed] = img
                time_delay(5)
            except:
                not_found.append(breed)
        elif breed in special_dog_list:
            try:
                dog = breed.split("/")[0].split("(")[0].strip()
                # print(dog)
                img = create_image(dog, False, amount, size)[0]
                # print(img.content_url)
                breed_imgs[breed] = img
                # time_delay(1)
            except:
                not_found.append(breed)
        else:
            not_found.append(breed)
    if len(not_found) > 0:
        for breed in not_found:
            if breed in DOG_IMGS_NOT_FOUND:
                try:
                    img = create_image(DOG_IMGS_NOT_FOUND[breed], False, amount, size)[0]
                    breed_imgs[breed] = img
                    # print(img.content_url)
                except:
                    pass
            else:
                pass
    return breed_imgs

# print(len(LIST_OF_BREEDS))
BREED_IMGS = create_dog_images(LIST_OF_BREEDS[180:200])
# key_list = sorted(list(BREED_IMGS.keys()))
# for i in range(len(key_list)):
#     if sorted(LIST_OF_BREEDS)[i] != key_list[i]:
#         print('{}  ,    {}'.format(LIST_OF_BREEDS[i], key_list[i]))






#
