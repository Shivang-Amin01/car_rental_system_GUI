# Car Rental System

## Overview
The Car Rental System is a comprehensive application designed to manage vehicle rentals, customer information, and user accounts. It provides functionalities for managing vehicles, customers, and generating financial reports.

## Project Structure
```
car_rental_system
├── car_rental_system
│   ├── databases
│   │   ├── customer.db        # SQLite database for storing customer information
│   │   ├── user.db           # SQLite database for storing user information
│   │   └── vehicle.db        # SQLite database for storing vehicle information
│   ├── reports
│   │   └── financial_reports.py # Contains the FinancialReports class for generating financial summaries and reports
│   ├── app.py                # Main application file that initializes the Car Rental System
│   └── README.md             # Documentation for the project
```

## Setup Instructions
1. **Clone the Repository**
   Clone the repository to your local machine using:
   ```
   git clone <repository-url>
   ```

2. **Install Dependencies**
   Ensure you have Python installed. Install any required packages using:
   ```
   pip install -r requirements.txt
   ```

3. **Database Initialization**
   The application will automatically create the necessary SQLite databases (`customer.db`, `user.db`, `vehicle.db`) upon first run.

4. **Run the Application**
   Start the application by executing:
   ```
   python app.py
   ```

## Usage
- **Login**: Users can log in using their credentials.
- **Manage Vehicles**: Add, update, or delete vehicle information.
- **Customer Management**: Add and manage customer details.
- **Financial Reports**: Generate financial summaries, revenue reports, and booking statistics through the financial reports section.

## Contributing
Contributions are welcome! Please submit a pull request or open an issue for any enhancements or bug fixes.

## License
This project is licensed under the MIT License. See the LICENSE file for more details.