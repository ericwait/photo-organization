# %% 
from os import path
from GPSPhoto import gpsphoto
from location import get_closest_city

# %%
root_dir = 'C:/Users/eric/Desktop/test-images'
file_name = '2020-01-01_15-34-28.jpg'

file_path = path.join(root_dir, file_name)

# %%
data = gpsphoto.getGPSData(file_path)
country, state, city = get_closest_city(data['Latitude'], data['Longitude'])
print(f'Country:{country} State:{state} City:{city}')
