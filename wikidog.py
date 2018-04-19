#   this file takes a long time to run even with the cache, thats why I have it seperate
import sqlite3
import requests
import json
from bs4 import BeautifulSoup
from nato import *
from secrets import *
import time


print("***"*20)
print('\n')

DBNAME = 'dog.db'
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
    def __init__(self, breed, breed_dict = None, group_dict = BREED_GROUPS):
        self.kind = breed
        self.group = group_dict[self.kind]
        self.origin = "Unknown"
        self.coat = "Unknown"
        self.color = "Unknown"
        self.life_span = "Unknown"
        self.litter_size = "Unknown"
        self.weight = "Unknown"
        self.height = "Unknown"
        if breed_dict != None:
            self.origin = breed_dict['origin'].title().strip()
            self.coat = breed_dict['coat'].capitalize().strip()
            self.color = breed_dict['color'].capitalize().strip()
            self.life_span = breed_dict['life-span'].capitalize().strip()
            self.litter_size = breed_dict['litter-size'].capitalize().strip()
            self.weight = breed_dict['weight'].capitalize().strip(':').strip("_").strip('~').strip()
            self.height = breed_dict['height'].capitalize().strip(':').strip("_").strip('~').strip()

    def __str__(self):
        return ('{}, {}, {}, {}, {}, {}, {}, {}, {}'.format(self.kind, self.origin, self.group, self.coat, self.color, self.life_span, self.litter_size, self.weight, self.height))


def time_delay(number = 15):
    for i in range(number):
        print(number-i)
        time.sleep(1)


def soup_it(nps):
    soup = BeautifulSoup(nps, "html.parser")
    return soup

CALLING_LIMIT = 0
DUMMY3 = True
DUMMY4 = True
def soup_data_cache(search_url):
    global DUMMY3
    global DUMMY4
    global CALLING_LIMIT
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
            CALLING_LIMIT += 1
            print(CALLING_LIMIT, "Getting fresh data")
        return (soup_it(data))

def get_wiki_data(search):
    search_url = 'https://en.wikipedia.org/wiki/{}?action=render'.format(search)
    wiki_data = soup_data_cache(search_url)

    return wiki_data

def create_breed_dictionary(rows):
    dog_breed = {}
    dog_breed['origin'] = "Unknown"
    dog_breed['coat'] = "Unknown"
    dog_breed['color'] = "Unknown"
    dog_breed['life-span'] = "Unknown"
    dog_breed['litter-size'] = "Unknown"
    dog_breed['weight'] = "Unknown"
    dog_breed['height'] = "Unknown"
    for row in rows:
        if (type(row.th)) == (type(None)):
            pass
        elif (type(row.td)) == (type(None)):
            pass
        else:
            heading = str(row.th.text.lower().replace('\n', ' ').replace('\xa0', '-')).split('[')[0]
            texting = str(row.td.text.lower().replace('\n', ' ').replace('\xa0', '-')).split('[')[0]
            if heading == "origin":
                dog_breed[heading] = texting
            elif heading == 'coat':
                dog_breed[heading] = texting
            elif heading == 'color':
                dog_breed[heading] = texting
            elif heading == 'colour':
                dog_breed['color'] = texting
            elif heading =='life-span':
                dog_breed[heading] = texting
            elif heading == 'litter-size':
                dog_breed[heading] = texting
            else:
                pass
    return dog_breed


def create_wiki_dict(breed_list):
    wiki_dict = {}
    not_found = []
    timer = 0
    for breed in breed_list:
        breed_to_search = breed.split('/')[0].strip()
        if breed == "Husky":
            breed_to_search = ("Siberian" + breed)
        elif breed == 'Wirehaired Terrier':
            breed_to_search = ('Wire Fox Terrier')
        elif breed == 'Yorkshire Terrier Yorkie':
            breed_to_search = ('Yorkshire Terrier')
        elif breed == "Yellow Labrador Retriever":
            breed_to_search = ('Labrador Retriever')
        elif breed == 'Black Labrador Retriever':
            breed_to_search = ('Labrador Retriever')
        elif breed == 'Chocolate Labrador Retriever':
            breed_to_search = ('Labrador Retriever')
        elif breed == 'West Highland White Terrier Westie':
            breed_to_search = 'West Highland White Terrier'
        elif breed == 'Eskimo Dog':
            breed_to_search = "American Eskimo Dog"
        elif breed == "Collie":
            breed_to_search = 'Border Collie'
        else:
            pass
        info = get_wiki_data(breed_to_search)
        try:
            try:
                table = info.find('table', attrs = {'class': 'infobox biota'})
                rows = table.find_all('tr')
            except:
                try:
                    info = get_wiki_data((breed_to_search + '%20dog'))
                    table = info.find('table', attrs = {'class': 'infobox biota'})
                    rows = table.find_all('tr')
                except:
                    pass
            timer = (breed_list.index(breed))
            timer += 1
            # print("*****"+ str(timer) + "*****")
            # time_delay(20)
            dog_breed = create_breed_dictionary(rows)

            table_text = []
            for row in rows:
                for stuff in row.contents:
                    try:
                        table_text.append((stuff.text).lower())
                    except:
                        pass
            new_table_text = []
            for item in table_text:
                more = item.replace(' ', '_').replace('\n', ' ').replace('\xa0', '-').replace('male', '').replace('female',
                '').replace('traits', '').replace(';', '').strip().split()
                new_table_text.append(more)
            cleaner_table_text = []
            for item in new_table_text:
                if (len(item)) > 1:
                    for x in item:
                        cleaner_table_text.append(x)
            if 'weight' in cleaner_table_text:
                to_index = (cleaner_table_text.index('weight')) + 1
                dog_breed['weight'] = (cleaner_table_text[to_index].split('[')[0])
            if 'height' in cleaner_table_text:
                to_index = (cleaner_table_text.index('height')) + 1
                dog_breed['height'] = (cleaner_table_text[to_index].split('[')[0])

            wiki_dict[breed] = Breed(breed, dog_breed)
        except:
            not_found.append(breed)
    # print(not_found)
    return wiki_dict




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
                'Breed_Group' TEXT,
                'Origin' TEXT,
                'Height' TEXT,
                'Weight' TEXT,
                'Coat' TEXT,
                'Color' TEXT,
                'Life_Span' TEXT,
                'Litter_Size' TEXT

            );
        '''
        cur.execute(statement)
        conn.commit()
        return True


def insert_breeds(breed_dict, db_name= DBNAME):
    try:
        conn = sqlite3.connect(db_name)
        cur = conn.cursor()
        breed_keys = sorted(list(breed_dict.keys()))
        for key in breed_keys:
            breed = breed_dict[key]
            insertion = (breed.kind, breed.group, breed.origin, breed.height, breed.weight, breed.coat, breed.color, breed.life_span, breed.litter_size)
            statement = 'INSERT INTO Breeds (Breed, Breed_Group, Origin, Height, Weight, Coat, Color, Life_Span, Litter_Size) '
            statement += 'VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)'
            cur.execute(statement, insertion)
            conn.commit()
        conn.close()

    except Exception as e:
        print(e)



def update_tables_from_breeds(conn, cur):
    statement= '''
    update Images set Breed_Id = (select Breeds.Id FROM Breeds  WHERE Breeds.Breed = Images.Breed )
    WHERE EXISTS (  SELECT *  FROM Breeds  WHERE Breeds.Breed = Images.Breed  ) '''
    cur.execute(statement)
    conn.commit()
    statement= '''
    update Dogs set Breed_Id = (select Breeds.Id FROM Breeds WHERE Breeds.Breed = Dogs.Breed )
    WHERE EXISTS ( SELECT * FROM Breeds WHERE Breeds.Breed = Dogs.Breed ) '''
    cur.execute(statement)
    conn.commit()
    statement='''
    update Dogs  set MixBreed_Id = (select Breeds.Id 	FROM Breeds  WHERE Breeds.Breed = Dogs.MixBreed )
    WHERE EXISTS  (  SELECT * FROM Breeds WHERE Breeds.Breed = Dogs.MixBreed  ) '''
    cur.execute(statement)
    conn.commit()

def alter_breeds_table(conn, cur):
    statement= '''ALTER TABLE Breeds ADD COLUMN Tally INT'''
    cur.execute(statement)
    conn.commit()
    statement=   ''' update Breeds set Tally = ( select count(*) FROM Dogs where
    breeds.id = dogs.Breed_Id group by breed ) WHERE EXISTS
    (  SELECT *  FROM Dogs  where breeds.id = dogs.Breed_Id group by breed ) '''
    cur.execute(statement)
    conn.commit()
    statement = ''' update Breeds set tally = 0 where tally is Null '''
    cur.execute(statement)
    conn.commit()

def init_db_breeds(db_name, dog_breeds):
    try:
        conn = sqlite3.connect(db_name)
        cur = conn.cursor()
        checkd = check_breeds(conn, cur)
        if checkd:
            insert_breeds(dog_breeds, db_name = db_name)
            update_tables_from_breeds(conn, cur)
            alter_breeds_table(conn, cur)
    except Exception as e:
        print(e)



############################################################
#
#   Calling Code
#
#
############################################################




DOG_BREED_DICT = create_wiki_dict(LIST_OF_BREEDS)
init_db_breeds(DBNAME, DOG_BREED_DICT)

print('\n')
print("***"*20)
