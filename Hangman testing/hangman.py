import random
import sys
import re

from graphics import HANGMAN_UI
from language import DICTIONARY

# Colors for terminal
RESET = "\033[0m"
GREEN = "\033[32m"
RED = "\033[31m"
YELLOW = "\033[33m"
BLUE = "\033[34m"

# Ask language
language = input(f"{DICTIONARY['en']['msgLanguageChoice']}\n\n{DICTIONARY['no']['msgLanguageChoice']}\n> ").strip().lower()
if language not in DICTIONARY:  # Default to English
    language = "en"

# Read word list
list_of_words = DICTIONARY[language]['wordList']
with open(list_of_words, 'r', encoding='utf-8') as f:
    all_words = [w.strip() for w in f.read().splitlines() if w.strip()]

# Pick a random word
word = random.choice(all_words).lower()
letters_in_word = list(word)

# Helpers
def pull_randomly_from_list(list):
    return random.choice(list)

# Make visual
def make_visual_from_word(word):
    return ["_"] * len(word)


# Reset game
mistake = []  # List of wrong guesses
correct = []  # List of correct guesses
stat_trackers = []  # Track number of guesses per round
rounds_played = 0
total_guesses = 0

def reset_game():
    global mistake, correct, word, word_length, status
    mistake = []
    correct = []
    word = pull_randomly_from_list(all_words).lower()
    word_length = list(word)

status = make_visual_from_word(word)
# Main loop
play_again = True
while play_again:
    reset_game()
    rounds_played += 1

    def show_status(wrong):
        print("\n HANGMAN")
        print(HANGMAN_UI[len(mistake)])
        if wrong and len(mistake) >= len(HANGMAN_UI) -1:
            print(f"GAME OVER! {DICTIONARY[language]['msgWordWas']}{word}\n")
        elif not wrong and "_" not in status:
            print(f"{GREEN}{DICTIONARY[language]['msgWin']}{RESET}\n")
        else:
            print(" ".join(status))
            if len(mistake) > 0: 
                print(f"{DICTIONARY[language]['msgCurrentMistakes']} {' '.join(mistake)}\n")


    def hangman_game():
        global total_guesses
        total_guesses = 0
        is_playing = True
        show_status(False)
        while is_playing:
            chosen = input(DICTIONARY[language]["msgChoice"]).strip().lower()[:1]
            if not re.match("^[a-zA-Z]$", chosen):
                print(f"{DICTIONARY[language]['msgLegalPrompter']}\n")
                continue
            if chosen in correct:
                print(f"{DICTIONARY[language]['msgChosen']}{RESET}\n")
            else:
                wrong_guess = False
                if chosen in word:
                    for i, char in enumerate(word):
                        if char == chosen:
                            status[i] = f"{GREEN}{chosen}{RESET}"
                else:
                    mistake.append(chosen)
                    wrong_guess = True
                correct.append(chosen)

                if len(mistake) == len(HANGMAN_UI) - 1:
                    print("GAME OVER!")
                    is_playing = False
                elif "_" not in status:
                    print(f"{DICTIONARY[language]['msgWin']}{RESET}\n")
                    is_playing = False
            
                total_guesses += 1
            show_status(wrong_guess if 'wrong_guess' in locals() else False)
        return total_guesses

    total_guesses = hangman_game()
    stat_trackers.append(total_guesses)
    response = input(DICTIONARY[language]["msgPlayAgain"]).strip().lower()
    play_again = response.strip().lower().startswith('y')

print(f"{DICTIONARY[language]['msgTotalGuess']} {sum(stat_trackers)} {DICTIONARY[language]['msgTimes']}.")
print(f"{DICTIONARY[language]['msgTotalRounds']} {rounds_played} {DICTIONARY[language]['msgRounds']}.")

sys.exit(0)