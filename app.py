import sqlite3
import tkinter as tk
from tkinter import messagebox, ttk
from datetime import datetime

# Constants for database names and other repeated values
DATABASES = {
    "user": "user.db",
    "customer": "customer.db",
    "vehicle": "vehicle.db",
    "reservations": "reservations.db",
    "logs": "logs.db",
    "settings": "settings.db",
}

DAYS_OF_WEEK = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

# Utility class for database operations
class DatabaseUtility:
    @staticmethod
    def execute_query(db_name, query, params=(), fetch=False):
        conn = sqlite3.connect(db_name)
        cursor = conn.cursor()
        cursor.execute(query, params)
        result = cursor.fetchall() if fetch else None
        conn.commit()
        conn.close()
        return result

# Utility function to create Treeview widgets
def create_treeview(parent, columns, column_width=120):
    tree = ttk.Treeview(parent, columns=columns, show="headings")
    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, width=column_width)
    return tree

# Database initialization
class DatabaseManager:
    """Handles database operations."""
    @staticmethod
    def initialize_database():
        # Initialize user.db
        DatabaseUtility.execute_query(DATABASES["user"], """
            CREATE TABLE IF NOT EXISTS users (
                username TEXT PRIMARY KEY,
                password TEXT NOT NULL,
                role TEXT NOT NULL,
                first_name TEXT,
                last_name TEXT,
                phone TEXT,
                email TEXT,
                employee_id TEXT,
                address TEXT
            )
        """)
        dummy_users = [
            ('manager', 'man123', 'Manager', 'Default', 'Manager', '1234567890', 'manager@example.com', '1000', '123 Manager St'),
            ('employee1', 'emp123', 'Employee', 'John', 'Doe', '555-1111', 'john.doe@example.com', '2001', '456 Elm St'),
            ('employee2', 'emp123', 'Employee', 'Jane', 'Smith', '555-2222', 'jane.smith@example.com', '2002', '789 Oak St'),
            ('employee3', 'emp123', 'Employee', 'Alice', 'Johnson', '555-3333', 'alice.johnson@example.com', '2003', '123 Pine St'),
            ('employee4', 'emp123', 'Employee', 'Michael', 'Brown', '555-4444', 'michael.brown@example.com', '2004', '456 Maple St'),
            ('employee5', 'emp123', 'Employee', 'Emily', 'Davis', '555-5555', 'emily.davis@example.com', '2005', '789 Birch St'),
        ]
        for user in dummy_users:
            DatabaseUtility.execute_query(DATABASES["user"], """
                INSERT OR IGNORE INTO users (username, password, role, first_name, last_name, phone, email, employee_id, address)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, params=user)

        # Initialize customer.db
        DatabaseUtility.execute_query(DATABASES["customer"], """
            CREATE TABLE IF NOT EXISTS customers (
                name TEXT PRIMARY KEY,
                address TEXT NOT NULL,
                phone TEXT NOT NULL,
                license_number TEXT NOT NULL,
                insurance_company TEXT NOT NULL,
                policy_number TEXT NOT NULL
            )
        """)
        dummy_customers = [
            ("John Doe", "123 Elm Street", "555-1234", "LN12345", "ABC Insurance", "PN98765"),
            ("Jane Smith", "456 Oak Avenue", "555-5678", "LN67890", "XYZ Insurance", "PN54321"),
            ("Alice Johnson", "789 Pine Road", "555-9012", "LN11223", "DEF Insurance", "PN11223"),
        ]
        for customer in dummy_customers:
            DatabaseUtility.execute_query(DATABASES["customer"], """
                INSERT OR IGNORE INTO customers (name, address, phone, license_number, insurance_company, policy_number)
                VALUES (?, ?, ?, ?, ?, ?)
            """, params=customer)

        # Initialize feedback table
        DatabaseUtility.execute_query(DATABASES["customer"], """
            CREATE TABLE IF NOT EXISTS feedback (
                feedback_id INTEGER PRIMARY KEY AUTOINCREMENT,
                customer_name TEXT NOT NULL,
                rating INTEGER NOT NULL,
                comment TEXT,
                date TEXT NOT NULL
            )
        """)
        dummy_feedback = [
            ("John Doe", 5, "Excellent service! Highly recommend.", "2025-03-01"),
            ("Jane Smith", 4, "Good experience, but the car was slightly dirty.", "2025-03-02"),
            ("Alice Johnson", 3, "Average service. Could be better.", "2025-03-03"),
            ("Michael Brown", 5, "Amazing staff and great cars!", "2025-03-04"),
            ("Emily Davis", 2, "Had issues with the car's AC.", "2025-03-05"),
        ]
        for feedback in dummy_feedback:
            DatabaseUtility.execute_query(DATABASES["customer"], """
                INSERT INTO feedback (customer_name, rating, comment, date)
                VALUES (?, ?, ?, ?)
            """, params=feedback)

        # Initialize vehicle.db
        DatabaseUtility.execute_query(DATABASES["vehicle"], """
            CREATE TABLE IF NOT EXISTS vehicles (
                car_id INTEGER PRIMARY KEY,
                brand TEXT NOT NULL,
                model TEXT NOT NULL,
                year INTEGER NOT NULL,
                rate_per_day REAL NOT NULL,
                rate_per_km REAL NOT NULL,
                status TEXT NOT NULL DEFAULT 'Available'
            )
        """)
        dummy_vehicles = [
            (10, "Toyota", "Corolla", 2020, 50.0, 0.2, "Available"),
            (11, "Honda", "Civic", 2019, 45.0, 0.18, "Ongoing"),
            (12, "Ford", "Focus", 2021, 55.0, 0.25, "Upcoming"),
            (13, "Chevrolet", "Malibu", 2018, 40.0, 0.15, "Available"),
            (14, "Nissan", "Altima", 2020, 50.0, 0.2, "Available"),
        ]
        for vehicle in dummy_vehicles:
            DatabaseUtility.execute_query(DATABASES["vehicle"], """
                INSERT OR IGNORE INTO vehicles (car_id, brand, model, year, rate_per_day, rate_per_km, status)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, params=vehicle)

        # Initialize reservations.db
        DatabaseUtility.execute_query(DATABASES["reservations"], """
            CREATE TABLE IF NOT EXISTS reservations (
                reservation_id INTEGER PRIMARY KEY,
                customer_name TEXT NOT NULL,
                car_id INTEGER NOT NULL,
                start_date TEXT NOT NULL,
                end_date TEXT NOT NULL,
                status TEXT NOT NULL,
                FOREIGN KEY (car_id) REFERENCES vehicles (car_id)
            )
        """)
        dummy_reservations = [
            (1, "John Doe", 10, "2025-01-01", "2025-01-10", "Completed"),
            (2, "Jane Smith", 11, "2025-03-10", "2025-03-15", "Ongoing"),
            (3, "Alice Johnson", 12, "2025-03-20", "2025-03-25", "Upcoming"),
        ]
        for reservation in dummy_reservations:
            DatabaseUtility.execute_query(DATABASES["reservations"], """
                INSERT OR IGNORE INTO reservations (reservation_id, customer_name, car_id, start_date, end_date, status)
                VALUES (?, ?, ?, ?, ?, ?)
            """, params=reservation)

        # Initialize logs.db
        DatabaseUtility.execute_query(DATABASES["logs"], """
            CREATE TABLE IF NOT EXISTS logs (
                log_id INTEGER PRIMARY KEY AUTOINCREMENT,
                user TEXT NOT NULL,
                action TEXT NOT NULL,
                timestamp TEXT NOT NULL
            )
        """)
        dummy_logs = [
            ("manager", "Added a new vehicle: Toyota Corolla", "2025-03-20 10:00:00"),
            ("employee1", "Updated reservation #1", "2025-03-21 14:30:00"),
            ("manager", "Deleted vehicle #12", "2025-03-22 09:15:00"),
            ("employee2", "Added a new customer: John Doe", "2025-03-23 11:45:00"),
            ("manager", "Generated financial report for March 2025", "2025-03-24 08:00:00"),
        ]
        for log in dummy_logs:
            DatabaseUtility.execute_query(DATABASES["logs"], """
                INSERT OR IGNORE INTO logs (user, action, timestamp)
                VALUES (?, ?, ?)
            """, params=log)

class Dashboard:
    """Handles dashboard-related operations."""
    def __init__(self, app):
        self.app = app

    def show_dashboard(self):
        self.app.clear_content_frame()
        tk.Label(self.app.content_frame, text="Dashboard", font=("Arial", 20)).pack(pady=10)

        # Key Metrics Overview
        tk.Label(self.app.content_frame, text="Key Metrics", font=("Arial", 16)).pack(pady=5)
        metrics_frame = tk.Frame(self.app.content_frame)
        metrics_frame.pack(pady=5)
        tk.Label(metrics_frame, text="Total Reservations: 120", font=("Arial", 14)).grid(row=0, column=0, padx=10)
        tk.Label(metrics_frame, text="Ongoing Reservations: 15", font=("Arial", 14)).grid(row=0, column=1, padx=10)
        tk.Label(metrics_frame, text="Upcoming Reservations: 5", font=("Arial", 14)).grid(row=1, column=0, padx=10)
        tk.Label(metrics_frame, text="Completed Reservations: 100", font=("Arial", 14)).grid(row=1, column=1, padx=10)

        # Upcoming Reservations
        tk.Label(self.app.content_frame, text="Upcoming Reservations", font=("Arial", 16)).pack(pady=5)
        columns = ("Reservation ID", "Customer Name", "Car ID", "Start Date", "End Date")
        upcoming_tree = ttk.Treeview(self.app.content_frame, columns=columns, show="headings")
        for col in columns:
            upcoming_tree.heading(col, text=col)
            upcoming_tree.column(col, width=120)  # Set column width
        upcoming_tree.pack(pady=5)

        # Recent Notifications
        self._show_recent_notifications()

        # Quick Actions
        self._show_quick_actions()

    def _show_upcoming_reservations(self):
        tk.Label(self.app.content_frame, text="Upcoming Reservations", font=("Arial", 16)).pack(pady=5)
        columns = ("Reservation ID", "Customer Name", "Car ID", "Start Date", "End Date")
        tree = create_treeview(self.app.content_frame, columns)
        upcoming_reservations = [
            (1, "John Doe", 10, "2025-03-25", "2025-03-30"),
            (2, "Jane Smith", 11, "2025-03-28", "2025-04-02"),
        ]
        for reservation in upcoming_reservations:
            tree.insert("", "end", values=reservation)
        tree.pack(fill=tk.BOTH, expand=True, pady=5)

    def _show_recent_notifications(self):
        tk.Label(self.app.content_frame, text="Recent Notifications", font=("Arial", 16)).pack(pady=5)
        columns = ("Notification ID", "Message", "Date")
        tree = create_treeview(self.app.content_frame, columns, column_width=150)
        notifications = [
            (1, "Car maintenance scheduled for Toyota Corolla", "2025-03-20"),
            (2, "New customer feedback received", "2025-03-19"),
        ]
        for notification in notifications:
            tree.insert("", "end", values=notification)
        tree.pack(fill=tk.BOTH, expand=True, pady=5)

    def _show_quick_actions(self):
        tk.Label(self.app.content_frame, text="Quick Actions", font=("Arial", 16)).pack(pady=5)
        actions_frame = tk.Frame(self.app.content_frame)
        actions_frame.pack(pady=5)
        actions = [
            ("Add New Reservation", self.app.show_new_reservation),
            ("Add New Vehicle", self.app.vehicle_manager.show_add_vehicle),
            ("View Reports", self.app.show_reports_and_analytics),
        ]
        for label, command in actions:
            tk.Button(actions_frame, text=label, command=command).pack(side=tk.LEFT, padx=5)

class UserManager:
    """Manages user-related operations."""
    def __init__(self, app):
        self.app = app

    def login(self, username, password):
        conn = sqlite3.connect("user.db")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
        user = cursor.fetchone()
        conn.close()
        return user

    def show_users(self):
        self.app.clear_content_frame()
        tk.Label(self.app.content_frame, text="List of Employees", font=("Arial", 16)).pack(pady=10)

        # Create a Treeview widget to display employees
        columns = ("Username", "Role", "First Name", "Last Name", "Phone", "Email", "Employee ID", "Address")
        tree = create_treeview(self.app.content_frame, columns)
        employees = DatabaseUtility.execute_query(DATABASES["user"], "SELECT * FROM users", fetch=True)
        for employee in employees:
            tree.insert("", "end", values=employee)

        tree.pack(fill=tk.BOTH, expand=True)

        # Add buttons below the employee list
        button_frame = tk.Frame(self.app.content_frame)
        button_frame.pack(pady=10)

        tk.Button(button_frame, text="Add Employee", command=self.show_add_employee).pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame, text="Delete Employee", command=self.show_delete_employee).pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame, text="Edit Employee Details", command=self.show_edit_employee).pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame, text="Back", command=self.app.show_main_menu).pack(side=tk.LEFT, padx=5)

    def show_add_employee(self):
        self.app.clear_content_frame()
        tk.Label(self.app.content_frame, text="Add Employee", font=("Arial", 16)).pack(pady=10)

        fields = ["Username", "Password", "First Name", "Last Name", "Phone", "Email", "Employee ID", "Address"]
        entries = {}
        for field in fields:
            tk.Label(self.app.content_frame, text=f"{field}:").pack()
            entry = tk.Entry(self.app.content_frame)
            entry.pack()
            entries[field] = entry

        # Add dropdown for Role
        tk.Label(self.app.content_frame, text="Role:").pack()
        role_var = tk.StringVar()
        role_dropdown = ttk.Combobox(self.app.content_frame, textvariable=role_var, values=["Manager", "Employee"])
        role_dropdown.pack()
        role_dropdown.current(1)  # Default to "Employee"

        def add_employee():
            values = {field: entry.get() for field, entry in entries.items()}
            role = role_var.get()
            if all(values.values()) and role in ["Manager", "Employee"]:
                try:
                    conn = sqlite3.connect("user.db")
                    cursor = conn.cursor()
                    cursor.execute("""
                        INSERT INTO users (username, password, role, first_name, last_name, phone, email, employee_id, address)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """, (values["Username"], values["Password"], role, values["First Name"], values["Last Name"], values["Phone"], values["Email"], values["Employee ID"], values["Address"]))
                    conn.commit()
                    messagebox.showinfo("Success", "Employee added successfully!")
                    self.show_users()
                except sqlite3.IntegrityError:
                    messagebox.showerror("Error", "Username already exists!")
                finally:
                    conn.close()
            else:
                messagebox.showerror("Error", "All fields are required, and Role must be valid!")

        tk.Button(self.app.content_frame, text="Submit", command=add_employee).pack(pady=10)
        tk.Button(self.app.content_frame, text="Back", command=self.show_users).pack(pady=5)

    def show_delete_employee(self):
        self.app.clear_content_frame()
        tk.Label(self.app.content_frame, text="Delete Employee", font=("Arial", 16)).pack(pady=10)

        tk.Label(self.app.content_frame, text="Username:").pack()
        username_entry = tk.Entry(self.app.content_frame)
        username_entry.pack()

        def delete_employee():
            username = username_entry.get()
            if username:
                conn = sqlite3.connect("user.db")
                cursor = conn.cursor()
                cursor.execute("DELETE FROM users WHERE username = ?", (username,))
                if cursor.rowcount > 0:
                    conn.commit()
                    messagebox.showinfo("Success", "Employee deleted successfully!")
                    self.show_users()
                else:
                    messagebox.showerror("Error", "Username not found!")
                conn.close()
            else:
                messagebox.showerror("Error", "Username is required!")

        tk.Button(self.app.content_frame, text="Delete", command=delete_employee).pack(pady=10)
        tk.Button(self.app.content_frame, text="Back", command=self.show_users).pack(pady=5)

    def show_edit_employee(self):
        self.app.clear_content_frame()
        tk.Label(self.app.content_frame, text="Edit Employee Details", font=("Arial", 16)).pack(pady=10)

        tk.Label(self.app.content_frame, text="Username:").pack()
        username_entry = tk.Entry(self.app.content_frame)
        username_entry.pack()

        fields = ["Password", "Role", "First Name", "Last Name", "Phone", "Email", "Employee ID", "Address"]
        entries = {}
        for field in fields:
            tk.Label(self.app.content_frame, text=f"{field}:").pack()
            entry = tk.Entry(self.app.content_frame)
            entry.pack()
            entries[field] = entry

        def edit_employee():
            username = username_entry.get()
            updates = {field: entry.get() for field, entry in entries.items()}
            if username and any(updates.values()):
                conn = sqlite3.connect("user.db")
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
                if cursor.fetchone():
                    cursor.execute("""
                        UPDATE users
                        SET password = ?, role = ?, first_name = ?, last_name = ?, phone = ?, email = ?, employee_id = ?, address = ?
                        WHERE username = ?
                    """, (updates["Password"], updates["Role"], updates["First Name"], updates["Last Name"], updates["Phone"], updates["Email"], updates["Employee ID"], updates["Address"], username))
                    conn.commit()
                    messagebox.showinfo("Success", "Employee details updated successfully!")
                    self.show_users()
                else:
                    messagebox.showerror("Error", "Username not found!")
                conn.close()
            else:
                messagebox.showerror("Error", "Username and at least one field are required!")

        tk.Button(self.app.content_frame, text="Update", command=edit_employee).pack(pady=10)
        tk.Button(self.app.content_frame, text="Back", command=self.show_users).pack(pady=5)

class VehicleManager:
    """Manages vehicle-related operations."""
    def __init__(self, app):
        self.app = app  # Initialize the app reference

    def show_add_vehicle(self):
        self.app.clear_content_frame()
        tk.Label(self.app.content_frame, text="Add Vehicle").pack()
        fields = ["Car Brand", "Car Model", "Car Year", "Kilometers on Car", "Price Per Day", "Price Per KM"]
        self.vehicle_entries = {}
        for field in fields:
            tk.Label(self.app.content_frame, text=f"{field}:").pack()
            entry = tk.Entry(self.app.content_frame)
            entry.pack()
            self.vehicle_entries[field] = entry

        tk.Label(self.app.content_frame, text="Vehicle Type:").pack()
        self.vehicle_type = ttk.Combobox(self.app.content_frame, values=["Car", "Truck", "SUV", "Van"])
        self.vehicle_type.pack()
        self.vehicle_type.bind("<<ComboboxSelected>>", self.update_vehicle_class)

        tk.Label(self.app.content_frame, text="Vehicle Class:").pack()
        self.vehicle_class = ttk.Combobox(self.app.content_frame)
        self.vehicle_class.pack()

    def update_vehicle_class(self, event):
        vehicle_type = self.vehicle_type.get()
        if vehicle_type == "Car":
            self.vehicle_class['values'] = [
                "Compact Car", "Premium Car", "Sporty Car", "Hybrid Car", "Economy Car", "Convertible Car",
                "Intermediate Car", "Luxury Car", "Full Size Car", "Standard Car", "Elite Car", "Electric Car"
            ]
        elif vehicle_type == "Truck":
            self.vehicle_class['values'] = [
                "Full Size Pickup", "Box Truck", "Small Pickup", "Refrigerated Truck"
            ]
        elif vehicle_type == "SUV":
            self.vehicle_class['values'] = [
                "Standard SUV", "Premium & Luxury SUV", "Electric SUV", "Intermediate SUV", "Compact SUV",
                "Jeeps", "Full Size SUV", "Hybrid SUV"
            ]
        elif vehicle_type == "Van":
            self.vehicle_class['values'] = [
                "Cargo Van", "Passenger Van", "Refrigerated Van", "Minivan"
            ]

    def add_vehicle(self):
        brand = self.vehicle_entries["Car Brand"].get()
        model = self.vehicle_entries["Car Model"].get()
        year = self.vehicle_entries["Car Year"].get()
        kilometers = self.vehicle_entries["Kilometers on Car"].get()
        rate_per_day = self.vehicle_entries["Price Per Day"].get()
        rate_per_km = self.vehicle_entries["Price Per KM"].get()
        vehicle_type = self.vehicle_type.get()
        vehicle_class = self.vehicle_class.get()
        if brand and model and year and kilometers and rate_per_day and rate_per_km and vehicle_type and vehicle_class:
            conn = sqlite3.connect("vehicle.db")
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO vehicles (brand, model, year, kilometers, rate_per_day, rate_per_km, vehicle_type, vehicle_class)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (brand, model, year, kilometers, rate_per_day, rate_per_km, vehicle_type, vehicle_class))
            conn.commit()
            conn.close()
            self.log_action(self.current_user[0], f"Added vehicle: {brand} {model} ({year})")
            messagebox.showinfo("Success", "Vehicle added successfully!")
            self.app.show_main_menu()
        else:
            messagebox.showerror("Error", "All fields are required!")

    def show_vehicles_inventory(self):
        self.app.clear_content_frame()
        tk.Label(self.app.content_frame, text="Vehicles Inventory", font=("Arial", 16)).pack(pady=10)
        # Create a Treeview widget to display vehicles
        columns = ("Car ID", "Brand", "Model", "Year", "Rate/Day", "Rate/KM")
        tree = ttk.Treeview(self.app.content_frame, columns=columns, show="headings")
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=120)
        # Fetch vehicles from the database
        conn = sqlite3.connect("vehicle.db")
        cursor = conn.cursor()
        cursor.execute("SELECT car_id, brand, model, year, rate_per_day, rate_per_km FROM vehicles")
        vehicles = cursor.fetchall()
        conn.close()

        for vehicle in vehicles:
            tree.insert("", "end", values=vehicle)
        tree.pack(fill=tk.BOTH, expand=True)

        # Add buttons below the vehicle list
        button_frame = tk.Frame(self.app.content_frame)
        button_frame.pack(pady=10)

        tk.Button(button_frame, text="Add Vehicle", command=self.show_add_vehicle).pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame, text="Back", command=self.app.show_main_menu).pack(side=tk.LEFT, padx=5)

    def show_delete_vehicle(self):
        self.app.clear_content_frame()
        tk.Label(self.app.content_frame, text="Delete Car", font=("Arial", 16)).pack(pady=10)

        tk.Label(self.app.content_frame, text="Car ID:").pack()
        car_id_entry = tk.Entry(self.app.content_frame)
        car_id_entry.pack()

        def delete_car():
            car_id = car_id_entry.get()
            if car_id:
                conn = sqlite3.connect("vehicle.db")
                cursor = conn.cursor()
                cursor.execute("DELETE FROM vehicles WHERE car_id = ?", (car_id,))
                if cursor.rowcount > 0:
                    conn.commit()
                    messagebox.showinfo("Success", "Car deleted successfully!")
                    self.show_manage_cars()
                else:
                    messagebox.showerror("Error", "Car ID not found!")
                conn.close()
            else:
                messagebox.showerror("Error", "Car ID is required!")

        tk.Button(self.app.content_frame, text="Delete", command=delete_car).pack(pady=5)
        tk.Button(self.app.content_frame, text="Back", command=self.show_manage_cars).pack(pady=5)

    def show_update_vehicle(self):
        self.app.clear_content_frame()
        tk.Label(self.app.content_frame, text="Update Car Details", font=("Arial", 16)).pack(pady=10)

        tk.Label(self.app.content_frame, text="Car ID:").pack()
        car_id_entry = tk.Entry(self.app.content_frame)
        car_id_entry.pack()

        fields = ["Brand", "Model", "Year", "Rate Per Day", "Rate Per KM"]
        update_entries = {}
        for field in fields:
            tk.Label(self.app.content_frame, text=f"{field}:").pack()
            entry = tk.Entry(self.app.content_frame)
            entry.pack()
            update_entries[field] = entry

        def update_car():
            car_id = car_id_entry.get()
            updates = {field: entry.get() for field, entry in update_entries.items()}
            if car_id and all(updates.values()):
                conn = sqlite3.connect("vehicle.db")
                cursor = conn.cursor()
                try:
                    cursor.execute("""
                        UPDATE vehicles
                        SET brand = ?, model = ?, year = ?, rate_per_day = ?, rate_per_km = ?
                        WHERE car_id = ?
                    """, (updates["Brand"], updates["Model"], updates["Year"], updates["Rate Per Day"], updates["Rate Per KM"], car_id))
                    if cursor.rowcount > 0:
                        conn.commit()
                        messagebox.showinfo("Success", "Car details updated successfully!")
                        self.show_manage_cars()
                    else:
                        messagebox.showerror("Error", "Car ID not found!")
                except Exception as e:
                    messagebox.showerror("Error", f"An error occurred: {e}")
                finally:
                    conn.close()
            else:
                messagebox.showerror("Error", "All fields are required!")

        tk.Button(self.app.content_frame, text="Update", command=update_car).pack(pady=5)
        tk.Button(self.app.content_frame, text="Back", command=self.show_manage_cars).pack(pady=5)

    def show_manage_cars(self):
        self.app.clear_content_frame()
        tk.Label(self.app.content_frame, text="Manage Cars", font=("Arial", 20)).pack(pady=10)
        # Create a Treeview widget to display cars
        columns = ("Car ID", "Brand", "Model", "Year", "Rate/Day", "Rate/KM")
        tree = ttk.Treeview(self.app.content_frame, columns=columns, show="headings")
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=120)
        # Fetch car data from the database
        conn = sqlite3.connect("vehicle.db")
        cursor = conn.cursor()
        cursor.execute("SELECT car_id, brand, model, year, rate_per_day, rate_per_km FROM vehicles")
        cars = cursor.fetchall()
        conn.close()

        for car in cars:
            tree.insert("", "end", values=car)
        tree.pack(fill=tk.BOTH, expand=True)

        # Add buttons for car management
        button_frame = tk.Frame(self.app.content_frame)
        button_frame.pack(pady=10)

        tk.Button(button_frame, text="Add New Car", command=self.show_add_vehicle).pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame, text="Remove Car", command=self.show_delete_vehicle).pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame, text="Update Pricing", command=self.show_update_vehicle).pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame, text="Back", command=self.app.show_main_menu).pack(side=tk.LEFT, padx=5)

    def show_available_cars(self):
        self.app.clear_content_frame()
        tk.Label(self.app.content_frame, text="Available Cars", font=("Arial", 16)).pack(pady=10)

        # Create a Treeview widget to display available cars
        columns = ("Car ID", "Brand", "Model", "Year", "Rate/Day", "Rate/KM")
        tree = ttk.Treeview(self.app.content_frame, columns=columns, show="headings")
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=120)

        # Fetch available cars from the vehicle.db
        conn = sqlite3.connect(DATABASES["vehicle"])
        cursor = conn.cursor()
        cursor.execute("""
            SELECT car_id, brand, model, year, rate_per_day, rate_per_km
            FROM vehicles
            WHERE status = 'Available'
        """)
        available_cars = cursor.fetchall()
        conn.close()

        # Add available cars to the Treeview
        for car in available_cars:
            tree.insert("", "end", values=car)

        tree.pack(fill=tk.BOTH, expand=True)

        # Function to book a selected car
        def book_car():
            selected_item = tree.selection()
            if selected_item:
                car_id = tree.item(selected_item, "values")[0]  # Get the Car ID of the selected item

                # Open a new window for booking details
                booking_window = tk.Toplevel(self.app.root)
                booking_window.title("Book Car")

                tk.Label(booking_window, text="Customer Name:").pack(pady=5)
                customer_name_entry = tk.Entry(booking_window)
                customer_name_entry.pack(pady=5)

                tk.Label(booking_window, text="Start Date (YYYY-MM-DD):").pack(pady=5)
                start_date_entry = tk.Entry(booking_window)
                start_date_entry.pack(pady=5)

                tk.Label(booking_window, text="End Date (YYYY-MM-DD):").pack(pady=5)
                end_date_entry = tk.Entry(booking_window)
                end_date_entry.pack(pady=5)

                def confirm_booking():
                    customer_name = customer_name_entry.get()
                    start_date = start_date_entry.get()
                    end_date = end_date_entry.get()

                    if customer_name and start_date and end_date:
                        try:
                            # Update the vehicle status and add a reservation entry
                            conn = sqlite3.connect(DATABASES["vehicle"])
                            cursor = conn.cursor()
                            cursor.execute("""
                                UPDATE vehicles
                                SET status = 'Booked'
                                WHERE car_id = ?
                            """, (car_id,))
                            conn.commit()

                            # Add reservation details to the reservations table
                            conn = sqlite3.connect(DATABASES["reservations"])
                            cursor = conn.cursor()
                            cursor.execute("""
                                INSERT INTO reservations (customer_name, car_id, start_date, end_date, status)
                                VALUES (?, ?, ?, ?, 'Booked')
                            """, (customer_name, car_id, start_date, end_date))
                            conn.commit()
                            conn.close()

                            messagebox.showinfo("Success", f"Car with ID {car_id} has been booked successfully!")
                            booking_window.destroy()
                            self.show_available_cars()  # Refresh the available cars list
                        except Exception as e:
                            messagebox.showerror("Error", f"An error occurred: {e}")
                    else:
                        messagebox.showerror("Error", "All fields are required!")

                tk.Button(booking_window, text="Confirm Booking", command=confirm_booking).pack(pady=10)
                tk.Button(booking_window, text="Cancel", command=booking_window.destroy).pack(pady=5)
            else:
                messagebox.showerror("Error", "Please select a car to book.")

        # Add buttons below the Treeview
        button_frame = tk.Frame(self.app.content_frame)
        button_frame.pack(pady=10)

        tk.Button(button_frame, text="Book Car", command=book_car).pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame, text="Back", command=self.app.show_reservations).pack(side=tk.LEFT, padx=5)

    def show_available_cars_manager(self):
        self.app.clear_content_frame()
        tk.Label(self.app.content_frame, text="Available Cars", font=("Arial", 16)).pack(pady=10)

        # Create a Treeview widget to display available cars
        columns = ("Car ID", "Brand", "Model", "Year", "Rate/Day", "Rate/KM")
        tree = ttk.Treeview(self.app.content_frame, columns=columns, show="headings")
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=120)

        # Fetch available cars from the vehicle.db
        conn = sqlite3.connect(DATABASES["vehicle"])
        cursor = conn.cursor()
        cursor.execute("""
            SELECT car_id, brand, model, year, rate_per_day, rate_per_km
            FROM vehicles
            WHERE status = 'Available'
        """)
        available_cars = cursor.fetchall()
        conn.close()

        # Add available cars to the Treeview
        for car in available_cars:
            tree.insert("", "end", values=car)

        tree.pack(fill=tk.BOTH, expand=True)

        # Function to book a selected car
        def book_car():
            selected_item = tree.selection()
            if selected_item:
                car_details = tree.item(selected_item, "values")  # Get the selected car details

                # Open a new window for booking details
                booking_window = tk.Toplevel(self.app.root)
                booking_window.title("Book Car")

                tk.Label(booking_window, text="Car Details", font=("Arial", 14)).pack(pady=5)
                tk.Label(booking_window, text=f"Car ID: {car_details[0]}").pack()
                tk.Label(booking_window, text=f"Brand: {car_details[1]}").pack()
                tk.Label(booking_window, text=f"Model: {car_details[2]}").pack()
                tk.Label(booking_window, text=f"Year: {car_details[3]}").pack()
                tk.Label(booking_window, text=f"Rate/Day: {car_details[4]}").pack()
                tk.Label(booking_window, text=f"Rate/KM: {car_details[5]}").pack()

                tk.Label(booking_window, text="Customer Name:").pack(pady=5)
                customer_name_entry = tk.Entry(booking_window)
                customer_name_entry.pack(pady=5)

                tk.Label(booking_window, text="Start Date (YYYY-MM-DD):").pack(pady=5)
                start_date_entry = tk.Entry(booking_window)
                start_date_entry.pack(pady=5)

                tk.Label(booking_window, text="End Date (YYYY-MM-DD):").pack(pady=5)
                end_date_entry = tk.Entry(booking_window)
                end_date_entry.pack(pady=5)

                def confirm_booking():
                    customer_name = customer_name_entry.get()
                    start_date = start_date_entry.get()
                    end_date = end_date_entry.get()

                    if customer_name and start_date and end_date:
                        try:
                            # Update the vehicle status and add a reservation entry
                            conn = sqlite3.connect(DATABASES["vehicle"])
                            cursor = conn.cursor()
                            cursor.execute("""
                                UPDATE vehicles
                                SET status = 'Booked'
                                WHERE car_id = ?
                            """, (car_details[0],))
                            conn.commit()

                            # Add reservation details to the reservations table
                            conn = sqlite3.connect(DATABASES["reservations"])
                            cursor = conn.cursor()
                            cursor.execute("""
                                INSERT INTO reservations (customer_name, car_id, start_date, end_date, status)
                                VALUES (?, ?, ?, ?, 'Booked')
                            """, (customer_name, car_details[0], start_date, end_date))
                            conn.commit()
                            conn.close()

                            messagebox.showinfo("Success", f"Car with ID {car_details[0]} has been booked successfully!")
                            booking_window.destroy()
                            self.show_available_cars_manager()  # Refresh the available cars list
                        except Exception as e:
                            messagebox.showerror("Error", f"An error occurred: {e}")
                    else:
                        messagebox.showerror("Error", "All fields are required!")

                tk.Button(booking_window, text="Confirm Booking", command=confirm_booking).pack(pady=10)
                tk.Button(booking_window, text="Cancel", command=booking_window.destroy).pack(pady=5)
            else:
                messagebox.showerror("Error", "Please select a car to book.")

        # Add buttons below the Treeview
        button_frame = tk.Frame(self.app.content_frame)
        button_frame.pack(pady=10)

        tk.Button(button_frame, text="Book Car", command=book_car).pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame, text="Back", command=self.app.show_main_menu).pack(side=tk.LEFT, padx=5)

class CustomerManager:
    """Manages customer-related operations."""
    def __init__(self, app):
        self.app = app

    def show_customers(self):
        self.app.clear_content_frame()
        tk.Label(self.app.content_frame, text="Customer List", font=("Arial", 16)).pack(pady=10)

        # Create a Treeview widget to display customers
        columns = ("Name", "Address", "Phone Number", "License Number", "Insurance Company", "Policy Number")
        tree = ttk.Treeview(self.app.content_frame, columns=columns, show="headings")
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=150)

        # Fetch customer data from the database
        customers = DatabaseUtility.execute_query(DATABASES["customer"], "SELECT * FROM customers", fetch=True)
        for customer in customers:
            tree.insert("", "end", values=customer)
        tree.pack(fill=tk.BOTH, expand=True)

        # Add buttons below the customer list
        button_frame = tk.Frame(self.app.content_frame)
        button_frame.pack(pady=10)

        tk.Button(button_frame, text="Add Customer", command=self.show_add_customer).pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame, text="Delete Customer", command=self.show_delete_customer).pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame, text="Back", command=self.app.show_main_menu).pack(side=tk.LEFT, padx=5)

    def show_add_customer(self):
        self.app.clear_content_frame()
        tk.Label(self.app.content_frame, text="Add Customer", font=("Arial", 16)).pack(pady=10)

        fields = ["Name", "Address", "Phone Number", "License Number", "Insurance Company", "Policy Number"]
        self.customer_entries = {}
        for field in fields:
            tk.Label(self.app.content_frame, text=f"{field}:").pack()
            entry = tk.Entry(self.app.content_frame)
            entry.pack()
            self.customer_entries[field] = entry

        def add_customer():
            name = self.customer_entries["Name"].get()
            address = self.customer_entries["Address"].get()
            phone = self.customer_entries["Phone Number"].get()
            license_number = self.customer_entries["License Number"].get()
            insurance_company = self.customer_entries["Insurance Company"].get()
            policy_number = self.customer_entries["Policy Number"].get()
            if name and address and phone and license_number and insurance_company and policy_number:
                try:
                    conn = sqlite3.connect("customer.db")
                    cursor = conn.cursor()
                    cursor.execute("""
                        INSERT INTO customers (name, address, phone, license_number, insurance_company, policy_number)
                        VALUES (?, ?, ?, ?, ?, ?)
                    """, (name, address, phone, license_number, insurance_company, policy_number))
                    conn.commit()
                    messagebox.showinfo("Success", "Customer added successfully!")
                    self.show_customers()
                except sqlite3.IntegrityError:
                    messagebox.showerror("Error", "Customer with this name already exists!")
                finally:
                    conn.close()
            else:
                messagebox.showerror("Error", "All fields are required!")

        tk.Button(self.app.content_frame, text="Submit", command=add_customer).pack(pady=10)
        tk.Button(self.app.content_frame, text="Back", command=self.show_customers).pack(pady=5)

    def show_delete_customer(self):
        self.app.clear_content_frame()
        tk.Label(self.app.content_frame, text="Delete Customer", font=("Arial", 16)).pack(pady=10)

        tk.Label(self.app.content_frame, text="Name:").pack()
        name_entry = tk.Entry(self.app.content_frame)
        name_entry.pack()

        def delete_customer():
            name = name_entry.get()
            if name:
                try:
                    DatabaseUtility.execute_query(DATABASES["customer"], "DELETE FROM customers WHERE name = ?", (name,))
                    messagebox.showinfo("Success", "Customer deleted successfully!")
                    self.show_customers()
                except Exception as e:
                    messagebox.showerror("Error", f"An error occurred: {e}")
            else:
                messagebox.showerror("Error", "Name is required!")

        tk.Button(self.app.content_frame, text="Delete", command=delete_customer).pack(pady=10)
        tk.Button(self.app.content_frame, text="Back", command=self.show_customers).pack(pady=5)

class CarRentalApp:
    """Main application class."""
    def __init__(self, root):
        self.root = root
        self.root.title("Car Rental System")
        self.current_user = None

        # Initialize managers
        self.user_manager = UserManager(self)
        self.customer_manager = CustomerManager(self)
        self.vehicle_manager = VehicleManager(self)
        self.dashboard = Dashboard(self)

        # Login Frame
        self.login_frame = tk.Frame(self.root)
        self.login_frame.pack(pady=20)
        tk.Label(self.login_frame, text="Username:").grid(row=0, column=0)
        self.username_entry = tk.Entry(self.login_frame)
        self.username_entry.grid(row=0, column=1)
        tk.Label(self.login_frame, text="Password:").grid(row=1, column=0)
        self.password_entry = tk.Entry(self.login_frame, show="*")
        self.password_entry.grid(row=1, column=1)
        tk.Button(self.login_frame, text="Login", command=self.login).grid(row=2, column=1, pady=10)

        # Main Menu Frame (initially hidden)
        self.main_menu_frame = tk.Frame(self.root)
        self.main_menu_frame.pack(fill=tk.BOTH, expand=True)

        # Side Menu Frame (for Manager and Employee menu)
        self.side_menu_frame = tk.Frame(self.main_menu_frame, width=200, bg="lightgray")
        self.side_menu_frame.pack(side=tk.LEFT, fill=tk.Y)

        # Add a vertical separator between the side menu and the content frame
        separator = ttk.Separator(self.main_menu_frame, orient="vertical")
        separator.pack(side=tk.LEFT, fill=tk.Y)

        # Content Frame (for dynamic content on the right)
        self.content_frame = tk.Frame(self.main_menu_frame)
        self.content_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, pady=20, padx=20)

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        user = self.user_manager.login(username, password)
        if user:
            self.current_user = user
            self.login_frame.pack_forget()
            self.show_main_menu()
        else:
            messagebox.showerror("Login Failed", "Invalid username or password")

    def clear_content_frame(self):
        for widget in self.content_frame.winfo_children():
            widget.destroy()

    def show_main_menu(self):
        self.clear_content_frame()
        self.dashboard.show_dashboard()  # Show the Dashboard as the first page

        # Clear existing widgets in the side menu
        for widget in self.side_menu_frame.winfo_children():
            widget.destroy()

        # Get the user's role
        role = self.current_user[2]  # Assuming the role is the third column in the `users` table

        # Add buttons to the side menu based on the role
        tk.Button(self.side_menu_frame, text="Dashboard", command=self.dashboard.show_dashboard).pack(pady=5, fill=tk.X)
        tk.Button(self.side_menu_frame, text="Notifications", command=self.show_notifications).pack(pady=5, fill=tk.X)
        tk.Button(self.side_menu_frame, text="Car Reservation", command=self.show_reservations).pack(pady=5, fill=tk.X)
        tk.Button(self.side_menu_frame, text="Customer Feedback", command=self.show_customer_feedback).pack(pady=5, fill=tk.X)

        if role == "Manager":
            tk.Button(self.side_menu_frame, text="Available Cars", command=self.vehicle_manager.show_available_cars_manager).pack(pady=5, fill=tk.X)  # New Button
            tk.Button(self.side_menu_frame, text="Manage Cars", command=self.vehicle_manager.show_manage_cars).pack(pady=5, fill=tk.X)
            tk.Button(self.side_menu_frame, text="Manage Employees", command=self.user_manager.show_users).pack(pady=5, fill=tk.X)
            tk.Button(self.side_menu_frame, text="Employee Schedule", command=self.show_employee_schedule).pack(pady=5, fill=tk.X)
            tk.Button(self.side_menu_frame, text="Financial Reports", command=self.show_financial_reports).pack(pady=5, fill=tk.X)
            tk.Button(self.side_menu_frame, text="Settings", command=self.show_settings).pack(pady=5, fill=tk.X)
            tk.Button(self.side_menu_frame, text="Logs", command=self.show_logs).pack(pady=5, fill=tk.X)
            tk.Button(self.side_menu_frame, text="Reports and Analytics", command=self.show_reports_and_analytics).pack(pady=5, fill=tk.X)

        # Add a welcome message in the content frame
        tk.Label(self.content_frame, text=f"Welcome, {self.current_user[0]}!", font=("Arial", 16)).pack(pady=10)

    def show_notifications(self):
        self.clear_content_frame()
        tk.Label(self.content_frame, text="Notifications", font=("Arial", 20)).pack(pady=10)

        # Create a Treeview widget to display notifications
        columns = ("Notification ID", "Message", "Date")
        tree = ttk.Treeview(self.content_frame, columns=columns, show="headings")
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=150)

        # Dummy notifications data
        self.notifications = [
            (1, "Car maintenance scheduled for Toyota Corolla", "2025-03-20"),
            (2, "New customer feedback received", "2025-03-19"),
            (3, "Reservation #12 has been completed", "2025-03-18"),
            (4, "Insurance policy updated for Honda Civic", "2025-03-17"),
            (5, "System backup completed successfully", "2025-03-16"),
        ]

        # Add notifications to the Treeview
        for notification in self.notifications:
            tree.insert("", "end", values=notification)
        tree.pack(fill=tk.BOTH, expand=True)

        # Function to delete a selected notification
        def delete_notification():
            selected_item = tree.selection()
            if selected_item:
                # Get the Notification ID of the selected item
                notification_id = tree.item(selected_item, "values")[0]
                # Remove the notification from the Treeview
                tree.delete(selected_item)
                # Remove the notification from the list
                self.notifications = [n for n in self.notifications if n[0] != int(notification_id)]
                messagebox.showinfo("Success", f"Notification {notification_id} deleted successfully!")
            else:
                messagebox.showerror("Error", "Please select a notification to delete.")

        # Add buttons below the Treeview
        button_frame = tk.Frame(self.content_frame)
        button_frame.pack(pady=10)

        tk.Button(button_frame, text="Delete", command=delete_notification).pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame, text="Back", command=self.show_main_menu).pack(side=tk.LEFT, padx=5)

    def show_reservations(self):
        self.clear_content_frame()
        tk.Label(self.content_frame, text="Car Reservations", font=("Arial", 20)).pack(pady=10)

        # Create a Treeview widget to display reservations
        columns = ("Reservation ID", "Customer Name", "Car ID", "Start Date", "End Date", "Status")
        tree = ttk.Treeview(self.content_frame, columns=columns, show="headings")
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=120)

        # Fetch reservations from the database
        conn = sqlite3.connect(DATABASES["reservations"])
        cursor = conn.cursor()
        cursor.execute("SELECT reservation_id, customer_name, car_id, start_date, end_date, status FROM reservations")
        reservations = cursor.fetchall()
        conn.close()

        # Add reservations to the Treeview
        for reservation in reservations:
            tree.insert("", "end", values=reservation)

        tree.pack(fill=tk.BOTH, expand=True)

        # Function to update reservation status
        def update_status():
            selected_item = tree.selection()
            if selected_item:
                reservation_id = tree.item(selected_item, "values")[0]  # Get the Reservation ID
                car_id = tree.item(selected_item, "values")[2]  # Get the Car ID
                new_status = status_var.get()  # Get the new status from the dropdown

                if new_status in ["Completed", "Cancelled", "No Show"]:
                    try:
                        # Update the reservation status
                        conn = sqlite3.connect(DATABASES["reservations"])
                        cursor = conn.cursor()
                        cursor.execute("""
                            UPDATE reservations
                            SET status = ?
                            WHERE reservation_id = ?
                        """, (new_status, reservation_id))
                        conn.commit()

                        # Move the car back to "Available" in the vehicles table
                        conn = sqlite3.connect(DATABASES["vehicle"])
                        cursor = conn.cursor()
                        cursor.execute("""
                            UPDATE vehicles
                            SET status = 'Available'
                            WHERE car_id = ?
                        """, (car_id,))
                        conn.commit()
                        conn.close()

                        messagebox.showinfo("Success", f"Reservation status updated to '{new_status}', and car ID {car_id} is now available.")
                        self.show_reservations()  # Refresh the reservations list
                    except Exception as e:
                        messagebox.showerror("Error", f"An error occurred: {e}")
                else:
                    messagebox.showerror("Error", "Only 'Completed', 'Cancelled', or 'No Show' statuses can move the car back to available.")
            else:
                messagebox.showerror("Error", "Please select a reservation to update.")

        # Add a dropdown to select the new status
        tk.Label(self.content_frame, text="Update Reservation Status:").pack(pady=5)
        status_var = tk.StringVar()
        status_dropdown = ttk.Combobox(
            self.content_frame,
            textvariable=status_var,
            values=["Completed", "Cancelled", "No Show", "Ongoing", "Upcoming", "In Progress"]
        )
        status_dropdown.pack(pady=5)

        # Add buttons below the Treeview
        button_frame = tk.Frame(self.content_frame)
        button_frame.pack(pady=10)

        tk.Button(button_frame, text="Update Status", command=update_status).pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame, text="Back", command=self.show_main_menu).pack(side=tk.LEFT, padx=5)

    def show_new_reservation(self):
        self.clear_content_frame()
        tk.Label(self.content_frame, text="New Reservation", font=("Arial", 20)).pack(pady=10)

        # Left frame for the form
        form_frame = tk.Frame(self.content_frame)
        form_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Input fields for new reservation
        fields = ["Customer Name", "Car ID", "Start Date (YYYY-MM-DD)", "End Date (YYYY-MM-DD)"]
        entries = {}
        for field in fields:
            tk.Label(form_frame, text=f"{field}:").pack()
            entry = tk.Entry(form_frame)
            entry.pack()
            entries[field] = entry

        # Add a dropdown for Status
        tk.Label(form_frame, text="Status:").pack()
        status_var = tk.StringVar()
        status_dropdown = ttk.Combobox(
            form_frame,
            textvariable=status_var,
            values=["Completed", "Upcoming", "Hold", "Book Now", "Cancelled", "No Show", "Delayed", "In Progress"]
        )
        status_dropdown.pack()
        status_dropdown.current(1)  # Default to "Upcoming"

        def submit_reservation():
            customer_name = entries["Customer Name"].get()
            car_id = entries["Car ID"].get()
            start_date = entries["Start Date (YYYY-MM-DD)"].get()
            end_date = entries["End Date (YYYY-MM-DD)"].get()
            status = status_var.get()
            if customer_name and car_id and start_date and end_date and status:
                try:
                    conn = sqlite3.connect("reservations.db")
                    cursor = conn.cursor()
                    cursor.execute("""
                        INSERT INTO reservations (customer_name, car_id, start_date, end_date, status)
                        VALUES (?, ?, ?, ?, ?)
                    """, (customer_name, car_id, start_date, end_date, status))
                    conn.commit()
                    conn.close()
                    messagebox.showinfo("Success", "Reservation added successfully!")
                    self.show_reservations()  # Redirect to the Car Reservations page
                except Exception as e:
                    messagebox.showerror("Error", f"An error occurred: {e}")
            else:
                messagebox.showerror("Error", "All fields are required!")

        # Add "Submit" button
        tk.Button(form_frame, text="Submit", command=submit_reservation).pack(pady=10)
        # Add "Back" button
        tk.Button(form_frame, text="Back", command=self.show_reservations).pack(pady=5)

        # Right frame for the status description table
        table_frame = tk.Frame(self.content_frame)
        table_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10, pady=10)
        tk.Label(table_frame, text="Status Description", font=("Arial", 16)).pack(pady=5)

        # Create a Treeview widget for the status description table
        columns = ("Status", "Description")
        tree = ttk.Treeview(table_frame, columns=columns, show="headings")
        tree.heading("Status", text="Status")
        tree.heading("Description", text="Description")
        tree.column("Status", width=150)
        tree.column("Description", width=400)

        # Add status descriptions
        status_descriptions = [
            ("Completed", "Reservation has been successfully completed and car returned."),
            ("Upcoming", "Reservation is scheduled for a future date, and the rental period has not yet started."),
            ("Hold", "Reservation is on hold, pending confirmation (payment, verification, etc.)."),
            ("Book Now", "Customer is in the process of booking a car but hasn't confirmed the reservation yet."),
            ("Cancelled", "Reservation was canceled by the customer or rental agency before the rental started."),
            ("No Show", "Customer did not show up to pick up the car as scheduled."),
            ("Delayed", "Reservation is delayed due to late arrival, change in plans, or other reasons."),
            ("In Progress", "Car is currently rented and in use by the customer."),
        ]

        for status, description in status_descriptions:
            tree.insert("", "end", values=(status, description))

        tree.pack(fill=tk.BOTH, expand=True)

    def show_financial_reports(self):
        self.clear_content_frame()
        tk.Label(self.content_frame, text="Financial Reports", font=("Arial", 20)).pack(pady=10)

        # Create a Treeview widget to display financial summaries
        columns = ("Report ID", "Month", "Total Revenue", "Expenses", "Profit")
        tree = ttk.Treeview(self.content_frame, columns=columns, show="headings")
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=150)

        # Dummy financial reports data
        financial_reports = [
            (1, "January 2025", "$10,000", "$4,000", "$6,000"),
            (2, "February 2025", "$12,000", "$5,000", "$7,000"),
            (3, "March 2025", "$15,000", "$6,000", "$9,000"),
            (4, "April 2025", "$8,000", "$3,000", "$5,000"),
            (5, "May 2025", "$20,000", "$7,000", "$13,000"),
        ]

        # Add financial reports to the Treeview
        for report in financial_reports:
            tree.insert("", "end", values=report)
        tree.pack(fill=tk.BOTH, expand=True)

        # Add a Back button
        tk.Button(self.content_frame, text="Back", command=self.show_main_menu).pack(pady=10)

    def show_customer_feedback(self):
        self.clear_content_frame()
        tk.Label(self.content_frame, text="Customer Feedback", font=("Arial", 20)).pack(pady=10)

        # Create a Treeview widget to display feedback
        columns = ("Customer Name", "Rating", "Comment", "Date")
        tree = ttk.Treeview(self.content_frame, columns=columns, show="headings")
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=150)

        # Fetch feedback data from the database
        conn = sqlite3.connect("customer.db")
        cursor = conn.cursor()
        cursor.execute("SELECT customer_name, rating, comment, date FROM feedback")
        feedbacks = cursor.fetchall()
        conn.close()

        for feedback in feedbacks:
            tree.insert("", "end", values=feedback)
        tree.pack(fill=tk.BOTH, expand=True)

        # Add a Back button
        tk.Button(self.content_frame, text="Back", command=self.show_main_menu).pack(pady=10)

    def show_settings(self):
        self.clear_content_frame()
        tk.Label(self.content_frame, text="Settings", font=("Arial", 20)).pack(pady=10)

        # Section for Payment Gateway Settings
        tk.Label(self.content_frame, text="Payment Gateway Settings", font=("Arial", 16)).pack(pady=5)
        tk.Label(self.content_frame, text="Payment Gateway API Key:").pack()
        payment_gateway_entry = tk.Entry(self.content_frame)
        payment_gateway_entry.pack()

        # Section for Business Hours
        tk.Label(self.content_frame, text="Business Hours", font=("Arial", 16)).pack(pady=5)
        tk.Label(self.content_frame, text="Opening Time (HH:MM):").pack()
        opening_time_entry = tk.Entry(self.content_frame)
        opening_time_entry.pack()
        tk.Label(self.content_frame, text="Closing Time (HH:MM):").pack()
        closing_time_entry = tk.Entry(self.content_frame)
        closing_time_entry.pack()

        # Section for Notification Preferences
        tk.Label(self.content_frame, text="Notification Preferences", font=("Arial", 16)).pack(pady=5)
        tk.Label(self.content_frame, text="Enable Email Notifications:").pack()
        email_notifications_var = tk.BooleanVar()
        tk.Checkbutton(self.content_frame, variable=email_notifications_var).pack()
        tk.Label(self.content_frame, text="Enable SMS Notifications:").pack()
        sms_notifications_var = tk.BooleanVar()
        tk.Checkbutton(self.content_frame, variable=sms_notifications_var).pack()

        # Save Settings Functionality
        def save_settings():
            payment_gateway = payment_gateway_entry.get()
            opening_time = opening_time_entry.get()
            closing_time = closing_time_entry.get()
            email_notifications = email_notifications_var.get()
            sms_notifications = sms_notifications_var.get()

            # Open the database connection
            conn = sqlite3.connect("settings.db")
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS settings (
                    setting_name TEXT PRIMARY KEY,
                    setting_value TEXT NOT NULL
                )
            """)

            # Update settings in the database
            settings_to_update = [
                ("payment_gateway", payment_gateway),
                ("opening_time", opening_time),
                ("closing_time", closing_time),
                ("email_notifications", str(email_notifications)),
                ("sms_notifications", str(sms_notifications)),
            ]

            for setting_name, setting_value in settings_to_update:
                if setting_value:  # Only update non-empty values
                    cursor.execute("INSERT OR REPLACE INTO settings (setting_name, setting_value) VALUES (?, ?)", (setting_name, setting_value))

            conn.commit()
            conn.close()
            messagebox.showinfo("Success", "Settings saved successfully!")

        tk.Button(self.content_frame, text="Save Settings", command=save_settings).pack(pady=10)
        tk.Button(self.content_frame, text="Back", command=self.show_main_menu).pack(pady=10)

    def show_logs(self):
        self.clear_content_frame()
        tk.Label(self.content_frame, text="Logs", font=("Arial", 20)).pack(pady=10)

        # Create a Treeview widget to display logs
        columns = ("Log ID", "User", "Action", "Timestamp")
        tree = ttk.Treeview(self.content_frame, columns=columns, show="headings")
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=150)

        # Fetch logs from the database
        conn = sqlite3.connect("logs.db")
        cursor = conn.cursor()
        cursor.execute("SELECT log_id, user, action, timestamp FROM logs")
        logs = cursor.fetchall()
        conn.close()

        for log in logs:
            tree.insert("", "end", values=log)
        tree.pack(fill=tk.BOTH, expand=True)

        # Add a Back button
        tk.Button(self.content_frame, text="Back", command=self.show_main_menu).pack(pady=10)

    def show_reports_and_analytics(self):
        self.clear_content_frame()
        tk.Label(self.content_frame, text="Reports and Analytics", font=("Arial", 20)).pack(pady=10)

        # Create a Treeview widget to display booking statistics
        columns = ("Metric", "Value")
        tree = ttk.Treeview(self.content_frame, columns=columns, show="headings")
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=200)
        tree.pack(fill=tk.BOTH, expand=True)

        def load_data(period):
            # Clear the Treeview
            for item in tree.get_children():
                tree.delete(item)

            # Fetch data based on the selected period
            if period == "Yearly":
                data = [
                    ("Total Revenue", "$150,000"),
                    ("Total Bookings", "1,200"),
                    ("Most Booked Car", "Toyota Corolla"),
                    ("Highest Revenue Month", "March 2025"),
                ]
            elif period == "Monthly":
                data = [
                    ("Total Revenue", "$15,000"),
                    ("Total Bookings", "120"),
                    ("Most Booked Car", "Honda Civic"),
                    ("Highest Revenue Week", "Week 2 of March 2025"),
                ]
            elif period == "Weekly":
                data = [
                    ("Total Revenue", "$3,500"),
                    ("Total Bookings", "30"),
                    ("Most Booked Car", "Ford Focus"),
                    ("Highest Revenue Day", "March 10, 2025"),
                ]
            elif period == "Daily":
                data = [
                    ("Total Revenue", "$500"),
                    ("Total Bookings", "5"),
                    ("Most Booked Car", "BMW 3 Series"),
                    ("Peak Booking Hour", "10:00 AM"),
                ]
            else:
                data = []

            # Populate the Treeview with the fetched data
            for metric, value in data:
                tree.insert("", "end", values=(metric, value))

        # Create a frame for the buttons
        button_frame = tk.Frame(self.content_frame)
        button_frame.pack(pady=10)

        # Add buttons for different report types
        tk.Button(button_frame, text="Yearly", command=lambda: load_data("Yearly")).pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame, text="Monthly", command=lambda: load_data("Monthly")).pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame, text="Weekly", command=lambda: load_data("Weekly")).pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame, text="Daily", command=lambda: load_data("Daily")).pack(side=tk.LEFT, padx=5)

        # Add a Back button
        tk.Button(self.content_frame, text="Back", command=self.show_main_menu).pack(pady=10)

        # Load default data (e.g., Yearly) when the page is first displayed
        load_data("Yearly")

    def log_action(self, user, action):
        conn = sqlite3.connect("logs.db")
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS logs (
                log_id INTEGER PRIMARY KEY AUTOINCREMENT,
                user TEXT NOT NULL,
                action TEXT NOT NULL,
                timestamp TEXT NOT NULL
            )
        """)
        from datetime import datetime
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        cursor.execute("INSERT INTO logs (user, action, timestamp) VALUES (?, ?, ?)", (user, action, timestamp))
        conn.commit()
        conn.close()

    def show_employee_schedule(self):
        self.clear_content_frame()
        tk.Label(self.content_frame, text="Employee Schedule", font=("Arial", 20)).pack(pady=10)
        # Create a Treeview widget to display the schedule in calendar format
        columns = ["Time", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        tree = ttk.Treeview(self.content_frame, columns=columns, show="headings")
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=120)

        # Add hourly slots for the week
        hours = [f"{hour}:00" for hour in range(9, 18)]  # 9 AM to 5 PM
        for hour in hours:
            tree.insert("", "end", values=[hour, "", "", "", "", "", "", ""])

        # Dummy schedule data for 5 employees
        schedule_data = [
            ("John Doe", "Monday", "9:00", "Morning Shift"),
            ("Jane Smith", "Monday", "13:00", "Afternoon Shift"),
            ("Alice Johnson", "Tuesday", "9:00", "Morning Shift"),
            ("Michael Brown", "Wednesday", "13:00", "Afternoon Shift"),
            ("Emily Davis", "Thursday", "9:00", "Morning Shift"),
            ("John Doe", "Friday", "13:00", "Afternoon Shift"),
            ("Jane Smith", "Saturday", "9:00", "Morning Shift"),
            ("Alice Johnson", "Sunday", "13:00", "Afternoon Shift"),
        ]

        # Populate the schedule into the Treeview
        for employee, day, time, shift in schedule_data:
            for item in tree.get_children():
                row = tree.item(item, "values")
                if row[0] == time:  # Match the time slot
                    day_index = columns.index(day)  # Get the column index for the day
                    row = list(row)
                    row[day_index] = f"{employee} ({shift})"
                    tree.item(item, values=row)

        tree.pack(fill=tk.BOTH, expand=True)

        # Add buttons below the schedule
        button_frame = tk.Frame(self.content_frame)
        button_frame.pack(pady=10)

        tk.Button(button_frame, text="Schedule Employees", command=self.show_schedule_employees).pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame, text="Back", command=self.show_main_menu).pack(side=tk.LEFT, padx=5)

    def show_schedule_employees(self):
        self.clear_content_frame()
        tk.Label(self.content_frame, text="Schedule Employees", font=("Arial", 20)).pack(pady=10)

        # Input fields for scheduling employees
        tk.Label(self.content_frame, text="Employee Name:").pack()
        employee_name_entry = tk.Entry(self.content_frame)
        employee_name_entry.pack()
        tk.Label(self.content_frame, text="Day:").pack()
        day_var = tk.StringVar()
        day_dropdown = ttk.Combobox(self.content_frame, textvariable=day_var, values=["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"])
        day_dropdown.pack()
        tk.Label(self.content_frame, text="Time Slot (e.g., 9:00):").pack()
        time_slot_entry = tk.Entry(self.content_frame)
        time_slot_entry.pack()
        tk.Label(self.content_frame, text="Shift Description:").pack()
        shift_description_entry = tk.Entry(self.content_frame)
        shift_description_entry.pack()

        def schedule_employee():
            employee_name = employee_name_entry.get()
            day = day_var.get()
            time_slot = time_slot_entry.get()
            shift_description = shift_description_entry.get()
            if employee_name and day and time_slot and shift_description:
                # Logic to save the schedule (e.g., save to a database or update the Treeview)
                messagebox.showinfo("Success", f"Scheduled {employee_name} on {day} at {time_slot} for {shift_description}.")
                self.show_employee_schedule()  # Redirect back to the Employee Schedule page
            else:
                messagebox.showerror("Error", "All fields are required!")

        # Add "Submit" and "Back" buttons
        tk.Button(self.content_frame, text="Submit", command=schedule_employee).pack(pady=10)
        tk.Button(self.content_frame, text="Back", command=self.show_employee_schedule).pack(pady=5)

if __name__ == "__main__":
    root = tk.Tk()
    DatabaseManager.initialize_database()
    app = CarRentalApp(root)
    root.mainloop()