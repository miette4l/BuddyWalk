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
            db_connection = _connect_to_db(db_name)
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
            db_connection = _connect_to_db(db_name)
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


    def add_journey_request(username, current_loc, destination, ToD):
        db_connection = None
        try:
            db_name = "BuddyWalk"
            db_connection = _connect_to_db(db_name)
            cursor = db_connection.cursor()
            query = """
            INSERT INTO journey_requests 
            (user_username, CurrentLoc, Destination, ToD)
            VALUES (%s, %s, %s, %s)
            """
            vals = (username, current_loc, destination, ToD)
            cursor.execute(query, vals)
            db_connection.commit()
            print(cursor.rowcount, "record inserted.")
            cursor.close()

        except Exception:
            raise DBConnectionError('Failed to read the database')


    def get_matching_times(min_time, max_time):
        db_connection = None
        try:
            db_name = "BuddyWalk"
            db_connection = _connect_to_db(db_name)
            cursor = db_connection.cursor()
            query = """
            SELECT * FROM BuddyWalk.journey_requests
            WHERE
            %s < ToD < %s;
            """
            vals = (min_time, max_time)
            cursor.execute(query, vals)
            result = cursor.fetchall()
            for i in result:
                print(i)
            cursor.close()
            return result

        except Exception:
            raise DBConnectionError('Failed to read the database')