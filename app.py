
from flask import Flask, request, send_from_directory
import sqlite3
import os
import html

app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "messages.db")

# Create database
def create_database():
    conn = sqlite3.connect(DB_PATH)

    conn.execute('''
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            message TEXT NOT NULL
        )
    ''')

    conn.commit()
    conn.close()


# Display portfolio homepage
@app.route("/")
def home():
    return send_from_directory(BASE_DIR, "index.html")


# Load CSS
@app.route("/style.css")
def style():
    return send_from_directory(BASE_DIR, "style.css")


# Contact form backend
@app.route("/contact", methods=["POST"])
def contact():

    name = request.form.get("name", "").strip()
    email = request.form.get("email", "").strip()
    message = request.form.get("message", "").strip()

    if not name or not email or not message:
        return "Please fill all fields!", 400

    conn = sqlite3.connect(DB_PATH)

    conn.execute(
        "INSERT INTO messages (name, email, message) VALUES (?, ?, ?)",
        (name, email, message)
    )

    conn.commit()
    conn.close()

    return f'''
        <h1>Message Sent Successfully!</h1>
        <p>Thank you, {html.escape(name)}.</p>
        <a href="/">Return to Portfolio</a>
    '''


if __name__ == "__main__":
    create_database()
    app.run(host="0.0.0.0", port=5000)
