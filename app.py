from flask import Flask, jsonify, request, render_template, redirect, url_for, session
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


@app.route('/yourbuddy', methods=['GET'])
def your_buddy():
    return return_buddy(session["data"])


if __name__ == '__main__':
    app.run(debug=True, port=5000)  # localhost:5000 or 127.0.0.0.1:5000/
