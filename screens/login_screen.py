import tkinter as tk
from tkinter import messagebox
import hashlib
import pickle
import os

USER_DATA_FILE = "user_data.pkl"


class LoginScreen:
    def __init__(self, root, app):
        self.root = root
        self.app = app
        self.clear_screen()

        self.users = self.load_users()

        frame = tk.Frame(root, bg="#ffffff", padx=20, pady=20, relief="groove", bd=2)
        frame.place(relx=0.5, rely=0.5, anchor="center")

        tk.Label(frame, text="Welcome to Hangman!", font=("Helvetica", 18, "bold"), bg="#ffffff", fg="#333333").grid(
            row=0, column=0, columnspan=2, pady=(0, 10))

        tk.Label(frame, text="Username:", font=("Helvetica", 12), bg="#ffffff", fg="#555555").grid(row=1, column=0,
                                                                                                   pady=5, sticky="e")
        self.username_entry = tk.Entry(frame, font=("Helvetica", 12), width=25)
        self.username_entry.grid(row=1, column=1, pady=5, padx=5)

        tk.Label(frame, text="Password:", font=("Helvetica", 12), bg="#ffffff", fg="#555555").grid(row=2, column=0,
                                                                                                   pady=5, sticky="e")
        self.password_entry = tk.Entry(frame, show="*", font=("Helvetica", 12), width=25)
        self.password_entry.grid(row=2, column=1, pady=5, padx=5)

        tk.Button(frame, text="Login", font=("Helvetica", 12, "bold"), bg="#4CAF50", fg="#ffffff", width=10,
                  command=self.login_user).grid(row=3, column=0, pady=10, padx=5)
        tk.Button(frame, text="Register", font=("Helvetica", 12, "bold"), bg="#007BFF", fg="#ffffff", width=10,
                  command=self.show_registration_form).grid(row=3, column=1, pady=10, padx=5)

    def hash_password(self, password):
        return hashlib.sha256(password.encode()).hexdigest()

    def load_users(self):
        if os.path.exists(USER_DATA_FILE):
            with open(USER_DATA_FILE, "rb") as file:
                return pickle.load(file)
        return {}

    def save_users(self):
        with open(USER_DATA_FILE, "wb") as file:
            pickle.dump(self.users, file)

    def login_user(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        hashed_password = self.hash_password(password)

        if self.users.get(username) == hashed_password:
            self.app.logged_in_user = username
            self.app.show_main_menu()
        else:
            messagebox.showerror("Login Failed", "Invalid username or password.")

    def show_registration_form(self):
        reg_window = tk.Toplevel(self.root)
        reg_window.title("Register")
        reg_window.geometry("400x300")
        reg_window.configure(bg="#f8f9fa")

        frame = tk.Frame(reg_window, bg="#ffffff", padx=20, pady=20, relief="groove", bd=2)
        frame.place(relx=0.5, rely=0.5, anchor="center")

        tk.Label(frame, text="Register New Account", font=("Helvetica", 16, "bold"), bg="#ffffff", fg="#333333").grid(
            row=0, column=0, columnspan=2, pady=10)

        tk.Label(frame, text="Username:", font=("Helvetica", 12), bg="#ffffff", fg="#555555").grid(row=1, column=0,
                                                                                                   pady=5, sticky="e")
        username_entry = tk.Entry(frame, font=("Helvetica", 12), width=25)
        username_entry.grid(row=1, column=1, pady=5, padx=5)

        tk.Label(frame, text="Password:", font=("Helvetica", 12), bg="#ffffff", fg="#555555").grid(row=2, column=0,
                                                                                                   pady=5, sticky="e")
        password_entry = tk.Entry(frame, show="*", font=("Helvetica", 12), width=25)
        password_entry.grid(row=2, column=1, pady=5, padx=5)

        def register_user():
            username = username_entry.get()
            password = password_entry.get()
            hashed_password = self.hash_password(password)

            if username in self.users:
                messagebox.showerror("Error", "Username already exists!")
            else:
                self.users[username] = hashed_password
                self.save_users()
                messagebox.showinfo("Success", "Account created successfully!")
                reg_window.destroy()

        tk.Button(frame, text="Submit", font=("Helvetica", 12, "bold"), bg="#4CAF50", fg="#ffffff", width=10,
                  command=register_user).grid(row=3, column=0, pady=10, padx=5)
        tk.Button(frame, text="Cancel", font=("Helvetica", 12, "bold"), bg="#dc3545", fg="#ffffff", width=10,
                  command=reg_window.destroy).grid(row=3, column=1, pady=10, padx=5)

    def clear_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()
