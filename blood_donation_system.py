
import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector
from mysql.connector import Error
from datetime import datetime






DB_HOST = "localhost"
DB_USER = "root"
DB_PASSWORD = "932512"
DB_NAME = "blood_donation_db"


def get_server_connection():
    return mysql.connector.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD
    )


def get_db_connection():
    return mysql.connector.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME
    )


def setup_database():
    """Create database, tables and a demo login account."""
    try:
        conn = get_server_connection()
        cursor = conn.cursor()
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DB_NAME}")
        cursor.close()
        conn.close()

        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INT AUTO_INCREMENT PRIMARY KEY,
                username VARCHAR(50) UNIQUE NOT NULL,
                password VARCHAR(100) NOT NULL
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS donors (
                donor_id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(100) NOT NULL,
                age INT NOT NULL,
                gender VARCHAR(20) NOT NULL,
                blood_group VARCHAR(5) NOT NULL,
                phone VARCHAR(15) NOT NULL,
                email VARCHAR(100),
                city VARCHAR(100),
                last_donation_date DATE
            )
        """)

        cursor.execute(
            "SELECT id FROM users WHERE username = %s",
            ("admin",)
        )

        if cursor.fetchone() is None:
            cursor.execute(
                "INSERT INTO users (username, password) VALUES (%s, %s)",
                ("admin", "admin123")
            )

        conn.commit()
        cursor.close()
        conn.close()
        return True

    except Error as e:
        messagebox.showerror(
            "Database Error",
            f"Could not connect to MySQL.\n\n{e}\n\n"
            "Check MySQL Server and DB_PASSWORD in the code."
        )
        return False


class BloodDonationApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Blood Donation Management System")
        self.root.geometry("1180x700")
        self.root.minsize(1050, 620)
        self.root.configure(bg="#f5f7fb")

        self.current_user = None

        self.colors = {
            "red": "#c62828",
            "dark_red": "#8e1b1b",
            "light_red": "#ffebee",
            "white": "#ffffff",
            "bg": "#f5f7fb",
            "dark": "#263238",
            "gray": "#607d8b",
            "green": "#2e7d32",
            "blue": "#1565c0",
            "orange": "#ef6c00"
        }

        self.show_login()

    # =========================
    # COMMON HELPERS
    # =========================
    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def create_button(self, parent, text, command, bg=None, width=15):
        return tk.Button(
            parent,
            text=text,
            command=command,
            font=("Segoe UI", 10, "bold"),
            bg=bg or self.colors["red"],
            fg="white",
            activebackground=self.colors["dark_red"],
            activeforeground="white",
            relief="flat",
            cursor="hand2",
            width=width,
            padx=8,
            pady=8
        )




    def show_login(self):
        self.clear_window()

        outer = tk.Frame(self.root, bg=self.colors["bg"])
        outer.pack(fill="both", expand=True)

        card = tk.Frame(
            outer,
            bg=self.colors["white"],
            highlightbackground="#dddddd",
            highlightthickness=1
        )
        card.place(relx=0.5, rely=0.5, anchor="center", width=430, height=480)

        tk.Label(
            card,
            text="🩸",
            font=("Segoe UI Emoji", 48),
            bg="white",
            fg=self.colors["red"]
        ).pack(pady=(30, 0))

        tk.Label(
            card,
            text="Blood Donation",
            font=("Segoe UI", 24, "bold"),
            bg="white",
            fg=self.colors["dark"]
        ).pack()

        tk.Label(
            card,
            text="Management System",
            font=("Segoe UI", 16),
            bg="white",
            fg=self.colors["red"]
        ).pack(pady=(0, 25))

        form = tk.Frame(card, bg="white")
        form.pack(fill="x", padx=55)

        tk.Label(
            form, text="Username",
            font=("Segoe UI", 10, "bold"),
            bg="white", fg=self.colors["dark"]
        ).pack(anchor="w")

        self.login_username = tk.Entry(
            form, font=("Segoe UI", 12),
            relief="solid", bd=1
        )
        self.login_username.pack(fill="x", ipady=7, pady=(5, 15))

        tk.Label(
            form, text="Password",
            font=("Segoe UI", 10, "bold"),
            bg="white", fg=self.colors["dark"]
        ).pack(anchor="w")

        self.login_password = tk.Entry(
            form, font=("Segoe UI", 12),
            show="*", relief="solid", bd=1
        )
        self.login_password.pack(fill="x", ipady=7, pady=(5, 20))

        self.create_button(
            form, "LOGIN", self.login, width=20
        ).pack(pady=5)

        tk.Label(
            card,
            text="Demo Login: admin / admin123",
            font=("Segoe UI", 9),
            bg="white",
            fg=self.colors["gray"]
        ).pack(side="bottom", pady=20)

        self.login_username.focus()
        self.root.bind("<Return>", lambda event: self.login())

    def login(self):
        username = self.login_username.get().strip()
        password = self.login_password.get()

        if not username or not password:
            messagebox.showwarning(
                "Validation", "Please enter username and password."
            )
            return

        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute(
                "SELECT username FROM users WHERE username=%s AND password=%s",
                (username, password)
            )
            result = cursor.fetchone()
            cursor.close()
            conn.close()

            if result:
                self.current_user = username
                self.root.unbind("<Return>")
                self.show_dashboard()
            else:
                messagebox.showerror(
                    "Login Failed", "Invalid username or password."
                )

        except Error as e:
            messagebox.showerror("Database Error", str(e))





  
    def show_dashboard(self):
        self.clear_window()

        header = tk.Frame(
            self.root, bg=self.colors["red"], height=75
        )
        header.pack(fill="x")
        header.pack_propagate(False)

        tk.Label(
            header,
            text="🩸 Blood Donation Management System",
            font=("Segoe UI", 20, "bold"),
            bg=self.colors["red"],
            fg="white"
        ).pack(side="left", padx=25, pady=18)

        tk.Button(
            header,
            text=f"Logout  ({self.current_user})",
            command=self.logout,
            font=("Segoe UI", 10, "bold"),
            bg=self.colors["dark_red"],
            fg="white",
            relief="flat",
            cursor="hand2",
            padx=15,
            pady=7
        ).pack(side="right", padx=20)

        nav = tk.Frame(self.root, bg="white", height=60)
        nav.pack(fill="x")
        nav.pack_propagate(False)

        nav_items = [
            ("Dashboard", self.show_dashboard),
            ("Add Donor", self.show_add_donor),
            ("View Donors", self.show_view_donors),
            ("Search", self.show_search),
        ]

        for text, command in nav_items:
            tk.Button(
                nav, text=text, command=command,
                font=("Segoe UI", 10, "bold"),
                bg="white", fg=self.colors["dark"],
                activebackground=self.colors["light_red"],
                relief="flat", cursor="hand2",
                padx=18, pady=12
            ).pack(side="left", padx=4, pady=7)

        body = tk.Frame(self.root, bg=self.colors["bg"])
        body.pack(fill="both", expand=True, padx=25, pady=25)

        tk.Label(
            body,
            text="Dashboard",
            font=("Segoe UI", 24, "bold"),
            bg=self.colors["bg"],
            fg=self.colors["dark"]
        ).pack(anchor="w")

        tk.Label(
            body,
            text="Manage blood donor information efficiently.",
            font=("Segoe UI", 11),
            bg=self.colors["bg"],
            fg=self.colors["gray"]
        ).pack(anchor="w", pady=(0, 20))

        stats_frame = tk.Frame(body, bg=self.colors["bg"])
        stats_frame.pack(fill="x")

        total = self.get_count()
        groups = self.get_group_counts()

        cards = [
            ("Total Donors", total, self.colors["red"]),
            ("A Group", groups.get("A+", 0) + groups.get("A-", 0), self.colors["blue"]),
            ("B Group", groups.get("B+", 0) + groups.get("B-", 0), self.colors["green"]),
            ("O Group", groups.get("O+", 0) + groups.get("O-", 0), self.colors["orange"]),
        ]

        for title, value, color in cards:
            card = tk.Frame(
                stats_frame,
                bg="white",
                highlightbackground="#dddddd",
                highlightthickness=1
            )
            card.pack(side="left", fill="both", expand=True, padx=7)

            tk.Frame(card, bg=color, height=6).pack(fill="x")

            tk.Label(
                card, text=title,
                font=("Segoe UI", 11, "bold"),
                bg="white", fg=self.colors["gray"]
            ).pack(pady=(20, 5))

            tk.Label(
                card, text=str(value),
                font=("Segoe UI", 30, "bold"),
                bg="white", fg=color
            ).pack(pady=(0, 20))

        group_frame = tk.LabelFrame(
            body, text="Blood Group Summary",
            font=("Segoe UI", 12, "bold"),
            bg="white", fg=self.colors["dark"],
            padx=15, pady=15
        )
        group_frame.pack(fill="both", expand=True, pady=25)

        blood_groups = [
            "A+", "A-", "B+", "B-",
            "AB+", "AB-", "O+", "O-"
        ]

        for i, group in enumerate(blood_groups):
            r, c = divmod(i, 4)

            box = tk.Frame(
                group_frame,
                bg=self.colors["light_red"],
                highlightbackground="#ffcdd2",
                highlightthickness=1
            )
            box.grid(
                row=r, column=c,
                sticky="nsew", padx=8, pady=8
            )

            tk.Label(
                box, text=group,
                font=("Segoe UI", 16, "bold"),
                bg=self.colors["light_red"],
                fg=self.colors["red"]
            ).pack(pady=(10, 2))

            tk.Label(
                box, text=f"{groups.get(group, 0)} donor(s)",
                font=("Segoe UI", 10),
                bg=self.colors["light_red"],
                fg=self.colors["dark"]
            ).pack(pady=(0, 10))

        for i in range(4):
            group_frame.columnconfigure(i, weight=1)
        for i in range(2):
            group_frame.rowconfigure(i, weight=1)

    def get_count(self):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM donors")
            count = cursor.fetchone()[0]
            cursor.close()
            conn.close()
            return count
        except Error:
            return 0

    def get_group_counts(self):
        counts = {}
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute(
                "SELECT blood_group, COUNT(*) FROM donors GROUP BY blood_group"
            )
            for group, count in cursor.fetchall():
                counts[group] = count
            cursor.close()
            conn.close()
        except Error:
            pass
        return counts





    def show_add_donor(self):
        self.show_donor_form("Add Donor", self.add_donor)

    def show_donor_form(self, title, save_command, donor=None):
        self.clear_window()

        header = tk.Frame(self.root, bg=self.colors["red"], height=70)
        header.pack(fill="x")
        header.pack_propagate(False)

        tk.Label(
            header, text=title,
            font=("Segoe UI", 21, "bold"),
            bg=self.colors["red"], fg="white"
        ).pack(side="left", padx=25, pady=15)

        self.create_button(
            header, "← Dashboard", self.show_dashboard,
            bg=self.colors["dark_red"], width=14
        ).pack(side="right", padx=20, pady=13)

        container = tk.Frame(self.root, bg=self.colors["bg"])
        container.pack(fill="both", expand=True, padx=30, pady=25)

        form = tk.Frame(
            container, bg="white",
            highlightbackground="#dddddd",
            highlightthickness=1
        )
        form.pack(fill="x")

        fields = [
            ("Name", "name"),
            ("Age", "age"),
            ("Gender", "gender"),
            ("Blood Group", "blood_group"),
            ("Phone", "phone"),
            ("Email", "email"),
            ("City", "city"),
            ("Last Donation Date (YYYY-MM-DD)", "last_date")
        ]

        self.form_vars = {}

        for i, (label, key) in enumerate(fields):
            row = i // 2
            col = (i % 2) * 2

            tk.Label(
                form, text=label,
                font=("Segoe UI", 10, "bold"),
                bg="white", fg=self.colors["dark"]
            ).grid(
                row=row, column=col,
                sticky="w", padx=(25, 10), pady=(20, 5)
            )

            if key == "gender":
                var = tk.StringVar()
                widget = ttk.Combobox(
                    form, textvariable=var,
                    values=["Male", "Female", "Other"],
                    state="readonly",
                    font=("Segoe UI", 10)
                )
                widget.set("Male")
            elif key == "blood_group":
                var = tk.StringVar()
                widget = ttk.Combobox(
                    form, textvariable=var,
                    values=["A+", "A-", "B+", "B-",
                            "AB+", "AB-", "O+", "O-"],
                    state="readonly",
                    font=("Segoe UI", 10)
                )
                widget.set("A+")
            else:
                var = tk.StringVar()
                widget = tk.Entry(
                    form, textvariable=var,
                    font=("Segoe UI", 11),
                    relief="solid", bd=1
                )

            widget.grid(
                row=row, column=col + 1,
                sticky="ew", padx=(0, 25), pady=(20, 5),
                ipady=6
            )
            self.form_vars[key] = var

        for c in [1, 3]:
            form.columnconfigure(c, weight=1)

        if donor:



         
            values = {
                "name": donor[1],
                "age": donor[2],
                "gender": donor[3],
                "blood_group": donor[4],
                "phone": donor[5],
                "email": donor[6] or "",
                "city": donor[7] or "",
                "last_date": donor[8].strftime("%Y-%m-%d")
                if donor[8] else ""
            }

            for key, value in values.items():
                self.form_vars[key].set(str(value))

        button_frame = tk.Frame(container, bg=self.colors["bg"])
        button_frame.pack(fill="x", pady=20)

        self.create_button(
            button_frame, "SAVE", save_command,
            bg=self.colors["green"], width=15
        ).pack(side="left", padx=5)

        self.create_button(
            button_frame, "CLEAR", self.clear_form,
            bg=self.colors["gray"], width=15
        ).pack(side="left", padx=5)

    def clear_form(self):
        for key, var in self.form_vars.items():
            if key == "gender":
                var.set("Male")
            elif key == "blood_group":
                var.set("A+")
            else:
                var.set("")

    def validate_donor(self):
        data = {
            key: var.get().strip()
            for key, var in self.form_vars.items()
        }

        if not data["name"]:
            messagebox.showwarning("Validation", "Name is required.")
            return None

        try:
            age = int(data["age"])
            if age < 18 or age > 65:
                messagebox.showwarning(
                    "Validation",
                    "Age should be between 18 and 65."
                )
                return None
        except ValueError:
            messagebox.showwarning(
                "Validation", "Age must be a number."
            )
            return None

        phone = data["phone"]
        if not phone.isdigit() or len(phone) != 10:
            messagebox.showwarning(
                "Validation", "Phone number must contain exactly 10 digits."
            )
            return None

        if data["email"] and (
            "@" not in data["email"] or "." not in data["email"]
        ):
            messagebox.showwarning(
                "Validation", "Please enter a valid email address."
            )
            return None

        if data["last_date"]:
            try:
                donation_date = datetime.strptime(
                    data["last_date"], "%Y-%m-%d"
                ).date()
            except ValueError:
                messagebox.showwarning(
                    "Validation",
                    "Date must be in YYYY-MM-DD format."
                )
                return None
        else:
            donation_date = None

        data["age"] = age
        data["last_date"] = donation_date
        return data

    def add_donor(self):
        data = self.validate_donor()
        if not data:
            return

        try:
            conn = get_db_connection()
            cursor = conn.cursor()

            query = """
                INSERT INTO donors
                (name, age, gender, blood_group, phone, email, city,
                 last_donation_date)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """

            values = (
                data["name"], data["age"], data["gender"],
                data["blood_group"], data["phone"], data["email"],
                data["city"], data["last_date"]
            )

            cursor.execute(query, values)
            conn.commit()
            cursor.close()
            conn.close()

            messagebox.showinfo(
                "Success", "Donor added successfully."
            )
            self.show_view_donors()

        except Error as e:
            messagebox.showerror("Database Error", str(e))





    def show_view_donors(self, records=None):
        self.clear_window()

        header = tk.Frame(self.root, bg=self.colors["red"], height=70)
        header.pack(fill="x")
        header.pack_propagate(False)

        tk.Label(
            header, text="Donor Records",
            font=("Segoe UI", 21, "bold"),
            bg=self.colors["red"], fg="white"
        ).pack(side="left", padx=25, pady=15)

        self.create_button(
            header, "+ Add Donor", self.show_add_donor,
            bg=self.colors["green"], width=14
        ).pack(side="right", padx=20, pady=13)

        body = tk.Frame(self.root, bg=self.colors["bg"])
        body.pack(fill="both", expand=True, padx=25, pady=20)

        columns = (
            "ID", "Name", "Age", "Gender", "Blood Group",
            "Phone", "Email", "City", "Last Donation"
        )

        tree_frame = tk.Frame(body, bg="white")
        tree_frame.pack(fill="both", expand=True)

        self.tree = ttk.Treeview(
            tree_frame, columns=columns,
            show="headings", selectmode="browse"
        )

        widths = [55, 150, 55, 80, 90, 110, 180, 110, 120]

        for col, width in zip(columns, widths):
            self.tree.heading(col, text=col)
            self.tree.column(
                col, width=width,
                anchor="center" if col not in ["Name", "Email"] else "w"
            )

        vsb = ttk.Scrollbar(
            tree_frame, orient="vertical",
            command=self.tree.yview
        )
        hsb = ttk.Scrollbar(
            tree_frame, orient="horizontal",
            command=self.tree.xview
        )

        self.tree.configure(
            yscrollcommand=vsb.set,
            xscrollcommand=hsb.set
        )

        self.tree.grid(row=0, column=0, sticky="nsew")
        vsb.grid(row=0, column=1, sticky="ns")
        hsb.grid(row=1, column=0, sticky="ew")

        tree_frame.rowconfigure(0, weight=1)
        tree_frame.columnconfigure(0, weight=1)

        self.load_records(records)

        actions = tk.Frame(body, bg=self.colors["bg"])
        actions.pack(fill="x", pady=15)

        self.create_button(
            actions, "UPDATE SELECTED",
            self.update_selected,
            bg=self.colors["blue"], width=18
        ).pack(side="left", padx=5)

        self.create_button(
            actions, "DELETE SELECTED",
            self.delete_selected,
            bg=self.colors["red"], width=18
        ).pack(side="left", padx=5)

        self.create_button(
            actions, "REFRESH",
            self.show_view_donors,
            bg=self.colors["gray"], width=15
        ).pack(side="left", padx=5)

        self.create_button(
            actions, "DASHBOARD",
            self.show_dashboard,
            bg=self.colors["dark"], width=15
        ).pack(side="right", padx=5)

    def load_records(self, records=None):
        for item in self.tree.get_children():
            self.tree.delete(item)

        if records is None:
            try:
                conn = get_db_connection()
                cursor = conn.cursor()
                cursor.execute("""
                    SELECT donor_id, name, age, gender, blood_group,
                           phone, email, city, last_donation_date
                    FROM donors
                    ORDER BY donor_id DESC
                """)
                records = cursor.fetchall()
                cursor.close()
                conn.close()
            except Error as e:
                messagebox.showerror("Database Error", str(e))
                return

        for row in records:
            row = list(row)
            if row[8]:
                row[8] = row[8].strftime("%Y-%m-%d")
            self.tree.insert("", "end", values=row)

    def get_selected_donor_id(self):
        selected = self.tree.selection()

        if not selected:
            messagebox.showwarning(
                "Selection", "Please select a donor record."
            )
            return None

        values = self.tree.item(selected[0], "values")
        return values[0]

    def get_donor_by_id(self, donor_id):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute(
                "SELECT * FROM donors WHERE donor_id=%s",
                (donor_id,)
            )
            donor = cursor.fetchone()
            cursor.close()
            conn.close()
            return donor
        except Error as e:
            messagebox.showerror("Database Error", str(e))
            return None




  
    def update_selected(self):
        donor_id = self.get_selected_donor_id()
        if donor_id is None:
            return

        donor = self.get_donor_by_id(donor_id)
        if donor:
            self.show_update_form(donor)

    def show_update_form(self, donor):
        self.show_donor_form(
            "Update Donor",
            lambda: self.update_donor(donor[0]),
            donor
        )

    def update_donor(self, donor_id):
        data = self.validate_donor()
        if not data:
            return

        try:
            conn = get_db_connection()
            cursor = conn.cursor()

            query = """
                UPDATE donors
                SET name=%s, age=%s, gender=%s, blood_group=%s,
                    phone=%s, email=%s, city=%s,
                    last_donation_date=%s
                WHERE donor_id=%s
            """

            values = (
                data["name"], data["age"], data["gender"],
                data["blood_group"], data["phone"], data["email"],
                data["city"], data["last_date"], donor_id
            )

            cursor.execute(query, values)
            conn.commit()
            cursor.close()
            conn.close()

            messagebox.showinfo(
                "Success", "Donor record updated successfully."
            )
            self.show_view_donors()

        except Error as e:
            messagebox.showerror("Database Error", str(e))





   
    def delete_selected(self):
        donor_id = self.get_selected_donor_id()
        if donor_id is None:
            return

        selected = self.tree.selection()[0]
        donor_name = self.tree.item(selected, "values")[1]

        confirm = messagebox.askyesno(
            "Confirm Delete",
            f"Are you sure you want to delete donor '{donor_name}'?"
        )

        if not confirm:
            return

        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute(
                "DELETE FROM donors WHERE donor_id=%s",
                (donor_id,)
            )
            conn.commit()
            cursor.close()
            conn.close()

            messagebox.showinfo(
                "Deleted", "Donor record deleted successfully."
            )
            self.show_view_donors()

        except Error as e:
            messagebox.showerror("Database Error", str(e))





    def show_search(self):
        self.clear_window()

        header = tk.Frame(self.root, bg=self.colors["red"], height=70)
        header.pack(fill="x")
        header.pack_propagate(False)

        tk.Label(
            header, text="Search Donor",
            font=("Segoe UI", 21, "bold"),
            bg=self.colors["red"], fg="white"
        ).pack(side="left", padx=25, pady=15)

        self.create_button(
            header, "← Dashboard", self.show_dashboard,
            bg=self.colors["dark_red"], width=14
        ).pack(side="right", padx=20, pady=13)

        body = tk.Frame(self.root, bg=self.colors["bg"])
        body.pack(fill="both", expand=True, padx=25, pady=20)

        search_box = tk.Frame(body, bg="white")
        search_box.pack(fill="x", pady=(0, 15))

        tk.Label(
            search_box, text="Search By:",
            font=("Segoe UI", 10, "bold"),
            bg="white"
        ).pack(side="left", padx=(20, 8), pady=18)

        self.search_field = ttk.Combobox(
            search_box,
            values=["Name", "Blood Group", "Phone", "City"],
            state="readonly",
            width=15,
            font=("Segoe UI", 10)
        )
        self.search_field.set("Name")
        self.search_field.pack(side="left", padx=5)

        self.search_entry = tk.Entry(
            search_box, font=("Segoe UI", 11),
            relief="solid", bd=1
        )
        self.search_entry.pack(
            side="left", fill="x", expand=True,
            padx=8, ipady=6
        )

        self.create_button(
            search_box, "SEARCH",
            self.perform_search,
            bg=self.colors["blue"], width=12
        ).pack(side="left", padx=5)

        self.create_button(
            search_box, "SHOW ALL",
            self.show_search,
            bg=self.colors["gray"], width=12
        ).pack(side="left", padx=(5, 20))

        columns = (
            "ID", "Name", "Age", "Gender", "Blood Group",
            "Phone", "Email", "City", "Last Donation"
        )

        tree_frame = tk.Frame(body, bg="white")
        tree_frame.pack(fill="both", expand=True)

        self.search_tree = ttk.Treeview(
            tree_frame, columns=columns,
            show="headings"
        )

        widths = [55, 150, 55, 80, 90, 110, 180, 110, 120]

        for col, width in zip(columns, widths):
            self.search_tree.heading(col, text=col)
            self.search_tree.column(col, width=width, anchor="center")

        vsb = ttk.Scrollbar(
            tree_frame, orient="vertical",
            command=self.search_tree.yview
        )
        hsb = ttk.Scrollbar(
            tree_frame, orient="horizontal",
            command=self.search_tree.xview
        )

        self.search_tree.configure(
            yscrollcommand=vsb.set,
            xscrollcommand=hsb.set
        )

        self.search_tree.grid(row=0, column=0, sticky="nsew")
        vsb.grid(row=0, column=1, sticky="ns")
        hsb.grid(row=1, column=0, sticky="ew")

        tree_frame.rowconfigure(0, weight=1)
        tree_frame.columnconfigure(0, weight=1)

        self.load_search_records()

    def load_search_records(self, records=None):
        for item in self.search_tree.get_children():
            self.search_tree.delete(item)

        if records is None:
            try:
                conn = get_db_connection()
                cursor = conn.cursor()
                cursor.execute("""
                    SELECT donor_id, name, age, gender, blood_group,
                           phone, email, city, last_donation_date
                    FROM donors
                    ORDER BY donor_id DESC
                """)
                records = cursor.fetchall()
                cursor.close()
                conn.close()
            except Error as e:
                messagebox.showerror("Database Error", str(e))
                return

        for row in records:
            row = list(row)
            if row[8]:
                row[8] = row[8].strftime("%Y-%m-%d")
            self.search_tree.insert("", "end", values=row)

    def perform_search(self):
        text = self.search_entry.get().strip()
        field = self.search_field.get()

        if not text:
            messagebox.showwarning(
                "Search", "Please enter a search value."
            )
            return

        field_map = {
            "Name": "name",
            "Blood Group": "blood_group",
            "Phone": "phone",
            "City": "city"
        }

        db_field = field_map[field]

        try:
            conn = get_db_connection()
            cursor = conn.cursor()

            query = f"""
                SELECT donor_id, name, age, gender, blood_group,
                       phone, email, city, last_donation_date
                FROM donors
                WHERE {db_field} LIKE %s
                ORDER BY donor_id DESC
            """

            cursor.execute(query, (f"%{text}%",))
            records = cursor.fetchall()

            cursor.close()
            conn.close()

            self.load_search_records(records)

            if not records:
                messagebox.showinfo(
                    "Search", "No matching donor records found."
                )

        except Error as e:
            messagebox.showerror("Database Error", str(e))




  
    def logout(self):
        confirm = messagebox.askyesno(
            "Logout", "Are you sure you want to logout?"
        )
        if confirm:
            self.current_user = None
            self.show_login()






if __name__ == "__main__":
    root = tk.Tk()

    if setup_database():
        app = BloodDonationApp(root)
        root.mainloop()
    else:
        root.destroy()
