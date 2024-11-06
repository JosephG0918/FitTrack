from flask import Flask, request, redirect, render_template
import mariadb

app = Flask(__name__, template_folder='templates', static_folder='static')

# Database connection details
with open("creds/user.txt", "r") as f1:
    user = f1.readline().strip()
with open("creds/pass.txt", "r") as f2:
    password = f2.readline().strip()
with open("creds/host.txt", "r") as f3:
    host = f3.readline().strip()
with open("creds/port.txt", "r") as f4:
    port = f4.readline().strip()

def get_data():
    conn = mariadb.connect(
        user=user,
        password=password,
        host=host,
        port=int(port),
        database="workout_db"
    )
    cur = conn.cursor()
    cur.execute("""
        SELECT
            ers.id AS ROW_ID,
            date,
            calories_lost,
            cts.duration_minutes AS cardio_duration,
            cts.intensity AS cardio_intensity,
            sts.duration_minutes AS strength_duration,
            sts.intensity AS strength_intensity,
            cts.duration_minutes + sts.duration_minutes AS total_duration
        FROM
            EXERCISE_RECORDS ers
        JOIN
            CARDIO_TRACKERS cts ON (ers.cardio_id = cts.cardio_id)
        JOIN
            STRENGTH_TRACKERS sts ON (ers.strength_id = sts.strength_id);
    """)
    data = cur.fetchall()
    conn.close()
    return data

@app.route('/')
def index():
    data = get_data()
    return render_template('index.html', data=data)

@app.route('/add_record', methods=['POST'])
def add_record():
    date = request.form['date']
    calories_lost = request.form['calories_lost']
    cardio_duration = request.form['cardio_duration']
    cardio_intensity = request.form['cardio_intensity']
    cardio_type = request.form['cardio_type']
    strength_duration = request.form['strength_duration']
    strength_intensity = request.form['strength_intensity']

    conn = mariadb.connect(
        user=user,
        password=password,
        host=host,
        port=int(port),
        database="workout_db"
    )
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO CARDIO_TRACKERS (calories_lost, duration_minutes, intensity, cardio_type)
        VALUES (?, ?, ?, ?)
    """, (calories_lost, cardio_duration, cardio_intensity, cardio_type))
    conn.commit()
    cardio_id = cur.lastrowid

    cur.execute("""
        INSERT INTO STRENGTH_TRACKERS (duration_minutes, intensity)
        VALUES (?, ?)
    """, (strength_duration, strength_intensity))
    conn.commit()
    strength_id = cur.lastrowid

    cur.execute("""
        INSERT INTO EXERCISE_RECORDS (cardio_id, strength_id, date)
        VALUES (?, ?, ?)
    """, (cardio_id, strength_id, date))
    conn.commit()

    conn.close()
    
    return redirect('/')

@app.route('/delete_record', methods=['POST'])
def delete_record():
    row_id = request.form['row_id']
    
    conn = mariadb.connect(
        user=user,
        password=password,
        host=host,
        port=int(port),
        database="workout_db"
    )
    cur = conn.cursor()

    # Delete from EXERCISE_RECORDS
    cur.execute("""
        DELETE FROM EXERCISE_RECORDS WHERE id = (?);
    """, (row_id,))
    conn.commit()

    # Delete from CARDIO_TRACKERS
    cur.execute("""
        DELETE FROM CARDIO_TRACKERS WHERE cardio_id = (?);
    """, (row_id,))
    conn.commit()

    # Delete from STRENGTH_TRACKERS
    cur.execute("""
        DELETE FROM STRENGTH_TRACKERS WHERE strength_id = (?);
    """, (row_id,))
    conn.commit()

    conn.close()

    return redirect('/')

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=80, debug=True)