# Workout Tracker Application 🏋️‍♂️ 📊

A Flask-based web application for tracking workout sessions with both cardio and strength training components. This application helps users record, manage, and analyze their exercise data over time.

## Features

- Log workout sessions with date, calories burned, and exercise details
- Track cardio exercises with duration, intensity, and type
- Record strength training with duration and intensity metrics
- View workout history in chronological order
- Calculate total workout duration for each session
- Delete unwanted workout records

## Requirements

- Python 3.11+ (Check the Pipfile)
- MariaDB/MySQL
- Pipenv (for dependency management)

## Project Structure

```
workout-tracker/
├── app.py              # Main application file
├── Pipfile             # Pipenv dependency definitions
├── Pipfile.lock        # Locked dependencies
├── templates/
│   └── index.html      # Main page template
├── static/
│   └── style.css       # Main page styles
└── .env                # Environment variables (not in version control)
README.md
LICENSE
```

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/JosephG0918/FitTrack.git
   cd workout-tracker
   ```

2. Install dependencies using Pipenv:
   
   Make sure you have pipenv installed. If not, install it using:
   ```
   pip install pipenv
   ```
   or
   ```
   sudo apt install pipenv
   ```
   
   Activate the virtual environment using:
   ```
   pipenv shell
   ```

   Then install all project dependencies using:
   ```
   pipenv install
   ```

   More info about pipenv [here](https://pypi.org/project/pipenv/)

3. Create a `.env` file in the project root with your database credentials:
   ```
   DB_HOST=localhost
   DB_USER=your_database_user
   DB_PASS=your_database_password
   DB_PORT=3306
   ```

4. Set up the database:
   
   Create a database named `workout_db` and set up the required tables:

   ```sql
   CREATE DATABASE workout_db;
   USE workout_db;

   CREATE TABLE CARDIO_TRACKERS (
     cardio_id INT AUTO_INCREMENT PRIMARY KEY,
     calories_lost INT NOT NULL,
     duration_minutes INT NOT NULL,
     intensity VARCHAR(50) NOT NULL,
     cardio_type VARCHAR(50) NOT NULL
   );

   CREATE TABLE STRENGTH_TRACKERS (
     strength_id INT AUTO_INCREMENT PRIMARY KEY,
     duration_minutes INT NOT NULL,
     intensity VARCHAR(50) NOT NULL
   );

    CREATE TABLE EXERCISE_RECORDS (
    cardio_id INT NOT NULL,
    strength_id INT NOT NULL,
    date DATE NOT NULL,
    PRIMARY KEY (cardio_id, strength_id, date),
    FOREIGN KEY (cardio_id) REFERENCES CARDIO_TRACKERS(cardio_id),
    FOREIGN KEY (strength_id) REFERENCES STRENGTH_TRACKERS(strength_id)
    );
   ```

   Entity Relationship Diagram:
   ![ERD](https://github.com/user-attachments/assets/d46587be-d8d4-46b8-aa79-a79c116fba1a)

## Usage

1. Activate the Pipenv environment and start the application:
   ```bash
   pipenv shell
   python app.py
   ```

2. Open your web browser and navigate to `http://localhost:80`

   **Note for Linux users:** 
   - Port 80 requires root privileges on Linux. If you encounter permission issues, modify the port in `app.py`:
     ```python
     # Change this line at the bottom of app.py
     app.run(host="0.0.0.0", port=5000, debug=True)
     ```
   - Then access the application at `http://localhost:5000` instead

3. To add a new workout record:
   - Fill out the form with your workout details
   - Click "Add Record" to save the data

4. To delete a workout record:
   - Find the record in the workout history table
   - Click the delete or "x" button next to the record

## Security Notes

- The application uses a randomly generated secret key for Flask sessions
- Database credentials are stored in environment variables for security
- Connection management ensures proper resource cleanup

## Credits
- Claude AI helping write this readme file.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
