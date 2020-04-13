# Author:   Tomáš Kožár, xkozar02
#           Faculty of Information Technology, Brno University of Technology
# Bachelor's Thesis: Parsing for ET0L systems

from ruleReader import RuleReader
from pprint import pprint
import sys

class ContextFreeGrammarParser:

    def __init__(self, word, rules):
        self.word = word
        self.reader = RuleReader(rules)
        self.rules = self.reader.contentToRules(True)
        self.table = [['' for i in range(word.__len__())] for j in range(word.__len__())]
        self.modified = True # Determines whether rules table was modified

    def printTable(self):
        temp = self.table.copy()
        temp.reverse()
        
        sizeTemplate = []
        for col in zip(*temp):
            sizeTemplate.append(max(col, key=len).__len__())

        for row in temp:
            rowToPrint = ""
            print("[", end="")
            for y, value in enumerate(row):
                if y != 0 and y != row.__len__():
                    print("|", end="")
                spacePadding = (sizeTemplate[y] - value.__len__()) * " "
                print(" " + value + spacePadding + " ", end="")
            print("]")

    def findRule(self, rightSide):
        result = ''
        for leftSide in self.rules:
            if rightSide in self.rules[leftSide]:
                result = result + leftSide
        
        return(result)

    def findPairForRule(self, row, column, nTerminal):
        if column == self.word.__len__()-1:
            return

        for col, tRules in enumerate(self.table[column+1]):
            if tRules == '':
                continue
            for nTerm in tRules:
                result = self.findRule(nTerminal + nTerm)
                # if result == '':
                #     continue
                for character in result:
                    if self.table[row][col].find(character) < 0:
                        self.table[row][col] = self.table[row][col] + character
                        self.modified = True

    def parse(self):
        for i in range(self.word.__len__()):
            for lSide in self.rules:
                if self.word[i] in self.rules[lSide]:
                    self.table[i][i] = self.table[i][i] + lSide

        while self.modified:
            self.modified = False
            self.printTable()
            print('-----------------------------------------')
            for idr, row in enumerate(self.table):
                for idc, tableRules in enumerate(row):
                    if(tableRules is not ''):
                        for nonTerminal in tableRules:
                            self.findPairForRule(idr, idc, nonTerminal)

            print('end of loop')

        self.printTable()
        if self.table[0][self.word.__len__()-1].find('S') >= 0:
            return True
        else:
            return False

