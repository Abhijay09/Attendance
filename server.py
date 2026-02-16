from flask import Flask, request, jsonify, render_template_string
import sqlite3
import datetime

app = Flask(__name__)

# --- DATABASE SETUP (SQLite) ---
def init_db():
    conn = sqlite3.connect('attendance.db')
    c = conn.cursor()
    # Create table if it doesn't exist
    c.execute('''CREATE TABLE IF NOT EXISTS students 
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                  name TEXT, 
                  roll_no TEXT, 
                  timestamp TEXT, 
                  status TEXT)''')
    conn.commit()
    conn.close()

init_db()

# --- HTML DASHBOARD (The Admin View) ---
HTML_PAGE = """
<!DOCTYPE html>
<html>
<head>
    <title>Live Attendance Dashboard</title>
    <meta http-equiv="refresh" content="3"> <!-- Auto-refresh every 3 sec -->
    <style>
        body { font-family: Arial, sans-serif; padding: 20px; background: #f4f4f9; }
        h1 { color: #333; }
        table { width: 100%; border-collapse: collapse; background: white; }
        th, td { border: 1px solid #ddd; padding: 12px; text-align: left; }
        th { background-color: #007bff; color: white; }
        tr:nth-child(even) { background-color: #f2f2f2; }
    </style>
</head>
<body>
    <h1>Classroom Live Feed</h1>
    <table>
        <tr><th>Name</th><th>Roll No</th><th>Time In</th><th>Status</th></tr>
        {% for row in rows %}
        <tr>
            <td>{{ row[1] }}</td>
            <td>{{ row[2] }}</td>
            <td>{{ row[3] }}</td>
            <td style="color:green; font-weight:bold;">{{ row[4] }}</td>
        </tr>
        {% endfor %}
    </table>
</body>
</html>
"""

@app.route('/')
def dashboard():
    conn = sqlite3.connect('attendance.db')
    c = conn.cursor()
    c.execute("SELECT * FROM students ORDER BY id DESC")
    rows = c.fetchall()
    conn.close()
    return render_template_string(HTML_PAGE, rows=rows)

@app.route('/mark_present', methods=['GET']) # Using GET for easiest App Inventor integration
def mark_present():
    name = request.args.get('name')
    roll_no = request.args.get('roll_no')
    time_now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    conn = sqlite3.connect('attendance.db')
    c = conn.cursor()
    c.execute("INSERT INTO students (name, roll_no, timestamp, status) VALUES (?, ?, ?, ?)", 
              (name, roll_no, time_now, "PRESENT"))
    conn.commit()
    conn.close()
    
    print(f"MARKED: {name} - {roll_no}")
    return "OK"

if __name__ == '__main__':
    # '0.0.0.0' makes it visible to phones on the network
    app.run(host='0.0.0.0', port=5000)
