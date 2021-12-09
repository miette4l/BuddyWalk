from flask import Flask, jsonify, request, render_template, redirect, url_for, send_file

app = Flask(__name__)


# note: Time of Departure is a str

@app.route('/', methods=['GET', 'POST'])
def user_input():
    """User inputs their user name, location, destination, time of departure. Redirect to finding buddy site."""
    data = {}
    if request.method == 'POST':
        data = request.form.to_dict()
        # instead of print(data) call calc_route(data) and find_buddy(data)
        print(data)

        # testing for user input in all fields:
        missing = []
        for k, v in data.items():
            if v == "":
                missing.append(k)

        if missing:
            feedback = f"Missing fields for {', '.join(missing)}"
            return render_template("form.html", feedback=feedback)

        return redirect(url_for('your_buddy'))
    # do a redirect
    return render_template('form.html', data=data)


@app.route('/yourbuddy', methods=['GET', 'POST'])
def your_buddy():
    """Prints buddy's details, redirects to map with route on button click"""
    buddy = {'Name': 'Holly',
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
