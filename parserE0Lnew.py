# Author:   Tomáš Kožár, xkozar02
#           Faculty of Information Technology, Brno University of Technology
# Bachelor's Thesis: Parsing for ET0L systems

from ruleReader import RuleReader
from pprint import pprint
import copy

class E0LParser:

    def __init__(self, word, rules):
        self.word = word
        self.reader = RuleReader(rules)
        self.rules = self.reader.contentToRules(True)
        self.table = [[set() for i in range(word.__len__())] for j in range(word.__len__())]
        self.new_table = [[set() for i in range(word.__len__())] for j in range(word.__len__())]
        self.modified = True # Determines whether rules table was modified
        self.tableHistory = []
        self.emptyRules = set()
        self.fillEmptyRules()

    def fillEmptyRules(self):
        tempEmptyRules = self.findRule("-")
        emptyChanged = True

        while emptyChanged:
            emptyChanged = False
            updateEmptySet = set()
            for empty in tempEmptyRules:
                newEmpty = self.findRule(empty)
                if tempEmptyRules.intersection(newEmpty).__len__() < newEmpty.__len__():
                    emptyChanged = True
                    updateEmptySet.update(newEmpty)
            tempEmptyRules.update(updateEmptySet)

            for empty1 in tempEmptyRules:
                for empty2 in tempEmptyRules:
                    newEmpty = self.findRule(empty1 + empty2)
                    if tempEmptyRules.intersection(newEmpty).__len__() < newEmpty.__len__():
                        emptyChanged = True
                        updateEmptySet.update(newEmpty)
            tempEmptyRules.update(updateEmptySet)

            self.emptyRules.update(tempEmptyRules)

        print(self.emptyRules)

    def compareTables(self, tab1, tab2):
        for row1, row2 in zip(tab1, tab2):
            for cell1, cell2 in zip(row1, row2):
                if cell1.__len__() != cell2.__len__():
                    return False
                for val in cell1:
                    if val not in cell2:
                        return False
        return True

    def findInHistory(self, table):
        for t in self.tableHistory:
            if self.compareTables(table, t):
                return True
        return False

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

    def fillStart(self, word, table):
        for diag, character in enumerate(self.word):
            table[diag][diag] = self.findRule(character)

    def findRule(self, rightSide):
        result = set()
        for leftSide in self.rules:
            if rightSide in self.rules[leftSide]:
                result.add(leftSide)
        return result

    def findPartialRule(self, rightSide):
        result = set()
        for leftSide in self.rules:
            for rule in self.rules[leftSide]:
                if rightSide in rule and rule.__len__() ==  2:
                    result.add(leftSide)
        return result

    def reduceRules(self, row, column, nTerminal):
        if nTerminal == "":
            return
        unaryRuleFound = self.findRule(nTerminal)

        
        for unaryRule in unaryRuleFound:
            if nTerminal in self.table[row][column]:
                self.modified = True
                self.new_table[row][column].update(unaryRule)

        if nTerminal in self.table[row][column]:
            for first in set(nTerminal) | self.emptyRules:
                for second in set(nTerminal) | self.emptyRules:
                    if first in self.table[row][column] or second in self.table[row][column]:
                        rule = self.findRule(first + second)
                        self.modified = True
                        self.new_table[row][column].update(rule)


        if column == self.word.__len__()-1:
            return

        for col, tRules in enumerate(self.table[column+1] + [self.emptyRules]):
            if tRules == '':
                continue
            for nTerm in tRules:
                result = self.findRule(nTerminal + nTerm)
                for character in result:
                    if not character in self.table[row][col]:
                        self.new_table[row][col].add(character)
                        self.modified = True

    def parse(self): 
        print("Word: " + self.word)
        self.fillStart(self.word, self.table)

        while self.modified:
            self.modified = False
            self.printTable()
            for idr, row in enumerate(self.table):
                for idc, tableRules in enumerate(row):
                    if(tableRules is '' or idc < idr):
                        continue
                    for nonTerminal in tableRules | self.emptyRules:
                        self.reduceRules(idr, idc, nonTerminal)

            self.table = copy.deepcopy(self.new_table)
            self.new_table = [[set() for i in range(self.word.__len__())] for j in range(self.word.__len__())]

            if "S" in self.table[0][self.word.__len__()-1]:
                self.printTable()
                return True
            
            if self.findInHistory(self.table):
                print("Loop detected")
                return False
            self.tableHistory.append(self.table)
        return False

print(E0LParser("bcbc", "testRules.txt").parse())
