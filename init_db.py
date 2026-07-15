import sqlite3

conn = sqlite3.connect(
    'database.db'
)

cursor = conn.cursor()

# =========================
# USERS TABLE
# =========================

cursor.execute('''

CREATE TABLE IF NOT EXISTS users (

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    username TEXT NOT NULL,

    email TEXT NOT NULL UNIQUE,

    password TEXT NOT NULL
)

''')

# =========================
# APPLIANCES TABLE
# =========================

cursor.execute('''

CREATE TABLE IF NOT EXISTS appliances (

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    user_id INTEGER,

    appliance_name TEXT,

    power REAL,

    hours REAL,

    units REAL,

    bill REAL,

    category TEXT,

    created_at TIMESTAMP
    DEFAULT CURRENT_TIMESTAMP
)

''')

# =========================
# REMINDERS TABLE
# =========================

cursor.execute('''

CREATE TABLE IF NOT EXISTS reminders (

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    user_id INTEGER,

    title TEXT,

    reminder_time TEXT,

    status TEXT DEFAULT 'Pending'
)

''')

conn.commit()

conn.close()

print(
    "Database Created Successfully"
)