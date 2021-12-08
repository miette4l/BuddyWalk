import googlemaps
import gmaps
from pprint import pprint as pp

API_KEY = 'AIzaSyC6ShfxX_32v448NTO_xj-J9Wit9kNSLyg'
map_client = googlemaps.Client(API_KEY)

def get_lat_long(response):
    """get latitude and longitute for current location and destination from directions response"""
    current_location_coord = response[0]['legs'][0]['start_location']
    destination_coord = response[0]['legs'][0]['end_location']
    return current_location_coord, destination_coord


current_location = '12 Bolton Drive, Glasgow, G42 9DY'
destination = 'Phillies of Shawland'
response = map_client.directions(current_location, destination, mode='walking')

current_location_coord, destination_coord = get_lat_long(response)


# pp(response)
print(current_location_coord)
print(destination_coord)

#print(current_location_coord.values())

### THIS DOES NOT WORK YET
# configure api
gmaps.configure(api_key=API_KEY)

# Create the map
fig = gmaps.figure()
# create the layer
layer = gmaps.directions.Directions(current_location_coord.values(), destination_coord.values(), mode='walking')
# Add the layer
fig.add_layer(layer)
fig