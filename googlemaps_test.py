import googlemaps
from pprint import pprint as pp

API_KEY = 'AIzaSyC6ShfxX_32v448NTO_xj-J9Wit9kNSLyg'
map_client = googlemaps.Client(API_KEY)


def get_lat_long(response):
    """get latitude and longitude for current location and destination from directions response"""
    current_location_coord = response[0]['legs'][0]['start_location']
    destination_coord = response[0]['legs'][0]['end_location']
    return dict_val_to_tuple(current_location_coord), dict_val_to_tuple(destination_coord)


def get_steps_coord(response):
    """get latitude and longitude for end point of every step"""
    steps = []
    for step in response[0]['legs'][0]['steps']:
        steps.append(dict_val_to_tuple(step['end_location']))
    return steps


def dict_val_to_tuple(dict):
    """convert dictionary values to a tuple (necessary for folium)"""
    list = []
    for val in dict.values():
        list.append(val)
    return tuple(list)


current_location = '12 Bolton Drive, Glasgow, G42 9DY'
destination = 'Phillies of Shawland'
response = map_client.directions(current_location, destination, mode='walking')

current_location_coord, destination_coord = get_lat_long(response)
steps_coord = get_steps_coord(response)
print(steps_coord)

# pp(response)
print(current_location_coord)
print(destination_coord)
