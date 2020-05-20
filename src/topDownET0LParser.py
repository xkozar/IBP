# Author:   Tomáš Kožár, xkozar02
#           Faculty of Information Technology, Brno University of Technology
# Bachelor's Thesis: Parsing for ET0L systems

from ruleReaderET0L import RuleReader
from pprint import pprint
import itertools

class TopDownET0LParser:

    def __init__(self, ruleFile):
        self.reader = RuleReader(ruleFile)
        self.rules = self.reader.getRulesDictionary()
        self.results = set()
        self.rawResults = set()
        self.wordStack = []
        self.indexStack = []
        self.ruleStack = []
        self.historyStack = []
        self.mustChangeStack = []

    # Prints all generated valid words
    def printResults(self):
        temp = list(self.results)
        temp.sort()
        for x in temp:
            print(x)

    # Generates all possible words of max length
    def generateWords(self, length, startWord="S", parseWord = None):
        for x in self.rules:
            self.wordStack.append(startWord)
            self.indexStack.append(0)
            self.ruleStack.append(x)
            self.historyStack.append(set())
            self.mustChangeStack.append(False)
            
        while self.wordStack.__len__() != 0:
            word = self.wordStack.pop(0)
            index = self.indexStack.pop(0)
            ruleSet = self.ruleStack.pop(0)
            historyWords = self.historyStack.pop(0)
            mustChange = self.mustChangeStack.pop(0)

            # '-' that represents epsilon can only be deleted
            # on start of derivation step
            if index == 0:
                word = word.replace("-", "")

            # Empty word
            if word.__len__() == 0:
                continue
            # Index that is too big
            if index > word.__len__():
                continue
            # Word that is too long
            if word.replace("-", "").__len__() > length:
                continue
            # Word of right size and is generated in paralel
            if index == 0 and word.islower() and not mustChange:
                if parseWord != None and word == parseWord:
                    return True
                self.results.add(word)
            # Loop detection
            if word in historyWords and index == 0 and not mustChange:
                continue
            if ruleSet.get(word[index], []) == []:
                # No rule, throw away
                continue
            else:
                # Rule application
                for rule in ruleSet.get(word[index], []):
                    newWord = word[0:index] + rule + word[index+1:word.__len__()]
                    if newWord.__len__() == 0:
                        continue
                    if (index + rule.__len__()) % newWord.__len__() == 0:
                        for x in self.rules:
                            self.wordStack.append(newWord)
                            self.indexStack.append((index + rule.__len__()) % newWord.__len__())
                            self.ruleStack.append(x)
                            if index == 0 and not mustChange:
                                historyWords.add(word)
                            self.historyStack.append(historyWords.copy())
                            self.mustChangeStack.append(rule == "-")

                    else: 
                        self.wordStack.append(newWord)
                        self.indexStack.append((index + rule.__len__()) % newWord.__len__())
                        self.ruleStack.append(ruleSet)
                        if index == 0 and not mustChange:
                            historyWords.add(word)
                        self.historyStack.append(historyWords.copy())
                        self.mustChangeStack.append(rule == "-")

    # Returns set of all terminals from rules
    def getAllTerminals(self, ruleSet):
        terminals = set()

        for rule in ruleSet:
            if rule.islower():
                terminals.add(rule)
            for symbol in ruleSet[rule]:
                if symbol.islower():
                    terminals.add(symbol)
        return terminals

    # Returns all combinations of terminals of some length
    def generateAllCombinations(self, length):
        terminals = set()
        for ruleSet in self.rules:    
            terminals = terminals | self.getAllTerminals(ruleSet)

        result = set()
        for generationLength in range(1, length + 1):
            for x in itertools.product(list(terminals), repeat=generationLength):
                result.add(''.join(x))

        return result

    # Returns all valid words of max length
    def generateValidWords(self, length, startWord="S"):
        self.generateWords(length, startWord=startWord)
        return self.results

    # Parse word
    def parse(self, word, startWord="S"):
        if self.generateWords(word.__len__(), word, startWord) == True:
            return True
        return False
