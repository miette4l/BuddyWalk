from flask import Flask, request, render_template, redirect, url_for, session, send_file
import datetime
from find_buddy import find_buddy, geocode
from db_utils import DB
from route import Route, create_map


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
    data = {}
    if request.method == 'POST':
        data = request.form.to_dict()

        # Process data to be stored in DB for searching
        username = data['username']
        curr_loc = geocode(data['CurrentLoc'])
        curr_loc_lat = curr_loc['lat']
        curr_loc_lng = curr_loc['lng']
        destination = geocode(data['Destination'])
        destination_lat = destination['lat']
        destination_lng = destination['lng']
        tod = data['ToD']  # 'tod' = 'Time of Departure' (isoformat str)

        # Handle invalid location input
        # check_loc_inputs()

        # Handle invalid time input
        # could change to check_time_inputs()function
        now = datetime.datetime.now()
        time_given = datetime.datetime.fromisoformat(tod)
        time_diff = datetime.timedelta(minutes=20)
        if time_given < now:
            raise ValueError("Time of Departure is in the past!")
        if time_given - now > time_diff:
            raise ValueError("Time of Departure too far ahead!")

        DB.add_journey_request(username, curr_loc_lat, curr_loc_lng,
                               destination_lat, destination_lng, tod)

        current_user = {'username': username,
                        'curr_loc_lat': curr_loc_lat,
                        'curr_loc_lng': curr_loc_lng,
                        'destination_lat': destination_lat,
                        'destination_lng': destination_lng,
                        'tod': tod}

        print(current_user)

        session['current_user'] = current_user

    missing = []
    for k, v in data.items():
        if v == "":
            missing.append(k)

    if missing:
        feedback = f"Missing fields for {', '.join(missing)}"
        return render_template("form.html", feedback=feedback)

    return redirect(url_for('your_buddy'))
    # do a redirect to result page


@app.route('/yourbuddy', methods=['GET', 'POST'])
def your_buddy():
    """
    Find and print buddy's details
    Redirect to map with route on button click
    """
    buddy_username = find_buddy(session['current_user'])
    buddy_phone_number = "buddy's fake phone number"  # add logic for phone number

    meeting_time = datetime.datetime.strptime(session['current_user']['ToD'], "%H:%M")
    meeting_time = (meeting_time + datetime.timedelta(minutes=10)).time()  # meeting time is ToD + 10 minutes

    # add meeting point logic, i.e. get_meeting_point(current_loc) or so
    meeting_point = '140 Titwood Rd, Crossmyloof, Glasgow G41 4DA'
    joint_destination = 'Phillies of Shawlands'

    # this is where all data to display should be collected
    buddy = {
        'Username': buddy_username,  # my own username gets returned, not my buddy's!!
        'Phone number': buddy_phone_number,
        'Meeting point': meeting_point,
        'Joint destination': joint_destination,
        'Time to meet': meeting_time
    }

    if request.method == 'POST':
        # posts session details into routing functions
        route = Route(current_loc=buddy['Meeting point'], destination=buddy['Joint destination'])
        current_loc_coords = route.get_current_loc_coord()
        destination_coords = route.get_destination_coord()
        steps_coords = route.get_steps_coord()
        create_map(current_loc_coords, destination_coords, steps_coords)

        return redirect(url_for('show_map'))

    return render_template('your_buddy.html', buddy=buddy)


@app.route('/yourmap', methods=['GET'])
def show_map():
    """Shows map with route"""
    f_map = 'f_map.html'  # replace with backend logic to generate map
    return send_file(f'{f_map}')  # opens up interactive map


if __name__ == '__main__':
    app.run(debug=True, port=5000)  # localhost:5000 or 127.0.0.0.1:5000/
