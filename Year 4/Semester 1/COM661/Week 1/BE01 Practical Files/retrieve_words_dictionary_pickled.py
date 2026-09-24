import pickle

fin = open("words_dictionary.txt", "rb")
words_dict = pickle.load(fin)
fin.close()

letters = "abcdefghijklmnopqrstuvwxyz"
for letter in letters:
    print(letter, words_dict[letter], '\n')