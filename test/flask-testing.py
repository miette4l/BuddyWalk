import unittest
from app import *
from unittest import mock
from unittest import TestCase, main
from flask import request, url_for


class FlaskTestCase(unittest.TestCase):
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
        with self.app:
            response = self.app.post("/",
                                     data={"username": "test_user",
                                           "CurrentLoc": "12 Bolton Drive, Glasgow",
                                           "Destination": "Phillies of Shawlands",
                                           "ToD": "15:13"},
                                     follow_redirects=True)
            # check that the path changed
            assert request.path == url_for('your_buddy')

    # check if buddys data is displayed in '/yourbuddy' when GET method
    def test_your_buddy_get(self):
        user_data = {"username": "test_user",
                "CurrentLoc": "12 Bolton Drive, Glasgow",
                "Destination": "Phillies of Shawlands",
                "ToD": "15:13"}
        with self.app:
            with self.app.session_transaction() as sess:
                sess['current_user'] = user_data
                mock_buddy = {
                    'Username': "mock_buddy",  # my own username gets returned, not my buddy's!!
                    'Phone number': "mock_phone_number",
                    'Meeting point': "140 Titwood Rd, Crossmyloof, Glasgow G41 4DA",
                    'Joint destination': "Phillies of Shawlands",
                    'Time to meet': "16:14"
                }
            response = self.app.get("/yourbuddy", data=mock_buddy)

            self.assertIn("<p>Your Buddy's details:</p>".encode(), response.data)

    # test '/yourbuddy' redirect to map when POST
    def test_your_buddy_post(self):
        user_data = {"username": "test_user",
                "CurrentLoc": "12 Bolton Drive, Glasgow",
                "Destination": "Phillies of Shawlands",
                "ToD": "15:13"}
        with self.app:
            with self.app.session_transaction() as sess:
                sess['current_user'] = user_data
                mock_buddy = {
                    'Username': "mock_buddy",  # my own username gets returned, not my buddy's!!
                    'Phone number': "mock_phone_number",
                    'Meeting point': "140 Titwood Rd, Crossmyloof, Glasgow G41 4DA",
                    'Joint destination': "Phillies of Shawlands",
                    'Time to meet': "16:14"
                }
            response = self.app.post("/yourbuddy", data=mock_buddy, follow_redirects=True)
            assert request.path == url_for('show_map')

    # check that html file is returned from '/yourmap'
    def test_your_map(self):
        with self.app:
            response = self.app.get("/yourmap")
            assert response.mimetype == "text/html"




c = app.test_client()
#response = c.post('/',
                 # data={"username": "test_user",
                 #       "CurrentLoc": "12 Bolton Drive, Glasgow",
                 #       "Destination": "Phillies of Shawlands",
                 #       "ToD": "15:13"})
#print(response)


if __name__ == '__main__':
    main()
