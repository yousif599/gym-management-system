from tkinter import *
from tkinter import messagebox
from tkinter import ttk
import sqlite3
import os

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
    "gradient_start": "#667eea",
    "gradient_end": "#764ba2",
}


class ModernLogin:
    def __init__(self):
        self.root = Tk()
        self.setup_window()
        self.create_widgets()

    def setup_window(self):
        self.root.title("🏋️ Gym Management System - Login")
        self.root.configure(bg=COLORS["primary"])
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        self.root.geometry(f"{screen_width}x{screen_height}+0+0")
        # self.root.resizable(False, False)

    def center_window(self):
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f"{width}x{height}+{x}+{y}")

    def create_widgets(self):
        # Main container
        main_frame = Frame(self.root, bg=COLORS["primary"])
        # fill يمتد افقي و راسي
        # expand يملئ مساحه الشاشه
        main_frame.pack(fill=BOTH, expand=True)

        # Left side - Welcome section
        left_frame = Frame(main_frame, bg=COLORS["primary"], width=600)
        left_frame.pack(side=LEFT, fill=BOTH, expand=True, padx=40, pady=40)
        # بتلغي تكيف الاطار مع العناصر الي جواه
        left_frame.pack_propagate(False)

        # Welcome content
        welcome_frame = Frame(left_frame, bg=COLORS["primary"])
        welcome_frame.pack(expand=True)

        Label(
            welcome_frame,
            text="🏋️",
            font=("Arial", 80),
            bg=COLORS["primary"],
            fg=COLORS["secondary"],
        ).pack(pady=(100, 30))

        Label(
            welcome_frame,
            text="Gym Management",
            font=("Arial", 36, "bold"),
            bg=COLORS["primary"],
            fg=COLORS["white"],
        ).pack(pady=(0, 10))

        Label(
            welcome_frame,
            text="System",
            font=("Arial", 36, "bold"),
            bg=COLORS["primary"],
            fg=COLORS["secondary"],
        ).pack(pady=(0, 30))

        Label(
            welcome_frame,
            text="Manage your gym operations efficiently\nwith our comprehensive system",
            font=("Arial", 16),
            bg=COLORS["primary"],
            fg=COLORS["light"],
            justify=CENTER,
        ).pack(pady=(0, 40))

        # Features list
        features = [
            "👥 Member Management",
            "💼 Employee Management",
            "📦 Product Management",
            "📊 Sales Tracking",
        ]
        for feature in features:
            Label(
                welcome_frame,
                text=feature,
                font=("Arial", 14),
                bg=COLORS["primary"],
                fg=COLORS["light"],
                anchor=W,  # يثبت النص علي الشمال
            ).pack(pady=5, fill=X)

        # Right side - Login form
        right_frame = Frame(main_frame, bg=COLORS["white"], width=600)
        right_frame.pack(side=RIGHT, fill=BOTH, padx=40, pady=40)
        right_frame.pack_propagate(False)

        # Login form container
        form_container = Frame(right_frame, bg=COLORS["white"])
        form_container.pack(expand=True)

        # Login header
        Label(
            form_container,
            text="Welcome Back!",
            font=("Arial", 28, "bold"),
            bg=COLORS["white"],
            fg=COLORS["primary"],
        ).pack(pady=(40, 10))

        Label(
            form_container,
            text="Please sign in to your account",
            font=("Arial", 14),
            bg=COLORS["white"],
            fg=COLORS["dark"],
        ).pack(pady=(0, 40))

        # Username field
        Label(
            form_container,
            text="Username",
            font=("Arial", 12, "bold"),
            bg=COLORS["white"],
            fg=COLORS["dark"],
        ).pack(anchor=W, padx=40)

        username_frame = Frame(form_container, bg=COLORS["white"])
        username_frame.pack(pady=(5, 20), padx=40, fill=X)

        self.username_entry = Entry(
            username_frame, font=("Arial", 14), relief=RAISED, bd=10, bg=COLORS["light"]
        )  # زر  حدود بارزة RAISED
        self.username_entry.pack(fill=X, ipady=10)

        # Password field
        Label(
            form_container,
            text="Password",
            font=("Arial", 12, "bold"),
            bg=COLORS["white"],
            fg=COLORS["dark"],
        ).pack(anchor=W, padx=40)

        password_frame = Frame(form_container, bg=COLORS["white"])
        password_frame.pack(pady=(5, 30), padx=40, fill=X)

        self.password_entry = Entry(
            password_frame,
            font=("Arial", 14),
            show="*",
            relief=RAISED,
            bd=10,
            bg=COLORS["light"],
        )
        self.password_entry.pack(side=LEFT, fill=X, expand=True, ipady=10)

        self.show_btn = Button(
            password_frame,
            text="👁️",
            command=self.toggle_password,
            relief=RAISED,
            bg=COLORS["light"],
            font=("Arial", 12),
            cursor="hand2",
        )
        self.show_btn.pack(side=LEFT, padx=(7, 0))

        # Login button
        login_btn = Button(
            form_container,
            text="Sign In",
            command=self.login,
            font=("Arial", 14, "bold"),
            bg=COLORS["secondary"],
            fg=COLORS["white"],
            relief=RIDGE,
            cursor="hand2",
            activebackground=COLORS["primary"],
        )
        login_btn.pack(pady=20, padx=40, fill=X, ipady=12)

        # User type info
        info_frame = Frame(form_container, bg=COLORS["white"])
        info_frame.pack(pady=30, padx=40, fill=X)
        """
        Label(
            info_frame,
            text="Default Login Credentials:",
            font=("Arial", 12, "bold"),
            bg=COLORS["white"],
            fg=COLORS["dark"],
        ).pack()

        Label(
            info_frame,
            text="Admin: admin / admin123",
            font=("Arial", 10),
            bg=COLORS["white"],
            fg=COLORS["secondary"],
        ).pack(pady=2)

        Label(
            info_frame,
            text="Employee: ahmedk / 1234",
            font=("Arial", 10),
            bg=COLORS["white"],
            fg=COLORS["success"],
        ).pack(pady=2)

        Label(
            info_frame,
            text="Member: amar1 / 1234",
            font=("Arial", 10),
            bg=COLORS["white"],
            fg=COLORS["warning"],
        ).pack(pady=2)
        """
        # Bind Enter key
        self.root.bind("<Return>", lambda event: self.login())

    def toggle_password(self):
        if self.password_entry.cget("show") == "":
            self.password_entry.config(show="*")
            self.show_btn.config(text="👁️")
        else:
            self.password_entry.config(show="")
            self.show_btn.config(text="🙈")

    def login(self):
        user = self.username_entry.get().strip()
        pwd = self.password_entry.get().strip()

        if not user or not pwd:
            messagebox.showerror("Error", "Please enter both username and password")
            return

        try:
            conn = sqlite3.connect("gym_1.db")
            cur = conn.cursor()

            # Check Admin
            cur.execute(
                "SELECT * FROM admins WHERE username=? AND password=?", (user, pwd)
            )
            if cur.fetchone():
                conn.close()
                messagebox.showinfo("Success", "Welcome Admin! 👑")
                self.root.destroy()
                os.system("python admin_panel.py")
                return

            # Check Employee
            cur.execute(
                "SELECT employee_id FROM employees WHERE username=? AND password=?",
                (user, pwd),
            )
            employee = cur.fetchone()
            if employee:
                conn.close()
                messagebox.showinfo("Success", "Welcome Employee! 💼")
                self.root.destroy()
                os.system(f"python employee_view.py {employee[0]}")
                return

            # Check Member
            cur.execute(
                "SELECT member_id FROM members WHERE username=? AND password=?",
                (user, pwd),
            )
            member = cur.fetchone()
            if member:
                conn.close()
                messagebox.showinfo("Success", "Welcome Member! 🏋️")
                self.root.destroy()
                import member_home

                member_home.open_member_home(member[0])
                return

            conn.close()
            messagebox.showerror("Login Failed", "Invalid username or password")

        except sqlite3.Error as e:
            messagebox.showerror("Database Error", f"An error occurred: {e}")

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    app = ModernLogin()
    app.run()
