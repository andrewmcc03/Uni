while True:
    letters = input("Enter 3 letters: ").strip().lower()
    if len(letters) == 3 and letters.isalpha():
        break
    print("Please enter exactly 3 letters.")

# File IN (read in)
fin = open("words.txt", "r")
# File OUT (output)
fout = open("letters.txt", "w")
for line in fin:    # For each line in the input file (fin)...
    word = line.strip()
    word_letters = iter(word.lower())

    if all(letter in word_letters for letter in letters):
        fout.write(word + "\n")


# Close the files
fin.close()
fout.close()

#Output letters.txt
outputResult = open("letters.txt", "r")
print(outputResult.read())

outputResult.close()