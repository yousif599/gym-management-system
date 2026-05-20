from tkinter import *
from tkinter import ttk
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


class ProductViewEmployee:
    def __init__(self):
        self.root = Tk()
        self.setup_window()
        self.create_widgets()
        self.load_products()

    def setup_window(self):
        self.root.title("📦 Product Catalog - Employee Panel")
        self.root.geometry("1200x800")
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
            text="📦 Product Catalog",
            font=("Arial", 24, "bold"),
            bg=COLORS["primary"],
            fg=COLORS["white"],
        ).pack(pady=15)

        Label(
            header_content,
            text="Browse available products and help members with their inquiries",
            font=("Arial", 14),
            bg=COLORS["primary"],
            fg=COLORS["light"],
        ).pack()

        # Main content
        main_frame = Frame(self.root, bg=COLORS["light"])
        main_frame.pack(fill=BOTH, expand=True, padx=30, pady=30)

        # Filter section
        filter_frame = Frame(main_frame, bg=COLORS["white"], relief=RAISED, bd=2)
        filter_frame.pack(fill=X, pady=(0, 20), ipady=15)

        Label(
            filter_frame,
            text="🔍 Filter Products",
            font=("Arial", 16, "bold"),
            bg=COLORS["white"],
            fg=COLORS["primary"],
        ).pack(pady=(0, 10))

        filter_controls = Frame(filter_frame, bg=COLORS["white"])
        filter_controls.pack()

        Label(
            filter_controls,
            text="Category:",
            font=("Arial", 12, "bold"),
            bg=COLORS["white"],
            fg=COLORS["dark"],
        ).grid(row=0, column=0, padx=10)

        self.category_var = StringVar(value="All Categories")
        self.category_combo = ttk.Combobox(
            filter_controls,
            textvariable=self.category_var,
            font=("Arial", 12),
            width=20,
            state="readonly",
        )
        self.category_combo.grid(row=0, column=1, padx=10)
        self.category_combo.bind("<<ComboboxSelected>>", self.filter_by_category)

        Button(
            filter_controls,
            text="🔄 Refresh",
            command=self.load_products,
            font=("Arial", 12, "bold"),
            bg=COLORS["secondary"],
            fg=COLORS["white"],
            relief=FLAT,
            cursor="hand2",
        ).grid(row=0, column=2, padx=20, ipady=5)

        # Statistics section
        stats_frame = Frame(main_frame, bg=COLORS["white"], relief=RAISED, bd=2)
        stats_frame.pack(fill=X, pady=(0, 20), ipady=15)

        Label(
            stats_frame,
            text="📊 Product Statistics",
            font=("Arial", 16, "bold"),
            bg=COLORS["white"],
            fg=COLORS["primary"],
        ).pack(pady=(0, 10))

        stats_content = Frame(stats_frame, bg=COLORS["white"])
        stats_content.pack()

        self.total_products_label = Label(
            stats_content,
            text="Total Products: 0",
            font=("Arial", 12, "bold"),
            bg=COLORS["white"],
            fg=COLORS["success"],
        )
        self.total_products_label.grid(row=0, column=0, padx=20)

        self.avg_price_label = Label(
            stats_content,
            text="Average Price: 0 EGP",
            font=("Arial", 12, "bold"),
            bg=COLORS["white"],
            fg=COLORS["secondary"],
        )
        self.avg_price_label.grid(row=0, column=1, padx=20)

        self.categories_label = Label(
            stats_content,
            text="Categories: 0",
            font=("Arial", 12, "bold"),
            bg=COLORS["white"],
            fg=COLORS["warning"],
        )
        self.categories_label.grid(row=0, column=2, padx=20)

        # Product list
        list_frame = Frame(main_frame, bg=COLORS["white"], relief=RAISED, bd=2)
        list_frame.pack(fill=BOTH, expand=True, ipady=20)

        Label(
            list_frame,
            text="📋 Available Products",
            font=("Arial", 16, "bold"),
            bg=COLORS["white"],
            fg=COLORS["primary"],
        ).pack(pady=(0, 15))

        # Treeview with custom style
        style = ttk.Style()
        style.theme_use("clam")
        style.configure(
            "Custom.Treeview",
            background=COLORS["light"],
            foreground=COLORS["dark"],
            rowheight=35,
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

        # Scrollbars
        v_scrollbar = ttk.Scrollbar(tree_container, orient="vertical")
        h_scrollbar = ttk.Scrollbar(tree_container, orient="horizontal")

        # Treeview
        columns = ("ID", "Product Name", "Price (EGP)", "Category", "Price Range")
        self.tree = ttk.Treeview(
            tree_container,
            columns=columns,
            show="headings",
            style="Custom.Treeview",
            yscrollcommand=v_scrollbar.set,
            xscrollcommand=h_scrollbar.set,
        )

        # Configure scrollbars
        v_scrollbar.config(command=self.tree.yview)
        h_scrollbar.config(command=self.tree.xview)

        # Define columns
        column_widths = {
            "ID": 60,
            "Product Name": 400,
            "Price (EGP)": 120,
            "Category": 150,
            "Price Range": 120,
        }
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(
                col,
                width=column_widths[col],
                anchor=CENTER if col != "Product Name" else W,
            )

        # Pack treeview and scrollbars
        self.tree.grid(row=0, column=0, sticky="nsew")
        v_scrollbar.grid(row=0, column=1, sticky="ns")
        h_scrollbar.grid(row=1, column=0, sticky="ew")

        tree_container.grid_rowconfigure(0, weight=1)
        tree_container.grid_columnconfigure(0, weight=1)

        # Control buttons
        button_frame = Frame(main_frame, bg=COLORS["light"])
        button_frame.pack(pady=20)

        Button(
            button_frame,
            text="📋 Product Details",
            command=self.show_product_details,
            font=("Arial", 12, "bold"),
            bg=COLORS["success"],
            fg=COLORS["white"],
            relief=FLAT,
            cursor="hand2",
            width=18,
            activebackground="#1E8449",
        ).pack(side=LEFT, padx=10, ipady=10)

        Button(
            button_frame,
            text="🚪 Close",
            command=self.root.destroy,
            font=("Arial", 12, "bold"),
            bg=COLORS["danger"],
            fg=COLORS["white"],
            relief=FLAT,
            cursor="hand2",
            width=15,
            activebackground="#C0392B",
        ).pack(side=LEFT, padx=10, ipady=10)

    def load_products(self):
        """Load all products into the treeview"""
        for item in self.tree.get_children():
            self.tree.delete(item)

        try:
            conn = sqlite3.connect("gym_1.db")
            cur = conn.cursor()
            cur.execute(
                "SELECT product_id, name, price, category FROM products ORDER BY category, name"
            )
            products = cur.fetchall()

            # Get categories for filter
            cur.execute("SELECT DISTINCT category FROM products ORDER BY category")
            categories = [row[0] for row in cur.fetchall()]
            conn.close()

            # Update category combobox
            self.category_combo["values"] = ["All Categories"] + categories

            # Calculate statistics
            total_products = len(products)
            total_price = sum(product[2] for product in products)
            avg_price = total_price / total_products if total_products > 0 else 0
            total_categories = len(categories)

            # Update statistics labels
            self.total_products_label.config(text=f"Total Products: {total_products}")
            self.avg_price_label.config(text=f"Average Price: {avg_price:.2f} EGP")
            self.categories_label.config(text=f"Categories: {total_categories}")

            # Add products to treeview
            for product in products:
                price = product[2]
                # Determine price range
                if price < 500:
                    price_range = "💰 Budget"
                elif price < 1500:
                    price_range = "💳 Standard"
                else:
                    price_range = "💎 Premium"

                product_with_range = product + (price_range,)
                self.tree.insert("", "end", values=product_with_range)

        except sqlite3.Error as e:
            from tkinter import messagebox

            messagebox.showerror("Database Error", f"An error occurred: {e}")

    def filter_by_category(self, event=None):
        """Filter products by selected category"""
        selected_category = self.category_var.get()

        for item in self.tree.get_children():
            self.tree.delete(item)

        try:
            conn = sqlite3.connect("gym_1.db")
            cur = conn.cursor()

            if selected_category == "All Categories":
                cur.execute(
                    "SELECT product_id, name, price, category FROM products ORDER BY category, name"
                )
            else:
                cur.execute(
                    "SELECT product_id, name, price, category FROM products WHERE category = ? ORDER BY name",
                    (selected_category,),
                )

            products = cur.fetchall()
            conn.close()

            for product in products:
                price = product[2]
                # Determine price range
                if price < 500:
                    price_range = "💰 Budget"
                elif price < 1500:
                    price_range = "💳 Standard"
                else:
                    price_range = "💎 Premium"

                product_with_range = product + (price_range,)
                self.tree.insert("", "end", values=product_with_range)

        except sqlite3.Error as e:
            from tkinter import messagebox

            messagebox.showerror("Database Error", f"An error occurred: {e}")

    def show_product_details(self):
        """Show detailed information about selected product"""
        selected_item = self.tree.selection()
        if not selected_item:
            from tkinter import messagebox

            messagebox.showerror("Error", "Please select a product to view details.")
            return

        product_data = self.tree.item(selected_item, "values")

        # Create details window
        details_window = Toplevel(self.root)
        details_window.title(f"📦 Product Details")
        details_window.geometry("500x400")
        details_window.configure(bg=COLORS["light"])
        details_window.resizable(False, False)
        details_window.transient(self.root)
        details_window.grab_set()

        # Center the window
        details_window.update_idletasks()
        x = (details_window.winfo_screenwidth() // 2) - (250)
        y = (details_window.winfo_screenheight() // 2) - (200)
        details_window.geometry(f"500x400+{x}+{y}")

        # Header
        header_frame = Frame(details_window, bg=COLORS["primary"], height=80)
        header_frame.pack(fill=X)
        header_frame.pack_propagate(False)

        Label(
            header_frame,
            text="📦 Product Information",
            font=("Arial", 18, "bold"),
            bg=COLORS["primary"],
            fg=COLORS["white"],
        ).pack(pady=20)

        # Details content
        content_frame = Frame(details_window, bg=COLORS["white"])
        content_frame.pack(fill=BOTH, expand=True, padx=20, pady=20)

        details = [
            ("🆔 Product ID:", product_data[0]),
            ("📦 Product Name:", product_data[1]),
            ("💰 Price:", f"{product_data[2]} EGP"),
            ("📂 Category:", product_data[3]),
            ("💎 Price Range:", product_data[4]),
        ]

        for label, value in details:
            detail_frame = Frame(content_frame, bg=COLORS["light"], relief=RAISED, bd=1)
            detail_frame.pack(fill=X, pady=8, ipady=10)

            Label(
                detail_frame,
                text=label,
                font=("Arial", 12, "bold"),
                bg=COLORS["light"],
                fg=COLORS["dark"],
                width=18,
                anchor=W,
            ).pack(side=LEFT, padx=15)

            Label(
                detail_frame,
                text=str(value),
                font=("Arial", 12),
                bg=COLORS["light"],
                fg=COLORS["primary"],
            ).pack(side=LEFT, padx=(10, 0))

        # Close button
        Button(
            content_frame,
            text="✅ Close",
            command=details_window.destroy,
            font=("Arial", 12, "bold"),
            bg=COLORS["secondary"],
            fg=COLORS["white"],
            relief=FLAT,
            cursor="hand2",
            width=15,
        ).pack(pady=20, ipady=8)

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    app = ProductViewEmployee()
    app.run()
