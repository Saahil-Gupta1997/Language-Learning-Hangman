import tkinter as tk
from tkinter import ttk
from config import BG_COLOR, FONT_NAME, TITLE_FONT_SIZE, LABEL_FONT_SIZE, WORD_FONT_SIZE, BUTTON_COLOR, \
    BUTTON_TEXT_COLOR
from hangman_pics import HANGMAN_PICS

def setup_gui(app):
    """Set up the game UI."""
    app.main_frame = tk.Frame(app.root, bg=BG_COLOR)
    app.main_frame.pack(padx=20, pady=20, fill="both", expand=True)

    # Title Label
    app.title_label = tk.Label(app.main_frame, text="Language Learning Hangman",
                               font=(FONT_NAME, TITLE_FONT_SIZE, "bold"), bg=BG_COLOR)
    app.title_label.pack(pady=10)

    # Category Selection
    app.category_frame = tk.Frame(app.main_frame, bg=BG_COLOR)
    app.category_frame.pack(pady=5)

    tk.Label(app.category_frame, text="Category:", font=(FONT_NAME, LABEL_FONT_SIZE), bg=BG_COLOR).pack(side=tk.LEFT,
                                                                                                        padx=5)
    categories = app.db.get_categories()
    app.category_var = tk.StringVar(app.category_frame)
    app.category_var.set(categories[0])
    app.category_menu = ttk.Combobox(app.category_frame, textvariable=app.category_var, values=categories,
                                     state="readonly", font=(FONT_NAME, LABEL_FONT_SIZE))
    app.category_menu.config(font=(FONT_NAME, LABEL_FONT_SIZE), width=20)
    app.category_menu.pack(side=tk.LEFT, padx=5)

    # Difficulty Selection
    app.difficulty_frame = tk.Frame(app.main_frame, bg=BG_COLOR)
    app.difficulty_frame.pack(pady=5)

    tk.Label(app.difficulty_frame, text="Difficulty:", font=(FONT_NAME, LABEL_FONT_SIZE), bg=BG_COLOR).pack(
        side=tk.LEFT, padx=5)
    difficulties = app.db.get_difficulties()
    app.difficulty_var = tk.StringVar(app.difficulty_frame)
    app.difficulty_var.set(difficulties[0])
    app.difficulty_menu = ttk.Combobox(app.difficulty_frame, textvariable=app.difficulty_var, values=difficulties,
                                       state="readonly", font=(FONT_NAME, LABEL_FONT_SIZE))
    app.difficulty_menu.pack(side=tk.LEFT, padx=5)
    app.difficulty_menu.config(font=(FONT_NAME, LABEL_FONT_SIZE), width=20)

    # Start Game Buttons
    app.button_frame = tk.Frame(app.main_frame, bg=BG_COLOR)
    app.button_frame.pack(pady=10)

    app.start_easy_button = tk.Button(app.button_frame, text="Start Easy Mode",
                                      font=(FONT_NAME, LABEL_FONT_SIZE), bg=BUTTON_COLOR, fg=BUTTON_TEXT_COLOR,
                                      command=lambda: start_game(app, mode="easy"))
    app.start_easy_button.pack(side=tk.LEFT, padx=10)

    app.start_hard_button = tk.Button(app.button_frame, text="Start Hard Mode",
                                      font=(FONT_NAME, LABEL_FONT_SIZE), bg="#f44336", fg=BUTTON_TEXT_COLOR,
                                      command=lambda: start_game(app, mode="hard"))
    app.start_hard_button.pack(side=tk.LEFT, padx=10)

    # GAME UI - Initially Hidden
    app.word_label = tk.Label(app.main_frame, text="", font=(FONT_NAME, WORD_FONT_SIZE), bg=BG_COLOR)
    app.hangman_label = tk.Label(app.main_frame, text=HANGMAN_PICS[0], font=("Courier", 16), bg=BG_COLOR)
    app.guess_frame = tk.Frame(app.main_frame, bg=BG_COLOR)

    app.guess_entry = tk.Entry(app.guess_frame, font=(FONT_NAME, LABEL_FONT_SIZE))
    app.guess_button = tk.Button(app.guess_frame, text="Guess", font=(FONT_NAME, LABEL_FONT_SIZE),
                                 bg=BUTTON_COLOR, fg=BUTTON_TEXT_COLOR, command=app.make_guess)

    app.lives_label = tk.Label(app.main_frame, text="Lives: ", font=(FONT_NAME, LABEL_FONT_SIZE), bg=BG_COLOR)
    app.guesses_label = tk.Label(app.main_frame, text="Guesses: ", font=(FONT_NAME, LABEL_FONT_SIZE), bg=BG_COLOR)
    app.wrong_guess_label = tk.Label(app.main_frame, text="Wrong guess: ", font=(FONT_NAME, LABEL_FONT_SIZE),
                                     bg=BG_COLOR)

    # Initially hide game elements
    hide_game_ui(app)

    # Hangman Animation (Add before difficulty selection)
    app.hangman_label = tk.Label(app.main_frame, text=HANGMAN_PICS[0], font=("Courier", 16), bg=BG_COLOR)
    app.hangman_label.pack(pady=10)

    def animate_hangman(index=0):
        """Loops through Hangman images continuously every 60 seconds"""
        if not hasattr(app, "hangman_label") or not app.hangman_label.winfo_exists():
            return  # Exit if hangman_label does not exist

        if index < len(HANGMAN_PICS):
            app.hangman_label.config(text=HANGMAN_PICS[index])
            app.root.after(500, lambda: animate_hangman(index + 1))  # Update every 500ms
        else:
            app.root.after(60000, lambda: animate_hangman(0))  # Restart animation every 60s

    # Start animation
    animate_hangman()

    # Comment Label - Shows feedback for correct/incorrect guesses
    app.comment_label = tk.Label(app.main_frame, text="", font=(FONT_NAME, LABEL_FONT_SIZE), bg=BG_COLOR, fg="blue")
    app.comment_label.pack(pady=5)

    # Hint Label - Shows hints as lives decrease
    app.hint_label = tk.Label(app.main_frame, text="", font=(FONT_NAME, LABEL_FONT_SIZE), bg=BG_COLOR, fg="darkred")
    app.hint_label.pack(pady=5)
    app.hint_label.pack_forget()  # Hide at the start


def start_game(app, mode):
    """Start the game and transition the UI."""
    category = app.category_var.get()
    difficulty = app.difficulty_var.get()

    # Hide selection UI
    app.category_frame.pack_forget()
    app.difficulty_frame.pack_forget()
    app.button_frame.pack_forget()

    # Start the game logic
    if mode == "easy":
        app.start_easy_mode()
    else:
        app.start_hard_mode()

    # Show game UI
    show_game_ui(app)


def hide_game_ui(app):
    """Hide game UI elements initially."""
    app.word_label.pack_forget()
    app.hangman_label.pack_forget()
    app.guess_frame.pack_forget()
    app.lives_label.pack_forget()
    app.guesses_label.pack_forget()
    app.wrong_guess_label.pack_forget()


def show_game_ui(app):
    """Show the game UI after starting."""
    app.word_label.pack(pady=5)
    app.hangman_label.pack(pady=5)

    app.guess_frame.pack(pady=5)
    app.guess_entry.pack(side=tk.LEFT)
    app.guess_button.pack(side=tk.LEFT, padx=5)

    app.lives_label.pack(pady=5)
    app.guesses_label.pack(pady=5)
    app.wrong_guess_label.pack(pady=5)
