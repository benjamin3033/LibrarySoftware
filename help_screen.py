import tkinter as tk
from tkinter import ttk


class HelpScreen(tk.Frame):
    menu_geometry = "340x450"

    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.create_widgets()
    
    def create_widgets(self):

        text = ttk.Label(self, text="1. Membership Form:\n- Add new members by filling all required fields\n- Select membership type: Regular, Premium, or Kids\n- Choose payment plan: Monthly or Annual\n- Check optional extras as needed\n- Library card provides 10% discount on membership\n\n2. Search Form:\n- Search by name, membership ID, or library card number\n- Use filters to narrow results by membership type\n- Double-click a result to view/edit member details\n- Right-click for options to update or delete records\n\n3. Statistics Form:\n- View real-time membership statistics\n- See breakdown by membership type and payment plan\n- Check optional extras popularity\n- View projected monthly income calculations\n- Data updates automatically when opened\n\nNavigation:\n- Use the menu buttons to switch between forms\n- Click 'Back to Main Menu' to return from any form")
        text.grid(row=0, column=0, columnspan=2, padx=20, pady=20)

        back_btn = ttk.Button(
            self,
            text="Back to Main Menu",
            command=lambda: self.controller.show_menu("MainMenu")
        )
        back_btn.grid(row=1, column=0, columnspan=2, pady=20)
    
    def on_show(self):
        print("Help Screen Shown")