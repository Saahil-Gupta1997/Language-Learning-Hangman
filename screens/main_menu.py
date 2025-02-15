import tkinter as tk

class MainMenu:
    def __init__(self, root, app):
        self.root = root
        self.app = app
        self.clear_screen()

        frame = tk.Frame(root, bg="#f8f9fa", padx=20, pady=20)
        frame.place(relx=0.5, rely=0.5, anchor="center")

        tk.Label(frame, text=f"Welcome, {self.app.logged_in_user}!", font=("Helvetica", 16, "bold"), bg="#f8f9fa", fg="#333333").pack(pady=10)
        tk.Label(frame, text="Main Menu", font=("Helvetica", 20, "bold"), bg="#f8f9fa", fg="#333333").pack(pady=20)

        tk.Button(frame, text="Start Game", font=("Helvetica", 14, "bold"), bg="#4CAF50", fg="#ffffff", width=15, command=self.app.initialize_game).pack(pady=10)
        tk.Button(frame, text="Select Language", font=("Helvetica", 14, "bold"), bg="#FF9800", fg="white", width=20, command=self.app.show_language_selection_screen).pack(pady=10)
        tk.Button(frame, text="Update Profile", font=("Helvetica", 14, "bold"), bg="#007BFF", fg="white", width=20, command=self.app.show_update_profile_screen).pack(pady=10)
        tk.Button(frame, text="Logout", font=("Helvetica", 14, "bold"), bg="#dc3545", fg="#ffffff", width=15, command=self.app.show_login_screen).pack(pady=10)

    def clear_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()
