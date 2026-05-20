from tkinter import *
from tkinter import messagebox
from tkinter import ttk
import sqlite3
from datetime import datetime

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


def open_member_home(member_id):
    class MemberHome:
        def __init__(self, member_id):
            self.member_id = member_id
            self.root = Tk()
            self.setup_window()
            self.setup_database()
            self.get_member_info()
            self.create_widgets()

        def setup_window(self):
            self.root.title("🏋️ Member Dashboard - Gym Management System")
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

        def setup_database(self):
            self.conn = sqlite3.connect("gym_1.db")
            self.cur = self.conn.cursor()

        def get_member_info(self):
            self.cur.execute(
                "SELECT * FROM members WHERE member_id=?", (self.member_id,)
            )
            self.member = self.cur.fetchone()
            if not self.member:
                messagebox.showerror("Error", "Member not found.")
                self.root.destroy()
                return

        def create_widgets(self):
            # Header
            header_frame = Frame(self.root, bg=COLORS["primary"], height=120)
            header_frame.pack(fill=X)
            header_frame.pack_propagate(False)

            header_content = Frame(header_frame, bg=COLORS["primary"])
            header_content.pack(expand=True)

            Label(
                header_content,
                text=f"🏋️ Welcome, {self.member[1]}!",
                font=("Arial", 24, "bold"),
                bg=COLORS["primary"],
                fg=COLORS["white"],
            ).pack(pady=(15, 5))

            Label(
                header_content,
                text=f"Subscription: {self.member[7]} | Valid until: {self.member[9]}",
                font=("Arial", 14),
                bg=COLORS["primary"],
                fg=COLORS["light"],
            ).pack()

            # Main content
            main_frame = Frame(self.root, bg=COLORS["light"])
            main_frame.pack(fill=BOTH, expand=True, padx=30, pady=30)

            # Left side - Member info
            left_frame = Frame(main_frame, bg=COLORS["white"], relief=RAISED, bd=2)
            left_frame.pack(side=LEFT, fill=Y, padx=(0, 15), ipadx=20, ipady=20)

            Label(
                left_frame,
                text="📋 Member Information",
                font=("Arial", 16, "bold"),
                bg=COLORS["white"],
                fg=COLORS["primary"],
            ).pack(pady=(0, 20))

            info_data = [
                ("👤 Full Name:", self.member[1]),
                ("📧 Username:", self.member[2]),
                ("🎂 Age:", f"{self.member[4]} years"),
                ("⚧ Gender:", self.member[5]),
                ("📱 Phone:", self.member[6]),
                ("💳 Subscription:", self.member[7]),
                ("📅 Start Date:", self.member[8]),
                ("⏰ End Date:", self.member[9]),
            ]

            for label, value in info_data:
                info_frame = Frame(left_frame, bg=COLORS["white"])
                info_frame.pack(fill=X, pady=5)

                Label(
                    info_frame,
                    text=label,
                    font=("Arial", 12, "bold"),
                    bg=COLORS["white"],
                    fg=COLORS["dark"],
                    width=15,
                    anchor=W,
                ).pack(side=LEFT)

                Label(
                    info_frame,
                    text=str(value),
                    font=("Arial", 12),
                    bg=COLORS["white"],
                    fg=COLORS["primary"],
                ).pack(side=LEFT, padx=(10, 0))

            # Right side - Products
            right_frame = Frame(main_frame, bg=COLORS["white"], relief=RAISED, bd=2)
            right_frame.pack(
                side=RIGHT, fill=BOTH, expand=True, padx=(15, 0), ipadx=20, ipady=20
            )

            Label(
                right_frame,
                text="🛒 Available Products",
                font=("Arial", 16, "bold"),
                bg=COLORS["white"],
                fg=COLORS["primary"],
            ).pack(pady=(0, 20))

            # Products container with scrollbar
            products_container = Frame(right_frame, bg=COLORS["white"])
            products_container.pack(fill=BOTH, expand=True)

            # Scrollable frame
            canvas = Canvas(products_container, bg=COLORS["white"])
            scrollbar = ttk.Scrollbar(
                products_container, orient="vertical", command=canvas.yview
            )
            self.products_frame = Frame(canvas, bg=COLORS["white"])

            self.products_frame.bind(
                "<Configure>",
                lambda e: canvas.configure(scrollregion=canvas.bbox("all")),
            )

            canvas.create_window((0, 0), window=self.products_frame, anchor="nw")
            canvas.configure(yscrollcommand=scrollbar.set)

            canvas.pack(side="left", fill="both", expand=True)
            scrollbar.pack(side="right", fill="y")

            self.load_products()

            # Logout button
            logout_frame = Frame(self.root, bg=COLORS["light"])
            logout_frame.pack(pady=20)

            logout_btn = Button(
                logout_frame,
                text="🚪 Logout",
                command=self.logout,
                font=("Arial", 14, "bold"),
                bg=COLORS["danger"],
                fg=COLORS["white"],
                relief=FLAT,
                cursor="hand2",
                width=20,
                activebackground="#C0392B",
            )
            logout_btn.pack(ipady=10)

        def load_products(self):
            self.cur.execute("SELECT * FROM products")
            products = self.cur.fetchall()

            for i, product in enumerate(products):
                product_frame = Frame(
                    self.products_frame, bg=COLORS["light"], relief=RAISED, bd=1
                )
                product_frame.pack(fill=X, pady=5, padx=10, ipady=10)

                # Product info
                info_frame = Frame(product_frame, bg=COLORS["light"])
                info_frame.pack(side=LEFT, fill=X, expand=True, padx=10)

                Label(
                    info_frame,
                    text=product[1],
                    font=("Arial", 14, "bold"),
                    bg=COLORS["light"],
                    fg=COLORS["primary"],
                    anchor=W,
                ).pack(fill=X)

                Label(
                    info_frame,
                    text=f"Category: {product[3]}",
                    font=("Arial", 11),
                    bg=COLORS["light"],
                    fg=COLORS["dark"],
                    anchor=W,
                ).pack(fill=X)

                Label(
                    info_frame,
                    text=f"Price: {product[2]} EGP",
                    font=("Arial", 12, "bold"),
                    bg=COLORS["light"],
                    fg=COLORS["success"],
                    anchor=W,
                ).pack(fill=X)

                # Buy button
                buy_btn = Button(
                    product_frame,
                    text="🛒 Buy Now",
                    command=lambda p_id=product[0]: self.place_order(p_id),
                    font=("Arial", 12, "bold"),
                    bg=COLORS["success"],
                    fg=COLORS["white"],
                    relief=FLAT,
                    cursor="hand2",
                    activebackground="#1E8449",
                )
                buy_btn.pack(side=RIGHT, padx=10, ipady=5, ipadx=10)

        def place_order(self, product_id):
            try:
                order_date = datetime.today().strftime("%Y-%m-%d")
                self.cur.execute(
                    "INSERT INTO orders (member_id, product_id, order_date) VALUES (?, ?, ?)",
                    (self.member_id, product_id, order_date),
                )
                self.conn.commit()
                messagebox.showinfo("Success", "🎉 Product purchased successfully!")
            except Exception as e:
                messagebox.showerror("Error", f"An error occurred: {str(e)}")

        def logout(self):
            self.conn.close()
            self.root.destroy()
            import os

            os.system("python login.py")

        def run(self):
            self.root.mainloop()

    app = MemberHome(member_id)
    app.run()
