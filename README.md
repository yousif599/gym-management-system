# Gym Management System

A desktop-based Gym Management System developed using **Python** and **Tkinter** for managing gym operations efficiently.

The system provides different interfaces for admins, employees, and members, allowing easy management of members, employees, products, and orders through a user-friendly GUI.

---

# Technologies Used

- Python
- Tkinter (GUI)
- SQLite Database

---

# Project Structure

```bash
GYM_V0/
│
├── src/
│   ├── login.py
│   ├── admin_panel.py
│   ├── employee_view.py
│   ├── member_home.py
│   ├── manage_members.py
│   ├── manage_employees.py
│   ├── manage_products.py
│   ├── register_member.py
│   ├── register_employee.py
│   ├── view_members_employee.py
│   ├── view_products_employee.py
│   ├── view_orders.py
│   └── init_db.py
│
├── README.md
├── requirements.txt
└── .gitignore
```

---

# Project Files Description

## `login.py`
Handles the login system and authentication for Admin, Employee, and Member roles.

## `admin_panel.py`
Main dashboard for the admin to manage the entire system.

## `employee_view.py`
Employee interface for handling member-related operations.

## `member_home.py`
Home page for gym members displaying available services and features.

## `manage_members.py`
Provides functionality for adding, updating, deleting, and managing gym members.

## `manage_employees.py`
Handles employee records and management operations.

## `manage_products.py`
Used for managing gym products and inventory.

## `register_member.py`
Registration form for adding new gym members.

## `register_employee.py`
Registration form for adding new employees.

## `view_members_employee.py`
Allows employees to search and view member information.

## `view_products_employee.py`
Displays available products for employees.

## `view_orders.py`
Manages customer orders and purchase records.

## `init_db.py`
Initializes the SQLite database and creates all required tables.

---

# Features

- User Authentication System
- Admin and Employee Roles
- Member Management
- Product Management
- Order Tracking
- SQLite Database Integration
- User-Friendly Tkinter GUI

---

# Future Improvements

- Payment Integration
- Attendance Tracking
- Subscription Management
- Dashboard Analytics
- Barcode System for Products

---

# Author

Yusuf
