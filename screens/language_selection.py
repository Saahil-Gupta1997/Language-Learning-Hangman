import tkinter as tk
from tkinter import messagebox
from tkinter import ttk  # Use themed widgets for a modern UI

class LanguageSelection:
    def __init__(self, root, app):
        self.root = root
        self.app = app
        self.clear_screen()

        self.languages = ["English", "Spanish", "Italian", "German"]
        current_language = getattr(self.app, "selected_language", "English")  # ✅ Fix: Use local storage

        frame = tk.Frame(root, bg="#f0f0f0", padx=25, pady=25, relief="groove", bd=3)
        frame.place(relx=0.5, rely=0.5, anchor="center")

        tk.Label(frame, text="Select Your Learning Language", font=("Helvetica", 18, "bold"), bg="#f0f0f0", fg="#333333").pack(pady=10)

        # Styled dropdown using ttk.Combobox
        self.selected_language = tk.StringVar(value=current_language)
        self.language_dropdown = ttk.Combobox(frame, textvariable=self.selected_language, values=self.languages, state="readonly", font=("Helvetica", 14))
        self.language_dropdown.pack(pady=10, padx=10, ipadx=5)

        # Buttons
        tk.Button(frame, text="Confirm", font=("Helvetica", 12, "bold"), bg="#28a745", fg="white", width=15, command=self.save_language_selection).pack(pady=10)
        tk.Button(frame, text="Cancel", font=("Helvetica", 12, "bold"), bg="#dc3545", fg="white", width=15, command=self.app.show_main_menu).pack(pady=10)

    def save_language_selection(self):
        """Save selected language to app storage and reload word database."""
        self.app.selected_language = self.selected_language.get()  # Store in app
        self.app.db.set_language(self.app.selected_language)  # Update database with new language
        messagebox.showinfo("Success", f"Learning language set to {self.app.selected_language}!")
        self.app.show_main_menu()

    def clear_screen(self):
        """Clear all widgets from the root window."""
        for widget in self.root.winfo_children():
            widget.destroy()
