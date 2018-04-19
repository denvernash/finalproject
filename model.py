
from mapping import *
DBNAME = 'dogs.db'

app_breed_list = []
app_map_list = []

def init_breeds(list_of_breeds = DISPLAY_BREED_LIST):
    global app_breed_list
    for breed in list_of_breeds:
        breed_display = []
        breed_display.append(breed.id)
        breed_display.append(breed.breed)
        breed_display.append(breed.breed_group)
        breed_display.append(breed.origin)
        breed_display.append(breed.count)
        app_breed_list.append(breed_display)


def get_breeds_listing(sortby='breed', sortorder='asc'):
    if sortby == 'breed':
        sortcol = 1
    elif sortby == 'breed_group':
        sortcol = 2
    elif sortby == 'origin':
        sortcol = 3
    elif sortby == 'count':
        sortcol = 4
    else:
        sortcol = 0
    rev = (sortorder == 'desc')
    sorted_list = sorted(app_breed_list, key=lambda row: row[sortcol], reverse=rev)
    return sorted_list

def get_maps(shelters = DISPLAY_SHELTER_LIST, dogs = DISPLAY_DOG_LIST, breed = 'Boston Terrier'):
    pass
