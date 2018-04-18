





def plot_trace(site_dict, name= "object", symb = 'star', col = 'purple', size = 15):
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
    padding = max_range * .10
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
            title = 'National Sites and Nearby Places',
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
