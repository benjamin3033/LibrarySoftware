import tkinter as tk
from tkinter import ttk
import os
import sqlite3


class SearchForm(tk.Frame):
    menu_geometry = "1320x600"

    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        self.member_id = tk.StringVar()
        self.last_name = tk.StringVar()
        self.membership_plan = tk.StringVar()
        self.payment_plan = tk.StringVar()

        self.plan_options = ["All", "Regular", "Premium", "Kids"]
        self.payment_options = ["All", "Monthly", "Annual"]

        self.create_widgets()
    
    def create_widgets(self):
        title_label = ttk.Label(self, text="Member Search", font=('Helvetica', 14))
        title_label.grid(row=1, column=0, columnspan=2, pady=(0, 20))

        ttk.Label(self, text="Member ID:").grid(row=2, column=0, sticky="e", padx=5, pady=5)
        ttk.Entry(self, textvariable=self.member_id, width=25).grid(row=2, column=1, sticky="w", pady=5)

        ttk.Label(self, text="Last Name:").grid(row=3, column=0, sticky="e", padx=5, pady=5)
        ttk.Entry(self, textvariable=self.last_name, width=25).grid(row=3, column=1, sticky="w", pady=5)

        ttk.Label(self, text="Membership Plan:").grid(row=4, column=0, sticky="e", padx=5, pady=5)
        plan_combo = ttk.Combobox(self, textvariable=self.membership_plan, values=self.plan_options, width=22)
        plan_combo.current(0)
        plan_combo.grid(row=4, column=1, sticky="w", pady=5)

        ttk.Label(self, text="Payment Plan:").grid(row=5, column=0, sticky="e", padx=5, pady=5)
        payment_combo = ttk.Combobox(self, textvariable=self.payment_plan, 
                                   values=self.payment_options, width=22)
        payment_combo.current(0)
        payment_combo.grid(row=5, column=1, sticky="w", pady=5)

        search_btn = ttk.Button(
            self,
            text="Search Members",
            command=self.perform_search,
            width=20
        )
        search_btn.grid(row=6, column=0, columnspan=2, pady=20)

        

        results_frame = ttk.LabelFrame(self, text="Search Results")
        results_frame.grid(row=8, column=0, columnspan=2, sticky="nsew", padx=10, pady=5)

        self.grid_rowconfigure(8, weight=1)
        self.grid_columnconfigure(8, weight=1)
        results_frame.grid_rowconfigure(8, weight=1)
        results_frame.grid_columnconfigure(8, weight=1)

        self.tree = ttk.Treeview(results_frame, columns=(
            "Member ID", "First Name", "Last Name", "Address", "Mobile",
            "Membership Plan", "Payment Plan", "Book Rental", "Private Area",
            "Booklet", "Ebook Rental", "Library Card", "Library Card Number"
        ), show='headings', selectmode="browse")

        columns = [
            ("Member ID", 80),
            ("First Name", 100),
            ("Last Name", 100),
            ("Address", 150),
            ("Mobile", 100),
            ("Membership Plan", 100),
            ("Payment Plan", 100),
            ("Book Rental", 80),
            ("Private Area", 80),
            ("Booklet", 80),
            ("Ebook Rental", 80),
            ("Library Card", 100),
            ("Library Card Number", 130)
        ]

        for col, width in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=width, anchor="center")
        
        y_scroll = ttk.Scrollbar(results_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=y_scroll.set)

        x_scroll = ttk.Scrollbar(results_frame, orient="horizontal", command=self.tree.xview)
        self.tree.configure(xscrollcommand=x_scroll.set)

        self.tree.grid(row=0, column=0, sticky="nsew")
        y_scroll.grid(row=0, column=1, sticky="ns")
        x_scroll.grid(row=1, column=0, sticky="ew")

        self.status_label = ttk.Label(self, text="Ready to search")
        self.status_label.grid(row=7, column=0, columnspan=2, sticky="w", padx=10, pady=5)

        back_btn = ttk.Button(
            self,
            text="Back to Main Menu",
            command=lambda: self.controller.show_menu("MainMenu")
        )
        back_btn.grid(row=9, column=0, columnspan=2, pady=20)
        
    
    def perform_search(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "library_database.db")

        with sqlite3.connect(db_path) as conn:
            cursor = conn.cursor()

            query = """
            SELECT
                MemberID, First_Name, Last_Name, Address, Mobile,
                Membership_Plan, Payment_Plan, Extra_Book_Rental,
                Extra_Private_Area, Extra_Booklet,
                Extra_Ebook_Rental,
                CASE WHEN Library_Card_Number IS NOT NULL THEN 'Yes' ELSE 'No' END,
                Library_Card_Number
            FROM Memberships
            WHERE 1=1
            """

            params = []

            if self.member_id.get().strip():
                    query += " AND MemberID = ?"
                    params.append(self.member_id.get().strip())
                    
            if self.last_name.get().strip():
                query += " AND Last_Name LIKE ?"
                params.append(f"%{self.last_name.get().strip()}%")
                    
            if self.membership_plan.get() != "All":
                query += " AND Membership_Plan = ?"
                params.append(self.membership_plan.get())
                    
            if self.payment_plan.get() != "All":
                query += " AND Payment_Plan = ?"
                params.append(self.payment_plan.get())
                
            query += " ORDER BY Last_Name, First_Name"

            cursor.execute(query, params)
            results = cursor.fetchall()

            for row in results:
                formatted_row = list(row)
                # Convert boolean values to Yes/No
                formatted_row[7] = "Yes" if row[7] else "No"  # Book Rental
                formatted_row[8] = "Yes" if row[8] else "No"  # Private Area
                formatted_row[9] = "Yes" if row[9] else "No"  # Booklet
                formatted_row[10] = "Yes" if row[10] else "No"  # Ebook Rental
                    
                self.tree.insert("", "end", values=formatted_row)
            
            self.status_label.config(text=f"Found {len(results)} members")
    
    def on_show(self):
        print("Search Form Shown")