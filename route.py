import googlemaps
import folium
from pprint import pprint as pp


class Route:

    def __init__(self, current_loc, destination):
        self.current_loc = current_loc
        self.destination = destination

        # initialise googlemaps client and call response
        API_KEY = 'AIzaSyC6ShfxX_32v448NTO_xj-J9Wit9kNSLyg'
        map_client = googlemaps.Client(API_KEY)
        self.response = map_client.directions(current_location, destination, mode='walking')

        # get coordinates from response
        self.current_location_coord = self.response[0]['legs'][0]['start_location']
        self.current_location_coord = tuple(list(self.current_location_coord.values()))

        self.destination_coord = self.response[0]['legs'][0]['end_location']
        self.destination_coord = tuple(list(self.destination_coord.values()))

        self.steps = []
        for step in self.response[0]['legs'][0]['steps']:
            self.steps.append(tuple(list(step['end_location'].values())))

    def get_current_loc_coord(self):
        """get latitude and longitude for current location"""
        return self.current_location_coord

    def get_destination_coord(self):
        """get latitude and longitude for destination"""
        return self.destination_coord

    def get_steps_coord(self):
        """get latitude and longitude for steps"""
        return self.steps

    def print_response(self):
        pp(self.response)


current_location = '12 Bolton Drive, Glasgow, G42 9DY'
destination = 'Philies of Shwland'

route = Route(current_location, destination)
#route.print_response()

current_location_coord = route.get_current_loc_coord()
destination_coord = route.get_destination_coord()
steps_coord = route.get_steps_coord()

# print(current_location_coord)
# print(destination_coord)
# print(steps_coord)

# instantiate folium map
f_map = folium.Map(location=current_location_coord)

# creates and adds marker on map for start and end location
marker_dest = folium.Marker(destination_coord)
marker_dest.add_to(f_map)
marker_loc = folium.Marker(current_location_coord)
marker_loc.add_to(f_map)

# create line between two points
folium.PolyLine(steps_coord, color="green", weight=2.5, opacity=1).add_to(f_map)

# create empty html file
html_page = 'f_map.html'
# save map to html file
f_map.save(html_page)





