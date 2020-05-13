# Author:   Tomáš Kožár, xkozar02
#           Faculty of Information Technology, Brno University of Technology
# Bachelor's Thesis: Parsing for ET0L systems

from ruleReader import RuleReader
from pprint import pprint
import itertools

class TopDownCFGParser:

    def __init__(self, ruleFile):
        self.reader = RuleReader(ruleFile)
        self.rules = self.reader.getRulesDictionary()
        self.results = set()
        self.newWordStack = []

    def printResults(self):
        for x in self.results:
            print(x)

    def generateWords(self, startWord, length, parseWord = None):
        self.newWordStack.append(startWord)

        while self.newWordStack.__len__() > 0:
            word = self.newWordStack.pop(0)
            if(word.__len__() > length):
                continue
            if(word.islower()):
                if parseWord != None and word == parseWord:
                    return True
                self.results.add(word)
                continue
            for letterIndex in range(word.__len__()):
                for rule in self.rules.get(word[letterIndex], []):
                    newWord = word[0:letterIndex] + rule + word[letterIndex+1:word.__len__()]
                    if newWord not in self.newWordStack:
                        self.newWordStack.append(newWord)

    def getAllTerminals(self):
        terminals = set()

        for rule in self.rules:
            if rule.islower():
                terminals.add(rule)
            for symbol in self.rules[rule]:
                if symbol.islower():
                    terminals.add(symbol)
        return terminals

    def generateAllCombinations(self, length):
        terminals = self.getAllTerminals()

        result = set()
        for generationLength in range(1, length + 1):
            for x in itertools.product(list(terminals), repeat=generationLength):
                result.add(''.join(x))

        return result

    def generateValidWords(self, length):
        self.generateWords("S", length)
        return self.results

    def parse(self, word, startWord="S"):
        if self.generateWords(startWord, word.__len__(), word) == True:
            return True
        return False

# print(ContextFreeGrammarGenerator("testRules.txt").generate(4))
