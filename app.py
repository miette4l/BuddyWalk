from flask import Flask, jsonify, request, render_template, redirect, url_for

app = Flask(__name__)


# note: Time of Departure is a str

@app.route('/', methods=['GET', 'POST'])
def user_input():
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


@app.route('/yourbuddy', methods=['GET'])
def your_buddy():
    return 'Finding you a buddy'


if __name__ == '__main__':
    app.run(debug=True, port=5000)  # localhost:5000 or 127.0.0.0.1:5000/
