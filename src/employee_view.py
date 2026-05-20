from tkinter import *
import os
import sqlite3
import sys
from tkinter import messagebox

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


class EmployeeView:
    def __init__(self, employee_id):
        self.employee_id = employee_id
        self.root = Tk()
        self.get_employee_details()
        self.setup_window()
        self.create_widgets()

    def get_employee_details(self):
        """Fetches employee details from the database using their ID."""
        try:
            conn = sqlite3.connect("gym_1.db")
            cur = conn.cursor()
            cur.execute(
                "SELECT full_name, job_title FROM employees WHERE employee_id=?",
                (self.employee_id,),
            )
            employee = cur.fetchone()
            conn.close()

            if employee:
                self.employee_name = employee[0]
                self.job_title = employee[1]
            else:
                messagebox.showerror(
                    "Authentication Error",
                    "Could not find details for the logged-in employee.",
                )
                sys.exit()

        except sqlite3.Error as e:
            messagebox.showerror("Database Error", f"An error occurred: {e}")
            sys.exit()

    def setup_window(self):
        self.root.title(f"💼 Employee Dashboard - {self.employee_name}")
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
        header_frame = Frame(self.root, bg=COLORS["primary"], height=120)
        header_frame.pack(fill=X)
        header_frame.pack_propagate(False)

        header_content = Frame(header_frame, bg=COLORS["primary"])
        header_content.pack(expand=True)

        Label(
            header_content,
            text=f"💼 Welcome, {self.employee_name}!",
            font=("Arial", 24, "bold"),
            bg=COLORS["primary"],
            fg=COLORS["white"],
        ).pack(pady=(15, 5))

        Label(
            header_content,
            text=f"Position: {self.job_title}",
            font=("Arial", 14),
            bg=COLORS["primary"],
            fg=COLORS["light"],
        ).pack()

        # Main content
        main_frame = Frame(self.root, bg=COLORS["light"])
        main_frame.pack(fill=BOTH, expand=True, padx=40, pady=40)

        # Welcome message
        welcome_frame = Frame(main_frame, bg=COLORS["white"], relief=RAISED, bd=2)
        welcome_frame.pack(fill=X, pady=(0, 30), ipady=20)

        Label(
            welcome_frame,
            text="🎯 Employee Dashboard",
            font=("Arial", 18, "bold"),
            bg=COLORS["white"],
            fg=COLORS["primary"],
        ).pack(pady=(0, 10))

        Label(
            welcome_frame,
            text="Access your daily tasks and member management tools",
            font=("Arial", 14),
            bg=COLORS["white"],
            fg=COLORS["dark"],
        ).pack()

        # Feature sections
        features_frame = Frame(main_frame, bg=COLORS["light"])
        features_frame.pack(fill=BOTH, expand=True)

        # Member Management section
        self.create_feature_section(
            features_frame,
            "👥 Member Management",
            [
                ("Register New Member", "python register_member.py", COLORS["success"]),
                (
                    "View & Search Members",
                    "python view_members_employee.py",
                    COLORS["secondary"],
                ),
            ],
            0,
            0,
        )

        # Product Management section
        self.create_feature_section(
            features_frame,
            "📦 Product Management",
            [
                (
                    "View Available Products",
                    "python view_products_employee.py",
                    COLORS["warning"],
                ),
                ("Product Catalog", "python product_catalog.py", COLORS["dark"]),
            ],
            0,
            1,
        )

        # Reports section
        self.create_feature_section(
            features_frame,
            "📊 Reports & Analytics",
            [
                ("Daily Reports", "python daily_reports.py", "#9B59B6"),
                ("Member Statistics", "python member_stats.py", "#E67E22"),
            ],
            1,
            0,
        )

        # Personal section
        self.create_feature_section(
            features_frame,
            "⚙️ Personal Settings",
            [
                ("Update Profile", "python update_profile.py", COLORS["primary"]),
                ("Change Password", "python change_password.py", COLORS["secondary"]),
            ],
            1,
            1,
        )

        # Logout section
        logout_frame = Frame(main_frame, bg=COLORS["light"])
        logout_frame.pack(pady=30)

        logout_btn = Button(
            logout_frame,
            text="🚪 Logout",
            command=self.logout,
            font=("Arial", 16, "bold"),
            bg=COLORS["danger"],
            fg=COLORS["white"],
            relief=FLAT,
            cursor="hand2",
            width=20,
            activebackground="#C0392B",
        )
        logout_btn.pack(ipady=12)

    def create_feature_section(self, parent, title, buttons, row, col):
        section_frame = Frame(parent, bg=COLORS["white"], relief=RAISED, bd=2)
        section_frame.grid(
            row=row, column=col, padx=15, pady=15, sticky="nsew", ipadx=20, ipady=20
        )

        # Configure grid weights
        parent.grid_rowconfigure(row, weight=1)
        parent.grid_columnconfigure(col, weight=1)

        # Section title
        Label(
            section_frame,
            text=title,
            font=("Arial", 16, "bold"),
            bg=COLORS["white"],
            fg=COLORS["primary"],
        ).pack(pady=(0, 20))

        # Buttons
        for btn_text, command, color in buttons:
            btn = Button(
                section_frame,
                text=btn_text,
                command=lambda cmd=command: self.execute_command(cmd),
                font=("Arial", 12, "bold"),
                bg=color,
                fg=COLORS["white"],
                relief=FLAT,
                cursor="hand2",
                width=25,
                activebackground=self.darken_color(color),
            )
            btn.pack(pady=8, ipady=10)

    def execute_command(self, command):
        """Execute system command with error handling"""
        try:
            os.system(command)
        except Exception as e:
            messagebox.showerror("Error", f"Could not execute command: {e}")

    def darken_color(self, color):
        # Simple color darkening
        color_map = {
            COLORS["success"]: "#1E8449",
            COLORS["secondary"]: "#2980B9",
            COLORS["warning"]: "#D68910",
            COLORS["dark"]: "#1B2631",
            COLORS["primary"]: "#1B2631",
            "#9B59B6": "#8E44AD",
            "#E67E22": "#D35400",
        }
        return color_map.get(color, color)

    def logout(self):
        """Destroys the current window and re-opens the login screen."""
        self.root.destroy()
        os.system("python login.py")

    def run(self):
        self.root.mainloop()


def main():
    # Startup Check: Get Employee ID
    try:
        if len(sys.argv) < 2:
            messagebox.showerror(
                "Access Error",
                "This page cannot be opened directly. Please log in first.",
            )
            sys.exit()

        employee_id = sys.argv[1]
        app = EmployeeView(employee_id)
        app.run()

    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")
        sys.exit()


if __name__ == "__main__":
    main()
