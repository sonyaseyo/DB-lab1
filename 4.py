import psycopg2
import time
from concurrent.futures import ThreadPoolExecutor
import db


conn = psycopg2.connect(user=db.username, password=db.password, dbname=db.db)
cursor = conn.cursor()
cursor.execute(db.sqldrop)
cursor.execute(db.sqlcreate)
cursor.execute(db.sqlinsert)

def optimistic_concurrency_control_update(user_thread_id):
    with conn:
        for i in range(10_000):
            while True:
                cursor.execute(f"SELECT counter, version FROM user_counter WHERE user_id = {user_thread_id[0]}")
                current_values = cursor.fetchone()
                counter, version = current_values[0], current_values[1]
                counter += 1
                cursor.execute(
                    f"UPDATE user_counter SET counter = {counter}, version = {version + 1} WHERE user_id = {user_thread_id[0]} AND version = {version}")
                conn.commit()
                count = cursor.rowcount
                if count > 0:
                    break
    conn.close()


start_time = time.time()

with ThreadPoolExecutor(max_workers=10) as exec:
    exec.map(optimistic_concurrency_control_update, [(1, i) for i in range(10)])

end_time = time.time()
total_time = end_time - start_time

print("chumak sofiia; km-12. lab-1. #4.")
print(f"execution time: {total_time} sec.") #4.5224