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


class EmployeeRegistration:
    def __init__(self):
        self.root = Tk()
        self.setup_window()
        self.create_widgets()

    def setup_window(self):
        self.root.title("👤 Register New Employee - Admin Panel")
        self.root.geometry("1620x1000")
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
            text="👤 Register New Employee",
            font=("Arial", 24, "bold"),
            bg=COLORS["primary"],
            fg=COLORS["white"],
        ).pack(pady=15)

        Label(
            header_content,
            text="Add a new team member to your gym",
            font=("Arial", 14),
            bg=COLORS["primary"],
            fg=COLORS["light"],
        ).pack()

        # Main form
        main_frame = Frame(self.root, bg=COLORS["light"])
        main_frame.pack(fill=BOTH, expand=True, padx=40, pady=40)

        # Form container
        form_frame = Frame(main_frame, bg=COLORS["white"], relief=RAISED, bd=2)
        form_frame.pack(fill=BOTH, expand=True, ipady=30)

        Label(
            form_frame,
            text="📝 Employee Information",
            font=("Arial", 18, "bold"),
            bg=COLORS["white"],
            fg=COLORS["primary"],
        ).pack(pady=(0, 30))

        # Form fields
        fields_frame = Frame(form_frame, bg=COLORS["white"])
        fields_frame.pack(padx=50)

        # Full Name
        self.create_field(fields_frame, "👤 Full Name:", 0)
        self.name_entry = Entry(
            fields_frame, font=("Arial", 14), width=30, relief=FLAT, bd=8
        )
        self.name_entry.grid(row=0, column=1, pady=10, padx=(20, 0), ipady=5)

        # Username
        self.create_field(fields_frame, "🔑 Username:", 1)
        self.username_entry = Entry(
            fields_frame, font=("Arial", 14), width=30, relief=FLAT, bd=8
        )
        self.username_entry.grid(row=1, column=1, pady=10, padx=(20, 0), ipady=5)

        # Password
        self.create_field(fields_frame, "🔒 Password:", 2)
        self.password_entry = Entry(
            fields_frame, font=("Arial", 14), width=30, show="*", relief=FLAT, bd=8
        )
        self.password_entry.grid(row=2, column=1, pady=10, padx=(20, 0), ipady=5)

        # Job Title
        self.create_field(fields_frame, "💼 Job Title:", 3)
        self.job_entry = Entry(
            fields_frame, font=("Arial", 14), width=30, relief=FLAT, bd=8
        )
        self.job_entry.grid(row=3, column=1, pady=10, padx=(20, 0), ipady=5)

        # Salary
        self.create_field(fields_frame, "💰 Salary (EGP):", 4)
        self.salary_entry = Entry(
            fields_frame, font=("Arial", 14), width=30, relief=FLAT, bd=8
        )
        self.salary_entry.grid(row=4, column=1, pady=10, padx=(20, 0), ipady=5)

        # Hire Date
        self.create_field(fields_frame, "📅 Hire Date:", 5)
        hire_frame = Frame(fields_frame, bg=COLORS["white"])
        hire_frame.grid(row=5, column=1, pady=10, padx=(20, 0), sticky=W)

        self.hire_entry = Entry(
            hire_frame, font=("Arial", 14), width=20, relief=FLAT, bd=8
        )
        self.hire_entry.pack(side=LEFT, ipady=5)

        today_btn = Button(
            hire_frame,
            text="Today",
            command=self.set_today,
            font=("Arial", 10),
            bg=COLORS["secondary"],
            fg=COLORS["white"],
            relief=FLAT,
            cursor="hand2",
        )
        today_btn.pack(side=LEFT, padx=(10, 0), ipady=3)

        # Format hint
        Label(
            fields_frame,
            text="(YYYY-MM-DD format)",
            font=("Arial", 10),
            bg=COLORS["white"],
            fg=COLORS["dark"],
        ).grid(row=6, column=1, sticky=W, padx=(20, 0))

        # Buttons
        button_frame = Frame(form_frame, bg=COLORS["white"])
        button_frame.pack(pady=40)

        register_btn = Button(
            button_frame,
            text="✅ Register Employee",
            command=self.register_employee,
            font=("Arial", 16, "bold"),
            bg=COLORS["success"],
            fg=COLORS["white"],
            relief=FLAT,
            cursor="hand2",
            width=20,
            activebackground="#1E8449",
        )
        register_btn.pack(side=LEFT, padx=10, ipady=12)

        cancel_btn = Button(
            button_frame,
            text="❌ Cancel",
            command=self.root.destroy,
            font=("Arial", 16, "bold"),
            bg=COLORS["danger"],
            fg=COLORS["white"],
            relief=FLAT,
            cursor="hand2",
            width=15,
            activebackground="#C0392B",
        )
        cancel_btn.pack(side=LEFT, padx=10, ipady=12)

    def create_field(self, parent, text, row):
        Label(
            parent,
            text=text,
            font=("Arial", 14, "bold"),
            bg=COLORS["white"],
            fg=COLORS["dark"],
            width=15,
            anchor=W,
        ).grid(row=row, column=0, pady=10, sticky=W)

    def set_today(self):
        today = datetime.today().strftime("%Y-%m-%d")
        self.hire_entry.delete(0, END)
        self.hire_entry.insert(0, today)

    def register_employee(self):
        # Get all field values
        name = self.name_entry.get().strip()
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()
        job = self.job_entry.get().strip()
        salary = self.salary_entry.get().strip()
        hire_date = self.hire_entry.get().strip()

        # Validation
        if not all([name, username, password, job, salary, hire_date]):
            messagebox.showerror("Error", "All fields are required!")
            return

        # Validate salary
        try:
            salary_float = float(salary)
            if salary_float <= 0:
                raise ValueError("Salary must be positive")
        except ValueError:
            messagebox.showerror(
                "Invalid Input", "Please enter a valid salary (positive number)."
            )
            return

        # Validate date format
        try:
            datetime.strptime(hire_date, "%Y-%m-%d")
        except ValueError:
            messagebox.showerror(
                "Invalid Date", "Please enter date in YYYY-MM-DD format."
            )
            return

        # Save to database
        try:
            conn = sqlite3.connect("gym_1.db")
            cur = conn.cursor()
            cur.execute(
                """
                INSERT INTO employees (full_name, username, password, job_title, salary, hire_date)
                VALUES (?, ?, ?, ?, ?, ?)
            """,
                (name, username, password, job, salary_float, hire_date),
            )
            conn.commit()
            conn.close()

            messagebox.showinfo(
                "Success", f"Employee '{name}' registered successfully! 🎉"
            )

            # Ask if user wants to register another employee
            if messagebox.askyesno(
                "Continue?", "Do you want to register another employee?"
            ):
                self.clear_form()
            else:
                self.root.destroy()

        except sqlite3.IntegrityError:
            messagebox.showerror(
                "Error", "Username already exists! Please choose a different username."
            )
        except sqlite3.Error as e:
            messagebox.showerror("Database Error", f"An error occurred: {e}")

    def clear_form(self):
        """Clear all form fields"""
        self.name_entry.delete(0, END)
        self.username_entry.delete(0, END)
        self.password_entry.delete(0, END)
        self.job_entry.delete(0, END)
        self.salary_entry.delete(0, END)
        self.hire_entry.delete(0, END)
        self.name_entry.focus()

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    app = EmployeeRegistration()
    app.run()
