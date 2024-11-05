import psycopg2
from psycopg2 import DatabaseError
from config.data_base import user,password,port,db_name,domain

def check_connection():
    try:
        #connection
        connection = psycopg2.connect(
            host=domain,
            database=db_name,
            user=user,
            password=password,
            port=port,
        )
        print("Connection successful")

        # close connection
        connection.close()
    except DatabaseError as err:
        print(f"Error connection: {err}")

if __name__ == "__main__":
    check_connection()
