import tkinter as tk
from tkinter import messagebox
from main_window import MainWindow
from logic import authentification
from logic import mongodb_database
from cryptography.fernet import Fernet

encrypted =b'gAAAAABmOGFI1fUVefSN3G5rTeKzt8TbAaXSutMOvjv9MmDVhwhcKAiXspjXr4h23toEzgIZtkaqZKKcCfv2KaE0G5ecJccCIAXQJiWvwzRpMCIxyOmpKwILAVD5HfbehQn9R8ynJMbTBYYYIb0SDJQosXY3ODLBBg=='
class LoginWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Login")
        self.geometry("300x200")

        self.label_username = tk.Label(self, text="Username:")
        self.label_password = tk.Label(self, text="Password:")
        self.entry_username = tk.Entry(self)
        self.entry_password = tk.Entry(self, show="*")

        self.label_username.grid(row=0, column=0, sticky=tk.E)
        self.label_password.grid(row=1, column=0, sticky=tk.E)
        self.entry_username.grid(row=0, column=1)
        self.entry_password.grid(row=1, column=1)

        self.button_login = tk.Button(self, text="Login", command=self.login)
        self.button_login.grid(row=2, column=0, columnspan=2)

    def login(self):
        username = self.entry_username.get()
        password = self.entry_password.get()
        
        if  authentification.authenticate_user(username, password):
            
            
            key=mongodb_database.generate_key(password)
            decrypted_mongodb_url = mongodb_database.decrypt_url(encrypted, key)
            mongodb_database.connect_to_mongodb(decrypted_mongodb_url)
            self.destroy()  # Close the login window
            app = MainWindow()  # Open the main application window
            app.mainloop()
        else:
            messagebox.showerror("Login Failed", "Invalid username or password")


def main():
    login_window = LoginWindow()
    login_window.mainloop()

if __name__ == "__main__":
    main()
