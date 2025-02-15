import random
import pandas as pd


class WordDatabase:
    def __init__(self, filepath):
        self.filepath = filepath
        self.language = "English"  # Default language
        self.words = self.load_words()
        self.unused_words = self.words.copy()

    def load_words(self):
        """Load words from the selected language sheet in the Excel file."""
        try:
            df = pd.read_excel(self.filepath, sheet_name=self.language)
        except FileNotFoundError:
            raise Exception("Words file not found.")
        except pd.errors.ParserError:
            raise Exception("Error reading the words file.")

        words = []
        for _, row in df.iterrows():
            hints = {
                'meaning': row['hint1'],
                'synonym': row['hint2'],
                'association': row['hint3']
            }
            difficulty = row.get('difficulty', 'Unknown')

            words.append({
                'word': row['word'],
                'category': row['category'],
                'hints': hints,
                'difficulty': difficulty
            })
        return words

    def get_random_word(self, category=None, difficulty=None):
        """Get a random word, optionally filtered by category and difficulty."""
        available_words = [
            word for word in self.unused_words
            if (category is None or word['category'] == category)
               and (difficulty is None or word['difficulty'] == difficulty)
        ]

        if not available_words:
            raise ValueError(f"No words available for difficulty '{difficulty}' and category '{category}'")

        chosen_word = random.choice(available_words)
        self.unused_words.remove(chosen_word)
        return chosen_word

    def get_categories(self):
        """Return a list of categories available."""
        return sorted(set(word['category'] for word in self.words))

    def get_difficulties(self):
        """Return a list of difficulty levels available."""
        return sorted(set(word['difficulty'] for word in self.words))

    def set_language(self, language):
        """Update the language and reload words."""
        self.language = language
        self.words = self.load_words()
        self.unused_words = self.words.copy()
