from tkinter import *
from tkinter import messagebox
from tkinter import ttk
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


class MemberRegistration:
    def __init__(self):
        self.root = Tk()
        self.setup_window()
        self.create_widgets()

    def setup_window(self):
        self.root.title("🏋️ Register New Member - Employee Panel")
        # Increased window size and made it resizable
        self.root.geometry("1000x900")
        self.root.minsize(900, 800)
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
        # Header - reduced height
        header_frame = Frame(self.root, bg=COLORS["primary"], height=80)
        header_frame.pack(fill=X)
        header_frame.pack_propagate(False)

        header_content = Frame(header_frame, bg=COLORS["primary"])
        header_content.pack(expand=True)

        Label(
            header_content,
            text="🏋️ Register New Member",
            font=("Arial", 20, "bold"),
            bg=COLORS["primary"],
            fg=COLORS["white"],
        ).pack(pady=(10, 5))

        Label(
            header_content,
            text="Add a new member to your gym community",
            font=("Arial", 12),
            bg=COLORS["primary"],
            fg=COLORS["light"],
        ).pack()

        # Main content with scrollable frame
        main_container = Frame(self.root, bg=COLORS["light"])
        main_container.pack(fill=BOTH, expand=True, padx=20, pady=15)

        # Create canvas and scrollbar for scrolling
        canvas = Canvas(main_container, bg=COLORS["light"], highlightthickness=0)
        scrollbar = Scrollbar(main_container, orient="vertical", command=canvas.yview)
        scrollable_frame = Frame(canvas, bg=COLORS["light"])

        # Configure scrollable frame to expand and center
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        # Create window in canvas and make it expand to full width
        canvas_window = canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        
        # Function to configure canvas window width
        def configure_canvas_window(event):
            canvas_width = event.width
            canvas.itemconfig(canvas_window, width=canvas_width)
        
        canvas.bind('<Configure>', configure_canvas_window)
        canvas.configure(yscrollcommand=scrollbar.set)

        # Pack canvas and scrollbar
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Form container - now will stretch full width
        form_frame = Frame(scrollable_frame, bg=COLORS["white"], relief=RAISED, bd=2)
        form_frame.pack(fill=BOTH, expand=True, padx=20, pady=15, ipady=25)

        Label(
            form_frame,
            text="📝 Member Information",
            font=("Arial", 16, "bold"),
            bg=COLORS["white"],
            fg=COLORS["primary"],
        ).pack(pady=(0, 25))

        # Create form in two columns - centered
        fields_container = Frame(form_frame, bg=COLORS["white"])
        fields_container.pack(expand=True)

        # Configure grid weights for centering
        fields_container.grid_columnconfigure(0, weight=1)
        fields_container.grid_columnconfigure(1, weight=1)

        # Left column
        left_column = Frame(fields_container, bg=COLORS["white"])
        left_column.grid(row=0, column=0, padx=30, sticky="nsew")

        # Right column
        right_column = Frame(fields_container, bg=COLORS["white"])
        right_column.grid(row=0, column=1, padx=30, sticky="nsew")

        # Left column fields
        self.create_field_section(
            left_column,
            "Personal Information",
            [
                ("👤 Full Name", "name"),
                ("🔑 Username", "username"),
                ("🔒 Password", "password"),
                ("🎂 Age", "age"),
            ],
        )

        # Right column fields
        self.create_field_section(
            right_column,
            "Contact & Subscription",
            [
                ("⚧ Gender", "gender"),
                ("📱 Phone Number", "phone"),
                ("💳 Subscription Type", "subscription"),
                ("📅 Start Date", "start_date"),
            ],
        )

        # Subscription preview - centered and full width
        preview_frame = Frame(form_frame, bg=COLORS["light"], relief=RAISED, bd=2)
        preview_frame.pack(fill=X, padx=40, pady=20, ipady=12)

        Label(
            preview_frame,
            text="📋 Subscription Preview",
            font=("Arial", 12, "bold"),
            bg=COLORS["light"],
            fg=COLORS["primary"],
        ).pack(pady=(0, 8))

        self.preview_label = Label(
            preview_frame,
            text="Select subscription type to see details",
            font=("Arial", 11),
            bg=COLORS["light"],
            fg=COLORS["dark"],
        )
        self.preview_label.pack()

        # Buttons - centered
        button_container = Frame(form_frame, bg=COLORS["white"])
        button_container.pack(pady=25)

        button_frame = Frame(button_container, bg=COLORS["white"])
        button_frame.pack()

        # Create buttons with consistent sizing
        btn_register = Button(
            button_frame,
            text="✅ Register Member",
            command=self.register_member,
            font=("Arial", 14, "bold"),
            bg=COLORS["success"],
            fg=COLORS["white"],
            relief=FLAT,
            cursor="hand2",
            width=18,
            height=2,
            activebackground="#1E8449",
        )
        btn_register.pack(side=LEFT, padx=12)

        btn_clear = Button(
            button_frame,
            text="🔄 Clear Form",
            command=self.clear_form,
            font=("Arial", 14, "bold"),
            bg=COLORS["warning"],
            fg=COLORS["white"],
            relief=FLAT,
            cursor="hand2",
            width=15,
            height=2,
            activebackground="#D68910",
        )
        btn_clear.pack(side=LEFT, padx=12)

        btn_cancel = Button(
            button_frame,
            text="❌ Cancel",
            command=self.root.destroy,
            font=("Arial", 14, "bold"),
            bg=COLORS["danger"],
            fg=COLORS["white"],
            relief=FLAT,
            cursor="hand2",
            width=15,
            height=2,
            activebackground="#C0392B",
        )
        btn_cancel.pack(side=LEFT, padx=12)

        # Bind mousewheel to canvas for scrolling
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        
        canvas.bind_all("<MouseWheel>", _on_mousewheel)

    def create_field_section(self, parent, section_title, fields):
        """Create a section of form fields"""
        # Section title
        Label(
            parent,
            text=section_title,
            font=("Arial", 13, "bold"),
            bg=COLORS["white"],
            fg=COLORS["secondary"],
        ).pack(pady=(0, 18))

        # Store entry widgets
        if not hasattr(self, "entries"):
            self.entries = {}

        for label_text, field_name in fields:
            # Field container
            field_frame = Frame(parent, bg=COLORS["white"])
            field_frame.pack(fill=X, pady=8)

            # Label
            Label(
                field_frame,
                text=label_text,
                font=("Arial", 11, "bold"),
                bg=COLORS["white"],
                fg=COLORS["dark"],
            ).pack(anchor=W)

            # Entry widget
            if field_name == "password":
                entry = Entry(
                    field_frame,
                    font=("Arial", 11),
                    width=32,
                    show="*",
                    relief=FLAT,
                    bd=5,
                    bg=COLORS["light"],
                )
            elif field_name == "gender":
                entry = ttk.Combobox(
                    field_frame,
                    font=("Arial", 11),
                    width=30,
                    values=["Male", "Female"],
                    state="readonly",
                )
                entry.set("Male")
            elif field_name == "subscription":
                entry = ttk.Combobox(
                    field_frame,
                    font=("Arial", 11),
                    width=30,
                    values=["1 Month", "3 Months", "1 Year"],
                    state="readonly",
                )
                entry.set("1 Month")
                entry.bind("<<ComboboxSelected>>", self.update_subscription_preview)
            elif field_name == "start_date":
                entry = Entry(
                    field_frame,
                    font=("Arial", 11),
                    width=32,
                    relief=FLAT,
                    bd=5,
                    bg=COLORS["light"],
                )
                entry.insert(0, datetime.today().strftime("%Y-%m-%d"))
            else:
                entry = Entry(
                    field_frame,
                    font=("Arial", 11),
                    width=32,
                    relief=FLAT,
                    bd=5,
                    bg=COLORS["light"],
                )

            entry.pack(pady=(4, 0), ipady=5)
            self.entries[field_name] = entry

    def update_subscription_preview(self, event=None):
        """Update subscription preview when type changes"""
        sub_type = self.entries["subscription"].get()
        start_date = self.entries["start_date"].get()

        try:
            end_date = self.calculate_end_date(start_date, sub_type)
            duration_map = {
                "1 Month": "30 days",
                "3 Months": "90 days",
                "1 Year": "365 days",
            }
            duration = duration_map.get(sub_type, "Unknown")

            preview_text = f"Duration: {duration}\nStart: {start_date}\nEnd: {end_date}"
            self.preview_label.config(text=preview_text)
        except:
            self.preview_label.config(text="Invalid start date format")

    def calculate_end_date(self, start_date_str, sub_type):
        """Calculate subscription end date"""
        start = datetime.strptime(start_date_str, "%Y-%m-%d")
        if sub_type == "1 Month":
            end = start + timedelta(days=30)
        elif sub_type == "3 Months":
            end = start + timedelta(days=90)
        elif sub_type == "1 Year":
            end = start + timedelta(days=365)
        else:
            end = start
        return end.strftime("%Y-%m-%d")

    def register_member(self):
        """Register new member"""
        # Get all field values
        values = {}
        for field_name, entry in self.entries.items():
            values[field_name] = entry.get().strip()

        # Validation
        required_fields = ["name", "username", "password", "age", "phone"]
        for field in required_fields:
            if not values[field]:
                messagebox.showerror("Error", f"Please fill in all required fields!")
                return

        # Validate age
        try:
            age = int(values["age"])
            if age < 16 or age > 100:
                raise ValueError("Age must be between 16 and 100")
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter a valid age (16-100).")
            return

        # Validate phone
        if len(values["phone"]) < 10:
            messagebox.showerror("Invalid Input", "Please enter a valid phone number.")
            return

        # Validate date format
        try:
            datetime.strptime(values["start_date"], "%Y-%m-%d")
        except ValueError:
            messagebox.showerror(
                "Invalid Date", "Please enter date in YYYY-MM-DD format."
            )
            return

        # Calculate end date
        end_date = self.calculate_end_date(values["start_date"], values["subscription"])

        # Save to database
        try:
            conn = sqlite3.connect("gym_1.db")
            cur = conn.cursor()
            cur.execute(
                """
                INSERT INTO members (full_name, username, password, age, gender, phone, 
                                   subscription_type, start_date, end_date)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
                (
                    values["name"],
                    values["username"],
                    values["password"],
                    age,
                    values["gender"],
                    values["phone"],
                    values["subscription"],
                    values["start_date"],
                    end_date,
                ),
            )
            conn.commit()
            conn.close()

            messagebox.showinfo(
                "Success",
                f"🎉 Member '{values['name']}' registered successfully!\n\nSubscription: {values['subscription']}\nValid until: {end_date}",
            )

            # Ask if user wants to register another member
            if messagebox.askyesno(
                "Continue?", "Do you want to register another member?"
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
        for field_name, entry in self.entries.items():
            if field_name == "gender":
                entry.set("Male")
            elif field_name == "subscription":
                entry.set("1 Month")
            elif field_name == "start_date":
                entry.delete(0, END)
                entry.insert(0, datetime.today().strftime("%Y-%m-%d"))
            else:
                entry.delete(0, END)

        self.preview_label.config(text="Select subscription type to see details")
        self.entries["name"].focus()

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    app = MemberRegistration()
    app.run()