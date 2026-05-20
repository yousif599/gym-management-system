import sqlite3


def initialize_database():
    conn = sqlite3.connect("gym_1.db")
    cur = conn.cursor()

    # Drop old tables if they exist
    cur.execute("DROP TABLE IF EXISTS admins")
    cur.execute("DROP TABLE IF EXISTS employees")
    cur.execute("DROP TABLE IF EXISTS members")
    cur.execute("DROP TABLE IF EXISTS products")
    cur.execute("DROP TABLE IF EXISTS orders")

    # Admins Table
    cur.execute(
        """
    CREATE TABLE admins (
        admin_id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL
    )
    """
    )

    # Employees Table
    cur.execute(
        """
    CREATE TABLE employees (
        employee_id INTEGER PRIMARY KEY AUTOINCREMENT,
        full_name TEXT NOT NULL,
        username TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL,
        job_title TEXT,
        salary REAL,
        hire_date TEXT
    )
    """
    )

    # Members Table
    cur.execute(
        """
    CREATE TABLE members (
        member_id INTEGER PRIMARY KEY AUTOINCREMENT,
        full_name TEXT NOT NULL,
        username TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL,
        age INTEGER,
        gender TEXT,
        phone TEXT,
        subscription_type TEXT,
        start_date TEXT,
        end_date TEXT
    )
    """
    )

    # Products Table
    cur.execute(
        """
    CREATE TABLE products (
        product_id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        price REAL NOT NULL,
        category TEXT
    )
    """
    )

    # Orders Table
    cur.execute(
        """
    CREATE TABLE orders (
        order_id INTEGER PRIMARY KEY AUTOINCREMENT,
        member_id INTEGER,
        product_id INTEGER,
        order_date TEXT,
        FOREIGN KEY (member_id) REFERENCES members(member_id) ON DELETE CASCADE,
        FOREIGN KEY (product_id) REFERENCES products(product_id) ON DELETE SET NULL
    )
    """
    )

    # Insert sample data
    cur.execute(
        "INSERT INTO admins (username, password) VALUES (?, ?)",
        ("admin", "admin123"),
    )
    cur.execute(
        "INSERT INTO admins (username, password) VALUES (?, ?)",
        ("admin1", "admin123"),
    )

    cur.execute(
        """
    INSERT INTO employees (full_name, username, password, job_title, salary, hire_date)
    VALUES (?, ?, ?, ?, ?, ?)
    """,
        ("Ahmed Khaled", "ahmedk", "1234", "Trainer", 5000, "2024-01-10"),
    )

    products = [
        ("Creatine HCL - 270g - Watermelon", 1200, "Supplement"),
        ("NitroTech Whey Gold - 2.27KG - Chocolate", 2800, "Supplement"),
        ("Max Whey - 1050g - French Chocolate", 1600, "Supplement"),
        ("Challenger Whey Isolate - 900g - Strawberry", 1900, "Supplement"),
        ("Gym Sport Bag - Red & Black", 450, "Accessories"),
        ("Dry Fit Gym T-Shirt - White", 300, "Clothing"),
    ]
    cur.executemany(
        "INSERT INTO products (name, price, category) VALUES (?, ?, ?)", products
    )

    cur.execute(
        """
    INSERT INTO members (full_name, username, password, age, gender, phone, subscription_type, start_date, end_date)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """,
        (
            "Amar Yasser",
            "amar1",
            "1234",
            25,
            "Male",
            "0123456789",
            "Gold",
            "2023-01-01",
            "2024-01-01",
        ),
    )

    conn.commit()
    conn.close()
    print("✅ Database initialized successfully.")


# Run the script
if __name__ == "__main__":
    initialize_database()
