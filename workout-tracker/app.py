from flask import Flask, request, redirect, render_template, flash
import mariadb
from dotenv import load_dotenv
import os
from contextlib import contextmanager
import secrets

load_dotenv()
app = Flask(__name__, template_folder='templates', static_folder='static')
app.secret_key = secrets.token_hex(16)

@contextmanager
def get_db_connection():
    """
    Context manager for database connections to ensure proper resource handling.
    Automatically closes the connection when the context ends.
    """
    conn = mariadb.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASS"),
        port=int(os.getenv("DB_PORT", 3306)),
        database="workout_db"
    )
    try:
        yield conn
    finally:
        conn.close()

def get_data():
    """
    Retrieves exercise records with cardio and strength details from the workout_db database.
    Returns data including workout duration, intensity, and calories burned.
    """
    try:
        with get_db_connection() as conn:
            cur = conn.cursor(dictionary=True)  # Use dictionary cursor for named columns
            cur.execute("""
                SELECT
                    ers.id AS row_id,
                    date,
                    calories_lost,
                    cts.cardio_id,
                    sts.strength_id,
                    cts.duration_minutes AS cardio_duration,
                    cts.intensity AS cardio_intensity,
                    cts.cardio_type,
                    sts.duration_minutes AS strength_duration,
                    sts.intensity AS strength_intensity,
                    cts.duration_minutes + sts.duration_minutes AS total_duration
                FROM
                    EXERCISE_RECORDS ers
                JOIN
                    CARDIO_TRACKERS cts ON (ers.cardio_id = cts.cardio_id)
                JOIN
                    STRENGTH_TRACKERS sts ON (ers.strength_id = sts.strength_id)
                ORDER BY
                    date ASC;
            """)
            return cur.fetchall()
    except mariadb.Error as e:
        print(f"Database error: {e}")

@app.route('/')
def index():
    """
    Renders the index page with workout data for display.
    Handles database errors gracefully with appropriate user feedback.
    """
    data = get_data()
    return render_template('index.html', data=data)

@app.route('/add_record', methods=['POST'])
def add_record():
    """
    Processes form submission to add a new workout record.
    Creates entries for cardio and strength components, then links them in the main record.
    Provides user feedback and error handling for the database operations.
    """
    try:
        date = request.form['date']
        calories_lost = request.form['calories_lost']
        cardio_duration = request.form['cardio_duration']
        cardio_intensity = request.form['cardio_intensity']
        cardio_type = request.form['cardio_type']
        strength_duration = request.form['strength_duration']
        strength_intensity = request.form['strength_intensity']

        with get_db_connection() as conn:
            cur = conn.cursor()
            
            # Add cardio record
            cur.execute("""
                INSERT INTO CARDIO_TRACKERS (calories_lost, duration_minutes, intensity, cardio_type)
                VALUES (?, ?, ?, ?)
            """, (calories_lost, cardio_duration, cardio_intensity, cardio_type))
            cardio_id = cur.lastrowid
            
            # Add strength record
            cur.execute("""
                INSERT INTO STRENGTH_TRACKERS (duration_minutes, intensity)
                VALUES (?, ?)
            """, (strength_duration, strength_intensity))
            strength_id = cur.lastrowid
            
            # Create main exercise record linking both components
            cur.execute("""
                INSERT INTO EXERCISE_RECORDS (cardio_id, strength_id, date)
                VALUES (?, ?, ?)
            """, (cardio_id, strength_id, date))
            conn.commit()
            
        flash("Workout record added successfully!", "success")
    except mariadb.Error as e:
        flash(f"Error adding record: {e}", "error")
    except Exception as e:
        flash(f"An unexpected error occurred: {e}", "error")
        
    return redirect('/')

@app.route('/delete_record', methods=['POST'])
def delete_record():
    """
    Handles deletion of a workout record and its related components.
    Ensures proper cleanup of all related data with referential integrity.
    Provides feedback on operation success or failure.
    """
    try:
        row_id = request.form['row_id']
        
        with get_db_connection() as conn:
            cur = conn.cursor()
            
            # First get the cardio_id and strength_id for this record
            cur.execute("""
                SELECT cardio_id, strength_id FROM EXERCISE_RECORDS WHERE id = ?
            """, (row_id,))
            result = cur.fetchone()
            
            if not result:
                flash("Record not found", "error")
                return redirect('/')
                
            cardio_id, strength_id = result
            
            # Delete in correct order to maintain referential integrity
            cur.execute("DELETE FROM EXERCISE_RECORDS WHERE id = ?", (row_id,))
            cur.execute("DELETE FROM CARDIO_TRACKERS WHERE cardio_id = ?", (cardio_id,))
            cur.execute("DELETE FROM STRENGTH_TRACKERS WHERE strength_id = ?", (strength_id,))
            conn.commit()
            
        flash("Workout record deleted successfully!", "success")
    except mariadb.Error as e:
        flash(f"Database error: {e}", "error")
    except Exception as e:
        flash(f"An unexpected error occurred: {e}", "error")
        
    return redirect('/')

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=80, debug=True)