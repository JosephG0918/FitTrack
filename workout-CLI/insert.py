# Module Imports
import mariadb
import sys

f1 = open("creds/user.txt", "r")
f2 = open("creds/pass.txt", "r")
f3 = open("creds/host.txt", "r")
f4 = open("creds/port.txt", "r")

# Fetch command-line arguments
calories_lost = sys.argv[1]
cardio_duration_minutes = sys.argv[2]
cardio_intensity = sys.argv[3]
cardio_type = sys.argv[4]
strength_duration = sys.argv[5]
strength_intensity = sys.argv[6]
date = sys.argv[7]

# Connect to MariaDB Platform
try:
    conn = mariadb.connect(
        user=str(f1.readline()),
        password=str(f2.readline()),
        host=str(f3.readline()),
        port=int(f4.readline()),
        database="workout_db"
    )
except mariadb.Error as e:
    print(f"Error connecting to MariaDB Platform: {e}")

# Get Cursor
cur = conn.cursor()

# Adds a new exercise record to the workout_db database.
# Inserts entries into CARDIO_TRACKERS and STRENGTH_TRACKERS tables, then creates an entry in EXERCISE_RECORDS linking the cardio and strength records.
sql = """
    INSERT INTO CARDIO_TRACKERS (calories_lost, duration_minutes, intensity, cardio_type)
    VALUES (%s, %s, %s, %s)
"""
values = (calories_lost, cardio_duration_minutes, cardio_intensity, cardio_type)
cur.execute(sql, values)
conn.commit()
cardio_id = cur.lastrowid

sql = """
    INSERT INTO STRENGTH_TRACKERS (duration_minutes, intensity)
    VALUES (%s, %s)
"""
values = (strength_duration, strength_intensity)
cur.execute(sql, values)
conn.commit()
strength_id = cur.lastrowid

sql = """
    INSERT INTO EXERCISE_RECORDS (cardio_id, strength_id, date)
    VALUES (%s, %s, %s)
"""
values = (cardio_id, strength_id, date)
cur.execute(sql, values)
conn.commit()

print("Inserted!")

# Close the connection
cur.close()
conn.close()
f1.close()
f2.close()
f3.close()
f4.close()