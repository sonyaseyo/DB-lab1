import psycopg2
import time
from concurrent.futures import ThreadPoolExecutor
import db


def in_place_update(user_id):
    conn = psycopg2.connect(user=db.username, password=db.password, dbname=db.db)
    cursor = conn.cursor()
    cursor.execute(db.sqldrop)
    cursor.execute(db.sqlcreate)
    cursor.execute(db.sqlinsert)
    for i in range(10_000):
        cursor.execute(f"UPDATE user_counter SET counter = counter + 1 WHERE user_id = {user_id}")
    conn.commit()
    conn.close()

start_time = time.time()

with ThreadPoolExecutor(max_workers=10) as exec:
        exec.map(in_place_update, [1 for i in range(10)])

end_time = time.time()
total_time = end_time - start_time

print("chumak sofiia; km-12. lab-1. #2.")
print(f"execution time: {total_time} sec.") #22.898