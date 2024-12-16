import psycopg2

def postgres_connect():
    try:
        pg_conn = psycopg2.connect(
            user='me',
            password='123123',
            dbname='django_proj12',
            port='5432',
            host='localhost'
        )
        print("Connection successful!")
        return pg_conn
    except psycopg2.OperationalError as err:
        print(f"Connection failed: {err}")
        return None

# Пример использования
if __name__ == "__main__":
    connection = postgres_connect()
    if connection:
        # Закрытие соединения
        connection.close()