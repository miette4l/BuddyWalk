from unittest import TestCase, main
from route import Route, create_map
import os

current_location = 'Buchanan Galleries, Glasgow'
destination = 'Barrowlands Ballroom Glasgow'


class RouteTest(TestCase):
    def test_get_current_loc_coord(self):
        """tests generation of current location lat long"""
        test_route = Route(current_loc=current_location, destination=destination)
        expected = (55.8631907, -4.2531089)
        result = test_route.get_current_loc_coord()
        self.assertEqual(expected, result)

    def test_get_destination_coord(self):
        """tests generation of destination lat long"""
        test_route = Route(current_loc=current_location, destination=destination)
        expected = (55.8554007, -4.2367297)
        result = test_route.get_destination_coord()
        self.assertEqual(expected, result)

    def test_get_steps_coord(self):
        """checks if correct steps coordinates are generated"""
        test_route = Route(current_loc=current_location, destination=destination)
        expected = [(55.8619451, -4.2535551), (55.8586877, -4.2547659), (55.8580646, -4.254021),
                    (55.85789949999999, -4.2526319), (55.85751279999999, -4.2493352), (55.8567534, -4.243780399999999),
                    (55.8554007, -4.2367297)]
        result = test_route.get_steps_coord()
        self.assertEqual(expected, result)

    def test_create_map(self):
        """tests generation of f_map.html"""
        test_route = Route(current_loc=current_location, destination=destination)
        create_map(test_route.get_current_loc_coord(), test_route.get_destination_coord(),
                            test_route.get_steps_coord())
        expected_path = "f_map.html"
        assert os.path.isfile(expected_path)

    # def test_meeting_point(self):
    #     expected = (55.85955035, 25.80141815)
    #     result = meeting_point(current_location, destination)
    #     self.assertEqual(expected, result)


if __name__ == '__main__':
    main()
