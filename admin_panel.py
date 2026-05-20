from tkinter import *
from tkinter import ttk
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
}


class AdminPanel:
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
        # Header
        header_frame = Frame(self.root, bg=COLORS["primary"], height=112)
        header_frame.pack(fill=X)
        header_frame.pack_propagate(False)

        header_content = Frame(header_frame, bg=COLORS["primary"])
        header_content.pack(expand=True)

        Label(
            header_content,
            text="👑 Admin Dashboard",
            font=("Arial", 28, "bold"),
            bg=COLORS["primary"],
            fg=COLORS["white"],
        ).pack(pady=20)

        Label(
            header_content,
            text="Complete control over your gym management system",
            font=("Arial", 14),
            bg=COLORS["primary"],
            fg=COLORS["light"],
        ).pack()

        # Main content
        main_frame = Frame(self.root, bg=COLORS["light"])
        main_frame.pack(fill=BOTH, expand=True, padx=40, pady=40)

        # Management sections
        self.create_management_section(
            main_frame,
            "👥 Staff Management",
            [
                (
                    "📌 Add New Employee",
                    "python register_employee.py",
                    COLORS["secondary"],
                ),
                (
                    "🎮 Manage Employees",
                    "python manage_employees.py",
                    COLORS["primary"],
                ),
            ],
            0,
            0,
        )

        self.create_management_section(
            main_frame,
            "🏋️ Member Management",
            [
                ("🎮 Manage Members", "python manage_members.py", COLORS["success"]),
                ("📝 Member Reports", "python member_reports.py", COLORS["dark"]),
            ],
            0,
            1,
        )

        self.create_management_section(
            main_frame,
            "📦 Product Management",
            [
                ("🎮 Manage Products", "python manage_products.py", COLORS["warning"]),
                (
                    "📃 Inventory Reports",
                    "python inventory_reports.py",
                    COLORS["secondary"],
                ),
            ],
            1,
            0,
        )

        self.create_management_section(
            main_frame,
            "📊 Sales & Analytics",
            [
                ("💰 View Orders & Sales", "python view_orders.py", "#9B59B6"),
                ("📰 Financial Reports", "python financial_reports.py", "#E67E22"),
            ],
            1,
            1,
        )

        # Logout section
        logout_frame = Frame(main_frame, bg=COLORS["light"])
        logout_frame.grid(row=2, column=0, columnspan=2, pady=40)

        logout_btn = Button(
            logout_frame,
            text="🚪 Logout",
            command=self.logout,
            font=("Arial", 16, "bold"),
            bg=COLORS["danger"],
            fg=COLORS["white"],
            relief=RAISED,
            cursor="hand2",
            width=20,
            activebackground="#C0392B",
        )
        logout_btn.pack(ipady=10)

    def create_management_section(self, parent, title, buttons, row, col):
        section_frame = Frame(parent, bg=COLORS["white"], relief=RAISED, bd=2)
        section_frame.grid(
            row=row, column=col, padx=20, pady=20, sticky="nsew", ipadx=20, ipady=20
        )

        # Configure grid weights
        parent.grid_rowconfigure(row, weight=1)
        parent.grid_columnconfigure(col, weight=1)

        # Section title
        Label(
            section_frame,
            text=title,
            font=("Arial", 18, "bold"),
            bg=COLORS["white"],
            fg=COLORS["primary"],
        ).pack(pady=(0, 20))

        # Buttons
        for btn_text, command, color in buttons:
            btn = Button(
                section_frame,
                text=btn_text,
                command=lambda cmd=command: os.system(cmd),
                font=("Arial", 14, "bold"),
                bg=color,
                fg=COLORS["white"],
                relief=FLAT,
                cursor="hand2",
                width=25,
                activebackground=self.darken_color(color),
            )
            btn.pack(pady=10, ipady=12)

    def darken_color(self, color):
        # Simple color darkening (you can improve this)
        color_map = {
            COLORS["secondary"]: "#2980B9",
            COLORS["primary"]: "#1B2631",
            COLORS["success"]: "#1E8449",
            COLORS["warning"]: "#D68910",
            COLORS["dark"]: "#2C3E50",
            "#9B59B6": "#8E44AD",
            "#E67E22": "#D35400",
        }
        return color_map.get(color, color)

    def logout(self):
        self.root.destroy()
        os.system("python login.py")

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    app = AdminPanel()
    app.run()
