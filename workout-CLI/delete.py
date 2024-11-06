# Module Imports
import mariadb
import sys

f1 = open("creds/user.txt", "r")
f2 = open("creds/pass.txt", "r")
f3 = open("creds/host.txt", "r")
f4 = open("creds/port.txt", "r")

# Fetch command-line arguments
row_id = sys.argv[1]

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

# Deletes an exercise record from the workout_db database based on the provided row ID
# Removes the corresponding entries in EXERCISE_RECORDS, CARDIO_TRACKERS, and STRENGTH_TRACKERS tables
cur.execute(f"DELETE FROM EXERCISE_RECORDS WHERE id = {row_id};")
conn.commit()

cur.execute(f"DELETE FROM CARDIO_TRACKERS WHERE cardio_id = {row_id};")
conn.commit()

cur.execute(f"DELETE FROM STRENGTH_TRACKERS WHERE strength_id = {row_id};")
conn.commit()

print("Deleted!")

# Close the connection
cur.close()
conn.close()
f1.close()
f2.close()
f3.close()
f4.close()