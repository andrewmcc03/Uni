# 1.3 Hangman PICKLED

import random
import pickle

def replace_all(guess, word, letter):
    for pos in range(len(guess)):
        if word[pos] == letter:
            guess = guess[:pos] + letter + guess[pos+1:]
    return guess

def get_words(number_of_letters):
    words_found=[]
    fin = open("words.txt")
    for line in fin:
        word = line.strip()
        if len(word) == number_of_letters:
            words_found.append(word)
    fin.close()		
    return words_found

#Load high score dictionary
try:
    fin = open("hangman_scores.pkl", "rb")
    scores = pickle.load(fin)
    fin.close()
except FileNotFoundError:
    scores = {}


number_of_letters = int(input("Enter word length: "))
words = get_words(number_of_letters)
print("There are {} words with {} letters".format(len(words), number_of_letters))

guess_word = words[random.randint(0, len(words) - 1)]

print("\nGuessing the word: {}".format(guess_word))

available_letters = "abcdefghijklmnopqrstuvwxyz"

lives = 6
guess_string = "_" * number_of_letters
while lives > 0:
    print("\nLetters available: {}".format(available_letters))
    this_letter = input("Guess a letter: ")

    if this_letter in available_letters:
        available_letters = available_letters.replace(this_letter, "_")

    if this_letter in guess_word:
        guess_string = replace_all(guess_string, guess_word, this_letter)
        if guess_string == guess_word:
            print("You guessed the word!")
            break
    else:
        lives = lives-1
        print("Letter not found - lives remaining: {}".format(lives))
    print(guess_string)

if lives > 0:
    player = input("Enter player name: ").strip()
    score = lives * number_of_letters

    #Add score to player's existing score in dictionary
    player_key = player.lower()

    if player_key in scores:
        scores[player_key] += score
    else:
        scores[player_key] = score

    #Pickle updated dictionary to file
    fout = open("hangman_scores.pkl", "wb")
    pickle.dump(scores, fout)

    fout.close()


    print("\nScore saved!\n")

    #Unpickle the dictionary and print it to the console
    outputPKLfile = open('hangman_scores.pkl', 'rb')
    print(pickle.load(outputPKLfile))
    outputPKLfile.close()


    # fout = open("hangman_scores.txt", "a")
    
    # new_score_text = "{}, {}\n".format(player, score)
    # fout.write(new_score_text)
    # fout.close()


if lives == 0:
    print("\nYou lost! The word was: {}".format(guess_word))