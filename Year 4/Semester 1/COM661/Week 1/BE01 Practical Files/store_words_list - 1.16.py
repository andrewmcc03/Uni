import random

all_words = []
fin = open("words.txt")
for line in fin:
    word = line.strip()
    all_words.append(word)
fin.close()		

words_list = []
for _ in range(26):
    words_list.append([])

for _ in range(50):
    random_word = all_words[ random.randint(0, len(all_words) - 1) ]
    words_list[ ord(random_word[0]) - ord('a') ].append(random_word)

letters = "abcdefghijklmnopqrstuvwxyz"
for i in range(26):
    print(letters[i], words_list[i], '\n')

for i in range(3):
    ##print(words_list)
    userInput = input(str("Attempt " + str(i + 1) + " of 3 - Please enter a search word: "))

    if(userInput in words_list[ord(userInput[0]) - ord('a')]):
        print("FOUND")
    else:
        print("NOT FOUND")