class HangmanGame:
    def __init__(self, word, hints, max_lives, hard_mode=False):
        self.word = word.lower()
        self.original_word = word
        self.hints = hints  # Now structured
        self.max_lives = max_lives
        self.guesses = set()
        self.wrong_guesses = set()
        self.lives = max_lives
        self.hard_mode = hard_mode
        self.display_word = ['_' for _ in self.original_word]
        self.displayed_hints = []

    def guess(self, letter):
        letter = letter.lower()
        if letter in self.guesses or letter in self.wrong_guesses:
            return False
        if letter in self.word:
            self.guesses.add(letter)
            return True
        else:
            self.wrong_guesses.add(letter)
            self.lives -= 1
            return False

    def get_hint(self):
        """Reveals hints based on difficulty level."""
        if self.hard_mode:
            # In Hard Mode, only show hints when the player has 1 life left
            if self.lives == 2 and not self.displayed_hints:
                self.displayed_hints.extend(self.hints.keys())  # Show all hints at once
        else:
            # In Slow Mode, reveal hints gradually
            hints_intervals = [self.max_lives - 1, self.max_lives - 3, self.max_lives - 5]
            hint_keys = list(self.hints.keys())

            for i in range(len(hints_intervals)):
                if self.lives == hints_intervals[i] and hint_keys[i] not in self.displayed_hints:
                    self.displayed_hints.append(hint_keys[i])  # Add hint to displayed hints

        return {k: self.hints[k] for k in self.displayed_hints}  # Return revealed hints

    def get_display_word(self):
        return " ".join([char if char in self.guesses else "_" for char in self.word])

    def is_won(self):
        return set(self.word) == self.guesses

    def is_lost(self):
        return self.lives <= 0
