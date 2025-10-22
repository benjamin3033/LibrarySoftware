import tkinter as tk
from tkinter import ttk
import sqlite3
import os


class StatsForm(tk.Frame):
    menu_geometry = "600x500"

    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.create_widgets()
    
    def create_widgets(self):
        back_btn = ttk.Button(
            self,
            text="Back to Main Menu",
            command=lambda: self.controller.show_menu("MainMenu")
        )
        back_btn.grid(row=2, column=0, pady=(10, 0))

        container = ttk.Frame(self)
        container.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)

        stats_frame = ttk.LabelFrame(container, text="Member Statistics")
        stats_frame.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)

        self.total_members_label = ttk.Label(stats_frame, text="Total Members: Loading...")
        self.total_members_label.grid(row=0, column=0, sticky="w", padx=5, pady=2)

        self.plan_stats_label = ttk.Label(stats_frame, text="Membership Plan Distribution: Loading...")
        self.plan_stats_label.grid(row=1, column=0, sticky="w", padx=5, pady=2)
        
        self.duration_stats_label = ttk.Label(stats_frame, text="Membership Duration: Loading...")
        self.duration_stats_label.grid(row=2, column=0, sticky="w", padx=5, pady=2)
        
        self.extras_stats_label = ttk.Label(stats_frame, text="Optional Extras Selection: Loading...")
        self.extras_stats_label.grid(row=3, column=0, sticky="w", padx=5, pady=2)
        
        self.no_extras_label = ttk.Label(stats_frame, text="Members with No Extras: Loading...")
        self.no_extras_label.grid(row=4, column=0, sticky="w", padx=5, pady=2)
        
        self.library_card_label = ttk.Label(stats_frame, text="Library Card Holders: Loading...")
        self.library_card_label.grid(row=5, column=0, sticky="w", padx=5, pady=2)

        income_frame = ttk.LabelFrame(container, text="Monthly Income Projection")
        income_frame.grid(row=1, column=0, sticky="nsew", padx=5, pady=5)

        self.income_tree = ttk.Treeview(income_frame, columns=("Option", "CostPerUnit", "MemberAmount", "TotalIncome"), show="headings")

        self.income_tree.heading("Option", text="Option")
        self.income_tree.heading("CostPerUnit", text="Cost Per Unit ($)")
        self.income_tree.heading("MemberAmount", text="Member Amount")
        self.income_tree.heading("TotalIncome", text="Total Income ($)")
        
        self.income_tree.column("Option", width=150)
        self.income_tree.column("CostPerUnit", width=100, anchor="e")
        self.income_tree.column("MemberAmount", width=100, anchor="e")
        self.income_tree.column("TotalIncome", width=100, anchor="e")
        
        self.income_tree.grid(row=0, column=0, sticky="nsew")

        scrollbar = ttk.Scrollbar(income_frame, orient="vertical", command=self.income_tree.yview)
        scrollbar.grid(row=0, column=1, sticky="ns")
        self.income_tree.configure(yscrollcommand=scrollbar.set)

        container.columnconfigure(0, weight=1)
        container.rowconfigure(0, weight=1)
        container.rowconfigure(1, weight=1)
        
        stats_frame.columnconfigure(0, weight=1)
        income_frame.columnconfigure(0, weight=1)
        income_frame.rowconfigure(0, weight=1)

    
    def on_show(self):
        print("Statistics Form Shown")

        db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "library_database.db")
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        self.update_member_stats(cursor)
        self.update_income_table(cursor)

        conn.close()
    

    def update_member_stats(self, cursor):
        cursor.execute("SELECT COUNT(*) FROM Memberships")
        total_members = cursor.fetchone()[0]

        cursor.execute("""
            SELECT Membership_Plan, COUNT(*) 
            FROM Memberships
            GROUP BY Membership_Plan
        """)
        plan_counts = dict(cursor.fetchall())

        cursor.execute("""
            SELECT Payment_Plan, COUNT(*) 
            FROM Memberships 
            GROUP BY Payment_Plan
        """)
        duration_counts = dict(cursor.fetchall())

        extras_counts = {
            "Book Rental": 0,
            "Private Area Access": 0,
            "Monthly Booklet": 0,
            "Online eBook Rental": 0
        }

        cursor.execute("SELECT SUM(Extra_Book_Rental) FROM Memberships")
        extras_counts["Book Rental"] = cursor.fetchone()[0] or 0
            
        cursor.execute("SELECT SUM(Extra_Private_Area) FROM Memberships")
        extras_counts["Private Area Access"] = cursor.fetchone()[0] or 0
            
        cursor.execute("SELECT SUM(Extra_Booklet) FROM Memberships")
        extras_counts["Monthly Booklet"] = cursor.fetchone()[0] or 0
            
        cursor.execute("SELECT SUM(Extra_Ebook_Rental) FROM Memberships")
        extras_counts["Online eBook Rental"] = cursor.fetchone()[0] or 0

        cursor.execute("""
            SELECT COUNT(*) FROM Memberships 
            WHERE Extra_Book_Rental = 0 
            AND Extra_Private_Area = 0 
            AND Extra_Booklet = 0 
            AND Extra_Ebook_Rental = 0
        """)
        no_extras_count = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM Memberships WHERE Has_Library_Card = 1")
        library_card_count = cursor.fetchone()[0]


        self.total_members_label.config(text=f"Total Members: {total_members}")
            
        plan_text = "Membership Plan Distribution: " + ", ".join([f"{k}: {v}" for k, v in plan_counts.items()])
        self.plan_stats_label.config(text=plan_text)
            
        duration_text = "Membership Duration: " + ", ".join([f"{k}: {v}" for k, v in duration_counts.items()])
        self.duration_stats_label.config(text=duration_text)
            
        extras_text = "Optional Extras Selection: " + ", ".join([f"{k}: {v}" for k, v in extras_counts.items()])
        self.extras_stats_label.config(text=extras_text)
            
        self.no_extras_label.config(text=f"Members with No Extras: {no_extras_count}")
        self.library_card_label.config(text=f"Library Card Holders: {library_card_count}")

    
    def update_income_table(self, cursor):
        pricing = {
            "Regular Plan": 10.00,
            "Premium Plan": 15.00,
            "Kids Plan": 5.00,
            "Book Rental": 5.00,
            "Private Area Access": 15.00,
            "Monthly Booklet": 2.00,
            "Online eBook Rental": 5.00
        }

        for item in self.income_tree.get_children():
            self.income_tree.delete(item)

        cursor.execute("""
            SELECT Membership_Plan, COUNT(*) 
            FROM Memberships 
            GROUP BY Membership_Plan
        """)
        plan_counts = dict(cursor.fetchall())

        cursor.execute("SELECT SUM(Extra_Book_Rental) FROM Memberships")
        book_rental_count = cursor.fetchone()[0] or 0
            
        cursor.execute("SELECT SUM(Extra_Private_Area) FROM Memberships")
        private_area_count = cursor.fetchone()[0] or 0
            
        cursor.execute("SELECT SUM(Extra_Booklet) FROM Memberships")
        booklet_count = cursor.fetchone()[0] or 0
            
        cursor.execute("SELECT SUM(Extra_Ebook_Rental) FROM Memberships")
        ebook_count = cursor.fetchone()[0] or 0

        member_counts = {
            "Regular Plan": plan_counts.get("Regular", 0),
            "Premium Plan": plan_counts.get("Premium", 0),
            "Kids Plan": plan_counts.get("Kids", 0),
            "Book Rental": book_rental_count,
            "Private Area Access": private_area_count,
            "Monthly Booklet": booklet_count,
            "Online eBook Rental": ebook_count
        }

        for option, cost in pricing.items():
            count = member_counts.get(option, 0)
            total_income = cost * count
            self.income_tree.insert("", "end", values=(
                option,
                f"{cost:.2f}",
                count,
                f"{total_income:.2f}"
            ))
            
        # Add a total row
        grand_total = sum(pricing[option] * member_counts.get(option, 0) for option in pricing)
        self.income_tree.insert("", "end", values=(
            "GRAND TOTAL",
            "",
            "",
            f"{grand_total:.2f}"
        ), tags=("total",))
            
        # Configure tag for total row
        self.income_tree.tag_configure("total", background="#f0f0f0", font=('TkDefaultFont', 9, 'bold'))