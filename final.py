import sqlite3
import requests
import json
from secrets import *
import time


DBNAME = 'dog.db'
CACHE_FNAME = 'dogs.json'


print("***"*20)
print('\n')

# opening cache if it exists

try:
    cache_file = open(CACHE_FNAME, 'r')
    cache_contents = cache_file.read()
    CACHE_DICTION = json.loads(cache_contents)
    cache_file.close()

except:
    CACHE_DICTION = {}

# dogs class
class Dog():
    def __init__(self, dog_dict):

        self.location = dog_dict['contact']['city']['$t'] + ', ' + dog_dict['contact']['state']['$t']
        self.age = dog_dict['age']['$t']
        self.size = dog_dict['size']['$t']
        self.id = dog_dict['id']['$t']
        self.sex = dog_dict['sex']['$t']
        self.mix = dog_dict['mix']['$t']
        self.shelter_id = dog_dict['shelterId']['$t']
        if len(dog_dict['description']) > 0:
            self.details = dog_dict['description']['$t']
        else:
            self.details = None
        if isinstance(dog_dict['breeds']['breed'], type(list())):
            self.breed = ''
            for breed in dog_dict['breeds']['breed']:
                if len(dog_dict['breeds']['breed']) > 1:
                    if breed['$t'] == dog_dict['breeds']['breed'][-1]['$t']:
                        self.breed += breed['$t'].strip() + ' mix'
                    else:
                        self.breed += breed['$t'].strip() + ", "
                else:
                    self.breed = breed['$t'].strip()
        else:
            self.breed = dog_dict['breeds']['breed']['$t'].strip()

        self.name = dog_dict['name']['$t'].split('-')[0].strip().split()[0].strip().capitalize()

    def __str__(self):
        return("{}  -  {}  -  located in {}".format(self.name, self.breed, self.location))



# breed class
class Breed():
    def __init__(self, breed_dict):
        self.kind = ''

# shelter class
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
DUMMY1 = True
DUMMY2 = True
def data_cache(search_url):
    global DUMMY1
    global DUMMY2
    if search_url in CACHE_DICTION:
        data = ((CACHE_DICTION[search_url]))
        if DUMMY1:
            print("Returning data from cache file")
            DUMMY1 = False
        return((data))
    else:
        resp = requests.get(search_url).text
        data = json.loads(resp)
        CACHE_DICTION[search_url] = data
        fname = open(CACHE_FNAME, 'w')
        fname.write(json.dumps((CACHE_DICTION), indent=2))
        fname.close()
        if DUMMY2:
            print("Getting fresh data")
            DUMMY2 = False
        return (data)


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
# print(get_img_url(img_search))


# get pet data, input api method, animal type, and breed
def get_api_data(method= 'breed.list', location= '48105',  breed= '', animal = 'dog',):
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
        dog_breeds.append(breed['$t'].strip())
    return dog_breeds

# print(breeds['petfinder']['breeds']['breed'][0]['$t'])

breed_data = get_api_data()
DOG_BREEDS = dog_breed_list(breed_data)
# print(type(dog_breeds[0]))
print(len(DOG_BREEDS))
breed_list = DOG_BREEDS
print(breed_list)

def create_available_dogs(breed):
    dog_type = []
    adoptable = get_api_data('pet.find', breed= breed)
    if int(adoptable['petfinder']['header']['status']['code']['$t']) != 100:
        dog_type.append("No Dogs")
    elif adoptable['petfinder']['pets'] == {}:
        dog_type.append("No Dogs")
    else:
        available_dog_list = adoptable['petfinder']['pets']['pet']
        if isinstance(available_dog_list, type(dict())):
            dog_type.append(Dog(available_dog_list))
        else:
            for dog in available_dog_list:
                dog_type.append(Dog(dog))
    return dog_type

def time_delay(number = 15):
    for i in range(number):
        print(number-i)
        time.sleep(1)

def all_available_dogs_dict(dog_breeds):
    available_dogs = {}
    for breed in dog_breeds:
        # print(breed)
        # time_delay()
        dog_list = create_available_dogs(breed)
        available_dogs[breed] = dog_list
    return available_dogs

DOG_DICT = all_available_dogs_dict(breed_list)
# for dog in DOG_DICT['Australian Cattle Dog / Blue Heeler']:
#     print(dog)
# print((DOG_DICT)['Bouvier des Flanders'][0])

all_dogs = 0
for bred in list(DOG_DICT.keys()):
    for dogs in DOG_DICT[bred]:
        all_dogs += 1

print(all_dogs)

def check_dogs(conn, cur):
    try:
        simple_check = "SELECT * FROM 'Dogs'"
        cur.execute(simple_check)
        print("Dog Table Exists")
        return True
    except:
        statement = '''
            CREATE TABLE 'Dogs' (
                'Id' INTEGER PRIMARY KEY,
                'Name' TEXT NOT NULL,
                'Breed' TEXT NOT NULL,
                'Breed_Id' INTEGER NOT NULL,
                'Mix' TEXT NOT NULL,
                'MixBreed' TEXT NOT NULL,
                'MixBreed_Id' INTEGER NOT NULL,
                'City' TEXT NOT NULL,
                'State' TEXT NOT NULL,
                'Age' TEXT NOT NULL,
                'Sex' TEXT NOT NULL,
                'Size' TEXT NOT NULL,
                'Description' TEXT NOT NULL,
                'ShelterId' INTEGER NOT NULL
            );
        '''
        cur.execute(statement)
        conn.commit()
        return False

def init_db(db_name):
    try:
        conn = sqlite3.connect(db_name)
        cur = conn.cursor()
        check = check_dogs(conn, cur)

        conn.close()
    except Exception as e:
        print(e)

def insert_data(dog_dict, db_name= DBNAME):
    try:
        conn = sqlite3.connect(db_name)
        cur = conn.cursor()



    except Exception as e:
        print(e)

init_db(DBNAME)



print('\n')
print("***"*20)
