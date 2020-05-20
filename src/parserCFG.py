# Author:   Tomáš Kožár, xkozar02
#           Faculty of Information Technology, Brno University of Technology
# Bachelor's Thesis: Parsing for ET0L systems

from ruleReader import RuleReader
from pprint import pprint
import sys

class CFGParserCYK:

    def __init__(self, rules):
        self.word = ""
        self.reader = RuleReader(rules)
        self.rules = self.reader.contentToRules(True)
        self.initializeBeginState()

    # Reset all variables that could be modified when parse was lastly run
    def initializeBeginState(self):
        self.modified = True # Determines whether rules table was modified
        self.table = [[set() for i in range(self.word.__len__())] for j in range(self.word.__len__())]

    # Formats CYK table nicely
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

    # Find all symbols that can be rewriten to passed argument
    def findRule(self, rightSide):
        result = ''
        for leftSide in self.rules:
            if rightSide in self.rules[leftSide]:
                result = result + leftSide
        
        return(result)

    # Does reduction of rules for symbol on [row, col] position
    def reduceRules(self, row, column, nTerminal):
        # Invalid column
        if column == self.word.__len__()-1:
            return

        # Reduce normal pairs
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

    # Runs CYK algorithm for word
    def parse(self, word):
        self.word = word
        self.initializeBeginState()
        # Fill diagonal with non terminals
        for i in range(self.word.__len__()):
            for lSide in self.rules:
                if self.word[i] in self.rules[lSide]:
                    self.table[i][i].add(lSide)

        # Loop through table
        while self.modified:
            self.modified = False
            self.printTable()
            for idr, row in enumerate(self.table):
                for idc, tableRules in enumerate(row):
                    # Empty or invalid position
                    if(tableRules is '' or idc < idr):
                        continue
                    for nonTerminal in tableRules:
                        self.reduceRules(idr, idc, nonTerminal)

        # self.printTable()
        if "S" in self.table[0][self.word.__len__()-1]:
            return True
        else:
            return False

# print(CFGParserCYK("bcbc", "demo.txt").parse())
