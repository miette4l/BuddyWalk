import math

import googlemaps
from haversine import haversine, Unit
from utils.api_key import GOOGLE_API_KEY


gmaps = googlemaps.Client(key=GOOGLE_API_KEY)


def geocode(loc: str) -> tuple:
    """
    Turn a location string into a gmaps geocode response
    """
    geocoded = gmaps.geocode(loc)[0]['geometry']['location']
    return geocoded


def degrees_to_rads(degrees: float) -> float:
    """Convert from degrees to radians"""
    rads = degrees * math.pi / 180
    return rads


def rads_to_degrees(rads: float) -> float:
    """Convert from radians to  degrees"""
    degrees = rads * 180 / math.pi
    return degrees


def midpoint(location1, location2) -> dict:
    """create halfway point meeting point between two locations"""

    if isinstance(location1, str):
        # check if locations are str type
        loc1 = geocode(location1)
        loc2 = geocode(location2)

        loc1_lat = loc1['lat']
        loc1_lng = loc1['lng']
        loc2_lat = loc2['lat']
        loc2_lng = loc2['lng']

    elif isinstance(location1, tuple):
        # if location are already tuples (lat, lng) execute this
        loc1_lat = rads_to_degrees(location1[0])
        loc1_lng = rads_to_degrees(location1[1])
        loc2_lat = rads_to_degrees(location2[0])
        loc2_lng = rads_to_degrees(location2[1])

    else:
        raise ValueError("Wrong location input type")

    midpoint_lat = (loc1_lat + loc2_lat) / 2
    midpoint_lng = (loc1_lng + loc2_lng) / 2

    coords = (midpoint_lat, midpoint_lng)
    address = gmaps.reverse_geocode(coords)[0]['address_components']
    short_address = address[0]['long_name'] + " " + address[1]['long_name']

    midpoint_data = {'coords': coords, 'address': short_address}

    return midpoint_data


def check_in_range(curr_loc_coords: tuple, range_d=10) -> bool:
    """
    Check location inputs are within range of London
    """
    london = (51.509865, -0.118092)  # app is currently only for London use
    curr_loc_coords = (float(val) for val in curr_loc_coords)
    distance = haversine(curr_loc_coords, london, unit=Unit.MILES)
    if distance < range_d:
        return True
    return False


def check_journey_length(curr_loc_coords: tuple, dest_coords: tuple, journey_len=10) -> bool:
    """
    Check the journey length is short enough to walk
    """
    curr_loc_coords = (float(val) for val in curr_loc_coords)
    dest_coords = (float(val) for val in dest_coords)
    distance = haversine(curr_loc_coords, dest_coords, unit=Unit.MILES)
    if distance < journey_len:
        return True
    return False
