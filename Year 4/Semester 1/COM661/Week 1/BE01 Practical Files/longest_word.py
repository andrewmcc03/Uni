fin = open("words.txt", "r")
biggest, num_of_words=0, 0
for line in fin:
    word = line.strip()
    num_of_words = num_of_words + 1
    if len(word) > biggest:
        biggest = len(word)

print("The longest of the {} words contains {} characters".format(num_of_words, biggest))

fin.seek(0)
fout = open("biggest.txt", "w")
for line in fin:
    word = line.strip()
    if len(word) == biggest:
        output = word + "\n"
        fout.write(output)
        print(word)  
        
fin.close()		
fout.close()
