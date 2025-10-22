import tkinter as tk
from tkinter import messagebox, ttk
import sqlite3
import os


class MembershipForm(tk.Frame):
    menu_geometry = "230x750"  # Custom size for this form
    
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        
        # Store text in variables
        self.plan_standard = "Regular"
        self.plan_premium = "Premium"
        self.plan_kids = "Kids"
        self.plan_monthly = "Monthly"
        self.plan_annual = "Annual"
        self.optional_1 = "Book Rental"
        self.optional_2 = "Private Area Access"
        self.optional_3 = "Monthly Booklet"
        self.optional_4 = "Online ebook Rental"
        
        # Initialize variables
        self.has_library_card = False
        self.membership_cost = 0
        self.optional_extras_cost = 0
        self.total_discount = 0
        self.total_cost = 0
        self.total_cost_perweek = 0
        self.annual_discount = 0
        self.total_cost_permonth = 0
        self.chosen_extras = []
        
        # Create variables for form fields
        self.membership_plan = tk.StringVar(self, self.plan_standard)
        self.payment_plan = tk.StringVar(self, self.plan_monthly)
        self.extra1 = tk.BooleanVar(self, False)
        self.extra2 = tk.BooleanVar(self, False)
        self.extra3 = tk.BooleanVar(self, False)
        self.extra4 = tk.BooleanVar(self, False)
        self.library_card = tk.StringVar(self)
        self.first_name = tk.StringVar(self)
        self.last_name = tk.StringVar(self)
        self.address = tk.StringVar(self)
        self.mobile = tk.StringVar(self)
        
        # Set up trace callbacks
        self.library_card.trace_add("write", self.card_check)
        self.first_name.trace_add("write", self.entry_check)
        self.last_name.trace_add("write", self.entry_check)
        self.address.trace_add("write", self.entry_check)
        self.mobile.trace_add("write", self.entry_check)
        
        self.create_widgets()
        self.calculate()
     
    def create_widgets(self):        
        
        # Personal Information Frame
        personal_frame = ttk.LabelFrame(self, text="Personal Information")
        personal_frame.grid(row=1, column=0, columnspan=2, sticky="ew", padx=10, pady=5)
        
        ttk.Label(personal_frame, text="First Name:").grid(row=0, column=0, sticky="w", pady=(0, 3))
        ttk.Entry(personal_frame, textvariable=self.first_name).grid(row=0, column=1, sticky="w", pady=(0, 3))
        
        ttk.Label(personal_frame, text="Last Name:").grid(row=1, column=0, sticky="w", pady=(0, 3))
        ttk.Entry(personal_frame, textvariable=self.last_name).grid(row=1, column=1, sticky="w", pady=(0, 3))
        
        ttk.Label(personal_frame, text="Address:").grid(row=2, column=0, sticky="w", pady=(0, 3))
        ttk.Entry(personal_frame, textvariable=self.address).grid(row=2, column=1, sticky="w", pady=(0, 3))
        
        ttk.Label(personal_frame, text="Mobile:").grid(row=3, column=0, sticky="w", pady=(0, 20))
        ttk.Entry(personal_frame, textvariable=self.mobile).grid(row=3, column=1, sticky="w", pady=(0, 20))
        
        # Membership Options Frame
        membership_frame = ttk.LabelFrame(self, text="Membership Options")
        membership_frame.grid(row=2, column=0, columnspan=2, sticky="ew", padx=10, pady=5)
        
        ttk.Label(membership_frame, text="Membership Plan:").grid(row=0, column=0, sticky="w")
        ttk.Radiobutton(membership_frame, text=self.plan_standard, variable=self.membership_plan, 
                       value=self.plan_standard, command=self.calculate).grid(row=0, column=1, sticky="w")
        ttk.Radiobutton(membership_frame, text=self.plan_premium, variable=self.membership_plan, 
                       value=self.plan_premium, command=self.calculate).grid(row=1, column=1, sticky="w")
        ttk.Radiobutton(membership_frame, text=self.plan_kids, variable=self.membership_plan, 
                       value=self.plan_kids, command=self.calculate).grid(row=2, column=1, sticky="w", pady=(0, 20))
        
        ttk.Label(membership_frame, text="Payment Plan:").grid(row=3, column=0, sticky="w")
        ttk.Radiobutton(membership_frame, text=self.plan_monthly, variable=self.payment_plan, 
                       value=self.plan_monthly, command=self.calculate).grid(row=3, column=1, sticky="w")
        ttk.Radiobutton(membership_frame, text=self.plan_annual, variable=self.payment_plan, 
                       value=self.plan_annual, command=self.calculate).grid(row=4, column=1, sticky="w", pady=(0, 20))
        
        # Optional Extras Frame
        extras_frame = ttk.LabelFrame(self, text="Optional Extras")
        extras_frame.grid(row=3, column=0, columnspan=2, sticky="ew", padx=10, pady=5)
        
        ttk.Checkbutton(extras_frame, text=self.optional_1, variable=self.extra1, 
                       command=self.calculate).grid(row=0, column=0, sticky="w")
        ttk.Checkbutton(extras_frame, text=self.optional_2, variable=self.extra2, 
                       command=self.calculate).grid(row=1, column=0, sticky="w")
        ttk.Checkbutton(extras_frame, text=self.optional_3, variable=self.extra3, 
                       command=self.calculate).grid(row=2, column=0, sticky="w")
        ttk.Checkbutton(extras_frame, text=self.optional_4, variable=self.extra4, 
                       command=self.calculate).grid(row=3, column=0, sticky="w", pady=(0, 20))
        
        # Library Card Frame
        card_frame = ttk.LabelFrame(self, text="Library Card")
        card_frame.grid(row=4, column=0, columnspan=2, sticky="ew", padx=10, pady=5)
        
        self.label_library_card = ttk.Label(card_frame, text="Card Number:")
        self.label_library_card.grid(row=0, column=0, sticky="w", pady=(0, 20))
        
        ttk.Entry(card_frame, textvariable=self.library_card).grid(row=0, column=1, sticky="w", pady=(0, 20))
        
        # Totals Frame
        totals_frame = ttk.LabelFrame(self, text="Cost Summary")
        totals_frame.grid(row=5, column=0, columnspan=2, sticky="ew", padx=10, pady=5)
        
        ttk.Label(totals_frame, text="Membership Cost:").grid(row=0, column=0, sticky="w")
        self.label_total_cost_base = ttk.Label(totals_frame, text="--")
        self.label_total_cost_base.grid(row=0, column=1, sticky="w")
        
        ttk.Label(totals_frame, text="Extra Charges:").grid(row=1, column=0, sticky="w")
        self.label_total_cost_extras = ttk.Label(totals_frame, text="--")
        self.label_total_cost_extras.grid(row=1, column=1, sticky="w")
        
        ttk.Label(totals_frame, text="Total Discount:").grid(row=2, column=0, sticky="w")
        self.label_total_cost_discount = ttk.Label(totals_frame, text="--")
        self.label_total_cost_discount.grid(row=2, column=1, sticky="w")
        
        ttk.Label(totals_frame, text="Total Weekly:").grid(row=3, column=0, sticky="w")
        self.label_total_cost_weekly = ttk.Label(totals_frame, text="--")
        self.label_total_cost_weekly.grid(row=3, column=1, sticky="w")
        
        ttk.Label(totals_frame, text="Total Cost:").grid(row=4, column=0, sticky="w")
        self.label_total_cost_total = ttk.Label(totals_frame, text="--")
        self.label_total_cost_total.grid(row=4, column=1, sticky="w")
        
        # Buttons Frame
        buttons_frame = ttk.Frame(self)
        buttons_frame.grid(row=6, column=0, columnspan=2, pady=(20, 0))
        
        ttk.Button(buttons_frame, text="Submit", command=self.validate_submition).grid(row=0, column=0, padx=5)
        ttk.Button(buttons_frame, text="Reset", command=self.clear_form_confirmation).grid(row=0, column=1, padx=5)

        back_btn = ttk.Button(
            self,
            text="Back to Main Menu",
            command=lambda: self.controller.show_menu("MainMenu")
        )
        back_btn.grid(row=71, column=0, padx=50)
    
    def calculate(self):
        # Reset variables
        self.membership_cost = 0
        self.optional_extras_cost = 0
        self.total_discount = 0
        self.total_cost = 0
        self.total_cost_perweek = 0
        self.annual_discount = 0
        self.total_cost_permonth = 0
        self.chosen_extras.clear()
        
        # Membership plan calculation
        selected_plan = self.membership_plan.get()
        if selected_plan == self.plan_standard:
            self.membership_cost = 10
        elif selected_plan == self.plan_premium:
            self.membership_cost = 15
        else:
            self.membership_cost = 5
        self.label_total_cost_base.config(text=f"${self.membership_cost}")
        
        # Optional extras calculation
        if self.extra1.get():
            self.optional_extras_cost += 5
            self.chosen_extras.append(self.optional_1)
        if self.extra2.get():
            self.optional_extras_cost += 15
            self.chosen_extras.append(self.optional_2)
        if self.extra3.get():
            self.optional_extras_cost += 2
            self.chosen_extras.append(self.optional_3)
        if self.extra4.get():
            self.optional_extras_cost += 5
            self.chosen_extras.append(self.optional_4)
        self.label_total_cost_extras.config(text=f"${self.optional_extras_cost}")
        
        # Payment plan
        if self.payment_plan.get() == self.plan_annual:
            self.annual_discount = self.membership_cost/12
            self.annual_discount = round(self.annual_discount, 2)
            self.total_discount = self.annual_discount
            self.total_cost_permonth = (self.membership_cost + self.optional_extras_cost - self.annual_discount)
        else:
            self.total_cost_permonth = (self.membership_cost + self.optional_extras_cost)
        
        # Discount calculation
        if self.has_library_card:
            self.total_discount = 0.1 * (self.membership_cost + self.optional_extras_cost)
            self.total_discount = round(self.total_discount, 2)
            if self.payment_plan.get() == self.plan_annual:
                self.total_discount += self.annual_discount
                self.total_cost_permonth = (self.membership_cost + self.optional_extras_cost - self.total_discount)
            self.total_discount = round(self.total_discount, 2)
        
        self.total_cost_perweek = round((self.total_cost_permonth / 4), 2)
        self.label_total_cost_discount.config(text=f"${self.total_discount}")
        
        # Total cost calculation
        if self.payment_plan.get() == self.plan_annual:
            self.total_cost = (self.total_cost_permonth) * 12
        else:
            self.total_cost = (self.total_cost_permonth) - self.total_discount
        
        self.total_cost = round(self.total_cost, 2)
        self.label_total_cost_weekly.config(text=f"${self.total_cost_perweek}")
        self.label_total_cost_total.config(text=f"${self.total_cost}")
    
    def card_check(self, *args):
        card_number = self.library_card.get()
        
        # Limit to 5 characters
        if len(card_number) > 5:
            new_text = card_number[:5]
            card_number = new_text
            self.library_card.set(new_text)
        
        # Remove non-digits
        card_number = self.remove_non_digits_from_string(card_number)
        self.library_card.set(card_number)
        
        # Check for correct library card
        if len(card_number) == 5:
            self.has_library_card = True
            self.label_library_card.config(foreground="#12b300")
        else:
            self.has_library_card = False
            self.label_library_card.config(foreground="#000000")
        
        self.calculate()
    
    def remove_non_digits_from_string(self, string):
        return ''.join(filter(str.isdigit, string))
    
    def remove_digits_from_string(self, string):
        return ''.join(filter(lambda x: not x.isdigit(), string))
    
    def entry_check(self, *args):
        first_name_value = self.first_name.get()
        self.first_name.set(self.remove_digits_from_string(first_name_value))
        
        last_name_value = self.last_name.get()
        self.last_name.set(self.remove_digits_from_string(last_name_value))
        
        mobile_value = self.mobile.get()
        self.mobile.set(self.remove_non_digits_from_string(mobile_value))
    
    def validate_submition(self):
        incorrect_fields = []
        
        if not self.first_name.get():
            incorrect_fields.append("First Name")
        if not self.last_name.get():
            incorrect_fields.append("Last Name")
        if not self.address.get():
            incorrect_fields.append("Address")
        if not self.mobile.get():
            incorrect_fields.append("Mobile")
        
        if incorrect_fields:
            message = "Missing Information:\n\n" + "\n".join(incorrect_fields)
            messagebox.showinfo("Missing Information", message)
            return
        
        self.submit()
    
    def submit(self):
        db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "library_database.db")
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        cursor.execute('''
        INSERT INTO Memberships (
            First_Name, Last_Name, Address, Mobile,
            Membership_Plan, Payment_Plan, Extra_Book_Rental, Extra_Private_Area, 
            Extra_Booklet, Extra_Ebook_Rental,
            Has_Library_Card, Library_Card_Number
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            self.first_name.get(),
            self.last_name.get(),
            self.address.get(),
            self.mobile.get(),
            self.membership_plan.get(),
            self.payment_plan.get(),
            1 if self.extra1.get() else 0,
            1 if self.extra2.get() else 0,
            1 if self.extra3.get() else 0,
            1 if self.extra4.get() else 0,
            1 if self.has_library_card else 0,
            self.library_card.get()
        ))

        conn.commit()
        messagebox.showinfo("Success", "Data successfully added!")
        self.clear_form()

        
    
    def clear_form_confirmation(self):
        confirm = messagebox.askyesno("Reset Confirmation", "Are you sure you want to reset the form?")
        if confirm:
            self.clear_form()
    
    def clear_form(self):
        self.first_name.set("")
        self.last_name.set("")
        self.address.set("")
        self.mobile.set("")
        self.library_card.set("")
        self.membership_plan.set(self.plan_standard)
        self.payment_plan.set(self.plan_monthly)
        self.extra1.set(False)
        self.extra2.set(False)
        self.extra3.set(False)
        self.extra4.set(False)
        self.calculate()
    
    def on_show(self):
        print("Membership form shown")