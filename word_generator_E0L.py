from ruleReader import RuleReader
from pprint import pprint


reader = RuleReader("rules.txt")
rules = reader.contentToPairs()
results = set()

def printResults():
    global results
    for x in results:
        print(x)

def generateFinal(word):
    global results
    if(word.islower()):
        # print(word)
        results.add(word)
        return

    for letterIndex in range(word.__len__()):
        if not word[letterIndex].islower():
            # print(word[letterIndex], "IS NOT LOWER!!!")
            for rule in rules.get(word[letterIndex], []):
                if rule.islower():
                    newWord = word[0:letterIndex] + rule + word[letterIndex+1:word.__len__()]
                    generateFinal(newWord)

def generateWords(word, length, index):
    if word.islower() and word.__len__() != length:
        return
    if index > word.__len__():
        return
    if word.__len__() == length and index == 0:
        print("---", word)
        generateFinal(word)
        return
    for letterIndex in range(index, word.__len__()):
        for rule in rules.get(word[letterIndex], []):
            newWord = word[0:letterIndex] + rule + word[letterIndex+1:word.__len__()]
            generateWords(newWord, length, (index + rule.__len__()) % newWord.__len__())
        else:
            generateWords(word, length, (index + 1) % word.__len__())


generateWords("AB", 4, 0)
#printResults()
