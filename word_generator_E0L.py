from ruleReader import RuleReader
from pprint import pprint

reader = RuleReader("rules.txt")
rules = reader.contentToPairs()
rawResults = set()
results = set()

wordStack = []
indexStack = []

def printResults():
    global results
    temp = list(results)
    temp.sort()
    for x in temp:
        print(x)

def generateFinal(w):
    global results
    newWordStack = []
    newWordStack.append(w)

    while newWordStack.__len__() != 0:
        word = newWordStack.pop()
        if(word.islower()):
            results.add(word)
            return

        for letterIndex in range(word.__len__()):
            if not word[letterIndex].islower():
                # print(word[letterIndex], "IS NOT LOWER!!!")
                for rule in rules.get(word[letterIndex], []):
                    if rule.islower():
                        newWord = word[0:letterIndex] + rule + word[letterIndex+1:word.__len__()]
                        newWordStack.append(newWord)


def finalizeWords():
    global rawResults
    for x in rawResults:
        generateFinal(x)

def generateWords():
    global rawResults
    wordStack.append("S")
    indexStack.append(0)
    length = 10

    while wordStack.__len__() != 0:
        word = wordStack.pop()
        index = indexStack.pop()

        if word.islower() and word.__len__() != length:
            continue
        if index > word.__len__():
            continue
        if word.__len__() > length:
            continue
        if word.__len__() == length and index == 0:
            # print("---", word)
            rawResults.add(word)
            continue

        if word[index].islower():
            wordStack.append(word)
            indexStack.append((index + 1) % word.__len__())
        else:
            for rule in rules.get(word[index], []):
                newWord = word[0:index] + rule + word[index+1:word.__len__()]
                wordStack.append(newWord)
                indexStack.append((index + rule.__len__()) % newWord.__len__())

generateWords()
finalizeWords()
printResults()
