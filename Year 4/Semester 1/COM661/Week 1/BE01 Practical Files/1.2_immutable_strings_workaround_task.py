name = input(str("Enter name: "))

nameList = list(name)

#print(nameList)

slotToBeReplaced = int(input("Enter character slot to be replaced (1-" + str(len(nameList)) + "): ")) - 1  # input will be 1 > index value
replacementChar = input("Enter replacement character: ")

nameList[slotToBeReplaced] = replacementChar

#print(nameList)

name = ''.join(nameList)

print(name)

#FIN

# ref: https://stackoverflow.com/questions/41752946/replacing-a-character-from-a-certain-index