import sqlite3
import requests
import json
import sys
import time
import random
import string
from secrets import *
from nato import *
from flickrdog import *



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

############################################################
#
#   CLASS DEFINITIONS
#
#
############################################################

# dog class
class Dog():
    def __init__(self, dog_dict):

        self.name = dog_dict['name']['$t'].split('-')[0].split('/')[0].split('~')[0].split(',')[0].split('.')[0].split('(')[0].split('_')[0].split()[0].strip("*").strip("\'").strip(":").strip('"').strip('!').strip().capitalize()
        if isinstance(dog_dict['breeds']['breed'], type(list())):
            self.breed1 = None
            for breed in dog_dict['breeds']['breed']:
                if len(dog_dict['breeds']['breed']) > 1:
                    if breed['$t'] == dog_dict['breeds']['breed'][-1]['$t']:
                        self.breed2 = breed['$t'].strip()
                    else:
                        self.breed1 = breed['$t'].strip()
                else:
                    self.breed1 = breed['$t'].strip()
                    self.breed2 = None
        else:
            self.breed1 = dog_dict['breeds']['breed']['$t'].strip()
            self.breed2 = None
        if self.breed2 == None:
            self.breed = self.breed1
        else:
            self.breed = self.breed1 + ', ' + self.breed2
        self.city = dog_dict['contact']['city']['$t']
        self.state = dog_dict['contact']['state']['$t']
        if self.state in STATES:
            self.country = "USA"
        elif self.state in CANADA:
            self.country = "CAN"
        else:
            self.country = "UNK"
        self.location = self.city + ', ' + self.state
        self.age = dog_dict['age']['$t']
        self.size = dog_dict['size']['$t']
        self.id = dog_dict['id']['$t']
        self.sex = dog_dict['sex']['$t']
        if self.breed2 == None:
            self.mix = 'No'
        else:
            self.mix = "Yes"
        self.shelter_id = dog_dict['shelterId']['$t']
        if len(dog_dict['description']) > 0:
            self.details = dog_dict['description']['$t']
        else:
            self.details = None




    def __str__(self):
        if self.breed2 == None:
            return("{}  -  {}  -  located in {}".format(self.name, self.breed, self.location))
        else:
            return("{}  -  {} Mix  -  located in {}".format(self.name, self.breed, self.location))

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            same = True
            if self.name != other.name:
                same = False
            elif self.location != other.location:
                same = False
            elif self.breed != other.breed:
                same = False
            elif self.age != other.age:
                same = False
            elif self.sex != other.sex:
                same = False
            elif self.size != other.size:
                same = False
            elif self.shelter_id != other.shelter_id:
                same = False
            return same
        else:
            return False



# breed class
class Breed():
    def __init__(self, breed_dict):
        self.kind = ''

# shelter class
class Shelter():
    def __init__(self, shelter_dict, id):
        self.id = id
        if shelter_dict['country']['$t'] == "US":
            self.country = "USA"
        elif shelter_dict['country']['$t'] == "CA":
            self.country = "CAN"
        else:
            self.country = "UNK"
        self.state = shelter_dict['state']['$t']
        self.city = shelter_dict['city']['$t']
        self.location = self.city + ', ' + self.state
        self.lon = shelter_dict['longitude']['$t']
        self.lat = shelter_dict['latitude']['$t']
        self.name = shelter_dict['name']['$t']


    def __str__(self):
        return ("{}  --  in {}".format(self.name, self.location))

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.__dict__ == other.__dict__
        else:
            return False



############################################################
#
#   CACHING FUNCTIONS
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

# setting up caching
BACKUP = 0
SHUTDOWN = 0
DUMMY1 = True
DUMMY2 = True
def data_cache(search_url):
    global DUMMY1
    global DUMMY2
    global BACKUP
    global SHUTDOWN
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
        BACKUP += 1
        # SHUTDOWN += 1
        if BACKUP >= 5:
            BACKUP = 0
            if BACKUP == 0:
                print("Writing Backup")
            fname = open('backup.json', 'w')
            fname.write(json.dumps((CACHE_DICTION), indent=2))
            fname.close()
        if DUMMY2:
            print("Getting fresh data")
            DUMMY2 = False
        if SHUTDOWN >= 15:
            sys.exit("YOU HAVE ATTEMPTED TO MAKE 15 CALLS TO THE API ALL AT ONCE")
        return (data)


############################################################
#
#   PETFINDER API - Dogs
#
#
#   attribution - “Powered by Petfinder” and link to www.petfinder.com.
#
#
############################################################

# makes a call to api to get data from petfinder or cache file
# input - api method and specified parameters
# output - petfinder api dictionary
def get_api_data(method= 'breed.list', location= '48105',  breed= '', animal = 'dog', id= ''):
    baseurl = 'http://api.petfinder.com/'
    search_params = '{}?key={}&animal={}&format=json'.format(method, api_key, animal)
    if method == 'pet.find':
        search_params += "&location={}".format(location)
        search_params += "&breed={}".format(breed)
        search_params += '&output=full'
    if method == 'shelter.get':
        search_params = '{}?key={}&id={}&format=json'.format(method, api_key, id)
    search_url = baseurl+search_params
    pet_data = (data_cache(search_url))

    return(pet_data)

# input - dog breed dictionary
# output - list of all dog breeds available on petfinder api
def dog_breed_list(dog_data):
    dog_breeds = []
    for breed in dog_data['petfinder']['breeds']['breed']:
        dog_breeds.append(breed['$t'].strip())
    return dog_breeds











# input -  a dog breed type
# output list of available dogs of that breed on petfinder if any
def create_available_dogs(breed):
    dog_type = []
    dog_return = []
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
    for dog in dog_type:
        if dog not in dog_return:
            dog_return.append(dog)
    return dog_return


# input - integer
# output - none
def time_delay(number = 15):
    for i in range(number):
        print(number-i)
        time.sleep(1)


# input - list of dog breeds
# output - dictionary of dogs in each breed
def all_available_dogs_dict(dog_breeds):
    available_dogs = {}
    for breed in dog_breeds:
        # print(breed)
        # time_delay()
        dog_list = create_available_dogs(breed)
        available_dogs[breed] = dog_list
    return available_dogs









# input - dictionary of dogs that needs some data cleaning
# output - dictionary of cleaned data
def clean_dog_dict(dog_dict):
    dumb_dog_names = ["adop", 'fost', 'ibr', 'westies', 'breed', 'need', 'kennel', 'mr', 'kt', "'", 'please', 'bh']
    for i in range(10):
        dumb_dog_names.append(str(i))
    all_dogs = 0
    no_dogs_list = []
    dog_ids = []
    DOG_DICT_TO_RETURN = {}
    for key in list(dog_dict.keys()):
        breed_to_dict = []
        for dog in dog_dict[key]:
            if dog != "No Dogs":
                all_dogs += 1
                if dog.id not in dog_ids:
                    dog_ids.append(dog.id)
                    for name in dumb_dog_names:
                        if name in dog.name.lower():
                            dog.name = NATO[random.choice(string.ascii_letters)]
                        elif len(dog.name) <= 2:
                            dog.name = NATO[random.choice(string.ascii_letters)]
                        elif dog.name in dog.breed:
                            dog.name = NATO[random.choice(string.ascii_letters)]
                    breed_to_dict.append(dog)
                else:
                    del dog
            else:
                no_dogs_list.append(key)
        if breed_to_dict != []:
            DOG_DICT_TO_RETURN[key] = breed_to_dict
    return DOG_DICT_TO_RETURN












############################################################
#
#   PETFINDER API - Shelters
#
#
############################################################

#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

# CAUTION!!!!
# CAUTION!!!!
# CAUTION!!!!

# - The function get_shelter_dict below will attempt to call

# the API 1800 times if the data is not found in dogs.json.

# The cache function has a backup to try to stop this from occuring


# input - dictionary of dogs with shelter id from each dog
# output - dictionary with all raw shelter data from api
def get_shelter_dict(dog_dict):
    dog_shelters = []
    shelter = {}
    for breed in list(dog_dict.keys()):
        for dog in dog_dict[breed]:
            if dog.shelter_id not in dog_shelters:
                dog_shelters.append(dog.shelter_id)
    for id in dog_shelters:
        # print(id)
        # time_delay(8)
        # x += 1
        # print("*****"+ str(x) + "*****")
        shelter_dict = get_api_data('shelter.get', id= id)
        shelter[id] = (shelter_dict)
    return shelter


# input - raw shelter data dictionary
# output - dictionary of class shelters
def create_shelters(shelter_dict):
    shelters = {}
    for key in list(shelter_dict.keys()):
        shell = shelter_dict[key]['petfinder']
        if int(shell['header']['status']['code']['$t']) != 100:
            shelters[key] = "Unlisted"
        else:
            shelters[key] = Shelter(shell['shelter'], key)
    return shelters










############################################################
#
#   DATABASE - Shelters
#
#
############################################################

def check_shelters(conn, cur):
    try:
        simple_check = "SELECT * FROM 'Shelters'"
        cur.execute(simple_check)
        print("Shelter Table Exists")
        return False
    except:
        print("Creating Table")
        statement = '''
        CREATE TABLE 'Shelters' (
        'Id' TEXT PRIMARY KEY,
        'Name' TEXT,
        'City' TEXT,
        'State' TEXT,
        'Country' TEXT,
        'Lat' TEXT,
        'Lon' TEXT
        );
        '''
        cur.execute(statement)
        conn.commit()
        return True


def insert_shelters(shelter_dict, db_name= DBNAME):
    try:
        conn = sqlite3.connect(db_name)
        cur = conn.cursor()
        for key in list(shelter_dict.keys()):
            shelter = shelter_dict[key]
            if shelter == "Unlisted":
                insertion = (key, 'Unlisted', 'Unlisted', 'Unlisted', 'Unlisted', 'Unlisted', 'Unlisted')
                statement = 'INSERT INTO Shelters (Id, Name, City, State, Country, Lat, Lon) '
                statement += 'VALUES (?, ?, ?, ?, ?, ?, ?)'
                cur.execute(statement, insertion)
                conn.commit()
            else:
                insertion = (key, shelter.name, shelter.city, shelter.state, shelter.country, shelter.lat, shelter.lon)
                statement = 'INSERT INTO Shelters (Id, Name, City, State, Country, Lat, Lon) '
                statement += 'VALUES (?, ?, ?, ?, ?, ?, ?)'
                cur.execute(statement, insertion)
                conn.commit()
    except Exception as e:
        print(e)

def update_shelters(conn, cur):
    statement = '''select dogs.City, dogs.State from Dogs join Shelters on
    dogs.ShelterId = Shelters.Id where Shelters.Name = "Unlisted" group by
    dogs.City order by dogs.State '''
    bars_data = conn.execute(statement)
    line = bars_data.fetchall()
    for x in line:
        location = "{}, {}".format(x[0], x[1])
        statement = ''' update Shelters set Lat = '{}'
        where City = '{}' AND State = '{}' AND Name =
        "Unlisted" '''.format(UNLISTED_SHELTER_LOCATIONS[location].split(',')[0], x[0], x[1])
        cur.execute(statement)
        conn.commit()
        statement = ''' update Shelters set Lon = '{}'
        where City = '{}' AND State = '{}' AND Name =
        "Unlisted" '''.format(UNLISTED_SHELTER_LOCATIONS[location].split(',')[1], x[0], x[1])
        cur.execute(statement)
        conn.commit()


    statement = ''' update Shelters set City = ( select dogs.City from dogs
    where dogs.ShelterId = Shelters.Id AND Shelters.Name = "Unlisted" )
    Where exists ( select dogs.City from dogs where dogs.ShelterId =
    Shelters.Id AND Shelters.Name = "Unlisted" ) '''
    cur.execute(statement)
    conn.commit()
    statement = ''' update Shelters set State = ( select dogs.State from dogs
    where dogs.ShelterId = Shelters.Id AND Shelters.Name = "Unlisted" )
    Where exists ( select dogs.State from dogs where dogs.ShelterId =
    Shelters.Id AND Shelters.Name = "Unlisted" ) '''
    cur.execute(statement)
    conn.commit()
    statement = ''' update Shelters set Country = ( select dogs.Country from dogs
    where dogs.ShelterId = Shelters.Id AND Shelters.Name = "Unlisted" )
    Where exists ( select dogs.Country from dogs where dogs.ShelterId =
    Shelters.Id AND Shelters.Name = "Unlisted" ) '''
    cur.execute(statement)
    conn.commit()

############################################################
#   Updating shelter geolocations
#   attribution: "This product includes data created by MaxMind, available from http://www.maxmind.com/"
############################################################



############################################################
#
#   DATABASE - Dogs
#
#
############################################################


def check_dogs(conn, cur):
    try:
        simple_check = "SELECT * FROM 'Dogs'"
        cur.execute(simple_check)
        print("Dog Table Exists")
        return False
    except:
        print("Creating Table")
        statement = '''
            CREATE TABLE 'Dogs' (
                'Id' INTEGER PRIMARY KEY,
                'Name' TEXT NOT NULL,
                'Breed' TEXT NOT NULL,
                'Breed_Id' INTEGER NOT NULL,
                'Mix' TEXT NOT NULL,
                'MixBreed' TEXT,
                'MixBreed_Id' INTEGER,
                'City' TEXT NOT NULL,
                'State' TEXT NOT NULL,
                'Country' TEXT NOT NULL,
                'Age' TEXT NOT NULL,
                'Sex' TEXT NOT NULL,
                'Size' TEXT NOT NULL,
                'Description' TEXT,
                'ShelterId' INTEGER NOT NULL
            );
        '''
        cur.execute(statement)
        conn.commit()
        return True



def insert_dogs(dog_dict, db_name= DBNAME):
    try:
        conn = sqlite3.connect(db_name)
        cur = conn.cursor()
        for breed in list(dog_dict.keys()):
            for dog in dog_dict[breed]:
                insertion = (dog.id, dog.name, dog.breed1, dog.breed2, dog.city, dog.state, dog.country, dog.age, dog.sex, dog.size, dog.details, dog.shelter_id, dog.mix, 0, 0)
                statement = 'INSERT INTO Dogs (Id, Name, Breed, MixBreed, City, State, Country, Age, Sex, Size, Description, ShelterId, Mix, Breed_Id, MixBreed_Id) '
                statement += 'VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)'
                cur.execute(statement, insertion)
                conn.commit()
        conn.close()

    except Exception as e:
        print(e)

def update_dogs(conn, cur):
    statement= '''update Dogs set MixBreed_Id = null where dogs.Id in
    (select dogs.id from dogs where dogs.MixBreed is Null) '''
    cur.execute(statement)
    conn.commit()



############################################################
#
#   DATABASE - Images
#
#
############################################################

def check_images(conn, cur):
    try:
        simple_check = "SELECT * FROM 'Images'"
        cur.execute(simple_check)
        print("Image Table Exists")
        return False
    except:
        print("Creating Table")
        statement = '''
            CREATE TABLE 'Images' (
                'Id' INTEGER PRIMARY KEY AUTOINCREMENT,
                'Breed' TEXT,
                'Breed_Id' INTEGER ,
                'Image_Url' TEXT,
                'Title' TEXT,
                'Username' TEXT,
                'Content_Url' TEXT,
                'License_Url' TEXT
            );
        '''
        cur.execute(statement)
        conn.commit()
        return True


def insert_images(img_dict, db_name= DBNAME):
    try:
        conn = sqlite3.connect(db_name)
        cur = conn.cursor()
        img_keys = sorted(list(img_dict.keys()))
        for key in img_keys:
            img = img_dict[key]
            insertion = (key, img.image_url, img.title, img.username, img.content_url, img.license_url, 0)
            statement = 'INSERT INTO Images (Breed, Image_Url, Title, Username, Content_Url, License_Url, Breed_Id) '
            statement += 'VALUES (?, ?, ?, ?, ?, ?, ?)'
            cur.execute(statement, insertion)
            conn.commit()
        conn.close()

    except Exception as e:
        print(e)





############################################################
#
#   DATABASE - Breeds
#
#
############################################################


def check_breeds(conn, cur):
    try:
        simple_check = "SELECT * FROM 'Breeds'"
        cur.execute(simple_check)
        print("Breed Table Exists")
        return False
    except:
        print("Creating Table")
        statement = '''
            CREATE TABLE 'Breeds' (
                'Id' INTEGER PRIMARY KEY AUTOINCREMENT,
                'Breed' TEXT,
                'Group' TEXT,
                'Origin' TEXT,
                'Other' TEXT,
                'Other' TEXT,
                'Other' TEXT
            );
        '''
        cur.execute(statement)
        conn.commit()
        return True



def insert_breeds(breed_dict, db_name= DBNAME):
    try:
        conn = sqlite3.connect(db_name)
        cur = conn.cursor()
        img_keys = sorted(list(breed_dict.keys()))
        for key in img_keys:
            img = img_dict[key]
            insertion = (key, img.image_url, img.title, img.username, img.content_url, img.license_url, 0)
            statement = 'INSERT INTO Images (Breed, Image_Url, Title, Username, Content_Url, License_Url, Breed_Id) '
            statement += 'VALUES (?, ?, ?, ?, ?, ?, ?)'
            cur.execute(statement, insertion)
            conn.commit()
        conn.close()

    except Exception as e:
        print(e)






############################################################
#
#   DATABASE - Calling all of the above code
#
#
############################################################




def init_db(db_name, dog_dict, shelter_dict, img_dict):
    try:
        conn = sqlite3.connect(db_name)
        cur = conn.cursor()
        checka = check_dogs(conn, cur)
        checkb = check_shelters(conn, cur)
        checkc = check_images(conn, cur)
        if checka:
            insert_dogs(dog_dict, db_name = db_name)
            update_dogs(conn, cur)
        if checkb:
             insert_shelters(shelter_dict, db_name = db_name)
             update_shelters(conn, cur)
        if checkc:
            insert_images(img_dict, db_name = db_name)
        conn.close()
    except Exception as e:
        print(e)




breed_data = get_api_data()
breed_list = dog_breed_list(breed_data)
uncleaned_dog_dict = all_available_dogs_dict(breed_list)

# cleaned dog dictionary of availabe dogs on petfinder
DOG_DICT = clean_dog_dict(uncleaned_dog_dict)

# shelter dictionary of shelters on petfinder from DOG_DICT
SHELTER_DICT = create_shelters(get_shelter_dict(DOG_DICT))


init_db(DBNAME, DOG_DICT, SHELTER_DICT, BREED_IMGS)



# try:
#     conn = sqlite3.connect(DBNAME)
#     cur = conn.cursor()
#     statement = '''select dogs.Breed from Dogs
# group by breed '''
#
#     bars_data = conn.execute(statement)
#     line = bars_data.fetchall()
#
#     print(len(line))
#     print(len(DOG_DICT))
#     key_list = list(DOG_DICT.keys())
#     # print(key_list)
#     # for i in range(len(key_list)):
#     #     print(line[i], key_list[i])
#
#
# except Exception as e:
#     print(e)

print('\n')
print("***"*20)
############################################
