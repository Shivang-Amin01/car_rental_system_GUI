import sqlite3

def init_db():
    conn = sqlite3.connect('car_rental.db')
    c = conn.cursor()

    # Create tables
    c.execute('''CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY,
                    username TEXT NOT NULL,
                    password TEXT NOT NULL,
                    role TEXT NOT NULL)''')
    
    c.execute('''CREATE TABLE IF NOT EXISTS vehicles (
                    id INTEGER PRIMARY KEY,
                    model TEXT NOT NULL,
                    brand TEXT NOT NULL,
                    year INTEGER NOT NULL,
                    price_per_day REAL NOT NULL,
                    is_available INTEGER DEFAULT 1)''')

    c.execute('''CREATE TABLE IF NOT EXISTS customers (
                    id INTEGER PRIMARY KEY,
                    name TEXT NOT NULL,
                    address TEXT,
                    phone_number TEXT,
                    license_number TEXT)''')

    c.execute('''CREATE TABLE IF NOT EXISTS bookings (
                    id INTEGER PRIMARY KEY,
                    vehicle_id INTEGER,
                    customer_name TEXT,
                    rental_start TEXT,
                    rental_end TEXT,
                    rental_price REAL,
                    FOREIGN KEY(vehicle_id) REFERENCES vehicles(id))''')

    # Create default manager account if not exists
    c.execute("SELECT * FROM users WHERE username = 'manager'")
    if c.fetchone() is None:
        c.execute("INSERT INTO users (username, password, role) VALUES ('manager', 'man123', 'manager')")

    conn.commit()
    conn.close()

def get_db_connection():
    conn = sqlite3.connect('car_rental.db')
    conn.row_factory = sqlite3.Row
    return conn
