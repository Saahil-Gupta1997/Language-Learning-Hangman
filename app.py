import tkinter as tk

from hangman_game import HangmanGame
from game_actions import start_easy_mode, start_hard_mode
from screens.login_screen import LoginScreen
from screens.main_menu import MainMenu
from screens.language_selection import LanguageSelection
from screens.update_profile import UpdateProfile
from setup_gui import setup_gui
from word_database import WordDatabase
from game_actions import *
from config import *
import pygame


class HangmanApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Language Learning Hangman Game")
        self.root.geometry("600x500")
        self.root.configure(bg=BG_COLOR)

        self.db = WordDatabase(WORDS_XLSX_PATH)  # Load word database
        self.current_user = None
        self.used_correct_lines = []
        self.used_incorrect_lines = []

        self.logged_in_user = None
        self.selected_language = "English"  # ✅ Fix: Store selected language in app instance

        self.start_easy_mode = lambda: start_easy_mode(self)
        self.start_hard_mode = lambda: start_hard_mode(self)

        pygame.mixer.init()
        self._initialize_sounds()

        self.make_guess = lambda: make_guess(self)

        # ✅ Add the missing reveal_first_letter function
        self.reveal_first_letter = lambda: reveal_first_letter(self)

        # Start with login screen
        self.show_login_screen()

    def show_login_screen(self):
        """Display the login screen."""
        LoginScreen(self.root, self)

    def show_main_menu(self):
        """Display the main menu."""
        MainMenu(self.root, self)

    def show_language_selection_screen(self):
        """Display the language selection screen."""
        LanguageSelection(self.root, self)

    def show_update_profile_screen(self):
        UpdateProfile(self.root, self)

    def initialize_game(self, mode="normal"):
        """Initialize the Hangman game using the selected language."""
        self.clear_screen()
        setup_gui(self)

        word_entry = self.db.get_random_word()  # Fetch word from the selected language
        self.game = HangmanGame(word_entry["word"], word_entry["hints"], max_lives=EASY_MODE_LIVES)
        update_display(self)

    def _initialize_sounds(self):
        """Load game sounds."""
        try:
            pygame.mixer.music.load(BACKGROUND_MUSIC_PATH)
            pygame.mixer.music.play(-1)
        except pygame.error:
            pass
        try:
            self.correct_sound = pygame.mixer.Sound(CORRECT_SOUND_PATH)
        except pygame.error:
            self.correct_sound = None
        try:
            self.incorrect_sound = pygame.mixer.Sound(INCORRECT_SOUND_PATH)
        except pygame.error:
            self.incorrect_sound = None

    def clear_screen(self):
        """Clear the window."""
        for widget in self.root.winfo_children():
            widget.destroy()
