import os

def load_high_score():
    if os.path.exists('highscore.dat'):
        with open('highscore.dat', 'r') as file:
            try:
                return int(file.read())
            except:
                return 0
    return 0

def save_high_score(score):
    with open('highscore.dat', 'w') as file:
        file.write(str(score))