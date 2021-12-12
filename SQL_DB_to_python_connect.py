import mysql.connector
from config import USER, PASSWORD, HOST


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

    except Exception:
        raise DBConnectionError('Failed to read the database')


def main():
    get_all_records()


if __name__ == '__main__':
    main()
