# Author:   Tomáš Kožár, xkozar02
#           Faculty of Information Technology, Brno University of Technology
# Bachelor's Thesis: Parsing for ET0L systems

from ruleReaderET0L import RuleReader
from pprint import pprint

class ET0LGenerator:

    def __init__(self, ruleFile):
        self.reader = RuleReader(ruleFile)
        self.rules = self.reader.getRulesDictionary()
        self.results = set()
        self.rawResults = set()
        self.wordStack = []
        self.indexStack = []
        self.ruleStack = []

    def printResults(self):
        temp = list(self.results)
        temp.sort()
        for x in temp:
            print(x)

    def possibleRuleApplication(self, word, ruleSet):
        for x in word:
            if ruleSet.get(x, []) != []:
                return True
        return False

    def generateFinal(self, w):
        newWordStack = []
        finalRuleStack = []
        for x in self.rules:
            newWordStack.append(w)
            finalRuleStack.append(x)

        while newWordStack.__len__() != 0:
            word = newWordStack.pop()
            ruleSet = finalRuleStack.pop()
            if(word.islower()):
                self.results.add(word)
                return

            for letterIndex in range(word.__len__()):
                if not word[letterIndex].islower():
                    for rule in ruleSet.get(word[letterIndex], []):
                        if rule.islower():
                            newWord = word[0:letterIndex] + rule + word[letterIndex+1:word.__len__()]
                            for x in self.rules:
                                newWordStack.append(newWord)
                                finalRuleStack.append(x)

    def finalizeWords(self):
        for x in self.rawResults:
            self.generateFinal(x)

    def generateWords(self, length):
        for x in self.rules:
            self.wordStack.append("S")
            self.indexStack.append(0)
            self.ruleStack.append(x)
            
        while self.wordStack.__len__() != 0:
            word = self.wordStack.pop()
            index = self.indexStack.pop()
            ruleSet = self.ruleStack.pop()

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
                self.rawResults.add(word)
                continue

            # skip terminals since no rule can be applied
            if word[index].islower():
                self.wordStack.append(word)
                self.indexStack.append((index + 1) % word.__len__())
                self.ruleStack.append(ruleSet)
            else:
                for rule in ruleSet.get(word[index], []):
                    newWord = word[0:index] + rule + word[index+1:word.__len__()]
                    if (index + rule.__len__()) % newWord.__len__() == 0:
                        for x in self.rules:
                            self.wordStack.append(newWord)
                            self.indexStack.append((index + rule.__len__()) % newWord.__len__())
                            self.ruleStack.append(x)
                    else: 
                        self.wordStack.append(newWord)
                        self.indexStack.append((index + rule.__len__()) % newWord.__len__())
                        self.ruleStack.append(ruleSet)

    def generate(self, length):
        self.generateWords(length)
        self.finalizeWords()
        return self.results

# print(ET0LGenerator("testRulesET0L.txt").generate(4))