from flask import Flask, render_template, request, redirect
import mysql.connector
from datetime import date, datetime

app = Flask(__name__)

# ---------------- DATABASE ----------------
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="bharath",   # change if needed
    database="attendance_db"
)

cursor = db.cursor()

# ---------------- HOME ----------------
@app.route('/')
def home():
    return render_template("index.html")


# ---------------- MARK ATTENDANCE ----------------
@app.route('/mark', methods=['POST'])
def mark():
    reg_no = request.form['reg_no']

    today = date.today()
    now = datetime.now().time()

    cursor.execute("SELECT * FROM student WHERE reg_no=%s", (reg_no,))
    student = cursor.fetchone()

    if student:
        cursor.execute(
            "INSERT INTO attendance (reg_no, date, time, status) VALUES (%s, %s, %s, %s)",
            (reg_no, today, now, "Present")
        )
        db.commit()
        return "Attendance Marked ✔"
    else:
        return "Student Not Found ❌"


# ---------------- LOGIN PAGE ----------------
@app.route('/login')
def login():
    return render_template("login.html")


# ---------------- LOGIN CHECK ----------------
@app.route('/check', methods=['POST'])
def check():
    username = request.form['username']
    password = request.form['password']
    semester = request.form['semester']

    cursor.execute("""
        SELECT * FROM teacher
        WHERE username=%s AND password=%s
    """, (username, password))

    result = cursor.fetchone()

    if result:
        return redirect(f'/dashboard/{semester}')
    else:
        return "Invalid Login ❌"


# ---------------- DASHBOARD ----------------
@app.route('/dashboard/<semester>')
def dashboard(semester):

    cursor.execute("""
        SELECT a.id, s.name, s.semester, a.reg_no, a.date, a.time, a.status
        FROM attendance a
        JOIN student s ON a.reg_no = s.reg_no
        WHERE s.semester = %s
    """, (semester,))

    data = cursor.fetchall()

    return render_template("dashboard.html", data=data, semester=semester)


# ---------------- RUN ----------------
if __name__ == '__main__':
    app.run(debug=True)