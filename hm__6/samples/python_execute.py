import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config import SettingsBD
import psycopg2

def execute_query(query_file):
    with open(query_file, 'r') as file:
        sql = file.read()
    with psycopg2.connect(
        host=SettingsBD.HOST.value,
        database=SettingsBD.DATABASE.value,
        user=SettingsBD.USER.value,
        password=SettingsBD.PASSWORD.value
    ) as conn:
        with conn.cursor() as cur:
            cur.execute(sql)
            return cur.fetchall()

if __name__ == '__main__':
    print(execute_query('query_1.sql'))

