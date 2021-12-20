import mysql.connector
from config import USER, PASSWORD, HOST


class DBConnectionError(Exception):
    pass


class DB:

    def _connect_to_db(db_name: str):
        cnx = mysql.connector.connect(host=HOST,
                                      user=USER,
                                      password=PASSWORD,
                                      auth_plugin='mysql_native_password',
                                      database=db_name)
        return cnx

    def get_all_records():
        db_connection = None
        try:
            db_name = "BuddyWalk"
            db_connection = DB._connect_to_db(db_name)
            cursor = db_connection.cursor()
            query = "SELECT * FROM BuddyWalk.user_details"
            cursor.execute(query)
            result = cursor.fetchall()
            for i in result:
                print(i)
            cursor.close()
            return result

        except Exception:
            raise DBConnectionError('Failed to read the database')

    def get_all_journey_requests():
        db_connection = None
        try:
            db_name = "BuddyWalk"
            db_connection = DB._connect_to_db(db_name)
            cursor = db_connection.cursor()
            query = "SELECT * FROM BuddyWalk.journey_requests"
            cursor.execute(query)
            result = cursor.fetchall()
            for i in result:
                print(i)
            cursor.close()
            return result

        except Exception:
            raise DBConnectionError('Failed to read the database')

    def add_journey_request(username, currentloc_lat, currentloc_lng, destination_lat, destination_lng, ToD):
        db_connection = None
        try:
            db_name = "BuddyWalk"
            db_connection = DB._connect_to_db(db_name)
            cursor = db_connection.cursor()
            query = """
            INSERT INTO journey_requests 
            (user_username, CurrentLocLat, CurrentLocLng, DestinationLat, DestinationLng, ToD)
            VALUES (%s, %s, %s, %s, %s, %s)
            """
            values = (username, currentloc_lat, currentloc_lng, destination_lat, destination_lng, ToD)
            cursor.execute(query, values)
            db_connection.commit()
            print(cursor.rowcount, "record inserted.")
            cursor.close()

        except Exception:
            raise DBConnectionError('Failed to read the database')

    def get_matching_journeys(min_time, max_time,
                      curr_loc_lat, curr_loc_lng, curr_dest_lat, curr_dest_lng,
                      username):
        db_connection = None
        try:
            db_name = "BuddyWalk"
            db_connection = DB._connect_to_db(db_name)
            cursor = db_connection.cursor()
            query = """
            SELECT * FROM BuddyWalk.journey_requests
            WHERE
            ToD BETWEEN %s and %s
            AND
            SQRT( POWER((CurrentLocLat - %s), 2) + POWER((CurrentLocLng - %s), 2)) < 0.015
            AND
            SQRT( POWER((DestinationLat - %s), 2) + POWER((DestinationLng - %s), 2)) < 0.015
            AND user_username != %s;
            """
            values = (min_time, max_time,
                      curr_loc_lat, curr_loc_lng, curr_dest_lat, curr_dest_lng,
                      username)
            cursor.execute(query, values)
            result = cursor.fetchall()
            if result:
                print("Matching Journey Requests:")
                for i in result:
                    print(i)
            else:
                print("Nobody found :(")
            cursor.close()
            return result

        except Exception:
            raise DBConnectionError('Failed to read the database')