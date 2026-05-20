from tkinter import *
from tkinter import ttk
from tkinter import messagebox
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


class MemberManager:
    def __init__(self):
        self.root = Tk()
        self.setup_window()
        self.create_widgets()
        self.load_members()

    def setup_window(self):
        self.root.title("🏋️ Member Management - Admin Panel")
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
            text="🏋️ Member Management",
            font=("Arial", 24, "bold"),
            bg=COLORS["primary"],
            fg=COLORS["white"],
        ).pack(pady=15)

        Label(
            header_content,
            text="Manage your gym members efficiently",
            font=("Arial", 14),
            bg=COLORS["primary"],
            fg=COLORS["light"],
        ).pack()

        # Main content
        main_frame = Frame(self.root, bg=COLORS["light"])
        main_frame.pack(fill=BOTH, expand=True, padx=30, pady=30)

        # Search and filter section
        search_frame = Frame(main_frame, bg=COLORS["white"], relief=RAISED, bd=2)
        search_frame.pack(fill=X, pady=(0, 20), ipady=15)

        Label(
            search_frame,
            text="🔍 Search & Filter",
            font=("Arial", 16, "bold"),
            bg=COLORS["white"],
            fg=COLORS["primary"],
        ).pack(pady=(0, 10))

        search_controls = Frame(search_frame, bg=COLORS["white"])
        search_controls.pack()

        Label(
            search_controls,
            text="Search:",
            font=("Arial", 12, "bold"),
            bg=COLORS["white"],
            fg=COLORS["dark"],
        ).grid(row=0, column=0, padx=10)

        self.search_entry = Entry(
            search_controls, font=("Arial", 12), width=30, relief=FLAT, bd=5
        )
        self.search_entry.grid(row=0, column=1, padx=10)
        self.search_entry.bind("<KeyRelease>", self.search_members)

        Button(
            search_controls,
            text="🔄 Reset",
            command=self.reset_search,
            font=("Arial", 10, "bold"),
            bg=COLORS["secondary"],
            fg=COLORS["white"],
            relief=FLAT,
            cursor="hand2",
        ).grid(row=0, column=2, padx=10)

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
            ("🔄 Refresh", self.load_members, COLORS["secondary"]),
            ("🗑️ Delete Selected", self.delete_member, COLORS["danger"]),
            ("📊 View Details", self.view_member_details, COLORS["success"]),
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
            btn.grid(row=0, column=i, padx=10, ipady=8)

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
        columns = ("ID", "Full Name", "Phone", "Subscription", "End Date", "Status")
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
            "Phone": 150,
            "Subscription": 120,
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

        # Store original data for searching
        self.original_data = []

    def load_members(self):
        # Clear existing data
        for item in self.tree.get_children():
            self.tree.delete(item)

        try:
            conn = sqlite3.connect("gym_1.db")
            cur = conn.cursor()
            cur.execute(
                "SELECT member_id, full_name, phone, subscription_type, end_date FROM members"
            )
            members = cur.fetchall()
            conn.close()

            self.original_data = []
            for member in members:
                # Determine status based on end date
                from datetime import datetime

                try:
                    end_date = datetime.strptime(member[4], "%Y-%m-%d")
                    today = datetime.today()
                    status = "Active" if end_date > today else "Expired"
                except:
                    status = "Unknown"

                member_with_status = member + (status,)
                self.original_data.append(member_with_status)
                self.tree.insert("", "end", values=member_with_status)

        except sqlite3.Error as e:
            messagebox.showerror("Database Error", f"An error occurred: {e}")

    def search_members(self, event=None):
        search_term = self.search_entry.get().lower()

        # Clear current items
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Filter and display matching members
        for member in self.original_data:
            if (
                search_term in member[1].lower()  # Full name
                or search_term in member[2].lower()  # Phone
                or search_term in member[3].lower()
            ):  # Subscription type
                self.tree.insert("", "end", values=member)

    def reset_search(self):
        self.search_entry.delete(0, END)
        self.load_members()

    def delete_member(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showerror("Error", "Please select a member to delete.")
            return

        # Get member info for confirmation
        member_data = self.tree.item(selected_item, "values")
        member_name = member_data[1]

        if not messagebox.askyesno(
            "Confirm Delete",
            f"Are you sure you want to delete member:\n{member_name}?\n\nThis action cannot be undone.",
        ):
            return

        try:
            member_id = member_data[0]
            conn = sqlite3.connect("gym_1.db")
            cur = conn.cursor()
            cur.execute("DELETE FROM members WHERE member_id=?", (member_id,))
            conn.commit()
            conn.close()

            messagebox.showinfo(
                "Success", f"Member '{member_name}' deleted successfully."
            )
            self.load_members()

        except sqlite3.Error as e:
            messagebox.showerror("Database Error", f"An error occurred: {e}")

    def view_member_details(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showerror("Error", "Please select a member to view details.")
            return

        member_data = self.tree.item(selected_item, "values")
        member_id = member_data[0]

        # Get full member details
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
        # Create details window
        details_window = Toplevel(self.root)
        details_window.title(f"Member Details - {member[1]}")
        details_window.geometry("500x600")
        details_window.configure(bg=COLORS["light"])
        details_window.resizable(False, False)

        # Center the window
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

        for i, (label, value) in enumerate(details):
            detail_frame = Frame(content_frame, bg=COLORS["white"])
            detail_frame.pack(fill=X, pady=8)

            Label(
                detail_frame,
                text=label,
                font=("Arial", 12, "bold"),
                bg=COLORS["white"],
                fg=COLORS["dark"],
                width=20,
                anchor=W,
            ).pack(side=LEFT)

            Label(
                detail_frame,
                text=str(value),
                font=("Arial", 12),
                bg=COLORS["white"],
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
            COLORS["danger"]: "#C0392B",
            COLORS["success"]: "#1E8449",
        }
        return color_map.get(color, color)

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    app = MemberManager()
    app.run()
