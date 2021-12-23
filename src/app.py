import datetime
import json
import math
import uuid

import haversine
from app_utils import match_details, buddy_results, record_to_dict, geocode, process_input, check_in_range, \
    check_journey_length, check_time_input, rads_to_degrees, degrees_to_rads, get_meeting_time, midpoint
from db_utils import DB
from find_buddy import find_buddy
from flask import Flask, request, render_template, redirect, url_for, session, send_file
from route import Route, create_map

app = Flask(__name__)
app.secret_key = 'AIzaSyC6ShfxX_32v448NTO_xj-J9Wit9kNSLyg'


@app.route('/', methods=['GET'])
def display_form():
    """Render the form"""
    return render_template('user_input.html')


@app.route('/', methods=['POST'])
def user_input():
    """
    Grab user data from form
    Process and save as new record in DB
    Find buddy
    """
    data = request.form.to_dict()

    # Check for missing values
    missing = []
    for k, v in data.items():
        if v == "":
            missing.append(k)

    if missing:
        feedback = f"Missing fields for {', '.join(missing)}"
        return render_template("user_input.html", feedback=feedback)

    # Process inputted data into DB record data
    user = process_input(data)

    # Handle invalid phone number input
    if not type(user['phone_no']) == int:
        raise ValueError("Wrong input for phone number: must be a number!")

    # Handle invalid location input
    # 1. check current location is in range i.e. within 10 miles of the center-point of London
    if not check_in_range(user['curr_loc_coords']):
        raise ValueError("You are out of the app's range!")
    # 2. check current location and destination are within 10 miles of each other
    if not check_journey_length(user['curr_loc_coords'], user['dest_coords']):
        raise ValueError("Your journey is too long.")

    # Handle invalid time input
    check_time_input(user['tod'])

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

    # Get user's journey request (jr) from DB
    jr = DB.get_record(user['user_id'])
    user = record_to_dict(jr)
    print("User's Journey request:", user)
    print("user 1 (first logon) is:", user['username'], user['user_id'])

    # Save user id in session dict for later
    session['user_id'] = user['user_id']

    # Run find_buddy() on user's journey request to get buddy's journey request
    buddy_jr = find_buddy(jr)

    if not buddy_jr:
        # Redirect to search page
        return redirect(url_for('search_page'))

    elif buddy_jr:
        buddy = record_to_dict(buddy_jr)
        session['buddy_id'] = buddy['user_id']

        meeting_point, joint_destination, meeting_time = match_details(user, buddy)

        # Add match in DB
        DB.add_match(
            user['user_id'],
            buddy['user_id'],
            json.dumps(meeting_point),
            json.dumps(joint_destination),
            meeting_time
        )

        # Update JRs from DB so matched journeys have 'matched=True'
        DB.update_matched_journeys(jr, buddy_jr)

        # Redirect to result page
        return redirect(url_for('your_buddy'))


@app.route('/yourbuddy', methods=['GET', 'POST'])
def your_buddy():
    """
    Print buddy and match details
    Redirect to map with route on button click
    """
    # Get user's journey request (jr) from DB
    jr = DB.get_record(session['user_id'])
    user = record_to_dict(jr)

    # Get buddy's jr from DB
    buddy_jr = DB.get_record(session['buddy_id'])
    buddy = record_to_dict(buddy_jr)

    match = DB.get_match(user['user_id'])
    meeting_point = json.loads(match[2])
    joint_destination = json.loads(match[3])
    meeting_time = match[4]

    buddy_display = buddy_results(user, buddy, meeting_point, joint_destination, meeting_time)

    if request.method == 'POST':
        if request.form['show_map'] == 'Show Map':
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
    """Render the page"""
    return render_template('check.html')


@app.route('/searching', methods=['POST'])
def no_instant_match():
    """
    When no match is found, display 'searching' page.
    Here, user can check on if they've been matched.
    """
    if request.form['check'] == 'Check':

        user_id = session['user_id']
        try:
            match = DB.get_match(user_id)
        except:
            return redirect(url_for('search_page'))

        else:

            # Extract buddy's ID from match record
            buddy_id = [match[0], match[1]]
            buddy_id.remove(user_id)  # This is cause we don't know which column is buddy_id and which is user_id

            # Get buddy's jr from DB
            buddy_jr = DB.get_record(buddy_id[0])
            buddy = record_to_dict(buddy_jr)

            # Get user's jr from DB
            jr = DB.get_record(session['user_id'])
            user = record_to_dict(jr)

            # Get pre-calculated match details from match record
            meeting_point = json.loads(match[2])
            joint_destination = json.loads(match[3])
            meeting_time = match[4]

            buddy_display = buddy_results(user, buddy, meeting_point, joint_destination, meeting_time)

            return render_template('your_buddy.html', buddy=buddy_display)


@app.route('/searching', methods=['POST'])
def delayed_map():
    if request.form['show_map'] == 'Show Map':
        # Put data into routing functions
        route = Route(current_loc=meeting_point['coords'], destination=joint_destination['coords'])
        current_loc_coords = route.get_current_loc_coord()
        destination_coords = route.get_destination_coord()
        steps_coords = route.get_steps_coord()
        create_map(current_loc_coords, destination_coords, steps_coords)

    return redirect(url_for('show_map'))


@app.route('/yourmap', methods=['GET'])
def show_map():
    """Show map with route"""
    f_map = 'f_map.html'  # replace with backend logic to generate map
    return send_file(f'{f_map}')  # opens up interactive map


if __name__ == '__main__':
    app.run(debug=True, port=5000)  # localhost:5000 or 127.0.0.0.1:5000/
