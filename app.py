from flask import Flask, render_template, request, redirect
import sqlite3
from datetime import datetime

app = Flask(__name__)

def get_db():
    return sqlite3.connect("database.db")

# DASHBOARD
@app.route('/')
def index():
    db = get_db()

    total_rooms = db.execute("SELECT COUNT(*) FROM rooms").fetchone()[0]
    available = db.execute("SELECT COUNT(*) FROM rooms WHERE status='Available'").fetchone()[0]
    occupied = db.execute("SELECT COUNT(*) FROM rooms WHERE status='Occupied'").fetchone()[0]

    guests = db.execute("SELECT * FROM guests ORDER BY guest_id DESC LIMIT 5").fetchall()

    return render_template('index.html',
                           total_rooms=total_rooms,
                           available=available,
                           occupied=occupied,
                           guests=guests)

# VIEW ROOMS
@app.route('/rooms')
def rooms():
    db = get_db()
    rooms = db.execute("SELECT * FROM rooms").fetchall()
    return render_template('rooms.html', rooms=rooms)

# ADD ROOM
@app.route('/add_room', methods=['GET', 'POST'])
def add_room():
    if request.method == 'POST':
        room_type = request.form['type']
        price = request.form['price']

        db = get_db()
        db.execute("INSERT INTO rooms (room_type, price, status) VALUES (?, ?, 'Available')",
                   (room_type, price))
        db.commit()

        return redirect('/rooms')

    return render_template('add_room.html')

# CHECK-IN
@app.route('/checkin', methods=['GET', 'POST'])
def checkin():
    db = get_db()

    if request.method == 'POST':
        name = request.form['name']
        phone = request.form['phone']
        room_id = request.form['room_id']

        db.execute("INSERT INTO guests (name, phone, room_id, checkin_date) VALUES (?, ?, ?, DATE('now'))",
                   (name, phone, room_id))

        db.execute("UPDATE rooms SET status='Occupied' WHERE room_id=?", (room_id,))
        db.commit()

        return redirect('/')

    rooms = db.execute("SELECT * FROM rooms WHERE status='Available'").fetchall()
    return render_template('checkin.html', rooms=rooms)

# CHECK-OUT
@app.route('/checkout', methods=['GET', 'POST'])
def checkout():
    db = get_db()

    if request.method == 'POST':
        guest_id = request.form['guest_id']

        guest = db.execute("SELECT * FROM guests WHERE guest_id=?", (guest_id,)).fetchone()
        room = db.execute("SELECT price FROM rooms WHERE room_id=?", (guest[3],)).fetchone()

        checkin_date = datetime.strptime(guest[4], "%Y-%m-%d")
        days = (datetime.now() - checkin_date).days + 1

        total = days * room[0]

        db.execute("UPDATE guests SET checkout_date=DATE('now'), total_bill=? WHERE guest_id=?",
                   (total, guest_id))

        db.execute("UPDATE rooms SET status='Available' WHERE room_id=?", (guest[3],))
        db.commit()

        return render_template('bill.html', guest=guest, total=total, days=days)

    guests = db.execute("SELECT * FROM guests WHERE checkout_date IS NULL").fetchall()
    return render_template('checkout.html', guests=guests)

# RUN APP
if __name__ == '__main__':
    app.run(debug=True)