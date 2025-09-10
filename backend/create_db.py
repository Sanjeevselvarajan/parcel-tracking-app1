import sqlite3

DB_NAME = "parcel_service.db"

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

print("Database initialized successfully.")
conn.commit()
conn.close()
