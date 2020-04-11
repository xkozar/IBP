# Author:   Tomáš Kožár, xkozar02
#           Faculty of Information Technology, Brno University of Technology
# Bachelor's Thesis: Parsing for ET0L systems

from ruleReader import RuleReader
from pprint import pprint

class ContextFreeGrammarGenerator:

    def __init__(self, ruleFile):
        self.reader = RuleReader(ruleFile)
        self.rules = self.reader.getRulesDictionary()
        self.results = set()
        self.newWordStack = []

    def printResults(self):
        for x in self.results:
            print(x)

    def generateWords(self, w, length):
        self.newWordStack.append(w)

        while self.newWordStack.__len__() > 0:
            word = self.newWordStack.pop(0)
            if(word.__len__() > length):
                continue
            if(word.__len__() == length and word.islower()):
                self.results.add(word)
                continue
            for letterIndex in range(word.__len__()):
                for rule in self.rules.get(word[letterIndex], []):
                    newWord = word[0:letterIndex] + rule + word[letterIndex+1:word.__len__()]
                    if newWord not in self.newWordStack:
                        self.newWordStack.append(newWord)

    def generate(self, length):
        self.generateWords("S", length)
        return self.results

print(ContextFreeGrammarGenerator("testRules.txt").generate(10))
