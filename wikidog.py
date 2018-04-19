import requests
import json
from bs4 import BeautifulSoup
from nato import *
from secrets import *
import time


print("***"*20)
print('\n')


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
    def __init__(self, breed, breed_dict = None):
        self.kind = breed
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
        return ('{}, {}, {}, {}, {}, {}, {}, {}'.format(self.kind, self.origin, self.coat, self.color, self.life_span, self.litter_size, self.weight, self.height))



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
            info = get_wiki_data("Siberian" + breed)
        elif breed == 'Wirehaired Terrier':
            info = get_wiki_data('Wire Fox Terrier')
        else:
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


DOG_BREED_DICT = create_wiki_dict(LIST_OF_BREEDS)

for key in DOG_BREED_DICT:
    pass
    # print(DOG_BREED_DICT[key])
    # print('\n')
print((DOG_BREED_DICT['Husky']))



print('\n')
print("***"*20)
