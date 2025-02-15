import tkinter as tk
from tkinter import messagebox
from hangman_game import HangmanGame
from utils import update_hangman_image  # Fixed import
from humorous_lines import get_random_line, CORRECT_LINES, INCORRECT_LINES  # Fixed import

def update_display(app):
    app.word_label.config(text=app.game.get_display_word())
    app.lives_label.config(text=f"Lives: {app.game.lives}")
    update_hangman_image(app, app.game.lives)

    if app.game.is_won():
        messagebox.showinfo("Congratulations!", f"You guessed the word: {app.game.word}")
        play_again = messagebox.askyesno("Play Again?", "Do you want to play another round?")
        if play_again:
            app.initialize_game()  # Take user to category/difficulty selection screen
        else:
            app.show_main_menu()  # Return to main menu
    elif app.game.is_lost():
        messagebox.showinfo("Game Over", f"The word was: {app.game.word}")
        play_again = messagebox.askyesno("Play Again?", "Do you want to try again?")
        if play_again:
            app.initialize_game()  # Take user to category/difficulty selection screen
        else:
            app.show_main_menu()  # Return to main menu


def make_guess(app):
    guess = app.guess_entry.get().strip().lower()
    app.guess_entry.delete(0, tk.END)

    if len(guess) != 1 or not guess.isalpha():
        messagebox.showerror("Invalid Input", "Please enter a single letter.")
        return

    correct = app.game.guess(guess)

    if correct and app.correct_sound:
        app.correct_sound.play()
        comment = get_random_line(CORRECT_LINES, app.used_correct_lines)
    elif not correct and app.incorrect_sound:
        app.incorrect_sound.play()
        comment = get_random_line(INCORRECT_LINES, app.used_incorrect_lines)

    app.comment_label.config(text=comment)  # Show feedback
    app.word_label.config(text=app.game.get_display_word())  # Update word progress
    app.lives_label.config(text=f"Lives: {app.game.lives}")  # Update lives count

    wrong_guesses = ", ".join(sorted(app.game.wrong_guesses)) if app.game.wrong_guesses else "None"
    app.wrong_guess_label.config(text=f"Wrong guesses: {wrong_guesses}")  # Show incorrect guesses

    # Combine both correct and wrong guesses
    all_guesses = sorted(app.game.guesses | app.game.wrong_guesses)  # Merge both sets
    guesses_text = ", ".join(all_guesses) if all_guesses else "None"

    # Update UI
    app.guesses_label.config(text=f"Guesses: {guesses_text}")
    update_hangman_image(app, app.game.lives)  # Update Hangman image

    # Check if a hint should be revealed
    hints = app.game.get_hint()
    if hints:
        hint_text = "\n".join([f"{k.capitalize()}: {v}" for k, v in hints.items()])
        app.hint_label.config(text=f"Hint:\n{hint_text}")
        app.hint_label.pack(pady=5)  # Show hint label only when hints are available

    update_display(app)


def start_easy_mode(app):
    """Start game in Easy Mode."""
    category = app.category_var.get()
    difficulty = app.difficulty_var.get()
    word_entry = app.db.get_random_word(category, difficulty)
    app.game = HangmanGame(word_entry['word'], word_entry['hints'], max_lives=7)
    update_display(app)


def start_hard_mode(app):
    """Start game in Hard Mode (fewer hints, fewer lives)."""
    category = app.category_var.get()
    difficulty = app.difficulty_var.get()
    word_entry = app.db.get_random_word(category, difficulty)
    app.game = HangmanGame(word_entry['word'], word_entry['hints'], max_lives=5, hard_mode=True)
    update_display(app)

