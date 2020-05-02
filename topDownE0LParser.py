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

    def possibleRuleApplication(self, word):
        for x in word:
            if self.rules.get(x, []) != []:
                return True
        return False

    def printResults(self):
        temp = list(self.generatedWords)
        temp.sort()
        for x in temp:
            print(x)

    def generateWords(self, length, startWord="S", parseWord=None):
        self.wordStack.append(startWord)
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
                self.generatedWords.add(word)
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

        return result - self.generatedWords

    def generate(self, length, startWord="S"):
        self.generateWords(length)
        
        return (self.generatedWords, self.generateFalseWords(length))

    def parse(self, word, startWord="S"):
        if self.generateWords(word.__len__(), word, startWord) == True:
            return True
        return False

# print(TopDownE0LParser("testRules.txt").generate(4))
