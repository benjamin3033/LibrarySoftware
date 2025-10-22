import tkinter as tk
from main_menu import MainMenu
from membership_form import MembershipForm
from search_form import SearchForm
from stats_form import StatsForm
from help_screen import HelpScreen


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Aurora Archive")
        self.default_geometry = "800x800"
        self.geometry(self.default_geometry)

        self.container = tk.Frame(self)
        self.container.pack(side="top", fill="both", expand=True)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        self.menus = {}

        self.show_menu("MainMenu")
    
    def show_menu(self, menu_name, *args):
        for menu in self.menus.values():
            menu.grid_forget()

        if menu_name not in self.menus:
            if menu_name == "MainMenu":
                self.menus[menu_name] = MainMenu(self.container, self)
            elif menu_name == "MembershipForm":
                self.menus[menu_name] = MembershipForm(self.container, self)
            elif menu_name == "SearchForm":
                self.menus[menu_name] = SearchForm(self.container, self)
            elif menu_name == "StatsForm":
                self.menus[menu_name] = StatsForm(self.container, self)
            elif menu_name == "HelpScreen":
                self.menus[menu_name] = HelpScreen(self.container, self)
        
        menu_frame = self.menus[menu_name]
        menu_frame.grid(row=0, column=0, sticky="nsew")
        menu_frame.tkraise()

        if hasattr(menu_frame, 'menu_geometry'):
            self.geometry(menu_frame.menu_geometry)
        else:
            self.geometry(self.default_geometry)

        if hasattr(self.menus[menu_name], 'on_show'):
            self.menus[menu_name].on_show(*args)

if __name__ == "__main__":
    app = App()
    app.mainloop()