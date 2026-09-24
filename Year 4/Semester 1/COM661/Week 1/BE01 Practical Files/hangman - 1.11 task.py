# 1.11 Hangman enhanced - extra task

import random

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
    player = input("Enter player name: ")
    score = lives * number_of_letters

    #Read existing scores
    scores = {} #Dictionary for names and scores
    try:
        fout = open("hangman_scores.txt", "r")
        for line in fout:
            searchName = line.strip().split(",")
            if len(searchName) == 2:
                name = searchName[0].strip()
                old_score = int(searchName[1].strip())
                scores[name.lower()] = [name, old_score]
            #if searchName[0] == player.strip().lower():
            #    print("\nPlayer name already exists - old score overwritten!")
        fout.close()
            
    except FileNotFoundError:
        pass

    #Output current
    #print("\nPlayer: {}".format(player))
    #print("Score: {}".format(score))

    #Add new score to player's existing score
    player_key = player.strip().lower()
    if player_key in scores:
        scores[player_key][1] += score
    else:
        scores[player_key] = [player.strip(), score]

    #Rewrite file
    fout = open("hangman_scores.txt", "w")

    for name, score in scores.values():
        fout.write("{}, {}\n".format(name, score))
    fout.close()

    print("Score saved!")


    # fout = open("hangman_scores.txt", "a")
    
    # new_score_text = "{}, {}\n".format(player, score)
    # fout.write(new_score_text)
    # fout.close()


if lives == 0:
    print("\nYou lost! The word was: {}".format(guess_word))