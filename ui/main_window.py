import tkinter as tk

import sys 
sys.path.append('../') 

from ui import clients,suppliers
from clients import ClientsWindow
from suppliers import SuppliersWindow

class MainWindow(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Main Window")
        sidebar_frame = tk.Frame(self, bg="lightgrey", width=100)
        sidebar_frame.pack(fill=tk.Y, side=tk.LEFT)

# Buttons on the sidebar
        suppliers_button = tk.Button(sidebar_frame, text="Suppliers", command=self.show_suppliers)
        suppliers_button.pack(pady=10)

        clients_button = tk.Button(sidebar_frame, text="Clients", command=self.show_clients)
        clients_button.pack(pady=10)
        content_frame = tk.Frame(self)
        content_frame.pack(fill=tk.BOTH, expand=True)
        home_label = tk.Label(content_frame, text="Welcome to Home!", font=("Arial", 18))
        home_label.pack(pady=50)
        

    def show_suppliers(self):
        suppliers_window = SuppliersWindow(self)
        suppliers_window.title("Suppliers")
        suppliers_window.geometry("400x300")
        suppliers_window.grab_set()

    def show_clients(self):
        clients_window = ClientsWindow(self)
        clients_window.title("Clients")
        clients_window.geometry("400x300")
        clients_window.grab_set()

if __name__ == "__main__":
    app = MainWindow()
    app.mainloop()
