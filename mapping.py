import sqlite3
import plotly.plotly as py


DBNAME = 'dog.db'


class Display_Shelter():
    def __init__(self, row):
        self.id = row[0]
        self.name = row[1]
        self.city = row[2]
        self.state = row[3]
        self.country = row[4]
        self.lat = row[5]
        self.lon = row[6]
    def __str__(self):
        return self.id

class Display_Breed():
    def __init__(self, row):
        self.id = row[0]
        self.breed = row[1]
        self.breed_group = row[2]
        self.origin = row[3]
        self.height = row[4]
        self.weight = row[5]
        self.coat = row[6]
        self.color = row[7]
        self.life_span = row[8]
        self.litter_size = row[9]
        self.count = row[10]
    def __str__(self):
        return self.id


class Display_Image():
    def __init__(self, row):
        self.id = row[0]
        self.breed = row[1]
        self.breed_id = row[2]
        self.image_url = row[3]
        self.title = row[4]
        self.username = row[5]
        self.content_url = row[6]
        self.license_url = row[7]
    def __str__(self):
        return self.id

class Display_Dog():
    def __init__(self, row):
        self.id = row[0]
        self.name = row[1]
        self.breed = row[2]
        self.breed_id = row[3]
        self.mix = row[4]
        self.mixbreed = row[5]
        self.mixbreed_id = row[6]
        self.city = row[7]
        self.state = row[8]
        self.country = row[9]
        self.age = row[10]
        self.sex = row[11]
        self.size = row[12]
        self.description = row[13]
        self.shelter_id = row[14]
    def __str__(self):
        if self.mix == "No":
            return("Hi! I'm {}  -  a(n) {}".format(self.name, self.breed))
        else:
            return("Hi! I'm {}  -  a(n) {} Mix".format(self.name, self.breed))


def generate_display_shelters(db_name = DBNAME):
    listing = []
    try:
        conn = sqlite3.connect(db_name)
        cur = conn.cursor()
        sql = 'SELECT * FROM Shelters'
        results = cur.execute(sql)
        result_list = results.fetchall()
        for tupp in result_list:
            listing.append(Display_Shelter(tupp))
        conn.close()
    except Exception as e:
        print(e)
    return listing

def generate_display_dogs(db_name = DBNAME):
    listing = []
    try:
        conn = sqlite3.connect(db_name)
        cur = conn.cursor()
        sql = 'SELECT * FROM Dogs'
        results = cur.execute(sql)
        result_list = results.fetchall()
        for tupp in result_list:
            listing.append(Display_Dog(tupp))
        conn.close()
    except Exception as e:
        print(e)
    return listing

def generate_display_images(db_name = DBNAME):
    listing = []
    try:
        conn = sqlite3.connect(db_name)
        cur = conn.cursor()
        sql = 'SELECT * FROM Images'
        results = cur.execute(sql)
        result_list = results.fetchall()
        for tupp in result_list:
            listing.append(Display_Image(tupp))
        conn.close()
    except Exception as e:
        print(e)
    return listing

def generate_display_breeds(db_name = DBNAME):
    listing = []
    try:
        conn = sqlite3.connect(db_name)
        cur = conn.cursor()
        sql = 'SELECT * FROM Breeds'
        results = cur.execute(sql)
        result_list = results.fetchall()
        for tupp in result_list:
            listing.append(Display_Breed(tupp))
        conn.close()
    except Exception as e:
        print(e)
    return listing








def get_geo_dict(shelter_list, dog_list, breed_type):
    parsing = []
    text = []
    for dog in dog_list:
        if dog.breed != breed_type:
            pass
        else:
            parsing.append(dog.shelter_id)
            text.append(str(dog))
    site_dict = {}
    lons = []
    lats = []

    for shell in shelter_list:
        if shell.country != "USA":
            pass
        if shell.id not in parsing:
            pass
        else:
            lons.append(shell.lon)
            lats.append(shell.lat)


    site_dict['lon'] = lons
    site_dict['lat'] = lats
    site_dict['text'] = text
    return site_dict


def plot_trace(site_dict, name= "object", symb = 'line', col = 'red', size = 15):
    trace1 = dict(
            type = 'scattergeo',
            locationmode = 'USA-states',
            lon = site_dict['lon'],
            lat = site_dict['lat'],
            text = site_dict['text'],
            mode = 'markers',
            name = name,
            marker = dict(
                size = size,
                symbol = symb,
                color = col
            ))
    data = [trace1]
    return data



def find_max_vals(site_dict):
    min_lat = 10000
    max_lat = -10000
    min_lon = 10000
    max_lon = -10000

    lat_vals = site_dict['lat']
    lon_vals = site_dict['lon']
    for str_v in lat_vals:
        v = float(str_v)
        if v < min_lat:
            min_lat = v
        if v > max_lat:
            max_lat = v
    for str_v in lon_vals:
        v = float(str_v)
        if v < min_lon:
            min_lon = v
        if v > max_lon:
            max_lon = v
    max_dict = {'lat_axis': [min_lat, max_lat],
    'lon_axis': [min_lon, max_lon]}
    return max_dict


def layout_lats(max_dict):
    max_lat = max_dict['lat_axis'][1]
    min_lat = max_dict['lat_axis'][0]
    max_lon = max_dict['lon_axis'][1]
    min_lon = max_dict['lon_axis'][0]
    center_lat = (max_lat+min_lat) / 2
    center_lon = (max_lon+min_lon) / 2

    max_range = max(abs(max_lat - min_lat), abs(max_lon - min_lon))
    padding = max_range * .20
    lat_axis = [min_lat - padding, max_lat + padding]
    lon_axis = [min_lon - padding, max_lon + padding]
    pad_dict = {}
    pad_dict['lat_pad'] = lat_axis
    pad_dict['lon_pad'] = lon_axis
    pad_dict['lat_cen'] = center_lat
    pad_dict['lon_cen'] = center_lon
    return pad_dict



def plot_layout(pad_dict):
    layout = dict(
            title = 'Adoption Shelters',
            geo = dict(
                scope='usa',
                projection=dict( type='albers usa' ),
                showland = True,
                landcolor = "rgb(250, 250, 250)",
                subunitcolor = "rgb(100, 217, 217)",
                countrycolor = "rgb(217, 100, 217)",
                lataxis = {'range': pad_dict['lat_pad']},
                lonaxis = {'range': pad_dict['lon_pad']},
                center= {'lat': pad_dict['lat_cen'], 'lon': pad_dict['lon_cen']},
                countrywidth = 3,
                subunitwidth = 3
            ),
        )
    return layout


def plot_sites_for_shelter(shelter_list, dog_list, breed_type):
    site_dict = get_geo_dict(shelter_list, dog_list, breed_type)
    data = plot_trace(site_dict, "Adoption Shelters")
    layout = plot_layout(layout_lats(find_max_vals(site_dict)))

    fig = dict(data=data, layout=layout )
    py.plot( fig, validate=False, filename='Adoption Shelters Across USA')




DISPLAY_SHELTER_LIST = generate_display_shelters()
DISPLAY_DOG_LIST = generate_display_dogs()
DISPLAY_IMAGE_LIST = generate_display_images()
DISPLAY_BREED_LIST = generate_display_breeds()





# plot_sites_for_shelter(DISPLAY_SHELTER_LIST, DISPLAY_DOG_LIST, 'Boston Terrier')
