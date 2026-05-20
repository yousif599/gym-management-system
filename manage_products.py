from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import sqlite3

# Color scheme
COLORS = {
    "primary": "#2C3E50",
    "secondary": "#3498DB",
    "success": "#27AE60",
    "danger": "#E74C3C",
    "warning": "#F39C12",
    "light": "#ECF0F1",
    "dark": "#34495E",
    "white": "#FFFFFF",
}


class ProductManager:
    def __init__(self):
        self.root = Tk()
        self.setup_window()
        self.create_widgets()
        self.load_products()

    def setup_window(self):
        self.root.title("📦 Product Management - Admin Panel")
        self.root.geometry("1400x900")
        self.root.configure(bg=COLORS["light"])
        self.center_window()

    def center_window(self):
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f"{width}x{height}+{x}+{y}")

    def create_widgets(self):
        # Header
        header_frame = Frame(self.root, bg=COLORS["primary"], height=100)
        header_frame.pack(fill=X)
        header_frame.pack_propagate(False)

        header_content = Frame(header_frame, bg=COLORS["primary"])
        header_content.pack(expand=True)

        Label(
            header_content,
            text="📦 Product Management",
            font=("Arial", 24, "bold"),
            bg=COLORS["primary"],
            fg=COLORS["white"],
        ).pack(pady=15)

        Label(
            header_content,
            text="Manage your gym products and inventory",
            font=("Arial", 14),
            bg=COLORS["primary"],
            fg=COLORS["light"],
        ).pack()

        # Main content
        main_frame = Frame(self.root, bg=COLORS["light"])
        main_frame.pack(fill=BOTH, expand=True, padx=30, pady=30)

        # Add product form
        form_frame = Frame(main_frame, bg=COLORS["white"], relief=RAISED, bd=2)
        form_frame.pack(fill=X, pady=(0, 20), ipady=20)

        Label(
            form_frame,
            text="➕ Add New Product",
            font=("Arial", 16, "bold"),
            bg=COLORS["white"],
            fg=COLORS["primary"],
        ).pack(pady=(0, 15))

        # Form fields
        fields_frame = Frame(form_frame, bg=COLORS["white"])
        fields_frame.pack(pady=10)

        # Product name
        Label(
            fields_frame,
            text="Product Name:",
            font=("Arial", 12, "bold"),
            bg=COLORS["white"],
            fg=COLORS["dark"],
        ).grid(row=0, column=0, padx=10, pady=5, sticky=W)
        self.name_entry = Entry(
            fields_frame, font=("Arial", 12), width=30, relief=FLAT, bd=5
        )
        self.name_entry.grid(row=0, column=1, padx=10, pady=5)

        # Price
        Label(
            fields_frame,
            text="Price (EGP):",
            font=("Arial", 12, "bold"),
            bg=COLORS["white"],
            fg=COLORS["dark"],
        ).grid(row=0, column=2, padx=10, pady=5, sticky=W)
        self.price_entry = Entry(
            fields_frame, font=("Arial", 12), width=15, relief=FLAT, bd=5
        )
        self.price_entry.grid(row=0, column=3, padx=10, pady=5)

        # Category
        Label(
            fields_frame,
            text="Category:",
            font=("Arial", 12, "bold"),
            bg=COLORS["white"],
            fg=COLORS["dark"],
        ).grid(row=1, column=0, padx=10, pady=5, sticky=W)
        self.category_entry = Entry(
            fields_frame, font=("Arial", 12), width=30, relief=FLAT, bd=5
        )
        self.category_entry.grid(row=1, column=1, padx=10, pady=5)

        # Add button
        add_btn = Button(
            fields_frame,
            text="➕ Add Product",
            command=self.add_product,
            font=("Arial", 12, "bold"),
            bg=COLORS["success"],
            fg=COLORS["white"],
            relief=FLAT,
            cursor="hand2",
            activebackground="#1E8449",
        )
        add_btn.grid(row=1, column=3, padx=10, pady=5, ipady=5)

        # Control buttons
        control_frame = Frame(main_frame, bg=COLORS["white"], relief=RAISED, bd=2)
        control_frame.pack(fill=X, pady=(0, 20), ipady=15)

        Label(
            control_frame,
            text="🎛️ Controls",
            font=("Arial", 16, "bold"),
            bg=COLORS["white"],
            fg=COLORS["primary"],
        ).pack(pady=(0, 10))

        button_frame = Frame(control_frame, bg=COLORS["white"])
        button_frame.pack()

        Button(
            button_frame,
            text="🔄 Refresh",
            command=self.load_products,
            font=("Arial", 12, "bold"),
            bg=COLORS["secondary"],
            fg=COLORS["white"],
            relief=FLAT,
            cursor="hand2",
            width=15,
            activebackground="#2980B9",
        ).grid(row=0, column=0, padx=10, ipady=8)

        Button(
            button_frame,
            text="🗑️ Delete Selected",
            command=self.delete_product,
            font=("Arial", 12, "bold"),
            bg=COLORS["danger"],
            fg=COLORS["white"],
            relief=FLAT,
            cursor="hand2",
            width=15,
            activebackground="#C0392B",
        ).grid(row=0, column=1, padx=10, ipady=8)

        # Product list
        list_frame = Frame(main_frame, bg=COLORS["white"], relief=RAISED, bd=2)
        list_frame.pack(fill=BOTH, expand=True, ipady=20)

        Label(
            list_frame,
            text="📋 Product List",
            font=("Arial", 16, "bold"),
            bg=COLORS["white"],
            fg=COLORS["primary"],
        ).pack(pady=(0, 15))

        # Treeview
        style = ttk.Style()
        style.theme_use("clam")
        style.configure(
            "Custom.Treeview",
            background=COLORS["light"],
            foreground=COLORS["dark"],
            rowheight=30,
            fieldbackground=COLORS["light"],
        )
        style.configure(
            "Custom.Treeview.Heading",
            background=COLORS["primary"],
            foreground=COLORS["white"],
            font=("Arial", 12, "bold"),
        )

        tree_container = Frame(list_frame, bg=COLORS["white"])
        tree_container.pack(fill=BOTH, expand=True, padx=20, pady=(0, 20))

        scrollbar = ttk.Scrollbar(tree_container, orient="vertical")

        columns = ("ID", "Name", "Price", "Category")
        self.tree = ttk.Treeview(
            tree_container,
            columns=columns,
            show="headings",
            style="Custom.Treeview",
            yscrollcommand=scrollbar.set,
        )

        scrollbar.config(command=self.tree.yview)

        # Define columns
        column_widths = {"ID": 80, "Name": 400, "Price": 120, "Category": 200}
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(
                col, width=column_widths[col], anchor=CENTER if col != "Name" else W
            )

        self.tree.pack(side=LEFT, fill=BOTH, expand=True)
        scrollbar.pack(side=RIGHT, fill=Y)

    def add_product(self):
        name = self.name_entry.get().strip()
        price = self.price_entry.get().strip()
        category = self.category_entry.get().strip()

        if not all([name, price, category]):
            messagebox.showerror("Error", "All fields are required.")
            return

        try:
            price_float = float(price)
            if price_float <= 0:
                raise ValueError("Price must be positive")

            conn = sqlite3.connect("gym_1.db")
            cur = conn.cursor()
            cur.execute(
                "INSERT INTO products (name, price, category) VALUES (?, ?, ?)",
                (name, price_float, category),
            )
            conn.commit()
            conn.close()

            # Clear entries
            self.name_entry.delete(0, END)
            self.price_entry.delete(0, END)
            self.category_entry.delete(0, END)

            messagebox.showinfo("Success", f"Product '{name}' added successfully!")
            self.load_products()

        except ValueError as e:
            messagebox.showerror(
                "Invalid Input", "Please enter a valid price (positive number)."
            )
        except sqlite3.Error as e:
            messagebox.showerror("Database Error", f"An error occurred: {e}")

    def load_products(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

        try:
            conn = sqlite3.connect("gym_1.db")
            cur = conn.cursor()
            cur.execute("SELECT product_id, name, price, category FROM products")
            products = cur.fetchall()
            conn.close()

            for product in products:
                # Format price
                formatted_product = list(product)
                formatted_product[2] = f"{product[2]:.2f} EGP"
                self.tree.insert("", "end", values=formatted_product)

        except sqlite3.Error as e:
            messagebox.showerror("Database Error", f"An error occurred: {e}")

    def delete_product(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showerror("Error", "Please select a product to delete.")
            return

        product_data = self.tree.item(selected_item, "values")
        product_name = product_data[1]

        if not messagebox.askyesno(
            "Confirm Delete",
            f"Are you sure you want to delete product:\n{product_name}?",
        ):
            return

        try:
            product_id = product_data[0]
            conn = sqlite3.connect("gym_1.db")
            cur = conn.cursor()
            cur.execute("DELETE FROM products WHERE product_id=?", (product_id,))
            conn.commit()
            conn.close()

            messagebox.showinfo(
                "Success", f"Product '{product_name}' deleted successfully."
            )
            self.load_products()

        except sqlite3.Error as e:
            messagebox.showerror("Database Error", f"An error occurred: {e}")

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    app = ProductManager()
    app.run()
