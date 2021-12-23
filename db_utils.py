import mysql.connector
from config import USER, PASSWORD, HOST


class DBConnectionError(Exception):
    pass


class DB:

    @staticmethod
    def _connect_to_db(db_name: str):
        cnx = mysql.connector.connect(host=HOST,
                                      user=USER,
                                      password=PASSWORD,
                                      auth_plugin='mysql_native_password',
                                      database=db_name)
        return cnx

    @staticmethod
    def get_all_user_records():

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
    def add_journey_request(
            user_id: str,
            username: str,
            curr_loc_lat: float,
            curr_loc_lng: float,
            destination_lat: float,
            destination_lng: float,
            tod: str,
            phone_no: int
            ) -> None:

        try:
            db_name = "BuddyWalk"
            db_connection = DB._connect_to_db(db_name)
            cursor = db_connection.cursor()

            query = """
            INSERT INTO journey_requests 
            (user_id, user_username, CurrentLocLat, CurrentLocLng, DestinationLat, DestinationLng, ToD, phone_number)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """

            values = (
                user_id,
                username,
                curr_loc_lat,
                curr_loc_lng,
                destination_lat,
                destination_lng,
                tod,
                phone_no
            )
            cursor.execute(query, values)
            db_connection.commit()
            print(cursor.rowcount, "record successfully inserted into Journey Requests table.")
            cursor.close()

        except Exception:
            raise DBConnectionError('Failed to insert the Journey Request record')

    @staticmethod
    def get_matching_journeys(
            min_time: str,
            max_time: str,
            curr_loc_lat: float,
            curr_loc_lng: float,
            curr_dest_lat: float,
            curr_dest_lng: float,
            username: str
    ) -> list:

        try:
            db_name = "BuddyWalk"
            db_connection = DB._connect_to_db(db_name)
            cursor = db_connection.cursor()

            query1 = """
            SET @min_time = %s,
            @max_time = %s,
            @curr_loc_lat = %s,
            @curr_loc_lng = %s,
            @curr_dest_lat = %s,
            @curr_dest_lng = %s,
            @username = %s,
            @R = 3958.761,
            @D = 1;
            """

            query2 = """
            SELECT * FROM BuddyWalk.journey_requests
            WHERE 
            ToD BETWEEN @min_time and @max_time
            AND
            user_username != @username
            AND
            matched = 'False'
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

            cursor.execute(query1, values)
            cursor.execute(query2)
            result = cursor.fetchall()

            if result:
                print("Matching Journey Requests:")
                for i in result:
                    print(i)
            else:
                print("No matching Journey Request at present.")
                return []
            cursor.close()

            return result

        except Exception:
            raise DBConnectionError('Failed to search for matching journeys')

    @staticmethod
    def get_record(user_id: str) -> tuple:

        try:
            db_name = "BuddyWalk"
            db_connection = DB._connect_to_db(db_name)
            cursor = db_connection.cursor()

            query = """
            SELECT * FROM BuddyWalk.journey_requests
            WHERE
            user_id = %s
            """

            cursor.execute(query, (user_id,))  # this syntax looks wrong, but is necessary
            result = cursor.fetchall()[0]
            if not result:
                print("Could not get record.")
            cursor.close()
            return result

        except Exception:
            raise DBConnectionError('Failed to get Journey Request record')

    @staticmethod
    def add_match(journey_request: tuple, buddy_journey_request: tuple) -> None:

        try:
            db_name = "BuddyWalk"
            db_connection = DB._connect_to_db(db_name)
            cursor = db_connection.cursor()

            query = """
            INSERT INTO BuddyWalk.matches
            (user_id_1, user_id_2)
            VALUES (%s, %s)
            """

            values = (journey_request[0], buddy_journey_request[0])
            cursor.execute(query, values)
            db_connection.commit()
            print(cursor.rowcount, "record successfully inserted into Matches table.")
            cursor.close()

        except Exception:
            raise DBConnectionError('Failed to insert match record into Matches table')

    @staticmethod
    def update_matched_journeys(journey_request: tuple, buddy_journey_request: tuple) -> None:

        try:
            db_name = "BuddyWalk"
            db_connection = DB._connect_to_db(db_name)
            cursor = db_connection.cursor()

            query = """
            UPDATE BuddyWalk.journey_requests
            SET matched = 'True'
            WHERE
            user_id = %s
            OR
            user_id = %s
            """

            values = (journey_request[0], buddy_journey_request[0])
            cursor.execute(query, values)
            db_connection.commit()
            if cursor.rowcount:
                print(cursor.rowcount, "records successfully updated in Journey Requests table.")
            cursor.close()

        except Exception:
            raise DBConnectionError('Failed to update Journey Requests table with matches')

    @staticmethod
    def get_match(user_id: str) -> tuple:

        try:
            db_name = "BuddyWalk"
            db_connection = DB._connect_to_db(db_name)
            cursor = db_connection.cursor()

            query = """
            SELECT * FROM BuddyWalk.matches
            WHERE
            user_id_1 = %s
            OR
            user_id_2 = %s
            """

            cursor.execute(query, (user_id, user_id))
            result = cursor.fetchall()[0]
            if cursor.rowcount:
                print(cursor.rowcount, "record found in Matches table.")
            cursor.close()
            if not result:
                return ()
            return result

        except Exception:
            raise DBConnectionError('Failed to retrieve match')
