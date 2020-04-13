# Author:   Tomáš Kožár, xkozar02
#           Faculty of Information Technology, Brno University of Technology
# Bachelor's Thesis: Parsing for ET0L systems

from ruleReader import RuleReader
from pprint import pprint

class E0LGenerator:

    def __init__(self, ruleFile):
        self.reader = RuleReader(ruleFile)
        self.rules = self.reader.getRulesDictionary()
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
            if word.__len__() == length and index == 0 and word.islower():
                # print("---", word)
                self.results.add(word)
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
        return self.results

# print(E0LGenerator("testRules.txt").generate(40))
