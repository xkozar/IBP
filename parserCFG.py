# Author:   Tomáš Kožár, xkozar02
#           Faculty of Information Technology, Brno University of Technology
# Bachelor's Thesis: Parsing for ET0L systems

from ruleReader import RuleReader
from pprint import pprint
import sys

class CFGParserCYK:

    def __init__(self, word, rules):
        self.word = word
        self.reader = RuleReader(rules)
        self.rules = self.reader.contentToRules(True)
        self.table = [[set() for i in range(word.__len__())] for j in range(word.__len__())]
        self.modified = True # Determines whether rules table was modified

    def printTable(self):
        temp = self.table.copy()
        temp.reverse()
        
        sizeTemplate = []
        for col in zip(*temp):
            sizeTemplate.append(max(col, key=len).__len__())

        for x, row in enumerate(temp):
            rowToPrint = ""
            rowToPrint += "["
            for y, value in enumerate(row):
                if y != 0 and y != row.__len__():
                    rowToPrint += "|"
                spacePadding = (sizeTemplate[y] - value.__len__()) * " "
                cellValue = ""
                for val in value:
                    cellValue = cellValue + val
                rowToPrint += " " + cellValue + spacePadding + " "
            rowToPrint += "]"
            if x == 0:
                print()
            print(rowToPrint)
            if x == row.__len__() - 1:
                print(rowToPrint.__len__() * "_")

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
                    if not character in self.table[row][col]:
                        self.table[row][col].add(character)
                        self.modified = True

    def parse(self):
        for i in range(self.word.__len__()):
            for lSide in self.rules:
                if self.word[i] in self.rules[lSide]:
                    self.table[i][i].add(lSide)

        while self.modified:
            self.modified = False
            self.printTable()
            for idr, row in enumerate(self.table):
                for idc, tableRules in enumerate(row):
                    if(tableRules is not ''):
                        for nonTerminal in tableRules:
                            self.findPairForRule(idr, idc, nonTerminal)

        # self.printTable()
        if "S" in self.table[0][self.word.__len__()-1]:
            return True
        else:
            return False

