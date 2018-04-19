
from mapping import *
DBNAME = 'dogs.db'

app_breed_list = []
app_map_list = []

def init_breeds(list_of_breeds = DISPLAY_BREED_LIST, list_of_images = DISPLAY_IMAGE_LIST):
    global app_breed_list
    for breed in list_of_breeds:
        breed_display = []
        breed_display.append(breed.id)
        breed_display.append(breed.breed)
        breed_display.append(breed.breed_group)
        breed_display.append(breed.origin)
        breed_display.append(breed.count)
        app_breed_list.append(breed_display)
    for li in app_breed_list:
        looking = li[0]
        for image in list_of_images:
            if looking == image.breed_id:
                li.append(image.content_url)

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

def get_maps(to_look_up = 1, shelters = DISPLAY_SHELTER_LIST, dogs = DISPLAY_DOG_LIST, breeds = DISPLAY_BREED_LIST):
    i = int(to_look_up) - 1
    breed = DISPLAY_BREED_LIST[i].breed
    return plot_sites_for_shelter(DISPLAY_SHELTER_LIST, DISPLAY_DOG_LIST, breed)

def get_images(number, images = DISPLAY_IMAGE_LIST):
    i = int(number) - 1
