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

print("Guessing the word: {}".format(guess_word))

lives = 6
guess_string = "_" * number_of_letters
while lives > 0:
    this_letter = input("Guess a letter: ")
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
    fout = open("hangman_scores.txt", "a")
    score = lives * number_of_letters
    new_score_text = "{}, {}\n".format(player, score)
    fout.write(new_score_text)
    fout.close()