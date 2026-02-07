from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3
import smtplib

app = Flask(__name__)
CORS(app)

def get_db_connection():
    conn = sqlite3.connect("database.db")
    conn.row_factory = sqlite3.Row
    return conn

def setup_db():
    conn = get_db_connection()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS applications (
            id INTEGER PRIMARY KEY,
            name TEXT,
            email TEXT,
            phone TEXT,
            message TEXT
        )
    """)
    conn.commit()
    conn.close()

setup_db()

def send_email(to_email, name):
    sender_email = "your_email@gmail.com"
    sender_password = "your_app_password" # Gmail App Password
    subject = "Application Received"
    body = f"Hello {name},\n\nYour application has been received. Thank you!"
    email_text = f"Subject: {subject}\n\n{body}"

    server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
    server.login(sender_email, sender_password)
    server.sendmail(sender_email, to_email, email_text)
    server.quit()
    
@app.route("/apply", methods=["POST"])
def apply():
    data = request.json
    name = data.get("name")
    email = data.get("email")
    phone = data.get("phone")
    message = data.get("message")

    conn = get_db_connection()
    conn.execute(
        "INSERT INTO applications (name, email, phone, message) VALUES (?, ?, ?, ?)",
        (name, email, phone, message)
    )
    conn.commit()
    conn.close()

    try:
        send_email(email, name)
        return jsonify({"message": "Application submitted and email sent!"})
    except:
        return jsonify({"message": "Application submitted but email failed."})

if __name__ == "__main__":
    app.run(debug=True)