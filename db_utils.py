import mysql.connector
from config import USER, PASSWORD, HOST
import math


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

    @staticmethod
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

    @staticmethod
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

    @staticmethod
    def add_journey_request(username, currentloc_lat, currentloc_lng, destination_lat, destination_lng, tod):
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
            values = (username, currentloc_lat, currentloc_lng, destination_lat, destination_lng, tod)
            cursor.execute(query, values)
            db_connection.commit()
            print(cursor.rowcount, "record inserted.")
            cursor.close()

        except Exception:
            raise DBConnectionError('Failed to read the database')

    @staticmethod
    def get_matching_journeys(
            min_time,
            max_time,
            curr_loc_lat,
            curr_loc_lng,
            curr_dest_lat,
            curr_dest_lng,
            username
    ):
        db_connection = None
        try:
            db_name = "BuddyWalk"
            db_connection = DB._connect_to_db(db_name)
        except Exception:
            raise DBConnectionError('Failed to read the database')
        cursor = db_connection.cursor()

        query1 = """
        SET @min_time = %s,
        @max_time = %s,
        @curr_loc_lat = %s,
        @curr_loc_lng = %s,
        @curr_dest_lat = %s,
        @curr_dest_lng = %s,
        @username = %s,
        @R = 3958761,
        @D = 1;
        """

        query2 = """
        SELECT * FROM BuddyWalk.journey_requests
        WHERE 
        ToD BETWEEN @min_time and @max_time
        AND
        user_username != @username
        AND
        @R * SQRT(POWER((CurrentLocLat - @curr_loc_lat), 2) + POWER(COS((CurrentLocLat + @curr_loc_lat) / 2)*(CurrentLocLng - @curr_loc_lng), 2)) < @D
        AND
        @R * SQRT(POWER((DestinationLat - @curr_dest_lat), 2) + POWER(COS((DestinationLat + @curr_dest_lat) / 2)*(DestinationLng - @curr_dest_lng), 2)) < @D;
        """

        values = (
            min_time,
            max_time,
            curr_loc_lat,
            curr_loc_lng,
            curr_dest_lat,
            curr_dest_lng,
            username)
        print(values)

        cursor.execute(query1, values)
        cursor.execute(query2)
        result = cursor.fetchall()

        if result:
            print("Matching Journey Requests:")
            for i in result:
                print(i)
        else:
            raise Exception("No Match Found.")
        cursor.close()

        return result

#
# DB.get_matching_journeys('2021-12-20T22:12:00', '2021-12-20T23:12:00', 0.8981902460764947,
# -0.0024100064816898335, 0.8981674206605371, -0.002007442799058838, 'sandy')
