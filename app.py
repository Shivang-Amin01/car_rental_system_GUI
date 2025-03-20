import sqlite3
import tkinter as tk
from tkinter import messagebox, ttk


class DatabaseManager:
    """Handles database operations."""
    @staticmethod
    def initialize_database():
        # Initialize user.db
        conn = sqlite3.connect("user.db")
        cursor = conn.cursor()
        # Create the users table if it doesn't exist
        cursor.execute("""
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
        # Insert the default manager user if it doesn't exist
        cursor.execute("""
            INSERT OR IGNORE INTO users (username, password, role, first_name, last_name, phone, email, employee_id, address)
            VALUES ('manager', 'man123', 'Manager', 'Default', 'Manager', '1234567890', 'manager@example.com', '1000', '123 Manager St')
        """)
        conn.commit()
        conn.close()

        # Initialize customer.db
        conn = sqlite3.connect("customer.db")
        cursor = conn.cursor()
        # Create the customers table if it doesn't exist
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS customers (
                name TEXT PRIMARY KEY,
                address TEXT NOT NULL,
                phone TEXT NOT NULL,
                license_number TEXT NOT NULL,
                insurance_company TEXT NOT NULL,
                policy_number TEXT NOT NULL
            )
        """)
        # Insert dummy customer data
        cursor.executemany("""
            INSERT OR IGNORE INTO customers (name, address, phone, license_number, insurance_company, policy_number)
            VALUES (?, ?, ?, ?, ?, ?)
        """, [
            ("John Doe", "123 Elm Street", "555-1234", "LN12345", "ABC Insurance", "PN98765"),
            ("Jane Smith", "456 Oak Avenue", "555-5678", "LN67890", "XYZ Insurance", "PN54321"),
            ("Alice Johnson", "789 Pine Road", "555-9012", "LN11223", "DEF Insurance", "PN11223")
        ])
        conn.commit()
        conn.close()

        # Initialize vehicles.db
        conn = sqlite3.connect("vehicles.db")
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS vehicles (
                car_id INTEGER PRIMARY KEY,
                brand TEXT NOT NULL,
                model TEXT NOT NULL,
                year INTEGER NOT NULL,
                rate_per_day REAL NOT NULL,
                rate_per_km REAL NOT NULL
            )
        """)
        cursor.executemany("""
            INSERT OR IGNORE INTO vehicles (car_id, brand, model, year, rate_per_day, rate_per_km)
            VALUES (?, ?, ?, ?, ?, ?)
        """, [
            (10, "Toyota", "Corolla", 2020, 50.0, 0.2),
            (11, "Honda", "Civic", 2019, 45.0, 0.18),
            (12, "Ford", "Focus", 2021, 55.0, 0.25),
            (13, "Chevrolet", "Malibu", 2018, 40.0, 0.15),
            (14, "Nissan", "Altima", 2020, 50.0, 0.2),
            (15, "BMW", "3 Series", 2022, 100.0, 0.3),
            (16, "Audi", "A4", 2021, 95.0, 0.28),
            (17, "Mercedes", "C-Class", 2022, 110.0, 0.35),
            (18, "Hyundai", "Elantra", 2019, 45.0, 0.18),
            (19, "Kia", "Optima", 2020, 50.0, 0.2)
        ])
        conn.commit()
        conn.close()


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
        tk.Label(self.app.content_frame, text="List of Users").pack(pady=10)

        # Create a Treeview widget
        columns = ("Username", "Role", "First Name", "Last Name", "Phone", "Email", "Employee ID", "Address")
        tree = ttk.Treeview(self.app.content_frame, columns=columns, show="headings")

        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=100)

        # Fetch user data from the database
        conn = sqlite3.connect("user.db")
        cursor = conn.cursor()
        cursor.execute("SELECT username, role, first_name, last_name, phone, email, employee_id, address FROM users")
        users = cursor.fetchall()
        conn.close()

        for user in users:
            tree.insert("", "end", values=user)

        tree.pack(fill=tk.BOTH, expand=True)

        tk.Button(self.app.content_frame, text="Add Employee", command=self.show_add_employee).pack(pady=5)
        tk.Button(self.app.content_frame, text="Delete Employee", command=self.show_delete_employee).pack(pady=5)
        tk.Button(self.app.content_frame, text="Back", command=self.app.show_main_menu).pack(pady=5)

    def show_add_employee(self):
        self.app.clear_content_frame()
        tk.Label(self.app.content_frame, text="Add Employee").pack()
        fields = ["Username", "Password", "First Name", "Last Name", "Phone", "Email", "Employee ID", "Address"]
        self.employee_entries = {}
        for field in fields:
            tk.Label(self.app.content_frame, text=f"{field}:").pack()
            entry = tk.Entry(self.app.content_frame)
            entry.pack()
            self.employee_entries[field] = entry

        tk.Label(self.app.content_frame, text="Role:").pack()
        self.role_combobox = ttk.Combobox(self.app.content_frame, values=["Manager", "Employee"])
        self.role_combobox.pack()

        tk.Button(self.app.content_frame, text="Submit", command=self.add_employee).pack()
        tk.Button(self.app.content_frame, text="Back", command=self.show_users).pack(pady=5)

    def add_employee(self):
        username = self.employee_entries["Username"].get()
        password = self.employee_entries["Password"].get()
        first_name = self.employee_entries["First Name"].get()
        last_name = self.employee_entries["Last Name"].get()
        phone = self.employee_entries["Phone"].get()
        email = self.employee_entries["Email"].get()
        employee_id = self.employee_entries["Employee ID"].get()
        address = self.employee_entries["Address"].get()
        role = self.role_combobox.get()

        if username and password and role:
            conn = sqlite3.connect("user.db")
            cursor = conn.cursor()
            try:
                cursor.execute("""
                    INSERT INTO users (username, password, role, first_name, last_name, phone, email, employee_id, address)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (username, password, role, first_name, last_name, phone, email, employee_id, address))
                conn.commit()
                messagebox.showinfo("Success", "Employee added successfully")
                self.show_users()
            except sqlite3.IntegrityError:
                messagebox.showerror("Error", "Username already exists")
            finally:
                conn.close()
        else:
            messagebox.showerror("Error", "Username, Password, and Role are required")

    def show_delete_employee(self):
        self.app.clear_content_frame()
        tk.Label(self.app.content_frame, text="Delete Employee").pack()
        tk.Label(self.app.content_frame, text="Username:").pack()
        self.del_employee_username_entry = tk.Entry(self.app.content_frame)
        self.del_employee_username_entry.pack()
        tk.Button(self.app.content_frame, text="Delete", command=self.delete_employee).pack()
        tk.Button(self.app.content_frame, text="Back", command=self.show_users).pack(pady=5)

    def delete_employee(self):
        username = self.del_employee_username_entry.get()
        conn = sqlite3.connect("user.db")
        cursor = conn.cursor()
        cursor.execute("DELETE FROM users WHERE username = ? AND role = 'Employee'", (username,))
        if cursor.rowcount > 0:
            conn.commit()
            messagebox.showinfo("Success", "Employee deleted successfully")
        else:
            messagebox.showerror("Error", "Employee not found or cannot delete manager")
        conn.close()
        self.show_users()


class VehicleManager:
    """Manages vehicle-related operations."""
    def __init__(self, app):
        self.app = app

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

        tk.Button(self.app.content_frame, text="Submit", command=self.add_vehicle).pack()
        tk.Button(self.app.content_frame, text="Back", command=self.app.show_main_menu).pack(pady=5)

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

    def show_vehicles_inventory(self):
        self.app.clear_content_frame()
        tk.Label(self.app.content_frame, text="Vehicles Inventory", font=("Arial", 16)).pack(pady=10)

        # Create a Treeview widget
        columns = ("Car ID", "Brand", "Model", "Year", "Rate/Day", "Rate/KM")
        tree = ttk.Treeview(self.app.content_frame, columns=columns, show="headings")

        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=120)

        # Fetch vehicles from the database
        conn = sqlite3.connect("vehicles.db")
        cursor = conn.cursor()
        cursor.execute("SELECT car_id, brand, model, year, rate_per_day, rate_per_km FROM vehicles")
        vehicles = cursor.fetchall()
        conn.close()

        # Add vehicles to the Treeview
        for vehicle in vehicles:
            tree.insert("", "end", values=vehicle)

        tree.pack(fill=tk.BOTH, expand=True)

        tk.Button(self.app.content_frame, text="Back", command=self.app.show_main_menu).pack(pady=5)

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
            vehicle_id = self.next_vehicle_id
            self.vehicles[vehicle_id] = {
                'brand': brand,
                'model': model,
                'year': year,
                'kilometers': kilometers,
                'rate_per_day': rate_per_day,
                'rate_per_km': rate_per_km,
                'vehicle_type': vehicle_type,
                'vehicle_class': vehicle_class,
                'available': True
            }
            self.next_vehicle_id += 1  # Increment Car ID for the next vehicle
            messagebox.showinfo("Success", "Vehicle added successfully")
            self.app.clear_content_frame()
        else:
            messagebox.showerror("Error", "All fields are required")


class CustomerManager:
    """Manages customer-related operations."""
    def __init__(self, app):
        self.app = app

    def show_add_customer(self):
        self.app.clear_content_frame()
        tk.Label(self.app.content_frame, text="Add Customer").pack()
        fields = ["Name", "Address", "Phone Number", "License Number", "Insurance Company", "Policy Number"]
        self.customer_entries = {}
        for field in fields:
            tk.Label(self.app.content_frame, text=f"{field}:").pack()
            entry = tk.Entry(self.app.content_frame)
            entry.pack()
            self.customer_entries[field] = entry

        tk.Button(self.app.content_frame, text="Submit", command=self.add_customer).pack()
        tk.Button(self.app.content_frame, text="Back", command=self.app.show_main_menu).pack(pady=5)

    def add_customer(self):
        name = self.customer_entries["Name"].get()
        address = self.customer_entries["Address"].get()
        phone = self.customer_entries["Phone Number"].get()
        license_number = self.customer_entries["License Number"].get()
        insurance_company = self.customer_entries["Insurance Company"].get()
        policy_number = self.customer_entries["Policy Number"].get()

        if name and address and phone and license_number and insurance_company and policy_number:
            conn = sqlite3.connect("customer.db")
            cursor = conn.cursor()
            try:
                cursor.execute("""
                    INSERT INTO customers (name, address, phone, license_number, insurance_company, policy_number)
                    VALUES (?, ?, ?, ?, ?, ?)
                """, (name, address, phone, license_number, insurance_company, policy_number))
                conn.commit()
                messagebox.showinfo("Success", "Customer added successfully")
                self.app.clear_content_frame()
            except sqlite3.IntegrityError:
                messagebox.showerror("Error", "Customer with this name already exists")
            finally:
                conn.close()
        else:
            messagebox.showerror("Error", "All fields are required")

    def show_customers(self):
        self.app.clear_content_frame()
        tk.Label(self.app.content_frame, text="Customer List", font=("Arial", 16)).pack(pady=10)

        # Create a Treeview widget
        columns = ("Name", "Address", "Phone Number", "Email", "Insurance Details")
        tree = ttk.Treeview(self.app.content_frame, columns=columns, show="headings")

        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=150)

        # Fetch customer data from the database
        conn = sqlite3.connect("customer.db")
        cursor = conn.cursor()
        cursor.execute("SELECT name, address, phone, '' AS email, '' AS insurance_details FROM customers")
        customers = cursor.fetchall()
        conn.close()

        # Add customers to the Treeview
        for customer in customers:
            tree.insert("", "end", values=customer)

        tree.pack(fill=tk.BOTH, expand=True)

        # Add a "View/Hide" button for insurance details
        def on_view_insurance():
            selected_item = tree.selection()
            if selected_item:
                customer_name = tree.item(selected_item, "values")[0]
                self.view_customer_details(customer_name)

        tk.Button(self.app.content_frame, text="View/Hide Insurance Details", command=on_view_insurance).pack(pady=5)
        tk.Button(self.app.content_frame, text="Back", command=self.app.show_main_menu).pack(pady=5)

    def view_customer_details(self, customer_name):
        self.app.clear_content_frame()
        tk.Label(self.app.content_frame, text=f"Details for {customer_name}", font=("Arial", 16)).pack(pady=10)

        # Fetch customer details from the database
        conn = sqlite3.connect("customer.db")
        cursor = conn.cursor()
        cursor.execute("""
            SELECT license_number, insurance_company, policy_number
            FROM customers
            WHERE name = ?
        """, (customer_name,))
        customer_details = cursor.fetchone()
        conn.close()

        if customer_details:
            labels = ["License Number", "Insurance Company", "Policy Number"]
            for label, detail in zip(labels, customer_details):
                tk.Label(self.app.content_frame, text=f"{label}: {detail}").pack(pady=5)
        else:
            tk.Label(self.app.content_frame, text="No details found for this customer.").pack(pady=10)

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
        self.main_menu_frame.pack(fill=tk.BOTH, expand=True)
        self.clear_content_frame()

        # Add buttons to the side menu
        for widget in self.side_menu_frame.winfo_children():
            widget.destroy()

        tk.Button(self.side_menu_frame, text="Manage Users", command=self.user_manager.show_users).pack(pady=5, fill=tk.X)
        tk.Button(self.side_menu_frame, text="Add Customer", command=self.customer_manager.show_add_customer).pack(pady=5, fill=tk.X)
        tk.Button(self.side_menu_frame, text="Customers", command=self.customer_manager.show_customers).pack(pady=5, fill=tk.X)
        tk.Button(self.side_menu_frame, text="Vehicles Inventory", command=self.vehicle_manager.show_vehicles_inventory).pack(pady=5, fill=tk.X)

        # Add a welcome message in the content frame
        tk.Label(self.content_frame, text="Welcome to Car Rental System", font=("Arial", 16)).pack(pady=10)

        # Display a list of all available vehicles
        tk.Label(self.content_frame, text="Available Vehicles:", font=("Arial", 14)).pack(pady=10)

        # Create a Treeview widget to display vehicles
        columns = ("Brand", "Model", "Year", "Kilometers", "Price Per Day", "Type", "Class", "Available")
        tree = ttk.Treeview(self.content_frame, columns=columns, show="headings")

        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=120)

        # Fetch vehicle data from the VehicleManager
        for vehicle_id, vehicle in self.vehicle_manager.vehicles.items():
            tree.insert("", "end", values=(
                vehicle['brand'], vehicle['model'], vehicle['year'], vehicle.get('kilometers', 'N/A'),
                vehicle['rate_per_day'], vehicle.get('vehicle_type', 'N/A'), vehicle.get('vehicle_class', 'N/A'),
                "Yes" if vehicle.get('available', True) else "No"
            ))

        tree.pack(fill=tk.BOTH, expand=True)


if __name__ == "__main__":
    DatabaseManager.initialize_database()  # Initialize both user.db and customer.db
    root = tk.Tk()
    app = CarRentalApp(root)
    root.mainloop()