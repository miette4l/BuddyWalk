from pprint import pprint as pp

import folium
import googlemaps


class Route:

    def __init__(self, current_loc, destination):
        self.current_loc = current_loc
        self.destination = destination

        # initialise googlemaps client and call response
        API_KEY = 'AIzaSyC6ShfxX_32v448NTO_xj-J9Wit9kNSLyg'
        map_client = googlemaps.Client(API_KEY)
        self.response = map_client.directions(current_loc, destination, mode='walking')

    def get_current_loc_coord(self):
        """get latitude and longitude for current location"""
        # get coordinates from response
        self.current_location_coord = self.response[0]['legs'][0]['start_location']
        self.current_location_coord = tuple(list(self.current_location_coord.values()))
        return self.current_location_coord

    def get_destination_coord(self):
        """get latitude and longitude for destination"""
        # get coordinates from response
        self.destination_coord = self.response[0]['legs'][0]['end_location']
        self.destination_coord = tuple(list(self.destination_coord.values()))
        return self.destination_coord

    def get_steps_coord(self):
        """get latitude and longitude for steps"""
        self.steps = []
        for step in self.response[0]['legs'][0]['steps']:
            self.steps.append(tuple(list(step['end_location'].values())))
        return self.steps

    def print_response(self):
        pp(self.response)


def create_map(current_location_coord, destination_coord, steps_coord):
    """Create map from coordinates with markers for current location and destination.
    Line plotted from steps coordinates."""
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
