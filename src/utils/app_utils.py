import datetime
import math
import uuid

from utils.location_utils import geocode, midpoint


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


def check_time_input(tod: str, interval=20) -> bool:
    now = datetime.datetime.now()
    time_given = datetime.datetime.fromisoformat(tod)
    time_diff = datetime.timedelta(minutes=interval)
    if time_given < now:
        raise ValueError("Time of Departure is in the past!")
    if time_given - now > time_diff:
        raise ValueError("Time of Departure too far ahead!")
    return True


def get_meeting_time(tod: str, interval=10):
    tod = datetime.datetime.fromisoformat(tod)
    meeting_time = (tod + datetime.timedelta(minutes=interval)).time()
    return meeting_time


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
