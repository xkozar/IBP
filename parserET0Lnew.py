# Author:   Tomáš Kožár, xkozar02
#           Faculty of Information Technology, Brno University of Technology
# Bachelor's Thesis: Parsing for ET0L systems

from ruleReaderET0L import RuleReader
from pprint import pprint
import copy

class ET0LParser:

    def __init__(self, word, rules):
        self.word = word
        self.reader = RuleReader(rules)
        self.rules = self.reader.contentToRules(True)
        self.emptyTable = [[set() for i in range(word.__len__())] for j in range(word.__len__())]
        self.new_table = [[set() for i in range(word.__len__())] for j in range(word.__len__())]

    def compareTables(self, tab1, tab2):
        for row1, row2 in zip(tab1, tab2):
            for cell1, cell2 in zip(row1, row2):
                if cell1.__len__() != cell2.__len__():
                    return False
                for val in cell1:
                    if val not in cell2:
                        return False
        return True

    def findInHistory(self, table, tableHistory):
        for t in tableHistory:
            if self.compareTables(table, t):
                return True
        return False

    def printTable(self, tab):
        temp = tab.copy()
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

    def findRule(self, rightSide, rules):
        result = set()
        for leftSide in rules:
            if rightSide in rules[leftSide]:
                result.add(leftSide)
        return result

    def reduceRules(self, row, column, nTerminal, rules, CYKtable, newCYKtable, modifiedContainer):
        unaryRuleFound = self.findRule(nTerminal, rules)
        if unaryRuleFound.__len__() > 0:
            self.modified = True
            newCYKtable[row][column].update(unaryRuleFound)

        if column == self.word.__len__()-1:
            return

        for col, tRules in enumerate(CYKtable[column+1]):
            if tRules == '':
                continue
            for nTerm in tRules:
                result = self.findRule(nTerminal + nTerm, rules)
                # if result == '':
                #     continue
                for character in result:
                    if not character in CYKtable[row][col]:
                        newCYKtable[row][col].add(character)
                        modifiedContainer[0] = True

    def set_initial_rules(self, table, rules):
        for diag, character in enumerate(self.word):
            table[diag][diag] = self.findRule(character, rules)
        
    def CYK_loop(self, CYKtable, ruleTable, modified, tableHistory):
        currentHistory = copy.deepcopy(tableHistory)
        newCYKtable = copy.deepcopy(self.emptyTable)

        modifiedContainer = [modified]
        self.printTable(CYKtable)
        for idr, row in enumerate(CYKtable):
            for idc, tableRules in enumerate(row):
                if(tableRules is ''):
                    continue
                for nonTerminal in tableRules:
                    self.reduceRules(idr, idc, nonTerminal, ruleTable, CYKtable, newCYKtable, modifiedContainer)

        if "S" in newCYKtable[0][self.word.__len__()-1]:
            self.printTable(newCYKtable)
            return True
        
        if self.findInHistory(newCYKtable, currentHistory):
            print("Loop detected")
            return False
        currentHistory.append(CYKtable)

        if modifiedContainer[0]:
            for rulesTable in self.rules:
                if self.CYK_loop(newCYKtable, rulesTable, False, currentHistory):
                    return True

    def parse(self):
        for rulesTable in self.rules:
            table = copy.deepcopy(self.emptyTable)
            self.set_initial_rules(table, rulesTable)
            tableHistory = []
            # This will start first step, need to use all tables again
            for rulesTable2 in self.rules:
                if self.CYK_loop(table, rulesTable2, True, tableHistory):
                    return True
        return False

print(ET0LParser("aaaa", "demoET0L.txt").parse())