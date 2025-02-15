from hangman_pics import HANGMAN_PICS

def update_hangman_image(app, lives):
    index = max(0, min(len(HANGMAN_PICS) - 1, lives))
    app.hangman_label.config(text=HANGMAN_PICS[index])
