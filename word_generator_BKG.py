from ruleReader import RuleReader
from pprint import pprint


reader = RuleReader("rules.txt")
rules = reader.contentToPairs()

def generateFinal(word):
    if(word.islower()):
        print(word)
        return

    for letterIndex in range(word.__len__()):
        if not word[letterIndex].islower():
            # print(word[letterIndex], "IS NOT LOWER!!!")
            for rule in rules.get(word[letterIndex], []):
                if rule.islower():
                    newWord = word[0:letterIndex] + rule + word[letterIndex+1:word.__len__()]
                    generateFinal(newWord)

def generateWords(word, length):
    if(word.__len__() == length):
        # print("---", word)
        generateFinal(word)
        return
    for letterIndex in range(word.__len__()):
        for rule in rules.get(word[letterIndex], []):
            newWord = word[0:letterIndex] + rule + word[letterIndex+1:word.__len__()]
            generateWords(newWord, length)

generateWords("S", 4)
