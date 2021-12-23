from unittest import TestCase, main
from app_utils import geocode, process_input, check_in_range, check_journey_length, check_time_input, \
    degrees_to_rads, rads_to_degrees, get_meeting_time, midpoint, record_to_dict, buddy_results, match_details
import datetime


class AppUtilsTest(TestCase):
    def test_geocode(self):
        """tests generation of lat long dict of address"""
        address = "Phillies of Shawlands"
        expected = {'lat': 55.8299623, 'lng': -4.282282299999999}
        result = geocode(address)
        self.assertEqual(expected, result)

    def test_check_in_range_false(self):
        glasgow_coords = (55.8299623, -4.2822822999999999)
        expected = False
        result = check_in_range(glasgow_coords)
        self.assertEqual(expected, result)

    def test_check_in_range_true(self):
        trafalgar_square_coords = (51.508039, -0.128069)
        expected = True
        result = check_in_range(trafalgar_square_coords)
        self.assertEqual(expected, result)

    def test_check_journey_length_false(self):
        glasgow_coords = (55.8299623, -4.2822822999999999)
        london_coords = (51.509865, -0.118092)
        expected = False
        result = check_journey_length(glasgow_coords, london_coords)
        self.assertEqual(expected, result)

    def test_check_journey_length_true(self):
        loc1 = (55.8299623, -4.2822822999999999)
        loc2 = (55.86, -4.29)
        expected = True
        result = check_journey_length(loc1, loc2)
        self.assertEqual(expected, result)

    def test_check_time_input_past(self):
        time = str(datetime.datetime.now() - datetime.timedelta(minutes=10))
        with self.assertRaises(ValueError, msg="Time of Departure is in the past!"):
            check_time_input(time)

    def test_check_time_input_ahead(self):
        time = str(datetime.datetime.now() + datetime.timedelta(minutes=30))
        with self.assertRaises(ValueError, msg="Time of Departure too far ahead!"):
            check_time_input(time)

    def test_check_time_input_true(self):
        time = str(datetime.datetime.now() + datetime.timedelta(minutes=10))
        expected = True
        result = check_time_input(time)
        self.assertEqual(expected, result)

    def test_degrees_to_rads_to_degrees(self):
        degrees = 180
        expected = 180
        result = rads_to_degrees(degrees_to_rads(degrees))
        self.assertEqual(expected, result)

    def test_get_meeting_time(self):
        time = datetime.datetime(day=14, month=11, year=2021, hour=13, minute=34)
        expected = datetime.time(hour=13, minute=44)
        result = get_meeting_time(str(time))
        self.assertEqual(expected, result)


if __name__ == '__main__':
    main()