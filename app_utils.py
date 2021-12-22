import uuid
import math
import googlemaps
import datetime
from haversine import haversine, Unit
gmaps = googlemaps.Client(key='AIzaSyDzj7gfcouVFtZAyzntCmyDUs8g_8s_yTM')


def geocode(loc: str) -> tuple:
    geocoded = gmaps.geocode(loc)[0]['geometry']['location']
    return geocoded


def process_input(data: dict) -> dict:
    user = {}

    user['user_id'] = str(uuid.uuid1())
    user['username'] = data['username']
    user['phone_no'] = int(data['phone_no'])
    user['curr_loc'] = geocode(data['current_loc'])  # convert to lat, lng using gmaps.geocode
    user['curr_loc_lat'] = user['curr_loc']['lat']  # unit: latitude in degrees
    user['curr_loc_lng'] = user['curr_loc']['lng']  # unit: longitude in degrees
    user['curr_loc_coords'] = (user['curr_loc_lat'], user['curr_loc_lng'])  # create (lat, lng) tuple
    user['destination'] = geocode(data['destination'])
    user['destination_lat'] = user['destination']['lat']
    user['destination_lng'] = user['destination']['lng']
    user['dest_coords'] = (user['destination_lat'], user['destination_lng'])
    user['tod'] = data['tod']  # 'tod' = 'Time of Departure' as iso-format string

    return user


def check_in_range(curr_loc_coords: tuple, range_d=10) -> bool:
    london = (51.509865, -0.118092)  # app is currently only for London use
    curr_loc_coords = (float(val) for val in curr_loc_coords)
    distance = haversine(curr_loc_coords, london, unit=Unit.MILES)
    if distance < range_d:
        return True
    return False


def check_journey_length(curr_loc_coords: tuple, dest_coords: tuple, journey_len=10) -> bool:
    curr_loc_coords = (float(val) for val in curr_loc_coords)
    dest_coords = (float(val) for val in dest_coords)
    distance = haversine(curr_loc_coords, dest_coords, unit=Unit.MILES)
    if distance < journey_len:
        return True
    return False


def check_time_input(tod: str, interval=20) -> bool:
    now = datetime.datetime.now()
    time_given = datetime.datetime.fromisoformat(tod)
    time_diff = datetime.timedelta(minutes=interval)
    if time_given < now:
        raise ValueError("Time of Departure is in the past!")
    if time_given - now > time_diff:
        raise ValueError("Time of Departure too far ahead!")
    return True


def degrees_to_rads(degrees: float) -> float:
    rads = degrees * math.pi / 180
    return rads


def rads_to_degrees(rads: float) -> float:
    degrees = rads * 180 / math.pi
    return degrees


def get_meeting_time(tod: str, interval=10):
    tod = datetime.datetime.fromisoformat(tod)
    meeting_time = (tod + datetime.timedelta(minutes=10)).time()
    return meeting_time


def midpoint(location1, location2) -> dict:
    """create halfway point meeting point between two locations"""

    if isinstance(location1, str):
        # check if locations are str type
        loc1 = geocode(location1)
        loc2 = geocode(location2)

        loc1_lat = loc1['lat']
        loc1_lng = loc1['lng']
        loc2_lat = loc2['lat']
        loc2_lng = loc2['lat']

    elif isinstance(location1, tuple):
        # if location are already tuples (lat, lng) execute this
        loc1_lat = rads_to_degrees(location1[0])
        loc1_lng = rads_to_degrees(location1[1])
        loc2_lat = rads_to_degrees(location2[0])
        loc2_lng = rads_to_degrees(location2[1])

    else:
        raise ValueError("Wrong location input type")

    midpoint_lat = (loc1_lat + loc2_lat) / 2
    midpoint_lng = (loc1_lng + loc2_lng) / 2

    coords = (midpoint_lat, midpoint_lng)
    address = gmaps.reverse_geocode(coords)[0]['address_components']
    short_address = address[0]['long_name'] + " " + address[1]['long_name']

    midpoint_data = {'coords': coords, 'address': short_address}

    return midpoint_data


def record_to_dict(jr: tuple) -> dict:
    user = {}

    user['user_id'] = jr[0]
    user['username'] = jr[1]
    user['curr_loc_lat'] = jr[2]
    user['curr_loc_lng'] = jr[3]
    user['curr_loc_coords'] = (jr[2], jr[3])
    user['destination_lat'] = jr[4]
    user['destination_lng'] = jr[5]
    user['destination_coords'] = (jr[4], jr[5])
    user['tod'] = jr[6]
    user['phone_no'] = jr[7]

    return user


if __name__ == '__main__':

    address = [{'address_components': [{'long_name': '76', 'short_name': '76', 'types': ['street_number']}, {'long_name': 'Venn Street', 'short_name': 'Venn St', 'types': ['route']}, {'long_name': 'London', 'short_name': 'London', 'types': ['postal_town']}, {'long_name': 'Greater London', 'short_name': 'Greater London', 'types': ['administrative_area_level_2', 'political']}, {'long_name': 'England', 'short_name': 'England', 'types': ['administrative_area_level_1', 'political']}, {'long_name': 'United Kingdom', 'short_name': 'GB', 'types': ['country', 'political']}, {'long_name': 'SW4 0AT', 'short_name': 'SW4 0AT', 'types': ['postal_code']}], 'formatted_address': '76 Venn St, London SW4 0AT, UK', 'geometry': {'bounds': {'northeast': {'lat': 51.4626684, 'lng': -0.1380097}, 'southwest': {'lat': 51.4623833, 'lng': -0.138414}}, 'location': {'lat': 51.462506, 'lng': -0.1382711}, 'location_type': 'ROOFTOP', 'viewport': {'northeast': {'lat': 51.46387483029149, 'lng': -0.136862869708498}, 'southwest': {'lat': 51.4611768697085, 'lng': -0.139560830291502}}}, 'place_id': 'ChIJae5LglIEdkgRtaeVUaVty6I', 'types': ['premise']}, {'address_components': [{'long_name': 'York House', 'short_name': 'York House', 'types': ['premise']}, {'long_name': '71', 'short_name': '71', 'types': ['street_number']}, {'long_name': 'Venn Street', 'short_name': 'Venn St', 'types': ['route']}, {'long_name': 'London', 'short_name': 'London', 'types': ['postal_town']}, {'long_name': 'Greater London', 'short_name': 'Greater London', 'types': ['administrative_area_level_2', 'political']}, {'long_name': 'England', 'short_name': 'England', 'types': ['administrative_area_level_1', 'political']}, {'long_name': 'United Kingdom', 'short_name': 'GB', 'types': ['country', 'political']}, {'long_name': 'SW4 0BD', 'short_name': 'SW4 0BD', 'types': ['postal_code']}], 'formatted_address': 'York House, 71 Venn St, London SW4 0BD, UK', 'geometry': {'location': {'lat': 51.4625823, 'lng': -0.1378894}, 'location_type': 'ROOFTOP', 'viewport': {'northeast': {'lat': 51.4639312802915, 'lng': -0.136540419708498}, 'southwest': {'lat': 51.46123331970851, 'lng': -0.139238380291502}}}, 'place_id': 'ChIJ08GxgFIEdkgRmE2pvjkkPh8', 'plus_code': {'compound_code': 'FV76+2R London, UK', 'global_code': '9C3XFV76+2R'}, 'types': ['street_address']}, {'address_components': [{'long_name': '55-73', 'short_name': '55-73', 'types': ['street_number']}, {'long_name': 'Venn Street', 'short_name': 'Venn St', 'types': ['route']}, {'long_name': 'London', 'short_name': 'London', 'types': ['postal_town']}, {'long_name': 'Greater London', 'short_name': 'Greater London', 'types': ['administrative_area_level_2', 'political']}, {'long_name': 'England', 'short_name': 'England', 'types': ['administrative_area_level_1', 'political']}, {'long_name': 'United Kingdom', 'short_name': 'GB', 'types': ['country', 'political']}, {'long_name': 'SW4 0BD', 'short_name': 'SW4 0BD', 'types': ['postal_code']}], 'formatted_address': '55-73 Venn St, London SW4 0BD, UK', 'geometry': {'bounds': {'northeast': {'lat': 51.4628786, 'lng': -0.1379319}, 'southwest': {'lat': 51.4624823, 'lng': -0.1382335}}, 'location': {'lat': 51.4626805, 'lng': -0.1380827}, 'location_type': 'GEOMETRIC_CENTER', 'viewport': {'northeast': {'lat': 51.4640294302915, 'lng': -0.136733719708498}, 'southwest': {'lat': 51.4613314697085, 'lng': -0.139431680291502}}}, 'place_id': 'ChIJa6FXgVIEdkgR5CyGoz7OhN4', 'types': ['route']}, {'address_components': [{'long_name': 'FV76+2Q', 'short_name': 'FV76+2Q', 'types': ['plus_code']}, {'long_name': 'London', 'short_name': 'London', 'types': ['postal_town']}, {'long_name': 'Greater London', 'short_name': 'Greater London', 'types': ['administrative_area_level_2', 'political']}, {'long_name': 'England', 'short_name': 'England', 'types': ['administrative_area_level_1', 'political']}, {'long_name': 'United Kingdom', 'short_name': 'GB', 'types': ['country', 'political']}], 'formatted_address': 'FV76+2Q London, UK', 'geometry': {'bounds': {'northeast': {'lat': 51.462625, 'lng': -0.138}, 'southwest': {'lat': 51.4625, 'lng': -0.138125}}, 'location': {'lat': 51.4625103, 'lng': -0.1380832}, 'location_type': 'GEOMETRIC_CENTER', 'viewport': {'northeast': {'lat': 51.46391148029149, 'lng': -0.136713519708498}, 'southwest': {'lat': 51.4612135197085, 'lng': -0.139411480291502}}}, 'place_id': 'GhIJFUiaiTO7SUARbUIQ1rWswb8', 'plus_code': {'compound_code': 'FV76+2Q London, UK', 'global_code': '9C3XFV76+2Q'}, 'types': ['plus_code']}, {'address_components': [{'long_name': 'SW4 0BD', 'short_name': 'SW4 0BD', 'types': ['postal_code']}, {'long_name': 'Venn Street', 'short_name': 'Venn St', 'types': ['route']}, {'long_name': 'London', 'short_name': 'London', 'types': ['postal_town']}, {'long_name': 'Greater London', 'short_name': 'Greater London', 'types': ['administrative_area_level_2', 'political']}, {'long_name': 'England', 'short_name': 'England', 'types': ['administrative_area_level_1', 'political']}, {'long_name': 'United Kingdom', 'short_name': 'GB', 'types': ['country', 'political']}], 'formatted_address': 'Venn St, London SW4 0BD, UK', 'geometry': {'bounds': {'northeast': {'lat': 51.4629809, 'lng': -0.1375277}, 'southwest': {'lat': 51.4624682, 'lng': -0.1383529}}, 'location': {'lat': 51.4626865, 'lng': -0.1377927}, 'location_type': 'APPROXIMATE', 'viewport': {'northeast': {'lat': 51.4640735302915, 'lng': -0.136591319708498}, 'southwest': {'lat': 51.4613755697085, 'lng': -0.139289280291502}}}, 'place_id': 'ChIJN3qigFIEdkgRddPwWYJlC_w', 'types': ['postal_code']}, {'address_components': [{'long_name': 'Clapham Town', 'short_name': 'Clapham Town', 'types': ['administrative_area_level_4', 'political']}, {'long_name': 'London', 'short_name': 'London', 'types': ['postal_town']}, {'long_name': 'Greater London', 'short_name': 'Greater London', 'types': ['administrative_area_level_2', 'political']}, {'long_name': 'England', 'short_name': 'England', 'types': ['administrative_area_level_1', 'political']}, {'long_name': 'United Kingdom', 'short_name': 'GB', 'types': ['country', 'political']}], 'formatted_address': 'Clapham Town, London, UK', 'geometry': {'bounds': {'northeast': {'lat': 51.47166619999999, 'lng': -0.1306055}, 'southwest': {'lat': 51.45971369999999, 'lng': -0.1512401}}, 'location': {'lat': 51.4658813, 'lng': -0.1413263}, 'location_type': 'APPROXIMATE', 'viewport': {'northeast': {'lat': 51.47166619999999, 'lng': -0.1306055}, 'southwest': {'lat': 51.45971369999999, 'lng': -0.1512401}}}, 'place_id': 'ChIJdSm_Yk0EdkgRORqsBNKfVUo', 'types': ['administrative_area_level_4', 'political']}, {'address_components': [{'long_name': 'Clapham', 'short_name': 'Clapham', 'types': ['political', 'sublocality', 'sublocality_level_1']}, {'long_name': 'London', 'short_name': 'London', 'types': ['postal_town']}, {'long_name': 'Greater London', 'short_name': 'Greater London', 'types': ['administrative_area_level_2', 'political']}, {'long_name': 'England', 'short_name': 'England', 'types': ['administrative_area_level_1', 'political']}, {'long_name': 'United Kingdom', 'short_name': 'GB', 'types': ['country', 'political']}], 'formatted_address': 'Clapham, London, UK', 'geometry': {'bounds': {'northeast': {'lat': 51.47166619999999, 'lng': -0.1273889}, 'southwest': {'lat': 51.4417523, 'lng': -0.1512401}}, 'location': {'lat': 51.4556236, 'lng': -0.1385876}, 'location_type': 'APPROXIMATE', 'viewport': {'northeast': {'lat': 51.47166619999999, 'lng': -0.1273889}, 'southwest': {'lat': 51.4417523, 'lng': -0.1512401}}}, 'place_id': 'ChIJy0zBQjQEdkgRh7jPLhAM8l0', 'types': ['political', 'sublocality', 'sublocality_level_1']}, {'address_components': [{'long_name': 'SW4', 'short_name': 'SW4', 'types': ['postal_code', 'postal_code_prefix']}, {'long_name': 'London', 'short_name': 'London', 'types': ['postal_town']}, {'long_name': 'Greater London', 'short_name': 'Greater London', 'types': ['administrative_area_level_2', 'political']}, {'long_name': 'England', 'short_name': 'England', 'types': ['administrative_area_level_1', 'political']}, {'long_name': 'United Kingdom', 'short_name': 'GB', 'types': ['country', 'political']}], 'formatted_address': 'London SW4, UK', 'geometry': {'bounds': {'northeast': {'lat': 51.4748852, 'lng': -0.1182876}, 'southwest': {'lat': 51.4479054, 'lng': -0.1606512}}, 'location': {'lat': 51.4597574, 'lng': -0.137753}, 'location_type': 'APPROXIMATE', 'viewport': {'northeast': {'lat': 51.4748852, 'lng': -0.1182876}, 'southwest': {'lat': 51.4479054, 'lng': -0.1606512}}}, 'place_id': 'ChIJ_czqJzQEdkgRGqiorBMZls0', 'types': ['postal_code', 'postal_code_prefix']}, {'address_components': [{'long_name': 'Lambeth', 'short_name': 'Lambeth', 'types': ['political', 'sublocality', 'sublocality_level_1']}, {'long_name': 'London', 'short_name': 'London', 'types': ['postal_town']}, {'long_name': 'Greater London', 'short_name': 'Greater London', 'types': ['administrative_area_level_2', 'political']}, {'long_name': 'England', 'short_name': 'England', 'types': ['administrative_area_level_1', 'political']}, {'long_name': 'United Kingdom', 'short_name': 'GB', 'types': ['country', 'political']}], 'formatted_address': 'Lambeth, London, UK', 'geometry': {'bounds': {'northeast': {'lat': 51.5098445, 'lng': -0.0900332}, 'southwest': {'lat': 51.4109847, 'lng': -0.1512401}}, 'location': {'lat': 51.4935082, 'lng': -0.1178424}, 'location_type': 'APPROXIMATE', 'viewport': {'northeast': {'lat': 51.5098445, 'lng': -0.0900332}, 'southwest': {'lat': 51.4109847, 'lng': -0.1512401}}}, 'place_id': 'ChIJHSzWIr8EdkgRcmFNv46Ix90', 'types': ['political', 'sublocality', 'sublocality_level_1']}, {'address_components': [{'long_name': 'London Borough of Lambeth', 'short_name': 'London Borough of Lambeth', 'types': ['administrative_area_level_3', 'political']}, {'long_name': 'London', 'short_name': 'London', 'types': ['postal_town']}, {'long_name': 'Greater London', 'short_name': 'Greater London', 'types': ['administrative_area_level_2', 'political']}, {'long_name': 'England', 'short_name': 'England', 'types': ['administrative_area_level_1', 'political']}, {'long_name': 'United Kingdom', 'short_name': 'GB', 'types': ['country', 'political']}], 'formatted_address': 'London Borough of Lambeth, London, UK', 'geometry': {'bounds': {'northeast': {'lat': 51.5098711, 'lng': -0.07830669999999999}, 'southwest': {'lat': 51.410991, 'lng': -0.1512314}}, 'location': {'lat': 51.4571477, 'lng': -0.1230681}, 'location_type': 'APPROXIMATE', 'viewport': {'northeast': {'lat': 51.5098711, 'lng': -0.07830669999999999}, 'southwest': {'lat': 51.410991, 'lng': -0.1512314}}}, 'place_id': 'ChIJt1zJSGgEdkgRsEAeRjCuDgo', 'types': ['administrative_area_level_3', 'political']}, {'address_components': [{'long_name': 'London', 'short_name': 'London', 'types': ['postal_town']}, {'long_name': 'Greater London', 'short_name': 'Greater London', 'types': ['administrative_area_level_2', 'political']}, {'long_name': 'England', 'short_name': 'England', 'types': ['administrative_area_level_1', 'political']}, {'long_name': 'United Kingdom', 'short_name': 'GB', 'types': ['country', 'political']}], 'formatted_address': 'London, UK', 'geometry': {'bounds': {'northeast': {'lat': 51.6723432, 'lng': 0.148271}, 'southwest': {'lat': 51.38494009999999, 'lng': -0.3514683}}, 'location': {'lat': 51.5569879, 'lng': -0.1411791}, 'location_type': 'APPROXIMATE', 'viewport': {'northeast': {'lat': 51.6723432, 'lng': 0.148271}, 'southwest': {'lat': 51.38494009999999, 'lng': -0.3514683}}}, 'place_id': 'ChIJ8_MXt1sbdkgRCrIAOXkukUk', 'types': ['postal_town']}, {'address_components': [{'long_name': 'London', 'short_name': 'London', 'types': ['locality', 'political']}, {'long_name': 'London', 'short_name': 'London', 'types': ['postal_town']}, {'long_name': 'Greater London', 'short_name': 'Greater London', 'types': ['administrative_area_level_2', 'political']}, {'long_name': 'England', 'short_name': 'England', 'types': ['administrative_area_level_1', 'political']}, {'long_name': 'United Kingdom', 'short_name': 'GB', 'types': ['country', 'political']}], 'formatted_address': 'London, UK', 'geometry': {'bounds': {'northeast': {'lat': 51.6723432, 'lng': 0.148271}, 'southwest': {'lat': 51.38494009999999, 'lng': -0.3514683}}, 'location': {'lat': 51.5072178, 'lng': -0.1275862}, 'location_type': 'APPROXIMATE', 'viewport': {'northeast': {'lat': 51.6723432, 'lng': 0.148271}, 'southwest': {'lat': 51.38494009999999, 'lng': -0.3514683}}}, 'place_id': 'ChIJdd4hrwug2EcRmSrV3Vo6llI', 'types': ['locality', 'political']}, {'address_components': [{'long_name': 'Greater London', 'short_name': 'Greater London', 'types': ['administrative_area_level_2', 'political']}, {'long_name': 'England', 'short_name': 'England', 'types': ['administrative_area_level_1', 'political']}, {'long_name': 'United Kingdom', 'short_name': 'GB', 'types': ['country', 'political']}], 'formatted_address': 'Greater London, UK', 'geometry': {'bounds': {'northeast': {'lat': 51.6918726, 'lng': 0.3339957}, 'southwest': {'lat': 51.28676, 'lng': -0.5103751}}, 'location': {'lat': 51.4309209, 'lng': -0.0936496}, 'location_type': 'APPROXIMATE', 'viewport': {'northeast': {'lat': 51.6918726, 'lng': 0.3339957}, 'southwest': {'lat': 51.28676, 'lng': -0.5103751}}}, 'place_id': 'ChIJb-IaoQug2EcRi-m4hONz8S8', 'types': ['administrative_area_level_2', 'political']}, {'address_components': [{'long_name': 'England', 'short_name': 'England', 'types': ['administrative_area_level_1', 'political']}, {'long_name': 'United Kingdom', 'short_name': 'GB', 'types': ['country', 'political']}], 'formatted_address': 'England, UK', 'geometry': {'bounds': {'northeast': {'lat': 55.81165979999999, 'lng': 1.7629159}, 'southwest': {'lat': 49.8647411, 'lng': -6.4185458}}, 'location': {'lat': 52.3555177, 'lng': -1.1743197}, 'location_type': 'APPROXIMATE', 'viewport': {'northeast': {'lat': 55.81165979999999, 'lng': 1.7629159}, 'southwest': {'lat': 49.8647411, 'lng': -6.4185458}}}, 'place_id': 'ChIJ39UebIqp0EcRqI4tMyWV4fQ', 'types': ['administrative_area_level_1', 'political']}, {'address_components': [{'long_name': 'United Kingdom', 'short_name': 'GB', 'types': ['country', 'political']}], 'formatted_address': 'United Kingdom', 'geometry': {'bounds': {'northeast': {'lat': 60.91569999999999, 'lng': 33.9165549}, 'southwest': {'lat': 34.5614, 'lng': -8.8988999}}, 'location': {'lat': 55.378051, 'lng': -3.435973}, 'location_type': 'APPROXIMATE', 'viewport': {'northeast': {'lat': 60.91569999999999, 'lng': 33.9165549}, 'southwest': {'lat': 34.5614, 'lng': -8.8988999}}}, 'place_id': 'ChIJqZHHQhE7WgIReiWIMkOg-MQ', 'types': ['country', 'political']}]
    address = address[0]['address_components']
    print(address[0]['long_name'] + " " + address[1]['long_name'])