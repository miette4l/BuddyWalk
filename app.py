from flask import Flask, request, render_template, redirect, url_for, session, send_file
import datetime
from find_buddy import find_buddy, geocode, check_in_range, check_journey_length
from db_utils import DB
from route import Route, create_map
import math
import uuid


app = Flask(__name__)
app.secret_key = 'AIzaSyC6ShfxX_32v448NTO_xj-J9Wit9kNSLyg'


@app.route('/', methods=['GET'])
def display_form():
    """Render the form"""
    return render_template('form.html')


@app.route('/', methods=['POST'])
def user_input():
    """
    Grab user data from form
    Process and save as new record in DB
    """
    data = request.form.to_dict()

    # Check for missing values
    missing = []
    for k, v in data.items():
        if v == "":
            missing.append(k)

    if missing:
        feedback = f"Missing fields for {', '.join(missing)}"
        return render_template("form.html", feedback=feedback)

    # Process inputted data into DB record data
    user_id = str(uuid.uuid1())
    username = data['username']
    phone_no = data['phone_no']
    curr_loc = geocode(data['current_loc'])  # convert to lat, lng using gmaps.geocode
    curr_loc_lat = curr_loc['lat']  # unit: latitude in degrees
    curr_loc_lng = curr_loc['lng']  # unit: longitude in degrees
    curr_loc_coords = (curr_loc_lat, curr_loc_lng)
    destination = geocode(data['destination'])
    destination_lat = destination['lat']
    destination_lng = destination['lng']
    dest_coords = (destination_lat, destination_lng)
    tod = data['tod']  # 'tod' = 'Time of Departure' as isoformat string

    # Handle invalid phone number input
    # <HERE>

    # Handle invalid location input
    # 1. check current location is in range i.e. within 10 miles of the centrepoint of London
    if not check_in_range(curr_loc_coords):
        raise ValueError("You are out of the app's range!")
    # 2. check current location and destination are within 10 miles of each other
    if not check_journey_length(curr_loc_coords, dest_coords):
        raise ValueError("Your journey is too long.")

    # Handle invalid time input
    # could change to check_time_inputs()function
    now = datetime.datetime.now()
    time_given = datetime.datetime.fromisoformat(tod)
    time_diff = datetime.timedelta(minutes=20)
    if time_given < now:
        raise ValueError("Time of Departure is in the past!")
    if time_given - now > time_diff:
        raise ValueError("Time of Departure too far ahead!")

    # Store data as processed in dict (changing this to DB pull)
    # current_user = {'username': username,
    #                 'curr_loc_lat': curr_loc_lat,
    #                 'curr_loc_lng': curr_loc_lng,
    #                 'destination_lat': destination_lat,
    #                 'destination_lng': destination_lng,
    #                 'tod': tod}

    # Save user_id to session for use in future routes
    session['user_id'] = user_id

    # Convert from degrees to rads for DB storage
    curr_loc_lat = curr_loc_lat * math.pi / 180
    curr_loc_lng = curr_loc_lng * math.pi / 180
    destination_lat = destination_lat * math.pi / 180
    destination_lng = destination_lng * math.pi / 180

    # Save data to DB
    DB.add_journey_request(
        user_id,
        username,
        curr_loc_lat,
        curr_loc_lng,
        destination_lat,
        destination_lng,
        tod,
        phone_no
    )

    # Redirect to result page
    return redirect(url_for('your_buddy'))


@app.route('/yourbuddy', methods=['GET', 'POST'])
def your_buddy():
    """
    Find and print buddy's details
    Redirect to map with route on button click
    """
    # Get user's journey request from DB
    journey_request = DB.get_record(session['user_id'])
    print("Journey request:", journey_request)

    # Run find_buddy() on user's JR
    buddy_journey_request = find_buddy(journey_request)  # Stores the buddy's JR

    # Prepare meeting time: ToD + 10 mins
    tod = datetime.datetime.fromisoformat(journey_request[0][6])
    meeting_time = (tod + datetime.timedelta(minutes=10)).time()

    # Add meeting point and joint destination logic
    # i.e. get_meeting_point(current_loc) or so HERE
    meeting_point = '140 Titwood Rd, Crossmyloof, Glasgow G41 4DA'
    joint_destination = 'Phillies of Shawlands'

    # Create dict for display
    buddy = {
        'Username': buddy_journey_request[1],
        'Phone Number': buddy_journey_request[7],
        'Meeting Point': meeting_point,
        'Joint Destination': joint_destination,
        'Time to Meet': meeting_time
    }

    if request.method == 'POST':
        # Put data into routing functions
        route = Route(current_loc=buddy['Meeting Point'], destination=buddy['Joint Destination'])
        current_loc_coords = route.get_current_loc_coord()
        destination_coords = route.get_destination_coord()
        steps_coords = route.get_steps_coord()
        create_map(current_loc_coords, destination_coords, steps_coords)

        return redirect(url_for('show_map'))

    return render_template('your_buddy.html', buddy=buddy)


@app.route('/yourmap', methods=['GET'])
def show_map():
    """Show map with route"""
    f_map = 'f_map.html'  # replace with backend logic to generate map
    return send_file(f'{f_map}')  # opens up interactive map


if __name__ == '__main__':
    app.run(debug=True, port=5000)  # localhost:5000 or 127.0.0.0.1:5000/
