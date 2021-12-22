from flask import Flask, request, render_template, redirect, url_for, session, send_file
import datetime
from find_buddy import find_buddy
from db_utils import DB
from route import Route, create_map
import math
import uuid
from app_utils import record_to_dict, geocode, process_input, check_in_range, check_journey_length, check_time_input, rads_to_degrees, degrees_to_rads, get_meeting_time, midpoint
import haversine


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
    user = process_input(data)

    # Handle invalid phone number input
    if not type(user['phone_no']) == int:
        raise ValueError("Wrong input for phone number: must be a number!")

    print('user[curr_loc_coords]:', user['curr_loc_coords'])
    # Handle invalid location input
    # 1. check current location is in range i.e. within 10 miles of the center-point of London
    if not check_in_range(user['curr_loc_coords']):
        raise ValueError("You are out of the app's range!")
    # 2. check current location and destination are within 10 miles of each other
    if not check_journey_length(user['curr_loc_coords'], user['dest_coords']):
        raise ValueError("Your journey is too long.")

    # Handle invalid time input
    check_time_input(user['tod'])

    # Save user_id to session for use in future routes
    session['user_id'] = user['user_id']

    # Convert locations from degrees to rads for DB storage
    points = [
        user['curr_loc_lat'],
        user['curr_loc_lng'],
        user['destination_lat'],
        user['destination_lng']
            ]
    radians = [degrees_to_rads(point) for point in points]

    # Save data to DB
    DB.add_journey_request(
        user['user_id'],
        user['username'],
        radians[0],
        radians[1],
        radians[2],
        radians[3],
        user['tod'],
        user['phone_no']
    )

    # Redirect to result page
    return redirect(url_for('your_buddy'))


@app.route('/yourbuddy', methods=['GET', 'POST'])
def your_buddy():
    """
    Find and print buddy's details
    Redirect to map with route on button click
    """
    # Get user's journey request (jr) from DB
    jr = DB.get_record(session['user_id'])
    user = record_to_dict(jr)
    print("User's Journey request:", user)

    # Run find_buddy() on user's journey request
    # Returns buddy's journey request
    buddy_jr = find_buddy(jr)

    if not buddy_jr:
        return redirect(url_for('search_page'))

    buddy = record_to_dict(buddy_jr)

    print("Buddy's Journey request:", buddy_jr)
    print("Buddies:", user['username'], "and", buddy['username'])

    # Prepare meeting time: ToD + 10 mins
    meeting_time = get_meeting_time(user['tod'])

    # Find the meeting point and joint destinations
    meeting_point = midpoint(user['curr_loc_coords'], buddy['curr_loc_coords'])
    joint_destination = midpoint(user['destination_coords'], buddy['destination_coords'])

    # Create dict for display
    buddy_display = {
        'Username': buddy['username'],
        'Phone Number': buddy['phone_no'],
        'Meeting Point': meeting_point['address'],
        'Joint Destination': joint_destination['address'],
        'Time to Meet': meeting_time
    }

    if request.method == 'POST':

        # Add match in DB
        DB.add_match(jr, buddy_jr)

        # Update JRs from DB so matched journeys have matched=True
        DB.update_matched_journeys(jr, buddy_jr)

        # Put data into routing functions
        route = Route(current_loc=meeting_point['coords'], destination=joint_destination['coords'])
        current_loc_coords = route.get_current_loc_coord()
        destination_coords = route.get_destination_coord()
        steps_coords = route.get_steps_coord()
        create_map(current_loc_coords, destination_coords, steps_coords)

        return redirect(url_for('show_map'))

    return render_template('your_buddy.html', buddy=buddy_display)


@app.route('/searching', methods=['GET'])
def search_page():
    """Render the button"""
    return render_template('button.html')


@app.route('/searching', methods=['GET', 'POST'])
def no_instant_match():
    """
    When no match is found, display 'searching' page.
    Here, user can check on if they've been matched.
    """
    user_id = session['user_id']

    if request.method == 'POST':
        if request.form.get('check') == 'Check':
            print("You've successfully got here")
            try:
                match = DB.get_match(user_id)
                print(match)
                print(user_id)
                print(list(match))
                buddy_id = list(match)
                buddy_id.remove(user_id)
                print(buddy_id)
                buddy_journey_request = get_record(buddy_id[0])
                print(buddy_journey_request)
                # Get user's journey request from DB
                journey_request = DB.get_record(session['user_id'])
                print(journey_request)

                # Prepare meeting time: ToD + 10 mins
                tod = datetime.datetime.fromisoformat(journey_request[6])
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

                return render_template('your_buddy.html', buddy=buddy)

            except:
                print("Something went wrong")
                return redirect(url_for('search_page'))


@app.route('/yourmap', methods=['GET'])
def show_map():
    """Show map with route"""
    f_map = 'f_map.html'  # replace with backend logic to generate map
    return send_file(f'{f_map}')  # opens up interactive map


if __name__ == '__main__':
    app.run(debug=True, port=5000)  # localhost:5000 or 127.0.0.0.1:5000/
