import sqlite3
import csv

conn = sqlite3.connect('hotel.db')
cursor = conn.cursor()

print("Starting import...")

# Clear old data
cursor.execute("DELETE FROM rooms")

with open('rooms_data.csv', 'r') as file:
    reader = csv.DictReader(file)

    for row in reader:
        print("Inserting:", row)  # DEBUG LINE
        cursor.execute(
            "INSERT INTO rooms (room_type, price, status) VALUES (?, ?, 'Available')",
            (row['room_type'], row['price'])
        )

conn.commit()
conn.close()

print("Data Imported Successfully!")