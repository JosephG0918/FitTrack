# Module Imports
import mariadb
import pandas as pd
from tabulate import tabulate
import warnings

# Suppress warnings
warnings.filterwarnings('ignore')

f1 = open("creds/user.txt", "r")
f2 = open("creds/pass.txt", "r")
f3 = open("creds/host.txt", "r")
f4 = open("creds/port.txt", "r")

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

df = pd.read_sql_query("""SELECT ers.id AS ROW_ID, date, calories_lost AS cardio_calories_lost, cts.duration_minutes AS cardio_duration_min, cts.intensity AS cardio_intensity, cts.cardio_type AS cardio_type, sts.duration_minutes AS strength_duration_min, sts.intensity AS strength_intensity, cts.duration_minutes + sts.duration_minutes AS total_duration_min 
                          FROM EXERCISE_RECORDS ers JOIN CARDIO_TRACKERS cts ON (ers.cardio_id = cts.cardio_id) JOIN STRENGTH_TRACKERS sts ON (ers.strength_id = sts.strength_id);""", conn)
print(tabulate(df, headers='keys', tablefmt='fancy_grid'))

# Close the connection
conn.close()
f1.close()
f2.close()
f3.close()
f4.close()