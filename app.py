from flask import Flask, jsonify, request, render_template, redirect, url_for, session, send_file
from find_buddy import find_buddy
from SQL_DB_to_python_connect import add_journey_request

app = Flask(__name__)
app.secret_key = 'AIzaSyC6ShfxX_32v448NTO_xj-J9Wit9kNSLyg'

# note: Time of Departure is a str


@app.route('/', methods=['GET'])
def display_form():
    """Render the form"""
    return render_template('form.html')


@app.route('/', methods=['POST'])
def user_input():
    """
    Grab user data from form, while checking if complete
    Save data as new record in DB
    """
    data = {}
    if request.method == 'POST':
        data = request.form.to_dict()
        session['current_user'] = data
        add_journey_request(data['username'], data['CurrentLoc'], data['Destination'], data['ToD'])

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
    Finds and prints buddy's details, redirects to map with route on button click
    """
    buddy_username = find_buddy(session['current_user'])

    buddy = {
        'Username': buddy_username,
        'Phone number': 'fake phonenumber',
        'Meeting Point': 'fake spot',
        'Time to meet': 'fake'
    }

    if request.method == 'POST':
        return redirect(url_for('show_map'))
    return render_template('your_buddy.html', buddy=buddy)


@app.route('/yourmap', methods=['GET'])
def show_map():
    """Shows map with route"""
    f_map = 'f_map.html'  # replace with backend logic to generate map
    return send_file(f'{f_map}')  # opens up interactive map


if __name__ == '__main__':
    app.run(debug=True, port=5000)  # localhost:5000 or 127.0.0.0.1:5000/
