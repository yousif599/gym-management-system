from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import sqlite3
import os
from datetime import date, timedelta, datetime

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


class MemberViewEmployee:
    def __init__(self):
        self.root = Tk()
        self.setup_window()
        self.create_widgets()
        self.load_all_members()

    def setup_window(self):
        self.root.title("👥 Member Management - Employee Panel")
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
            text="👥 Member Management",
            font=("Arial", 24, "bold"),
            bg=COLORS["primary"],
            fg=COLORS["white"],
        ).pack(pady=15)

        Label(
            header_content,
            text="View, search and manage member subscriptions",
            font=("Arial", 14),
            bg=COLORS["primary"],
            fg=COLORS["light"],
        ).pack()

        # Main content
        main_frame = Frame(self.root, bg=COLORS["light"])
        main_frame.pack(fill=BOTH, expand=True, padx=30, pady=30)

        # Search section
        search_frame = Frame(main_frame, bg=COLORS["white"], relief=RAISED, bd=2)
        search_frame.pack(fill=X, pady=(0, 20), ipady=15)

        Label(
            search_frame,
            text="🔍 Search Members",
            font=("Arial", 16, "bold"),
            bg=COLORS["white"],
            fg=COLORS["primary"],
        ).pack(pady=(0, 10))

        search_controls = Frame(search_frame, bg=COLORS["white"])
        search_controls.pack()

        Label(
            search_controls,
            text="Search by Name:",
            font=("Arial", 12, "bold"),
            bg=COLORS["white"],
            fg=COLORS["dark"],
        ).grid(row=0, column=0, padx=10)

        self.search_entry = Entry(
            search_controls, font=("Arial", 12), width=30, relief=FLAT, bd=5
        )
        self.search_entry.grid(row=0, column=1, padx=10)
        self.search_entry.bind("<KeyRelease>", self.on_search_change)

        Button(
            search_controls,
            text="🔍 Search",
            command=self.search_members,
            font=("Arial", 12, "bold"),
            bg=COLORS["secondary"],
            fg=COLORS["white"],
            relief=FLAT,
            cursor="hand2",
        ).grid(row=0, column=2, padx=10, ipady=5)

        Button(
            search_controls,
            text="📋 Show All",
            command=self.load_all_members,
            font=("Arial", 12, "bold"),
            bg=COLORS["dark"],
            fg=COLORS["white"],
            relief=FLAT,
            cursor="hand2",
        ).grid(row=0, column=3, padx=10, ipady=5)

        # Statistics section
        stats_frame = Frame(main_frame, bg=COLORS["white"], relief=RAISED, bd=2)
        stats_frame.pack(fill=X, pady=(0, 20), ipady=15)

        Label(
            stats_frame,
            text="📊 Member Statistics",
            font=("Arial", 16, "bold"),
            bg=COLORS["white"],
            fg=COLORS["primary"],
        ).pack(pady=(0, 10))

        stats_content = Frame(stats_frame, bg=COLORS["white"])
        stats_content.pack()

        self.total_members_label = Label(
            stats_content,
            text="Total Members: 0",
            font=("Arial", 12, "bold"),
            bg=COLORS["white"],
            fg=COLORS["success"],
        )
        self.total_members_label.grid(row=0, column=0, padx=20)

        self.active_members_label = Label(
            stats_content,
            text="Active: 0",
            font=("Arial", 12, "bold"),
            bg=COLORS["white"],
            fg=COLORS["secondary"],
        )
        self.active_members_label.grid(row=0, column=1, padx=20)

        self.expired_members_label = Label(
            stats_content,
            text="Expired: 0",
            font=("Arial", 12, "bold"),
            bg=COLORS["white"],
            fg=COLORS["danger"],
        )
        self.expired_members_label.grid(row=0, column=2, padx=20)

        # Control buttons
        control_frame = Frame(main_frame, bg=COLORS["white"], relief=RAISED, bd=2)
        control_frame.pack(fill=X, pady=(0, 20), ipady=15)

        Label(
            control_frame,
            text="🎛️ Actions",
            font=("Arial", 16, "bold"),
            bg=COLORS["white"],
            fg=COLORS["primary"],
        ).pack(pady=(0, 10))

        button_frame = Frame(control_frame, bg=COLORS["white"])
        button_frame.pack()

        buttons = [
            ("🔄 Refresh", self.load_all_members, COLORS["secondary"]),
            ("🔄 Renew Subscription", self.open_renewal_window, COLORS["warning"]),
            ("📋 View Details", self.view_member_details, COLORS["success"]),
            ("🚪 Close", self.root.destroy, COLORS["danger"]),
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
                width=18,
                activebackground=self.darken_color(color),
            )
            btn.grid(row=0, column=i, padx=8, ipady=8)

        # Member list
        list_frame = Frame(main_frame, bg=COLORS["white"], relief=RAISED, bd=2)
        list_frame.pack(fill=BOTH, expand=True, ipady=20)

        Label(
            list_frame,
            text="📋 Member List",
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
            "ID",
            "Full Name",
            "Phone",
            "Subscription",
            "Start Date",
            "End Date",
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
            "ID": 60,
            "Full Name": 200,
            "Phone": 120,
            "Subscription": 120,
            "Start Date": 120,
            "End Date": 120,
            "Status": 100,
        }
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(
                col,
                width=column_widths[col],
                anchor=CENTER if col != "Full Name" else W,
            )

        # Pack treeview and scrollbars
        self.tree.grid(row=0, column=0, sticky="nsew")
        v_scrollbar.grid(row=0, column=1, sticky="ns")
        h_scrollbar.grid(row=1, column=0, sticky="ew")

        tree_container.grid_rowconfigure(0, weight=1)
        tree_container.grid_columnconfigure(0, weight=1)

    def load_all_members(self):
        """Loads all members into the Treeview"""
        self.search_entry.delete(0, END)
        for item in self.tree.get_children():
            self.tree.delete(item)

        try:
            conn = sqlite3.connect("gym_1.db")
            cur = conn.cursor()
            cur.execute(
                "SELECT member_id, full_name, phone, subscription_type, start_date, end_date FROM members"
            )
            members = cur.fetchall()
            conn.close()

            total_members = len(members)
            active_count = 0
            expired_count = 0

            for member in members:
                # Determine status
                try:
                    end_date = datetime.strptime(member[5], "%Y-%m-%d")
                    today = datetime.today()
                    status = "✅ Active" if end_date > today else "❌ Expired"
                    if end_date > today:
                        active_count += 1
                    else:
                        expired_count += 1
                except:
                    status = "❓ Unknown"

                member_with_status = member + (status,)
                self.tree.insert("", "end", values=member_with_status)

            # Update statistics
            self.total_members_label.config(text=f"Total Members: {total_members}")
            self.active_members_label.config(text=f"Active: {active_count}")
            self.expired_members_label.config(text=f"Expired: {expired_count}")

        except sqlite3.Error as e:
            messagebox.showerror("Database Error", f"An error occurred: {e}")

    def on_search_change(self, event=None):
        """Real-time search as user types"""
        if len(self.search_entry.get()) >= 2:  # Start searching after 2 characters
            self.search_members()
        elif len(self.search_entry.get()) == 0:
            self.load_all_members()

    def search_members(self):
        """Filters the member list based on the search term"""
        search_term = self.search_entry.get().strip()
        if not search_term:
            messagebox.showwarning("Search", "Please enter a name to search.")
            return

        for item in self.tree.get_children():
            self.tree.delete(item)

        try:
            conn = sqlite3.connect("gym_1.db")
            cur = conn.cursor()
            cur.execute(
                """
                SELECT member_id, full_name, phone, subscription_type, start_date, end_date 
                FROM members 
                WHERE full_name LIKE ? OR phone LIKE ?
            """,
                (f"%{search_term}%", f"%{search_term}%"),
            )
            members = cur.fetchall()
            conn.close()

            for member in members:
                # Determine status
                try:
                    end_date = datetime.strptime(member[5], "%Y-%m-%d")
                    today = datetime.today()
                    status = "✅ Active" if end_date > today else "❌ Expired"
                except:
                    status = "❓ Unknown"

                member_with_status = member + (status,)
                self.tree.insert("", "end", values=member_with_status)

        except sqlite3.Error as e:
            messagebox.showerror("Database Error", f"An error occurred: {e}")

    def calculate_end_date(self, start_date_str, sub_type):
        """Calculate end date based on subscription type"""
        start = datetime.strptime(start_date_str, "%Y-%m-%d").date()
        if sub_type == "1 Month":
            end = start + timedelta(days=30)
        elif sub_type == "3 Months":
            end = start + timedelta(days=90)
        elif sub_type == "1 Year":
            end = start + timedelta(days=365)
        else:
            end = start
        return end.strftime("%Y-%m-%d")

    def open_renewal_window(self):
        """Open renewal window for selected member"""
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showerror(
                "Error",
                "Please select a member from the list to renew their subscription.",
            )
            return

        member_values = self.tree.item(selected_item, "values")
        member_id = member_values[0]
        member_name = member_values[1]

        # Create renewal window
        renewal_window = Toplevel(self.root)
        renewal_window.title("🔄 Renew Subscription")
        renewal_window.geometry("600x500")
        renewal_window.configure(bg=COLORS["light"])
        renewal_window.resizable(False, False)
        renewal_window.transient(self.root)
        renewal_window.grab_set()

        # Center the window
        renewal_window.update_idletasks()
        x = (renewal_window.winfo_screenwidth() // 2) - (300)
        y = (renewal_window.winfo_screenheight() // 2) - (250)
        renewal_window.geometry(f"600x500+{x}+{y}")

        # Header
        header_frame = Frame(renewal_window, bg=COLORS["primary"], height=80)
        header_frame.pack(fill=X)
        header_frame.pack_propagate(False)

        Label(
            header_frame,
            text=f"🔄 Renewing Subscription",
            font=("Arial", 18, "bold"),
            bg=COLORS["primary"],
            fg=COLORS["white"],
        ).pack(pady=20)

        # Content
        content_frame = Frame(renewal_window, bg=COLORS["white"])
        content_frame.pack(fill=BOTH, expand=True, padx=20, pady=20)

        Label(
            content_frame,
            text=f"Member: {member_name}",
            font=("Arial", 16, "bold"),
            bg=COLORS["white"],
            fg=COLORS["primary"],
        ).pack(pady=(0, 20))

        # Subscription options
        Label(
            content_frame,
            text="Select New Subscription Type:",
            font=("Arial", 14, "bold"),
            bg=COLORS["white"],
            fg=COLORS["dark"],
        ).pack(pady=(0, 10))

        sub_type_var = StringVar(value="1 Month")

        # Radio buttons for subscription types
        options_frame = Frame(content_frame, bg=COLORS["white"])
        options_frame.pack(pady=10)

        subscription_options = [
            ("1 Month", "30 days - Perfect for trying out"),
            ("3 Months", "90 days - Great value for regular users"),
            ("1 Year", "365 days - Best value for committed members"),
        ]

        for option, description in subscription_options:
            option_frame = Frame(options_frame, bg=COLORS["light"], relief=RAISED, bd=1)
            option_frame.pack(fill=X, pady=5, padx=10, ipady=10)

            Radiobutton(
                option_frame,
                text=f"{option}",
                variable=sub_type_var,
                value=option,
                font=("Arial", 12, "bold"),
                bg=COLORS["light"],
                activebackground=COLORS["light"],
            ).pack(anchor=W)

            Label(
                option_frame,
                text=description,
                font=("Arial", 10),
                bg=COLORS["light"],
                fg=COLORS["dark"],
            ).pack(anchor=W, padx=20)

        # Buttons
        button_frame = Frame(content_frame, bg=COLORS["white"])
        button_frame.pack(pady=30)

        Button(
            button_frame,
            text="✅ Confirm Renewal",
            command=lambda: self.process_renewal(
                member_id, sub_type_var, renewal_window
            ),
            font=("Arial", 14, "bold"),
            bg=COLORS["success"],
            fg=COLORS["white"],
            relief=FLAT,
            cursor="hand2",
            width=18,
            activebackground="#1E8449",
        ).pack(side=LEFT, padx=10, ipady=10)

        Button(
            button_frame,
            text="❌ Cancel",
            command=renewal_window.destroy,
            font=("Arial", 14, "bold"),
            bg=COLORS["danger"],
            fg=COLORS["white"],
            relief=FLAT,
            cursor="hand2",
            width=15,
            activebackground="#C0392B",
        ).pack(side=LEFT, padx=10, ipady=10)

    def process_renewal(self, member_id, sub_type_var, window_to_close):
        """Process the subscription renewal"""
        new_sub_type = sub_type_var.get()
        new_start_date = date.today().strftime("%Y-%m-%d")
        new_end_date = self.calculate_end_date(new_start_date, new_sub_type)

        if messagebox.askyesno(
            "Confirm Renewal",
            f"Renew subscription for {new_sub_type}?\n\nNew Start Date: {new_start_date}\nNew End Date: {new_end_date}",
        ):
            try:
                conn = sqlite3.connect("gym_1.db")
                cur = conn.cursor()
                cur.execute(
                    """
                    UPDATE members 
                    SET subscription_type = ?, start_date = ?, end_date = ?
                    WHERE member_id = ?
                """,
                    (new_sub_type, new_start_date, new_end_date, member_id),
                )
                conn.commit()
                conn.close()

                messagebox.showinfo("Success", "🎉 Subscription renewed successfully!")
                window_to_close.destroy()
                self.load_all_members()

            except sqlite3.Error as e:
                messagebox.showerror("Database Error", f"An error occurred: {e}")

    def view_member_details(self):
        """View detailed information about selected member"""
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showerror("Error", "Please select a member to view details.")
            return

        member_data = self.tree.item(selected_item, "values")
        member_id = member_data[0]

        try:
            conn = sqlite3.connect("gym_1.db")
            cur = conn.cursor()
            cur.execute("SELECT * FROM members WHERE member_id=?", (member_id,))
            member = cur.fetchone()
            conn.close()

            if member:
                self.show_member_details(member)

        except sqlite3.Error as e:
            messagebox.showerror("Database Error", f"An error occurred: {e}")

    def show_member_details(self, member):
        """Show member details in a popup window"""
        details_window = Toplevel(self.root)
        details_window.title(f"👤 Member Details - {member[1]}")
        details_window.geometry("500x600")
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
            text=f"👤 {member[1]}",
            font=("Arial", 20, "bold"),
            bg=COLORS["primary"],
            fg=COLORS["white"],
        ).pack(pady=20)

        # Details content
        content_frame = Frame(details_window, bg=COLORS["white"])
        content_frame.pack(fill=BOTH, expand=True, padx=20, pady=20)

        details = [
            ("🆔 Member ID:", member[0]),
            ("👤 Full Name:", member[1]),
            ("🔑 Username:", member[2]),
            ("🎂 Age:", f"{member[4]} years"),
            ("⚧ Gender:", member[5]),
            ("📱 Phone:", member[6]),
            ("💳 Subscription Type:", member[7]),
            ("📅 Start Date:", member[8]),
            ("⏰ End Date:", member[9]),
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
                width=20,
                anchor=W,
            ).pack(side=LEFT, padx=10)

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

    def darken_color(self, color):
        color_map = {
            COLORS["secondary"]: "#2980B9",
            COLORS["warning"]: "#D68910",
            COLORS["success"]: "#1E8449",
            COLORS["danger"]: "#C0392B",
        }
        return color_map.get(color, color)

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    app = MemberViewEmployee()
    app.run()
