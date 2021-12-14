import datetime
from SQL_DB_to_python_connect import get_matching_times
import googlemaps
gmaps = googlemaps.Client(key='AIzaSyDzj7gfcouVFtZAyzntCmyDUs8g_8s_yTM')


def find_buddy(current_user):
    """
    1. Query database to find Journey Requests with ToD within 10 min of current_user's
    2. Loop over those JRs to find that with nearest lat & long for current_loc and destination
    """
    ToD = current_user['ToD']
    time = datetime.datetime.fromisoformat(ToD)
    time_change = datetime.timedelta(minutes=10)
    min_time = time - time_change
    max_time = time + time_change
    candidates = get_matching_times(min_time, max_time)
    print(candidates)

    user_curr_loc = current_user['CurrentLoc']
    minutes = []
    for i, candidate in enumerate(candidates):
        candidate_curr_loc = candidate[1]
        response = gmaps.distance_matrix(user_curr_loc, candidate_curr_loc, 'walking')
        minutes.append(response['rows'][0]['elements'][0]['duration']['value'])
    minimum = min(minutes)
    pos = minutes.index(minimum)
    buddy = candidates[pos][0]
    return buddy