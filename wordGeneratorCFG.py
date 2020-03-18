from ruleReader import RuleReader
from pprint import pprint

class ContextFreeGrammarGenerator:

    def __init__(self, ruleFile):
        self.reader = RuleReader(ruleFile)
        self.rules = self.reader.contentToPairs()
        self.results = set()

    def printResults(self):
        for x in self.results:
            print(x)

    def generateFinal(self, word):
        if(word.islower()):
            # print(word)
            self.results.add(word)
            return

        for letterIndex in range(word.__len__()):
            if not word[letterIndex].islower():
                # print(word[letterIndex], "IS NOT LOWER!!!")
                for rule in self.rules.get(word[letterIndex], []):
                    if rule.islower():
                        newWord = word[0:letterIndex] + rule + word[letterIndex+1:word.__len__()]
                        self.generateFinal(newWord)

    def generateWords(self, word, length):
        if(word.__len__() == length):
            self.generateFinal(word)
            return
        for letterIndex in range(word.__len__()):
            for rule in self.rules.get(word[letterIndex], []):
                newWord = word[0:letterIndex] + rule + word[letterIndex+1:word.__len__()]
                self.generateWords(newWord, length)

    def generate(self, length):
        self.generateWords("S", length)
        return self.results

# TODO rewrite to iteration
# ContextFreeGrammarGenerator("rules.txt").generate(4)