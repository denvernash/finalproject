#model.py
import csv

DBNAME = 'dogs.db'

dogs_list = []


def init_dogs(db_name=DBNAME):
    global dogs_list
    with open(csv_file_name) as f:
        reader = csv.reader(f)
        next(reader) # throw away headers
        next(reader) # throw away headers
        global bb_seasons
        bb_seasons = [] # reset, start clean
        for r in reader:
            r[3] = int(r[3])
            r[4] = int(r[4])
            r[5] = float(r[5])
            bb_seasons.append(r)


def get_dogs_listing(sortby='breed', sortorder='asc'):
    if sortby == 'breed':
        sortcol = 1
    elif sortby == 'breed_group':
        sortcol = 2
    elif sortby == 'origin':
        sortcol = 3
    else:
        sortcol = 0
