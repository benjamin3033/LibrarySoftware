import tkinter as tk
from tkinter import font as tkFont


class MainMenu(tk.Frame):
    menu_geometry = "300x500"

    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.create_widgets()
    
    def create_widgets(self):
        helv18 = tkFont.Font(family = 'Helvetica', size = 18)

        membership_form_button = tk.Button(self, text = "Membership Form", font = helv18, width = 15, command=lambda: self.controller.show_menu("MembershipForm"))
        search_form_button = tk.Button(self, text = "Search Form", font = helv18, width = 15, command=lambda: self.controller.show_menu("SearchForm"))
        statistics_form_button = tk.Button(self, text = "Statistics Form", font = helv18, width = 15, command=lambda: self.controller.show_menu("StatsForm"))
        help_screen_button = tk.Button(self, text = "Help Screen", font = helv18, width = 15, command=lambda: self.controller.show_menu("HelpScreen"))

        membership_form_button.place(x = 40, y = 100)
        search_form_button.place(x = 40, y = 200)
        statistics_form_button.place(x = 40, y = 300)
        help_screen_button.place(x = 40, y = 400)
    
    def on_show(self):
        print("Main Menu Shown")