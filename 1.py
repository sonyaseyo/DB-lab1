import psycopg2
import time
from concurrent.futures import ThreadPoolExecutor
import db


conn = psycopg2.connect(user=db.username, password=db.password, dbname=db.db)
cursor = conn.cursor()
cursor.execute(db.sqldrop)
cursor.execute(db.sqlcreate)
cursor.execute(db.sqlinsert)


def lost_update(user_id):
    for i in range(10_000):
        cursor.execute(f"SELECT counter FROM user_counter WHERE user_id = {user_id}")
        counter = cursor.fetchone()[0]
        counter += 1
        cursor.execute(f"UPDATE user_counter SET counter = {counter} WHERE user_id = {user_id}")
    conn.commit()

start_time = time.time()

with ThreadPoolExecutor(max_workers = 10) as exec:
        exec.map(lost_update, [1 for i in range(10)])

end_time = time.time()
total_time = end_time - start_time

print("chumak sofiia; km-12. lab-1. #1.")
print(f"execution time: {total_time} sec.") #4.7925

cursor.close()
conn.close()