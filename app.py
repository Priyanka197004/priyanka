"""
=============================================================
 FEEDBACK MANAGEMENT SYSTEM — BACKEND (Flask + MySQL)
=============================================================
 Serves the frontend (templates/index.html + static assets)
 and exposes a REST API that stores feedback in a MySQL
 database (Railway-hosted). Falls back to a local feedback.json
 file automatically if no MySQL environment variables are set,
 so the project still runs locally with zero extra setup.
=============================================================
"""

import json
import os
import re
from datetime import datetime

from flask import Flask, request, jsonify, render_template
from flask_cors import CORS

# -------------------------------------------------------------------
# App configuration
# -------------------------------------------------------------------
app = Flask(__name__, static_folder="static", template_folder="templates")
CORS(app)  # Safe to keep enabled even when frontend + backend share a domain

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.join(BASE_DIR, "feedback.json")

EMAIL_REGEX = re.compile(r"^[^\s@]+@[^\s@]+\.[^\s@]+$")

# -------------------------------------------------------------------
# MySQL configuration (Railway injects these when you link the
# MySQL service to this app's Variables tab as References)
# -------------------------------------------------------------------
MYSQL_HOST = os.environ.get("MYSQLHOST")
MYSQL_PORT = os.environ.get("MYSQLPORT", "3306")
MYSQL_USER = os.environ.get("MYSQLUSER")
MYSQL_PASSWORD = os.environ.get("MYSQLPASSWORD")
MYSQL_DATABASE = os.environ.get("MYSQLDATABASE")

USE_MYSQL = all([MYSQL_HOST, MYSQL_USER, MYSQL_PASSWORD, MYSQL_DATABASE])

if USE_MYSQL:
    import mysql.connector

    def get_connection():
        """Open a fresh MySQL connection using Railway-provided credentials."""
        return mysql.connector.connect(
            host=MYSQL_HOST,
            port=int(MYSQL_PORT),
            user=MYSQL_USER,
            password=MYSQL_PASSWORD,
            database=MYSQL_DATABASE,
        )

    def init_db():
        """Create the feedback table if it doesn't exist yet."""
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS feedback (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                email VARCHAR(255) NOT NULL,
                rating INT NOT NULL,
                feedback TEXT NOT NULL,
                created_at DATETIME NOT NULL
            )
            """
        )
        conn.commit()
        cursor.close()
        conn.close()

    def load_feedback():
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute(
            "SELECT name, email, rating, feedback, created_at AS date "
            "FROM feedback ORDER BY id DESC"
        )
        rows = cursor.fetchall()
        cursor.close()
        conn.close()
        for row in rows:
            row["date"] = row["date"].strftime("%Y-%m-%d %H:%M")
        return rows

    def insert_feedback(entry):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO feedback (name, email, rating, feedback, created_at) "
            "VALUES (%s, %s, %s, %s, %s)",
            (
                entry["name"],
                entry["email"],
                entry["rating"],
                entry["feedback"],
                entry["date"],
            ),
        )
        conn.commit()
        cursor.close()
        conn.close()

else:
    # ---------------- Local JSON fallback (no MySQL env vars found) ----------------
    def init_db():
        if not os.path.exists(DATA_FILE):
            with open(DATA_FILE, "w", encoding="utf-8") as file:
                json.dump([], file)

    def load_feedback():
        if not os.path.exists(DATA_FILE):
            return []
        try:
            with open(DATA_FILE, "r", encoding="utf-8") as file:
                content = file.read().strip()
                return json.loads(content) if content else []
        except (json.JSONDecodeError, IOError):
            return []

    def insert_feedback(entry):
        entries = load_feedback()
        entries.insert(0, entry)
        with open(DATA_FILE, "w", encoding="utf-8") as file:
            json.dump(entries, file, indent=2, ensure_ascii=False)


# -------------------------------------------------------------------
# Validation
# -------------------------------------------------------------------
def validate_payload(data):
    errors = []

    name = (data.get("name") or "").strip()
    email = (data.get("email") or "").strip()
    rating = data.get("rating")
    feedback = (data.get("feedback") or "").strip()

    if not name:
        errors.append("Name is required.")
    elif len(name) < 3:
        errors.append("Name must be at least 3 characters.")

    if not email:
        errors.append("Email is required.")
    elif not EMAIL_REGEX.match(email):
        errors.append("A valid email address is required.")

    if rating is None or not isinstance(rating, (int, float)) or not (1 <= rating <= 5):
        errors.append("Rating must be between 1 and 5.")

    if not feedback:
        errors.append("Feedback is required.")
    elif len(feedback) < 20:
        errors.append("Feedback must be at least 20 characters.")

    return errors


# -------------------------------------------------------------------
# Routes
# -------------------------------------------------------------------
@app.route("/", methods=["GET"])
def home():
    """Serves the feedback form (templates/index.html)."""
    return render_template("index.html")


@app.route("/api/health", methods=["GET"])
def health_check():
    return jsonify({
        "status": "ok",
        "message": "Feedback Management System API is running.",
        "storage": "mysql" if USE_MYSQL else "json_file",
    })


@app.route("/submit-feedback", methods=["POST"])
def submit_feedback():
    data = request.get_json(silent=True)

    if data is None:
        return jsonify({"status": "error", "message": "Invalid or missing JSON body."}), 400

    errors = validate_payload(data)
    if errors:
        return jsonify({"status": "error", "message": " ".join(errors)}), 400

    new_entry = {
        "name": data.get("name").strip(),
        "email": data.get("email").strip(),
        "rating": int(data.get("rating")),
        "feedback": data.get("feedback").strip(),
        "date": datetime.now().strftime("%Y-%m-%d %H:%M"),
    }

    insert_feedback(new_entry)

    return jsonify({
        "status": "success",
        "message": "Feedback submitted successfully.",
        "data": new_entry,
    }), 201


@app.route("/feedback", methods=["GET"])
def get_all_feedback():
    """Utility route to view all stored feedback entries."""
    return jsonify(load_feedback()), 200


# -------------------------------------------------------------------
# Entry point
# -------------------------------------------------------------------
init_db()

if __name__ == "__main__":
    # Railway (and most hosts) inject the PORT env var — fall back to 5000 locally
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, host="0.0.0.0", port=port)
