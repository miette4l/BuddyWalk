from db_utils import DB
import datetime
import googlemaps
from geopy import distance
gmaps = googlemaps.Client(key='AIzaSyDzj7gfcouVFtZAyzntCmyDUs8g_8s_yTM')

class BuddyNotFoundError(Exception):
    pass

def find_buddy(current_user: dict):
    """
    1. Query database to find Journey Requests with ToD within 10 min of current_user's;
    further filter to find Journey Requests with distance measures within radius of current_user's
    2. Loop over those JRs to find that with nearest lat & long for current_loc and destination
    """

    tod = current_user['tod']
    time = datetime.datetime.fromisoformat(tod)
    time_window = datetime.timedelta(minutes=10)
    min_time = time - time_window
    max_time = time + time_window

    curr_loc_lat = current_user['curr_loc_lat']
    curr_loc_lng = current_user['curr_loc_lng']
    curr_dest_lat = current_user['destination_lat']
    curr_dest_lng = current_user['destination_lng']
    username = current_user['username']

    candidates = DB.get_matching_journeys(min_time, max_time,
                      curr_loc_lat, curr_loc_lng, curr_dest_lat, curr_dest_lng,
                      username)

    if not candidates:
        raise BuddyNotFoundError("We could not find you a buddy! :(")

    user_curr_loc = str((curr_loc_lat, curr_loc_lng)).replace(',', "")
    user_dest = str((curr_dest_lat, curr_dest_lng)).replace(',', "")

    total_diffs = []
    for i, candidate in enumerate(candidates):
        candidate_curr_loc = (candidate[1], candidate[2])
        candidate_curr_loc = str(candidate_curr_loc).replace(',', "")
        candidate_dest = (candidate[3], candidate[4])
        candidate_dest = str(candidate_dest).replace(',', "")
        response = gmaps.distance_matrix(user_curr_loc, candidate_curr_loc, 'walking')
        current_loc_diff = (response['rows'][0]['elements'][0]['duration']['value'])
        response = gmaps.distance_matrix(user_dest, candidate_dest, 'walking')
        destination_diff = (response['rows'][0]['elements'][0]['duration']['value'])
        total_diff = current_loc_diff + destination_diff
        total_diffs.append(total_diff)

    minimum = min(total_diffs)
    pos = minutes.index(minimum)
    buddy = candidates[pos][0]
    return buddy


def geocode(loc: str) -> tuple:
    geocoded = gmaps.geocode(loc)[0]['geometry']['location']
    return geocoded

