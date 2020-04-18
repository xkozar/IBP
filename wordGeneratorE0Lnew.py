# Author:   Tomáš Kožár, xkozar02
#           Faculty of Information Technology, Brno University of Technology
# Bachelor's Thesis: Parsing for ET0L systems

from ruleReader import RuleReader
from pprint import pprint
import itertools

class E0LGenerator:

    def __init__(self, ruleFile):
        self.reader = RuleReader(ruleFile)
        self.rules = self.reader.getRulesDictionary()
        self.results = set()
        self.falseWords = set()
        self.wordStack = []
        self.indexStack = []
        self.historyStack = []

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

    def generateWords(self, length, parseWord = None):
        self.wordStack.append("S")
        self.indexStack.append(0)
        self.historyStack.append(set())

        while self.wordStack.__len__() != 0:
            word = self.wordStack.pop()
            index = self.indexStack.pop()
            historyWords = self.historyStack.pop()

            if word in historyWords:
                continue
            if index > word.__len__():
                continue
            if word.__len__() > length:
                continue
            if index == 0 and word.islower():
                if parseWord != None and word == parseWord:
                    return True
                # print("---", word)
                self.results.add(word)
                continue

            if self.rules.get(word[index], []) == []:
                # No rule found, throw away word
                continue
            else:
                for rule in self.rules.get(word[index], []):
                    newWord = word[0:index] + rule + word[index+1:word.__len__()]
                    self.wordStack.append(newWord)
                    self.indexStack.append((index + rule.__len__()) % newWord.__len__())
                    historyWords.add(word)
                    self.historyStack.append(historyWords.copy())

    def getAllTerminals(self):
        terminals = set()

        for rule in self.rules:
            if rule.islower():
                terminals.add(rule)
            for symbol in self.rules[rule]:
                if symbol.islower():
                    terminals.add(symbol)
        return terminals

    def generateFalseWords(self, length):
        terminals = self.getAllTerminals()

        result = set()
        for x in itertools.product(list(terminals), repeat=length):
            result.add(''.join(x))

        return result - self.results

    def generate(self, length):
        self.generateWords(length)
        
        return [self.results, self.generateFalseWords(length)]

    def parse(self, word):
        if self.generateWords(word.__len__(), word) == True:
            return True
        return False

print(E0LGenerator("testRules.txt").generate(4))
