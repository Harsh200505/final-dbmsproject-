import sqlite3
import csv

conn = sqlite3.connect("hotel.db")
cursor = conn.cursor()

with open("rooms_data.csv", "r") as file:
    reader = csv.reader(file)
    next(reader)

    for row in reader:
        room_type = row[0]
        price = row[1]
        status = "Available"   # ✅ default value

        cursor.execute(
            "INSERT INTO rooms (room_type, price, status) VALUES (?, ?, ?)",
            (room_type, price, status)
        )

conn.commit()
conn.close()

print("CSV Data Imported Successfully!")