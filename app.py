from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

# Create the database and table if not exists
def init_db():
    conn = sqlite3.connect('bookings.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS bookings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            date TEXT NOT NULL,
            tour_type TEXT NOT NULL,
            tickets INTEGER NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

init_db()

# Home Page
@app.route('/')
def index():
    return render_template('index.html')

# Book Tickets Page
@app.route('/book', methods=['GET', 'POST'])
def book():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        date = request.form['date']
        tour_type = request.form['tour_type']
        tickets = request.form['tickets']

        conn = sqlite3.connect('bookings.db')
        c = conn.cursor()
        c.execute("INSERT INTO bookings (name, email, date, tour_type, tickets) VALUES (?, ?, ?, ?, ?)",
                  (name, email, date, tour_type, tickets))
        conn.commit()
        conn.close()

        return redirect('/thankyou')
    return render_template('book.html')

# View Bookings Page
@app.route('/bookings')
def bookings():
    conn = sqlite3.connect('bookings.db')
    c = conn.cursor()
    c.execute("SELECT * FROM bookings")
    all_bookings = c.fetchall()
    conn.close()
    return render_template('bookings.html', bookings=all_bookings)

# Thank You Page
@app.route('/thankyou')
def thankyou():
    return render_template('thankyou.html')

if __name__ == '__main__':
    app.run(debug=True)