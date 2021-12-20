from db_utils import DB
import datetime
from geopy import distance
from haversine import haversine, Unit
import math
import googlemaps
gmaps = googlemaps.Client(key='AIzaSyDzj7gfcouVFtZAyzntCmyDUs8g_8s_yTM')


def find_buddy(current_user: dict):
    """
    1. Query database to find Journey Requests with ToD within 10 min of current_user's;
    further filter to find Journey Requests with distance measures within radius of current_user's
    2. Loop over those JRs to find that with nearest lat & long for current_loc and destination
    """

    tod = current_user['tod']
    time = datetime.datetime.fromisoformat(tod)
    time_window = datetime.timedelta(minutes=30)
    min_time = (time - time_window).isoformat()
    max_time = (time + time_window).isoformat()

    candidates = DB.get_matching_journeys(
        min_time,
        max_time,
        current_user['curr_loc_lat'],  # convert from degrees to rads
        current_user['curr_loc_lng'],
        current_user['destination_lat'],
        current_user['destination_lng'],
        current_user['username']
    )
    print("Candidates:", candidates)

    user_curr_loc = (current_user['curr_loc_lat'], current_user['curr_loc_lng'])
    user_dest = (current_user['destination_lat'], current_user['destination_lng'])

    totals = []
    for i, candidate in enumerate(candidates):
        candidate_curr_loc = (candidate[1] * 180 / math.pi, candidate[2] * 180 / math.pi)
        candidate_dest = (candidate[3] * 180 / math.pi, candidate[4] * 180 / math.pi)
        starting_distance = haversine(user_curr_loc, candidate_curr_loc, unit=Unit.MILES)
        dest_distance = haversine(user_dest, candidate_dest, unit=Unit.MILES)
        total = starting_distance + dest_distance
        totals.append(total)
    minimum = min(totals)
    pos = totals.index(minimum)
    buddy = candidates[pos]
    return buddy


def geocode(loc: str) -> tuple:
    geocoded = gmaps.geocode(loc)[0]['geometry']['location']
    return geocoded


def check_in_range(curr_loc_coords: tuple) -> bool:
    london = (51.509865, -0.118092)
    curr_loc_coords = (float(val) for val in curr_loc_coords)
    distance = haversine(curr_loc_coords, london, unit=Unit.MILES)
    if distance < 10:
        return True
    return False


def check_journey_length(curr_loc_coords: tuple, dest_coords: tuple) -> bool:
    curr_loc_coords = (float(val) for val in curr_loc_coords)
    dest_coords = (float(val) for val in dest_coords)
    distance = haversine(curr_loc_coords, dest_coords, unit=Unit.MILES)
    if distance < 10:
        return True
    return False
