
from mapping import *


app_breed_list = []
app_dog_list = []

def init_breeds(list_of_breeds = DISPLAY_BREED_LIST, list_of_images = DISPLAY_IMAGE_LIST):
    global app_breed_list
    app_breed_list = []
    for breed in list_of_breeds:
        breed_display = []
        breed_display.append(breed.id)
        breed_display.append(breed.breed)
        breed_display.append(breed.breed_group)
        breed_display.append(breed.origin)
        breed_display.append(breed.count)
        app_breed_list.append(breed_display)

    for li in app_breed_list:
        looking = int(li[0])
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
    img = images[i]
    return img

def get_breed_details(number, breed= DISPLAY_BREED_LIST):
    i = int(number) - 1
    kind = breed[i]
    return kind



def get_dogs(number, list_of_dogs = DISPLAY_DOG_LIST):
    global app_dog_list
    app_dog_list = []
    i = int(number)
    for dog in list_of_dogs:
        dog_display = []
        if dog.breed_id == i:
            dog_display.append(dog.id)
            dog_display.append(dog.name)
            dog_display.append(dog.breed)
            if dog.mixbreed == None:
                dog_display.append(" ")
            else:
                dog_display.append(dog.mixbreed)
            dog_display.append(dog.city)
            dog_display.append(dog.state)
            dog_display.append(dog.sex)
            dog_display.append(dog.age)
            dog_display.append(dog.size)
        if len(dog_display) > 0:
            app_dog_list.append(dog_display)

def get_dogs_listing(sortby='name', sortorder='asc'):
    if sortby == 'mixbreed':
        sortcol = 3
    elif sortby == 'state':
        sortcol = 5
    elif sortby == 'age':
        sortcol = 7
    elif sortby == 'size':
        sortcol = 8
    else:
        sortcol = 1
    rev = (sortorder == 'desc')
    sorted_list = sorted(app_dog_list, key=lambda row: row[sortcol], reverse=rev)
    return sorted_list
