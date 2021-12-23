from app import *
from unittest import TestCase, main
from flask import request, url_for
import datetime


class FlaskTestCase(TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        #app.config['WTF_CSRF_ENABLED'] = False
        app.config['DEBUG'] = False
        self.app = app.test_client()
        self.assertEqual(app.debug, False)

    # check for a 200 response on index page
    def test_index_path(self):
        response = self.app.get("/")
        self.assertEqual(response.status_code, 200)

    # check for correct redirect to '/yourbuddy' after posting user input
    def test_user_input_path(self):
        user_data = {"username": "test_user",
                     "phone_no": 17305123456,
                     "current_loc": "trafalgar square london",
                     "destination": "st paul's cathedral london",
                     "tod": (datetime.datetime.now() + datetime.timedelta(minutes=10))}
        with self.app:
            with self.app.session_transaction() as sess:
                sess['current_user'] = user_data
            response = self.app.post("/",
                                     data=user_data,
                                     follow_redirects=True)

            # check that the path changed
            assert request.path == url_for('search_page')

    # check that html file is returned from '/yourmap'
    def test_your_map(self):
        with self.app:
            response = self.app.get("/yourmap")
            assert response.mimetype == "text/html"


if __name__ == '__main__':
    main()
