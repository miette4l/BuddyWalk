from flask import Flask, jsonify, request, render_template, redirect, url_for, session, send_file
from users import return_buddy

app = Flask(__name__)
app.secret_key = 'dljsaklqk24e21cjn!Ew@@dsa5'

# note: Time of Departure is a str


@app.route('/', methods=['GET'])
def display_form():
    """Render the form"""
    return render_template('form.html')


@app.route('/', methods=['POST'])
def user_input():
    """ Grab and store user data from form, while checking if complete"""
    data = {}
    if request.method == 'POST':
        data = request.form.to_dict()
        session["data"] = data

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
    buddy_user = return_buddy(session["data"])  # returns a User type
    # mock some data to fill the 'Your Buddy' template with:
    # @V: I changed Name to be the buddy returned by the return_buddy function above
    # so that is a real piece of buddy data
    buddy = {'Username': buddy_user.username,
             'Phone number': '12334556',
             'Meeting Point': 'some address, some postcode',
             'Meeting Time': '23:29 10/12/2021'}
    if request.method == 'POST':
        return redirect(url_for('show_map'))
    return render_template('your_buddy.html', buddy=buddy)


@app.route('/yourmap', methods=['GET'])
def show_map():
    """Shows map with route"""
    f_map = 'f_map.html'  # replace with backend logic to generate map
    return send_file(f'{f_map}') # opens up interactive map


if __name__ == '__main__':
    app.run(debug=True, port=5000)  # localhost:5000 or 127.0.0.0.1:5000/
