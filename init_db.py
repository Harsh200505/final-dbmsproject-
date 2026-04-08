import sqlite3

conn = sqlite3.connect('database.db')
c = conn.cursor()

# Rooms table
c.execute('''
CREATE TABLE IF NOT EXISTS rooms (
    room_id INTEGER PRIMARY KEY AUTOINCREMENT,
    room_type TEXT,
    price INTEGER,
    status TEXT
)
''')

# Guests table
c.execute('''
CREATE TABLE IF NOT EXISTS guests (
    guest_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    phone TEXT,
    room_id INTEGER,
    checkin_date TEXT,
    checkout_date TEXT,
    total_bill INTEGER
)
''')

# Insert sample rooms
c.execute("DELETE FROM rooms")

rooms_data = [
    ("Single", 1000, "Available"),
    ("Double", 2000, "Available"),
    ("Deluxe", 3000, "Available"),
    ("Suite", 5000, "Available")
]

c.executemany("INSERT INTO rooms (room_type, price, status) VALUES (?, ?, ?)", rooms_data)

conn.commit()
conn.close()

print("Database Ready with Rooms!")