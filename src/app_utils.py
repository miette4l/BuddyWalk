import datetime
import math
import uuid

import googlemaps
from haversine import haversine, Unit

gmaps = googlemaps.Client(key='AIzaSyDzj7gfcouVFtZAyzntCmyDUs8g_8s_yTM')


def geocode(loc: str) -> tuple:
    geocoded = gmaps.geocode(loc)[0]['geometry']['location']
    return geocoded


def process_input(data: dict) -> dict:
    user = {}

    user['user_id'] = str(uuid.uuid1())
    user['username'] = data['username']
    user['phone_no'] = int(data['phone_no'])
    user['curr_loc'] = geocode(data['current_loc'])  # convert to lat, lng using gmaps.geocode
    user['curr_loc_lat'] = user['curr_loc']['lat']  # unit: latitude in degrees
    user['curr_loc_lng'] = user['curr_loc']['lng']  # unit: longitude in degrees
    user['curr_loc_coords'] = (user['curr_loc_lat'], user['curr_loc_lng'])  # create (lat, lng) tuple
    user['destination'] = geocode(data['destination'])
    user['destination_lat'] = user['destination']['lat']
    user['destination_lng'] = user['destination']['lng']
    user['dest_coords'] = (user['destination_lat'], user['destination_lng'])
    user['tod'] = data['tod']  # 'tod' = 'Time of Departure' as iso-format string

    return user


def check_in_range(curr_loc_coords: tuple, range_d=10) -> bool:
    london = (51.509865, -0.118092)  # app is currently only for London use
    curr_loc_coords = (float(val) for val in curr_loc_coords)
    distance = haversine(curr_loc_coords, london, unit=Unit.MILES)
    if distance < range_d:
        return True
    return False


def check_journey_length(curr_loc_coords: tuple, dest_coords: tuple, journey_len=10) -> bool:
    curr_loc_coords = (float(val) for val in curr_loc_coords)
    dest_coords = (float(val) for val in dest_coords)
    distance = haversine(curr_loc_coords, dest_coords, unit=Unit.MILES)
    if distance < journey_len:
        return True
    return False


def check_time_input(tod: str, interval=20) -> bool:
    now = datetime.datetime.now()
    time_given = datetime.datetime.fromisoformat(tod)
    time_diff = datetime.timedelta(minutes=interval)
    if time_given < now:
        raise ValueError("Time of Departure is in the past!")
    if time_given - now > time_diff:
        raise ValueError("Time of Departure too far ahead!")
    return True


def degrees_to_rads(degrees: float) -> float:
    rads = degrees * math.pi / 180
    return rads


def rads_to_degrees(rads: float) -> float:
    degrees = rads * 180 / math.pi
    return degrees


def get_meeting_time(tod: str, interval=10):
    tod = datetime.datetime.fromisoformat(tod)
    meeting_time = (tod + datetime.timedelta(minutes=10)).time()
    return meeting_time


def midpoint(location1, location2) -> dict:
    """create halfway point meeting point between two locations"""

    if isinstance(location1, str):
        # check if locations are str type
        loc1 = geocode(location1)
        loc2 = geocode(location2)

        loc1_lat = loc1['lat']
        loc1_lng = loc1['lng']
        loc2_lat = loc2['lat']
        loc2_lng = loc2['lat']

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


def record_to_dict(jr: tuple) -> dict:
    user = {}

    user['user_id'] = jr[0]
    user['username'] = jr[1]
    user['curr_loc_lat'] = jr[2]
    user['curr_loc_lng'] = jr[3]
    user['curr_loc_coords'] = (jr[2], jr[3])
    user['destination_lat'] = jr[4]
    user['destination_lng'] = jr[5]
    user['destination_coords'] = (jr[4], jr[5])
    user['tod'] = jr[6]
    user['phone_no'] = jr[7]

    return user


def buddy_results(user: dict, buddy: dict, meeting_point, joint_destination, meeting_time):
    """
    Prepares and prints buddy information for user
    """

    # Create dict for display
    buddy_display = {
        'Username': buddy['username'],
        'Phone Number': buddy['phone_no'],
        'Meeting Point': meeting_point['address'],
        'Joint Destination': joint_destination['address'],
        'Time to Meet': meeting_time
    }

    return buddy_display


def match_details(user: dict, buddy: dict):
    # Find the meeting point and joint destinations
    meeting_point = midpoint(user['curr_loc_coords'], buddy['curr_loc_coords'])
    joint_destination = midpoint(user['destination_coords'], buddy['destination_coords'])

    # Prepare meeting time: ToD + 10 mins
    meeting_time = get_meeting_time(user['tod'])

    return meeting_point, joint_destination, meeting_time
