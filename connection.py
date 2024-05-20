import mysql.connector as conn


class Database_connect:
    message = ""
    try:
        @staticmethod
        def saaa():
            connection = conn.connect(
                host='localhost',
                user='root',
                password='',
                database='isd2'
            )
            if connection.is_connected():
                Database_connect.message = "Connected"

                return connection
            connection.close()
    except Exception as e:
        print(e)
