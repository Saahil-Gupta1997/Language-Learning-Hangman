import tkinter as tk
from tkinter import messagebox
import hashlib
import pickle
import os
import re

USER_DATA_FILE = "user_data.pkl"

class UpdateProfile:
    def __init__(self, root, app):
        self.root = root
        self.app = app
        self.clear_screen()

        frame = tk.Frame(root, bg="#ffffff", padx=20, pady=20, relief="groove", bd=2)
        frame.place(relx=0.5, rely=0.5, anchor="center")

        tk.Label(frame, text="Update Profile", font=("Helvetica", 18, "bold"), bg="#ffffff", fg="#333333").pack(pady=10)

        tk.Button(frame, text="Update Username", font=("Helvetica", 12, "bold"), bg="#007BFF", fg="#ffffff", width=20, command=self.show_update_username_screen).pack(pady=10)
        tk.Button(frame, text="Update Password", font=("Helvetica", 12, "bold"), bg="#4CAF50", fg="#ffffff", width=20, command=self.show_update_password_screen).pack(pady=10)
        tk.Button(frame, text="Cancel", font=("Helvetica", 12, "bold"), bg="#dc3545", fg="#ffffff", width=20, command=self.app.show_main_menu).pack(pady=10)

    def load_users(self):
        """Load user data from the local file."""
        if os.path.exists(USER_DATA_FILE):
            with open(USER_DATA_FILE, "rb") as file:
                return pickle.load(file)
        return {}

    def save_users(self, users):
        """Save updated user data to the local file."""
        with open(USER_DATA_FILE, "wb") as file:
            pickle.dump(users, file)

    def hash_password(self, password):
        return hashlib.sha256(password.encode()).hexdigest()

    def show_update_username_screen(self):
        """Open the Update Username screen with old and new username fields."""
        update_username_window = tk.Toplevel(self.root)
        update_username_window.title("Update Username")
        update_username_window.geometry("400x300")
        update_username_window.configure(bg="#f8f9fa")

        frame = tk.Frame(update_username_window, bg="#ffffff", padx=20, pady=20, relief="groove", bd=2)
        frame.place(relx=0.5, rely=0.5, anchor="center")

        tk.Label(frame, text="Update Username", font=("Helvetica", 16, "bold"), bg="#ffffff", fg="#333333").grid(row=0,
                                                                                                                 column=0,
                                                                                                                 columnspan=2,
                                                                                                                 pady=10)

        # Current username input
        tk.Label(frame, text="Current Username:", font=("Helvetica", 12), bg="#ffffff", fg="#555555").grid(row=1,
                                                                                                           column=0,
                                                                                                           pady=5,
                                                                                                           sticky="e")
        current_username_entry = tk.Entry(frame, font=("Helvetica", 12), width=25)
        current_username_entry.grid(row=1, column=1, pady=5, padx=5)

        # New username input
        tk.Label(frame, text="New Username:", font=("Helvetica", 12), bg="#ffffff", fg="#555555").grid(row=2, column=0,
                                                                                                       pady=5,
                                                                                                       sticky="e")
        new_username_entry = tk.Entry(frame, font=("Helvetica", 12), width=25)
        new_username_entry.grid(row=2, column=1, pady=5, padx=5)

        def update_username():
            """Handle updating the username."""
            current_username = current_username_entry.get().strip()
            new_username = new_username_entry.get().strip()
            users = self.load_users()

            # Check if the current username matches the logged-in user
            if current_username != self.app.logged_in_user:
                messagebox.showerror("Error", "Incorrect current username!", parent=update_username_window)
                return

            # Check if the new username is already taken
            if new_username in users:
                messagebox.showerror("Error", "Username already exists!", parent=update_username_window)
                return

            # Update username in storage
            users[new_username] = users.pop(current_username)
            self.save_users(users)

            # Update the logged-in username
            self.app.logged_in_user = new_username
            messagebox.showinfo("Success", "Username updated successfully!", parent=update_username_window)
            update_username_window.destroy()

        # Buttons
        tk.Button(frame, text="Submit", font=("Helvetica", 12, "bold"), bg="#4CAF50", fg="#ffffff", width=10,
                  command=update_username).grid(row=3, column=0, pady=10, padx=5)
        tk.Button(frame, text="Cancel", font=("Helvetica", 12, "bold"), bg="#dc3545", fg="#ffffff", width=10,
                  command=update_username_window.destroy).grid(row=3, column=1, pady=10, padx=5)

    def show_update_password_screen(self):
        """Open the Update Password screen with old and new password fields."""
        update_password_window = tk.Toplevel(self.root)
        update_password_window.title("Update Password")
        update_password_window.geometry("400x300")
        update_password_window.configure(bg="#f8f9fa")

        frame = tk.Frame(update_password_window, bg="#ffffff", padx=20, pady=20, relief="groove", bd=2)
        frame.place(relx=0.5, rely=0.5, anchor="center")

        tk.Label(frame, text="Update Password", font=("Helvetica", 16, "bold"), bg="#ffffff", fg="#333333").grid(row=0,
                                                                                                                 column=0,
                                                                                                                 columnspan=2,
                                                                                                                 pady=10)

        tk.Label(frame, text="Current Password:", font=("Helvetica", 12), bg="#ffffff", fg="#555555").grid(row=1,
                                                                                                           column=0,
                                                                                                           pady=5,
                                                                                                           sticky="e")
        current_password_entry = tk.Entry(frame, show="*", font=("Helvetica", 12), width=25)
        current_password_entry.grid(row=1, column=1, pady=5, padx=5)

        tk.Label(frame, text="New Password:", font=("Helvetica", 12), bg="#ffffff", fg="#555555").grid(row=2, column=0,
                                                                                                       pady=5,
                                                                                                       sticky="e")
        new_password_entry = tk.Entry(frame, show="*", font=("Helvetica", 12), width=25)
        new_password_entry.grid(row=2, column=1, pady=5, padx=5)

        def update_password():
            """Handle updating the password."""
            current_password = current_password_entry.get().strip()
            new_password = new_password_entry.get().strip()
            users = self.load_users()

            # Verify current password
            if self.app.logged_in_user not in users:
                messagebox.showerror("Error", "User not found!", parent=update_password_window)
                return

            if self.hash_password(current_password) != users[self.app.logged_in_user]:
                messagebox.showerror("Error", "Incorrect current password!", parent=update_password_window)
                return

            # Validate new password
            error_message = self.is_valid_password(new_password)
            if error_message:
                messagebox.showerror("Weak Password", error_message, parent=update_password_window)
                return

            # Update password
            users[self.app.logged_in_user] = self.hash_password(new_password)
            self.save_users(users)
            messagebox.showinfo("Success", "Password updated successfully!", parent=update_password_window)
            update_password_window.destroy()

        tk.Button(frame, text="Submit", font=("Helvetica", 12, "bold"), bg="#4CAF50", fg="#ffffff", width=10,
                  command=update_password).grid(row=3, column=0, pady=10, padx=5)
        tk.Button(frame, text="Cancel", font=("Helvetica", 12, "bold"), bg="#dc3545", fg="#ffffff", width=10,
                  command=update_password_window.destroy).grid(row=3, column=1, pady=10, padx=5)

    def is_valid_password(self, password):
        """Check if password meets security criteria."""
        if len(password) < 6:
            return "Password must be at least 6 characters long."
        if not re.search(r"[A-Z]", password):
            return "Password must contain at least one uppercase letter."
        if not re.search(r"[a-z]", password):
            return "Password must contain at least one lowercase letter."
        if not re.search(r"\d", password):
            return "Password must contain at least one digit."
        return None  # If all criteria are met, return None
    def clear_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()
