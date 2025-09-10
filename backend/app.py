import sqlite3
from flask import Flask, request, jsonify
from flask_cors import CORS
import uuid

app = Flask(__name__)
CORS(app)

DB_NAME = "parcel_service.db"


def init_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users (
                    id TEXT PRIMARY KEY,
                    username TEXT UNIQUE,
                    password TEXT,
                    role TEXT
                )''')

    c.execute('''CREATE TABLE IF NOT EXISTS parcels (
                    id TEXT PRIMARY KEY,
                    description TEXT,
                    status TEXT,
                    user_id TEXT,
                    FOREIGN KEY(user_id) REFERENCES users(id)
                )''')
    conn.commit()
    conn.close()


@app.route("/register", methods=["POST"])
def register():
    data = request.json
    user_id = str(uuid.uuid4())
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    try:
        c.execute("INSERT INTO users (id, username, password, role) VALUES (?, ?, ?, ?)",
                  (user_id, data["username"], data["password"], data["role"]))
        conn.commit()
    except sqlite3.IntegrityError:
        return jsonify({"error": "Username already exists"}), 400
    conn.close()
    return jsonify({"message": "User registered successfully", "id": user_id})


@app.route("/login", methods=["POST"])
def login():
    data = request.json
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE username=? AND password=? AND role=?",
              (data["username"], data["password"], data["role"]))
    user = c.fetchone()
    conn.close()
    if user:
        return jsonify({"message": "Login successful", "id": user[0]})
    return jsonify({"error": "Invalid credentials"}), 401


@app.route("/parcels", methods=["POST"])
def add_parcel():
    data = request.json
    parcel_id = str(uuid.uuid4())
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("INSERT INTO parcels (id, description, status, user_id) VALUES (?, ?, ?, ?)",
              (parcel_id, data["description"], "In Transit", data["user_id"]))
    conn.commit()
    conn.close()
    return jsonify({"message": "Parcel added successfully", "id": parcel_id})


@app.route("/parcels/<user_id>", methods=["GET"])
def get_parcels(user_id):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT * FROM parcels WHERE user_id=?", (user_id,))
    parcels = c.fetchall()
    conn.close()
    return jsonify([{"id": p[0], "description": p[1], "status": p[2]} for p in parcels])


if __name__ == "__main__":
    init_db()
    app.run(debug=True)
