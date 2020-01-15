# %%
import requests
import json

def get_closest_city(lat, long):
# %%
    api_key_file = open("../../api_key.txt",'r')
    api_key = api_key_file.readline()[:-1]
    api_key_file.close()

    lat = 40.714224
    long = -73.714224

    url = f'https://maps.googleapis.com/maps/api/geocode/json?latlng={lat},{long}&key={api_key}'

    rev_geocode = requests.get(url)
    rev_geocode_json = json.loads(rev_geocode.json())

    first_address = rev_geocode.json()['results'][0]['address_components']

    country = ''
    state = ''
    city = ''

    for i in first_address:
        cur_type = i['types'][0]
        if cur_type == 'country':
            country = i['short_name']
        elif cur_type == 'administrative_area_level_1':
            state = i['short_name']
        elif cur_type == 'administrative_area_level_3':
            city = i['short_name']

    return country, state, city
