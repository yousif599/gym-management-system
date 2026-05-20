from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import sqlite3
from datetime import datetime, timedelta

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


class OrdersView:
    def __init__(self):
        self.root = Tk()
        self.setup_window()
        self.create_widgets()
        self.load_orders()

    def setup_window(self):
        self.root.title("📊 Sales & Orders Management - Admin Panel")
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
            text="📊 Sales & Orders Dashboard",
            font=("Arial", 24, "bold"),
            bg=COLORS["primary"],
            fg=COLORS["white"],
        ).pack(pady=15)

        Label(
            header_content,
            text="Monitor your gym's product sales and revenue",
            font=("Arial", 14),
            bg=COLORS["primary"],
            fg=COLORS["light"],
        ).pack()

        # Main content
        main_frame = Frame(self.root, bg=COLORS["light"])
        main_frame.pack(fill=BOTH, expand=True, padx=30, pady=30)

        # Statistics section
        stats_frame = Frame(main_frame, bg=COLORS["white"], relief=RAISED, bd=2)
        stats_frame.pack(fill=X, pady=(0, 20), ipady=20)

        Label(
            stats_frame,
            text="💰 Revenue Statistics",
            font=("Arial", 16, "bold"),
            bg=COLORS["white"],
            fg=COLORS["primary"],
        ).pack(pady=(0, 15))

        stats_content = Frame(stats_frame, bg=COLORS["white"])
        stats_content.pack()

        # Revenue cards
        self.create_stat_card(
            stats_content, "💰 Total Revenue", "0 EGP", COLORS["success"], 0, 0
        )
        self.create_stat_card(
            stats_content, "📦 Total Orders", "0", COLORS["secondary"], 0, 1
        )
        self.create_stat_card(
            stats_content, "📅 Today's Sales", "0 EGP", COLORS["warning"], 0, 2
        )
        self.create_stat_card(
            stats_content, "📈 Average Order", "0 EGP", COLORS["dark"], 0, 3
        )

        # Filter section
        filter_frame = Frame(main_frame, bg=COLORS["white"], relief=RAISED, bd=2)
        filter_frame.pack(fill=X, pady=(0, 20), ipady=15)

        Label(
            filter_frame,
            text="🔍 Filter Orders",
            font=("Arial", 16, "bold"),
            bg=COLORS["white"],
            fg=COLORS["primary"],
        ).pack(pady=(0, 10))

        filter_controls = Frame(filter_frame, bg=COLORS["white"])
        filter_controls.pack()

        # Date filter
        Label(
            filter_controls,
            text="Date Filter:",
            font=("Arial", 12, "bold"),
            bg=COLORS["white"],
            fg=COLORS["dark"],
        ).grid(row=0, column=0, padx=10)

        self.date_filter_var = StringVar(value="All Time")
        date_options = ["All Time", "Today", "This Week", "This Month"]
        ttk.Combobox(
            filter_controls,
            textvariable=self.date_filter_var,
            values=date_options,
            font=("Arial", 12),
            width=15,
            state="readonly",
        ).grid(row=0, column=1, padx=10)

        # Member filter
        Label(
            filter_controls,
            text="Member:",
            font=("Arial", 12, "bold"),
            bg=COLORS["white"],
            fg=COLORS["dark"],
        ).grid(row=0, column=2, padx=10)

        self.member_entry = Entry(filter_controls, font=("Arial", 12), width=20)
        self.member_entry.grid(row=0, column=3, padx=10)

        # Filter buttons
        Button(
            filter_controls,
            text="🔍 Apply Filter",
            command=self.apply_filter,
            font=("Arial", 12, "bold"),
            bg=COLORS["secondary"],
            fg=COLORS["white"],
            relief=FLAT,
            cursor="hand2",
        ).grid(row=0, column=4, padx=20, ipady=5)

        Button(
            filter_controls,
            text="🔄 Reset",
            command=self.load_orders,
            font=("Arial", 12, "bold"),
            bg=COLORS["dark"],
            fg=COLORS["white"],
            relief=FLAT,
            cursor="hand2",
        ).grid(row=0, column=5, padx=10, ipady=5)

        # Orders list
        list_frame = Frame(main_frame, bg=COLORS["white"], relief=RAISED, bd=2)
        list_frame.pack(fill=BOTH, expand=True, ipady=20)

        Label(
            list_frame,
            text="📋 Order History",
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

        # Scrollbars
        v_scrollbar = ttk.Scrollbar(tree_container, orient="vertical")
        h_scrollbar = ttk.Scrollbar(tree_container, orient="horizontal")

        # Treeview
        columns = (
            "Order ID",
            "Member Name",
            "Product Name",
            "Category",
            "Price",
            "Order Date",
            "Status",
        )
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
            "Order ID": 80,
            "Member Name": 150,
            "Product Name": 250,
            "Category": 120,
            "Price": 100,
            "Order Date": 120,
            "Status": 100,
        }
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(
                col,
                width=column_widths[col],
                anchor=CENTER if col not in ["Member Name", "Product Name"] else W,
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

        buttons = [
            ("📊 Generate Report", self.generate_report, COLORS["success"]),
            ("📋 Order Details", self.show_order_details, COLORS["secondary"]),
            ("🗑️ Delete Order", self.delete_order, COLORS["danger"]),
            ("🚪 Close", self.root.destroy, COLORS["dark"]),
        ]

        for i, (text, command, color) in enumerate(buttons):
            btn = Button(
                button_frame,
                text=text,
                command=command,
                font=("Arial", 12, "bold"),
                bg=color,
                fg=COLORS["white"],
                relief=FLAT,
                cursor="hand2",
                width=15,
                activebackground=self.darken_color(color),
            )
            btn.grid(row=0, column=i, padx=10, ipady=10)

    def create_stat_card(self, parent, title, value, color, row, col):
        """Create a statistics card"""
        card_frame = Frame(parent, bg=color, relief=RAISED, bd=2, width=200, height=80)
        card_frame.grid(row=row, column=col, padx=15, pady=10, sticky="nsew")
        card_frame.pack_propagate(False)

        Label(
            card_frame,
            text=title,
            font=("Arial", 10, "bold"),
            bg=color,
            fg=COLORS["white"],
        ).pack(pady=(10, 0))

        value_label = Label(
            card_frame,
            text=value,
            font=("Arial", 14, "bold"),
            bg=color,
            fg=COLORS["white"],
        )
        value_label.pack(pady=(0, 10))

        # Store reference to update later
        if "Total Revenue" in title:
            self.total_revenue_label = value_label
        elif "Total Orders" in title:
            self.total_orders_label = value_label
        elif "Today's Sales" in title:
            self.today_sales_label = value_label
        elif "Average Order" in title:
            self.avg_order_label = value_label

    def load_orders(self):
        """Load all orders from database"""
        for item in self.tree.get_children():
            self.tree.delete(item)

        try:
            conn = sqlite3.connect("gym_1.db")
            cur = conn.cursor()

            # Complex query to get all order information
            query = """
            SELECT 
                o.order_id,
                m.full_name,
                p.name,
                p.category,
                p.price,
                o.order_date,
                CASE 
                    WHEN date(o.order_date) = date('now') THEN '✅ Recent'
                    WHEN date(o.order_date) >= date('now', '-7 days') THEN '📅 This Week'
                    ELSE '📋 Older'
                END as status
            FROM orders o
            JOIN members m ON o.member_id = m.member_id
            JOIN products p ON o.product_id = p.product_id
            ORDER BY o.order_id DESC
            """

            cur.execute(query)
            orders = cur.fetchall()
            conn.close()

            # Calculate statistics
            total_revenue = sum(order[4] for order in orders)
            total_orders = len(orders)

            # Today's sales
            today = datetime.now().strftime("%Y-%m-%d")
            today_sales = sum(order[4] for order in orders if order[5] == today)

            # Average order value
            avg_order = total_revenue / total_orders if total_orders > 0 else 0

            # Update statistics
            self.total_revenue_label.config(text=f"{total_revenue:,.2f} EGP")
            self.total_orders_label.config(text=str(total_orders))
            self.today_sales_label.config(text=f"{today_sales:,.2f} EGP")
            self.avg_order_label.config(text=f"{avg_order:,.2f} EGP")

            # Add orders to treeview
            for order in orders:
                formatted_order = list(order)
                formatted_order[4] = f"{order[4]:.2f} EGP"  # Format price
                self.tree.insert("", "end", values=formatted_order)

        except sqlite3.Error as e:
            messagebox.showerror("Database Error", f"An error occurred: {e}")

    def apply_filter(self):
        """Apply date and member filters"""
        date_filter = self.date_filter_var.get()
        member_filter = self.member_entry.get().strip()

        for item in self.tree.get_children():
            self.tree.delete(item)

        try:
            conn = sqlite3.connect("gym_1.db")
            cur = conn.cursor()

            # Build query based on filters
            base_query = """
            SELECT 
                o.order_id,
                m.full_name,
                p.name,
                p.category,
                p.price,
                o.order_date,
                CASE 
                    WHEN date(o.order_date) = date('now') THEN '✅ Recent'
                    WHEN date(o.order_date) >= date('now', '-7 days') THEN '📅 This Week'
                    ELSE '📋 Older'
                END as status
            FROM orders o
            JOIN members m ON o.member_id = m.member_id
            JOIN products p ON o.product_id = p.product_id
            WHERE 1=1
            """

            params = []

            # Date filter
            if date_filter == "Today":
                base_query += " AND date(o.order_date) = date('now')"
            elif date_filter == "This Week":
                base_query += " AND date(o.order_date) >= date('now', '-7 days')"
            elif date_filter == "This Month":
                base_query += " AND date(o.order_date) >= date('now', '-30 days')"

            # Member filter
            if member_filter:
                base_query += " AND m.full_name LIKE ?"
                params.append(f"%{member_filter}%")

            base_query += " ORDER BY o.order_id DESC"

            cur.execute(base_query, params)
            orders = cur.fetchall()
            conn.close()

            # Add filtered orders to treeview
            for order in orders:
                formatted_order = list(order)
                formatted_order[4] = f"{order[4]:.2f} EGP"  # Format price
                self.tree.insert("", "end", values=formatted_order)

        except sqlite3.Error as e:
            messagebox.showerror("Database Error", f"An error occurred: {e}")

    def show_order_details(self):
        """Show detailed information about selected order"""
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showerror("Error", "Please select an order to view details.")
            return

        order_data = self.tree.item(selected_item, "values")

        # Create details window
        details_window = Toplevel(self.root)
        details_window.title(f"📋 Order Details - #{order_data[0]}")
        details_window.geometry("500x400")
        details_window.configure(bg=COLORS["light"])
        details_window.resizable(False, False)
        details_window.transient(self.root)
        details_window.grab_set()

        # Header
        header_frame = Frame(details_window, bg=COLORS["primary"], height=80)
        header_frame.pack(fill=X)
        header_frame.pack_propagate(False)

        Label(
            header_frame,
            text=f"📋 Order #{order_data[0]}",
            font=("Arial", 18, "bold"),
            bg=COLORS["primary"],
            fg=COLORS["white"],
        ).pack(pady=20)

        # Details content
        content_frame = Frame(details_window, bg=COLORS["white"])
        content_frame.pack(fill=BOTH, expand=True, padx=20, pady=20)

        details = [
            ("🆔 Order ID:", order_data[0]),
            ("👤 Member Name:", order_data[1]),
            ("📦 Product Name:", order_data[2]),
            ("📂 Category:", order_data[3]),
            ("💰 Price:", order_data[4]),
            ("📅 Order Date:", order_data[5]),
            ("📊 Status:", order_data[6]),
        ]

        for label, value in details:
            detail_frame = Frame(content_frame, bg=COLORS["light"], relief=RAISED, bd=1)
            detail_frame.pack(fill=X, pady=5, ipady=8)

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

    def delete_order(self):
        """Delete selected order"""
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showerror("Error", "Please select an order to delete.")
            return

        order_data = self.tree.item(selected_item, "values")
        order_id = order_data[0]

        if messagebox.askyesno(
            "Confirm Delete",
            f"Are you sure you want to delete Order #{order_id}?\n\nThis action cannot be undone.",
        ):
            try:
                conn = sqlite3.connect("gym_1.db")
                cur = conn.cursor()
                cur.execute("DELETE FROM orders WHERE order_id=?", (order_id,))
                conn.commit()
                conn.close()

                messagebox.showinfo(
                    "Success", f"Order #{order_id} deleted successfully."
                )
                self.load_orders()

            except sqlite3.Error as e:
                messagebox.showerror("Database Error", f"An error occurred: {e}")

    def generate_report(self):
        """Generate a simple sales report"""
        try:
            conn = sqlite3.connect("gym_1.db")
            cur = conn.cursor()

            # Get report data
            cur.execute(
                """
                SELECT 
                    p.category,
                    COUNT(*) as order_count,
                    SUM(p.price) as total_revenue
                FROM orders o
                JOIN products p ON o.product_id = p.product_id
                GROUP BY p.category
                ORDER BY total_revenue DESC
            """
            )
            category_stats = cur.fetchall()

            cur.execute(
                """
                SELECT 
                    date(o.order_date) as order_date,
                    COUNT(*) as daily_orders,
                    SUM(p.price) as daily_revenue
                FROM orders o
                JOIN products p ON o.product_id = p.product_id
                WHERE date(o.order_date) >= date('now', '-7 days')
                GROUP BY date(o.order_date)
                ORDER BY order_date DESC
            """
            )
            daily_stats = cur.fetchall()

            conn.close()

            # Create report window
            report_window = Toplevel(self.root)
            report_window.title("📊 Sales Report")
            report_window.geometry("600x500")
            report_window.configure(bg=COLORS["light"])
            report_window.transient(self.root)

            # Header
            header_frame = Frame(report_window, bg=COLORS["primary"], height=80)
            header_frame.pack(fill=X)
            header_frame.pack_propagate(False)

            Label(
                header_frame,
                text="📊 Sales Report",
                font=("Arial", 18, "bold"),
                bg=COLORS["primary"],
                fg=COLORS["white"],
            ).pack(pady=20)

            # Report content
            content_frame = Frame(report_window, bg=COLORS["white"])
            content_frame.pack(fill=BOTH, expand=True, padx=20, pady=20)

            # Category statistics
            Label(
                content_frame,
                text="📂 Sales by Category",
                font=("Arial", 14, "bold"),
                bg=COLORS["white"],
                fg=COLORS["primary"],
            ).pack(pady=(0, 10))

            category_frame = Frame(
                content_frame, bg=COLORS["light"], relief=RAISED, bd=1
            )
            category_frame.pack(fill=X, pady=(0, 20), ipady=10)

            for i, (category, count, revenue) in enumerate(category_stats):
                Label(
                    category_frame,
                    text=f"{category}: {count} orders - {revenue:.2f} EGP",
                    font=("Arial", 11),
                    bg=COLORS["light"],
                    fg=COLORS["dark"],
                ).pack(anchor=W, padx=10, pady=2)

            # Daily statistics
            Label(
                content_frame,
                text="📅 Daily Sales (Last 7 Days)",
                font=("Arial", 14, "bold"),
                bg=COLORS["white"],
                fg=COLORS["primary"],
            ).pack(pady=(0, 10))

            daily_frame = Frame(content_frame, bg=COLORS["light"], relief=RAISED, bd=1)
            daily_frame.pack(fill=X, ipady=10)

            for date, orders, revenue in daily_stats:
                Label(
                    daily_frame,
                    text=f"{date}: {orders} orders - {revenue:.2f} EGP",
                    font=("Arial", 11),
                    bg=COLORS["light"],
                    fg=COLORS["dark"],
                ).pack(anchor=W, padx=10, pady=2)

            # Close button
            Button(
                content_frame,
                text="✅ Close Report",
                command=report_window.destroy,
                font=("Arial", 12, "bold"),
                bg=COLORS["secondary"],
                fg=COLORS["white"],
                relief=FLAT,
                cursor="hand2",
                width=15,
            ).pack(pady=20, ipady=8)

        except sqlite3.Error as e:
            messagebox.showerror("Database Error", f"An error occurred: {e}")

    def darken_color(self, color):
        color_map = {
            COLORS["success"]: "#1E8449",
            COLORS["secondary"]: "#2980B9",
            COLORS["danger"]: "#C0392B",
            COLORS["dark"]: "#1B2631",
        }
        return color_map.get(color, color)

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    app = OrdersView()
    app.run()
