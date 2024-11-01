import psycopg2
from psycopg2 import OperationalError
from config import SettingsBD


def check_connection():
    try:
        #connection
        connection = psycopg2.connect(
            host=SettingsBD.HOST.value,
            database=SettingsBD.DATABASE.value,
            user=SettingsBD.USER.value,
            password=SettingsBD.PASSWORD.value
        )
        print("Connection successful")

        # close connection
        connection.close()
    except OperationalError as err:
        print(f"Error connection: {err}")

if __name__ == "__main__":
    check_connection()
