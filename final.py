import requests
import json
from bs4 import BeautifulSoup
from secrets import *

print("***"*20)
print('\n')

# opening cache if it exists
CACHE_FNAME = 'dogs.json'
try:
    cache_file = open(CACHE_FNAME, 'r')
    cache_contents = cache_file.read()
    CACHE_DICTION = json.loads(cache_contents)
    cache_file.close()

except:
    CACHE_DICTION = {}


class Dog():
    def __init__(self, dog_dict):
        self.name = dog_dict['name']['$t']
            if isisntance(dog_dict['breeds']['breed'], list()):
                type = ''
                for breed in dog_dict['breeds']['breed']:
                    type += breed


        self.breed = dog_dict['breeds']['breed']['$t']
        self.location = dog_dict['contact']['city']['$t'] + ', ' + dog_dict['contact']['state']['$t']
        self.age = dog_dict['age']['$t']
        self.size = dog_dict['size']['$t']
        self.id = dog_dict['id']['$t']
        self.sex = dog_dict['sex']['$t']
        self.mix = dog_dict['mix']['$t']
        self.shelter_id = dog_dict['shelterId']['$t']
        self.details = dog_dict['description']['$t']
    def __str__(self):
        return("{} a {}, located in {}".format(self.name, self.breed, self.location))




class Breed():
    def __init__(self, breed_dict):
        self.kind = ''

class Shelter():
    def __init__(self, shelter_dict):
        self.id = ''



# caching key to ensure cache doesn't store the same information twice
def sorted_search_params(baseurl, params, private_keys=["api_key", 'key']):
    sorted_params = sorted(params.keys())
    acc = []
    for item in sorted_params:
        if item not in private_keys:
            acc.append("{}-{}".format(item, params[item]))
    return baseurl + "_".join(acc)

# setting up caching
def data_cache(search_url):
    if search_url in CACHE_DICTION:
        print("Returning data from cache file")
        data = ((CACHE_DICTION[search_url]))
        return((data))
    else:
        resp = requests.get(search_url).text
        print("Getting fresh data")
        data = json.loads(resp)
        CACHE_DICTION[search_url] = data
        fname = open(CACHE_FNAME, 'w')
        fname.write(json.dumps((CACHE_DICTION), indent=2))
        fname.close()
        return (data)


# get flicker image data from seach parameters
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
    if uniq_id in CACHE_DICTION:
        return CACHE_DICTION[uniq_id]
    else:
        flickr_text = requests.get(baseurl, params = params).text
        flickr_text_fixed = flickr_text[14:-1]
        flickr_data = json.loads(flickr_text_fixed)
        fname = open(CACHE_FNAME, 'w')
        CACHE_DICTION[uniq_id] = flickr_data
        fname.write(json.dumps((CACHE_DICTION), indent=2))
        fname.close()
        return flickr_data

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


img_search = "Poodle"
# print(get_img_url(img_search))


# get pet data, input api method, animal type, and breed
def get_pet_data(method= 'breed.list', location= '48105',  breed= '', animal = 'dog',):
    # Methods:
    # pet.get- Returns a record for a single pet.
    # pet.find - Searches for pets according to the criteria you provde and returns a collection of pet records matching your search
    # breed.list
    baseurl = 'http://api.petfinder.com/'
    search_params = '{}?key={}&animal={}&format=json'.format(method, api_key, animal)
    if method == 'pet.find':
        search_params += "&location={}".format(location)
        search_params += "&breed={}".format(breed)
        search_params += '&output=full'
    search_url = baseurl+search_params
    pet_data = (data_cache(search_url))

    return(pet_data)


def dog_breed_list(dog_data):
    dog_breeds = []
    for breed in dog_data['petfinder']['breeds']['breed']:
        # dog = breed['$t'].split('/')
        dog_breeds.append(breed['$t'].split('/')[0].strip())
    return dog_breeds

# print(breeds['petfinder']['breeds']['breed'][0]['$t'])

breed_data = get_pet_data()
dog_breeds = dog_breed_list(breed_data)
# print(type(dog_breeds[0]))

breed_list = dog_breeds[:1]
print(breed_list)

def create_available_dogs(breed):
    adoptable = get_pet_data('pet.find', breed= breed)
    available_dog_list = adoptable['petfinder']['pets']['pet']
    dog_type = []
    for dog in available_dog_list:
        dog_type.append(Dog(dog))
    return dog_type


def all_available_dogs_dict(dog_breeds):
    available_dogs = {}
    for breed in dog_breeds:
        dog_list = create_available_dogs(breed)
        available_dogs[breed] = dog_list
    return available_dogs

DOG_DICT = all_available_dogs_dict(breed_list)
print(DOG_DICT.keys())











print('\n')
print("***"*20)
