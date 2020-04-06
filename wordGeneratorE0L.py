from ruleReader import RuleReader
from pprint import pprint

class E0LGenerator:

    def __init__(self, ruleFile):
        self.reader = RuleReader(ruleFile)
        self.rules = self.reader.contentToPairs()
        self.results = set()
        self.rawResults = set()
        self.wordStack = []
        self.indexStack = []

    def possibleRuleApplication(self, word):
        for x in word:
            if self.rules.get(x, []) != []:
                return True
        return False

    def printResults(self):
        temp = list(self.results)
        temp.sort()
        for x in temp:
            print(x)

    def generateFinal(self, w, length):
        newWordStack = []
        newWordStack.append(w)

        while newWordStack.__len__() != 0:
            word = newWordStack.pop()
            if(word.__len__() > length):
                continue
            if(word.islower()):
                self.results.add(word)
                continue


            for letterIndex in range(word.__len__()):
                if not word[letterIndex].islower():
                    # print(word[letterIndex], "IS NOT LOWER!!!")
                    for rule in self.rules.get(word[letterIndex], []):
                        if rule.islower():
                            newWord = word[0:letterIndex] + rule + word[letterIndex+1:word.__len__()]
                            newWordStack.append(newWord)


    def finalizeWords(self, length):
        for x in self.rawResults:
            self.generateFinal(x, length)

    def generateWords(self, length):
        self.wordStack.append("S")
        self.indexStack.append(0)

        while self.wordStack.__len__() != 0:
            word = self.wordStack.pop()
            index = self.indexStack.pop()

            if word.islower() and word.__len__() != length and not self.possibleRuleApplication(word):
                continue
            if index > word.__len__():
                continue
            if word.__len__() > length:
                continue
            if word.__len__() == length and index == 0:
                # print("---", word)
                self.rawResults.add(word)
                continue

            if self.rules.get(word[index], []) == []:
                print("hele", word[index])
                self.wordStack.append(word)
                self.indexStack.append((index + 1) % word.__len__())
            else:
                for rule in self.rules.get(word[index], []):
                    newWord = word[0:index] + rule + word[index+1:word.__len__()]
                    self.wordStack.append(newWord)
                    self.indexStack.append((index + rule.__len__()) % newWord.__len__())
                    

    def generate(self, length):
        self.generateWords(length)
        self.finalizeWords(length)
        return self.results

    

print(E0LGenerator("debug.txt").generate(4), "Hola")
