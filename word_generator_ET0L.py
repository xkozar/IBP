from ruleReaderET0L import RuleReader
from pprint import pprint

reader = RuleReader("rules.txt")
rules = reader.contentToPairs()
rawResults = set()
results = set()

wordStack = []
indexStack = []
ruleStack = []

def printResults():
    global results
    temp = list(results)
    temp.sort()
    for x in temp:
        print(x)

def generateFinal(w):
    global results
    for x in rules:
        newWordStack = []
        newWordStack.append(w)
        finalRuleStack = []
        finalRuleStack.append(x)

    while newWordStack.__len__() != 0:
        word = newWordStack.pop()
        ruleSet = finalRuleStack.pop()
        if(word.islower()):
            results.add(word)
            return

        for letterIndex in range(word.__len__()):
            if not word[letterIndex].islower():
                # print(word[letterIndex], "IS NOT LOWER!!!")
                for rule in ruleSet.get(word[letterIndex], []):
                    if rule.islower():
                        newWord = word[0:letterIndex] + rule + word[letterIndex+1:word.__len__()]
                        for x in rules:
                            newWordStack.append(newWord)
                            finalRuleStack.append(x)


def finalizeWords():
    global rawResults
    for x in rawResults:
        generateFinal(x)

def generateWords():
    global rawResults
    for x in rules:
        wordStack.append("S")
        indexStack.append(0)
        ruleStack.append(x)
        
    length = 10

    while wordStack.__len__() != 0:
        word = wordStack.pop()
        index = indexStack.pop()
        ruleSet = ruleStack.pop()

        # word without non-terminal that is not right length
        if word.islower() and word.__len__() != length:
            continue
        # index that is too big
        if index > word.__len__():
            continue
        # word that is too long
        if word.__len__() > length:
            continue
        # word of right size and is generated in paralel
        if word.__len__() == length and index == 0:
            rawResults.add(word)
            continue

        # skip terminals since no rule can be applied
        if word[index].islower():
            wordStack.append(word)
            indexStack.append((index + 1) % word.__len__())
            ruleStack.append(ruleSet)
        else:
            for rule in ruleSet.get(word[index], []):
                newWord = word[0:index] + rule + word[index+1:word.__len__()]
                for x in rules:
                    wordStack.append(newWord)
                    indexStack.append((index + rule.__len__()) % newWord.__len__())
                    ruleStack.append(x)

generateWords()
finalizeWords()
printResults()
