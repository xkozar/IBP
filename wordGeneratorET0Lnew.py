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
        self.historyStack = []

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

    def generateWords(self, length, parseWord = None):
        for x in self.rules:
            self.wordStack.append("S")
            self.indexStack.append(0)
            self.ruleStack.append(x)
            self.historyStack.append(set())
            
        while self.wordStack.__len__() != 0:
            word = self.wordStack.pop()
            index = self.indexStack.pop()
            ruleSet = self.ruleStack.pop()
            historyWords = self.historyStack.pop()

            # index that is too big
            if index > word.__len__():
                continue
            # word that is too long
            if word.__len__() > length:
                continue
            # word of right size and is generated in paralel
            if index == 0 and word.islower():
                if parseWord != None and word == parseWord:
                    return True
                self.results.add(word)
                continue
            if word in historyWords:
                continue
            if ruleSet.get(word[index], []) == []:
                # No rule, throw away
                continue
            else:
                for rule in ruleSet.get(word[index], []):
                    newWord = word[0:index] + rule + word[index+1:word.__len__()]
                    if (index + rule.__len__()) % newWord.__len__() == 0:
                        for x in self.rules:
                            self.wordStack.append(newWord)
                            self.indexStack.append((index + rule.__len__()) % newWord.__len__())
                            self.ruleStack.append(x)
                            historyWords.add(word)
                            self.historyStack.append(historyWords.copy())
                    else: 
                        self.wordStack.append(newWord)
                        self.indexStack.append((index + rule.__len__()) % newWord.__len__())
                        self.ruleStack.append(ruleSet)
                        historyWords.add(word)
                        self.historyStack.append(historyWords.copy())

    def generate(self, length):
        self.generateWords(length)
        return self.results

    def parse(self, word):
        if self.generateWords(word.__len__(), word) == True:
            return True
        return False

print(ET0LGenerator("demoET0L.txt").generate(10))
print(ET0LGenerator("demoET0L.txt").parse("aaaaaaaa"))