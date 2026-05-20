from tkinter import *
from tkinter import ttk
from tkinter import messagebox
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
}


class EmployeeManager:
    def __init__(self):
        self.root = Tk()
        self.setup_window()
        self.create_widgets()
        self.load_employees()

    def setup_window(self):
        self.root.title("👥 Employee Management - Admin Panel")
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
            text="👥 Employee Management",
            font=("Arial", 24, "bold"),
            bg=COLORS["primary"],
            fg=COLORS["white"],
        ).pack(pady=15)

        Label(
            header_content,
            text="Manage your gym staff efficiently",
            font=("Arial", 14),
            bg=COLORS["primary"],
            fg=COLORS["light"],
        ).pack()

        # Main content
        main_frame = Frame(self.root, bg=COLORS["light"])
        main_frame.pack(fill=BOTH, expand=True, padx=30, pady=30)

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

        buttons = [
            ("🔄 Refresh", self.load_employees, COLORS["secondary"]),
            ("🗑️ Delete Selected", self.delete_employee, COLORS["danger"]),
            ("🏠 Back to Admin Panel", self.go_back, COLORS["success"]),
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
                width=20,
                activebackground=self.darken_color(color),
            )
            btn.grid(row=0, column=i, padx=10, ipady=8)

        # Employee list
        list_frame = Frame(main_frame, bg=COLORS["white"], relief=RAISED, bd=2)
        list_frame.pack(fill=BOTH, expand=True, ipady=20)

        Label(
            list_frame,
            text="📋 Employee List",
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
        columns = ("ID", "Full Name", "Job Title", "Salary", "Hire Date")
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
            "ID": 80,
            "Full Name": 200,
            "Job Title": 150,
            "Salary": 120,
            "Hire Date": 150,
        }
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=column_widths[col], anchor=CENTER)

        # Pack treeview and scrollbars
        self.tree.grid(row=0, column=0, sticky="nsew")
        v_scrollbar.grid(row=0, column=1, sticky="ns")
        h_scrollbar.grid(row=1, column=0, sticky="ew")

        tree_container.grid_rowconfigure(0, weight=1)
        tree_container.grid_columnconfigure(0, weight=1)

    def load_employees(self):
        # Clear existing data
        for item in self.tree.get_children():
            self.tree.delete(item)

        try:
            conn = sqlite3.connect("gym_1.db")
            cur = conn.cursor()
            cur.execute(
                "SELECT employee_id, full_name, job_title, salary, hire_date FROM employees"
            )
            employees = cur.fetchall()
            conn.close()

            for emp in employees:
                self.tree.insert("", "end", values=emp)

        except sqlite3.Error as e:
            messagebox.showerror("Database Error", f"An error occurred: {e}")

    def delete_employee(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showerror("Error", "Please select an employee to delete.")
            return

        # Get employee info for confirmation
        employee_data = self.tree.item(selected_item, "values")
        employee_name = employee_data[1]

        if not messagebox.askyesno(
            "Confirm Delete",
            f"Are you sure you want to delete employee:\n{employee_name}?",
        ):
            return

        try:
            employee_id = employee_data[0]
            conn = sqlite3.connect("gym_1.db")
            cur = conn.cursor()
            cur.execute("DELETE FROM employees WHERE employee_id=?", (employee_id,))
            conn.commit()
            conn.close()

            messagebox.showinfo(
                "Success", f"Employee {employee_name} deleted successfully."
            )
            self.load_employees()

        except sqlite3.Error as e:
            messagebox.showerror("Database Error", f"An error occurred: {e}")

    def go_back(self):
        self.root.destroy()
        os.system("python admin_panel.py")

    def darken_color(self, color):
        color_map = {
            COLORS["secondary"]: "#2980B9",
            COLORS["danger"]: "#C0392B",
            COLORS["success"]: "#1E8449",
        }
        return color_map.get(color, color)

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    app = EmployeeManager()
    app.run()
