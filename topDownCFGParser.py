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

    # Prints all generated valid words
    def printResults(self):
        for x in self.results:
            print(x)

    # Generates all possible words of max length
    def generateWords(self, startWord, length, parseWord = None):
        self.newWordStack.append(startWord)

        while self.newWordStack.__len__() > 0:
            word = self.newWordStack.pop(0)
            # Generated word too long
            if(word.__len__() > length):
                continue
            # Generated word is valid
            if(word.islower()):
                # If function is in parse mode
                if parseWord != None and word == parseWord:
                    return True
                self.results.add(word)
                continue
            # Apply rule to each symbol
            for letterIndex in range(word.__len__()):
                for rule in self.rules.get(word[letterIndex], []):
                    newWord = word[0:letterIndex] + rule + word[letterIndex+1:word.__len__()]
                    if newWord not in self.newWordStack:
                        self.newWordStack.append(newWord)

    # Returns set of all terminals from rules
    def getAllTerminals(self):
        terminals = set()

        for rule in self.rules:
            if rule.islower():
                terminals.add(rule)
            for symbol in self.rules[rule]:
                if symbol.islower():
                    terminals.add(symbol)
        return terminals

    # Returns all combinations of terminals of some length
    def generateAllCombinations(self, length):
        terminals = self.getAllTerminals()

        result = set()
        for generationLength in range(1, length + 1):
            for x in itertools.product(list(terminals), repeat=generationLength):
                result.add(''.join(x))

        return result

    # Returns all valid words of max length
    def generateValidWords(self, length):
        self.generateWords("S", length)
        return self.results

    # Parse word
    def parse(self, word, startWord="S"):
        if self.generateWords(startWord, word.__len__(), word) == True:
            return True
        return False

# print(ContextFreeGrammarGenerator("testRules.txt").generate(4))
