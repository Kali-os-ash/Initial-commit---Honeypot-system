from flask import Flask, request, render_template
import sqlite3
import datetime

app = Flask(__name__)

# Function to log attacker data
def log_attack(ip, user_agent, username, password):
    conn = sqlite3.connect('honeypot.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS attacks (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        ip TEXT,
                        user_agent TEXT,
                        username TEXT,
                        password TEXT,
                        timestamp TEXT)''')
    
    timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    cursor.execute("INSERT INTO attacks (ip, user_agent, username, password, timestamp) VALUES (?, ?, ?, ?, ?)", 
                   (ip, user_agent, username, password, timestamp))
    conn.commit()
    conn.close()

    # Save logs to a text file
    with open("honeypot.log", "a") as log_file:
        log_file.write("{} - IP: {} - User-Agent: {} - Username: {} - Password: {}\n"
                       .format(timestamp, ip, user_agent, username, password))

# Fake login page
@app.route('/')
def fake_login():
    return render_template('login.html')

# Capture login attempts
@app.route('/login', methods=['POST'])
def capture_login():
    ip = request.remote_addr
    user_agent = request.headers.get('User-Agent')
    
    # Capture username & password
    username = request.form.get('username')
    password = request.form.get('password')

    log_attack(ip, user_agent, username, password)

    return "Access Denied! Incident Logged."

# View logged attack attempts
@app.route('/logs')
def view_logs():
    conn = sqlite3.connect('honeypot.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM attacks")
    data = cursor.fetchall()
    conn.close()
    
    log_html = "<h2>Honeypot Logs</h2><table border='1'><tr><th>ID</th><th>IP Address</th><th>User-Agent</th><th>Username</th><th>Password</th><th>Timestamp</th></tr>"
    for row in data:
        log_html += f"<tr><td>{row[0]}</td><td>{row[1]}</td><td>{row[2]}</td><td>{row[3]}</td><td>{row[4]}</td><td>{row[5]}</td></tr>"
    log_html += "</table>"
    
    return log_html

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8080)
