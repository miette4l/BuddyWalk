import datetime
import math

import googlemaps
from db.db_utils import DB
from haversine import haversine, Unit
from utils.api_key import GOOGLE_API_KEY


gmaps = googlemaps.Client(key=GOOGLE_API_KEY)


def find_buddy(journey_request: tuple):
    """
    1. Query database to find Journey Requests with ToD within 10 min of current_user's;
    further filter to find Journey Requests with distance measures within 1 mile radius of current_user's
    2. Loop over those JRs to find that with nearest lat & long for current_loc and destination
    """

    # parse journey request into arguments for DB.get_matching_journeys()
    username = journey_request[1]
    curr_loc_lat = journey_request[2]
    curr_loc_lng = journey_request[3]
    destination_lat = journey_request[4]
    destination_lng = journey_request[5]
    tod = journey_request[6]

    # create max and min time values
    time = datetime.datetime.fromisoformat(tod)
    time_window = datetime.timedelta(minutes=10)
    min_time = (time - time_window).isoformat()
    max_time = (time + time_window).isoformat()

    # get matching journeys from db
    candidates = DB.get_matching_journeys(
        min_time,
        max_time,
        curr_loc_lat,
        curr_loc_lng,
        destination_lat,
        destination_lng,
        username,
    )

    if not candidates:
        return False

    # create lat, lng location tuples
    user_curr_loc = (curr_loc_lat, curr_loc_lng)
    user_dest = (destination_lat, destination_lng)

    # find candidate with nearest current location and destination to user's
    totals = []
    for i, candidate in enumerate(candidates):
        candidate_curr_loc = (candidate[2] * 180 / math.pi, candidate[3] * 180 / math.pi)
        candidate_dest = (candidate[4] * 180 / math.pi, candidate[5] * 180 / math.pi)
        starting_distance = haversine(user_curr_loc, candidate_curr_loc, unit=Unit.MILES)
        dest_distance = haversine(user_dest, candidate_dest, unit=Unit.MILES)
        total = starting_distance + dest_distance
        totals.append(total)
    minimum = min(totals)
    pos = totals.index(minimum)
    buddy = candidates[pos]
    print("Buddy found!:", buddy[1])
    return buddy
