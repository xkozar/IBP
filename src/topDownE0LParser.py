# Author:   Tomáš Kožár, xkozar02
#           Faculty of Information Technology, Brno University of Technology
# Bachelor's Thesis: Parsing for ET0L systems

from ruleReader import RuleReader
from pprint import pprint
import itertools

class TopDownE0LParser:

    def __init__(self, ruleFile):
        self.reader = RuleReader(ruleFile)
        self.rules = self.reader.getRulesDictionary()
        self.generatedWords = set()
        self.falseWords = set()
        self.wordStack = []
        self.indexStack = []
        self.historyStack = []
        self.mustChangeStack = []

    # Prints all generated valid words
    def printResults(self):
        temp = list(self.generatedWords)
        temp.sort()
        for x in temp:
            print(x)

    # Generates all possible words of max length
    def generateWords(self, length, startWord="S", parseWord=None):
        self.wordStack.append(startWord)
        self.indexStack.append(0)
        self.historyStack.append(set())
        self.mustChangeStack.append(False)

        while self.wordStack.__len__() != 0:
            word = self.wordStack.pop(0)
            index = self.indexStack.pop(0)
            historyWords = self.historyStack.pop(0)
            mustChange = self.mustChangeStack.pop(0)

            # '-' that represents epsilon can only be deleted
            # on start of derivation step
            if index == 0:
                word = word.replace("-", "")
            # Empty word
            if word.__len__() == 0:
                continue
            # Loop detection
            if word in historyWords and index == 0 and not mustChange:
                continue
            # Index is out of bounds
            if index > word.__len__():
                continue
            # Word is too long even without '-' that can be deleted
            if word.replace("-", "").__len__() > length:
                continue
            # Valid word
            if index == 0 and word.islower() and not mustChange:
                if parseWord != None and word == parseWord:
                    return True
                self.generatedWords.add(word)

            # Rule application
            ruleFound = self.rules.get(word[index], [])
            if ruleFound != []:
                # No rule found, throw away word
                for rule in ruleFound:
                    newWord = word[0:index] + rule + word[index+1:word.__len__()]
                    self.wordStack.append(newWord)
                    self.indexStack.append((index + rule.__len__()) % newWord.__len__())
                    if index == 0 and not mustChange:
                        historyWords.add(word)
                    self.historyStack.append(historyWords.copy())
                    self.mustChangeStack.append(rule == "")

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
    def generateValidWords(self, length, startWord="S"):
        self.generateWords(length)
        
        return self.generatedWords
    
    # Parse word
    def parse(self, word, startWord="S"):
        if self.generateWords(word.__len__(), word, startWord) == True:
            return True
        return False
