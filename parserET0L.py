# Author:   Tomáš Kožár, xkozar02
#           Faculty of Information Technology, Brno University of Technology
# Bachelor's Thesis: Parsing for ET0L systems

from ruleReaderET0L import RuleReader
from pprint import pprint
import copy

class ET0LParserCYK:

    def __init__(self, rules):
        self.word = ""
        self.reader = RuleReader(rules)
        self.rules = self.reader.contentToRules(True)
        self.initTables()

    def initTables(self):
        self.emptyTable = [[set() for i in range(self.word.__len__())] for j in range(self.word.__len__())]
        self.new_table = [[set() for i in range(self.word.__len__())] for j in range(self.word.__len__())]


    def fillEmptyRules(self, emptyRules, ruleTable, emptyChangedContainer):
        if emptyRules.__len__() == 0:
            newlyReduced = self.findRule("-", ruleTable)
            if newlyReduced.__len__() == 0:
                emptyChangedContainer[0] = False
            return newlyReduced

        newlyReduced = set()

        if emptyChangedContainer[0]:
            emptyChangedContainer[0] = False
            updateEmptySet = set()
            for empty in emptyRules:
                newEmpty = self.findRule(empty, ruleTable)
                if emptyRules.intersection(newEmpty).__len__() < newEmpty.__len__():
                    # emptyChangedContainer[0] = True
                    updateEmptySet.update(newEmpty)
            newlyReduced.update(updateEmptySet)

            for empty1 in emptyRules:
                for empty2 in emptyRules:
                    newEmpty = self.findRule(empty1 + empty2, ruleTable)
                    if emptyRules.intersection(newEmpty).__len__() < newEmpty.__len__():
                        # emptyChangedContainer[0] = True
                        updateEmptySet.update(newEmpty)
            newlyReduced.update(updateEmptySet)

        return newlyReduced


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

    def reduceRules(self, row, column, nTerminal, ruleTable, CYKtable, newCYKtable, modifiedContainer, emptyRules):
        unaryRuleFound = self.findRule(nTerminal, ruleTable)
        if unaryRuleFound.__len__() > 0:
            self.modified = True
            newCYKtable[row][column].update(unaryRuleFound)

        if nTerminal in CYKtable[row][column]:
            for first in set(nTerminal) | emptyRules:
                for second in set(nTerminal) | emptyRules:
                    if first in CYKtable[row][column] or second in CYKtable[row][column]:
                        rule = self.findRule(first + second, ruleTable)
                        if rule.__len__() == 0:
                            continue
                        self.modified = True
                        newCYKtable[row][column].update(rule)

        if column == self.word.__len__()-1:
            return

        for col, tRules in enumerate(CYKtable[column+1]):
            if tRules == '':
                continue
            for nTerm in tRules:
                result = self.findRule(nTerminal + nTerm, ruleTable)
                for character in result:
                    # if not character in CYKtable[row][col]:
                    newCYKtable[row][col].add(character)
                    modifiedContainer[0] = True

    def fillStart(self, table, rules):
        for diag, character in enumerate(self.word):
            table[diag][diag] = self.findRule(character, rules)
        
    def CYK_loop(self, CYKtable, ruleTable, modified, tableHistory, emptyRules, emptyModified):
        emptyModifiedContainer = [emptyModified]
        emptyRules = emptyRules | self.fillEmptyRules(emptyRules, ruleTable, emptyModifiedContainer)
        currentHistory = copy.deepcopy(tableHistory)
        newCYKtable = copy.deepcopy(self.emptyTable)

        modifiedContainer = [modified]
        # self.printTable(CYKtable)
        for idr, row in enumerate(CYKtable):
            for idc, tableRules in enumerate(row):
                if(tableRules is ''):
                    continue
                for nonTerminal in tableRules:
                    self.reduceRules(idr, idc, nonTerminal, ruleTable, CYKtable, newCYKtable, modifiedContainer, emptyRules)

        if self.findInHistory(newCYKtable, currentHistory) and emptyModified == False:
            # print("Loop detected")
            return False
        currentHistory.append(CYKtable)

        if "S" in newCYKtable[0][self.word.__len__()-1]:
            # self.printTable(newCYKtable)
            for x in currentHistory:
                self.printTable(x)
            self.printTable(newCYKtable)
            return True
        
        if modifiedContainer[0]:
            for rulesTable in self.rules:
                if self.CYK_loop(newCYKtable, rulesTable, False, currentHistory, emptyRules, emptyModifiedContainer[0]):
                    return True

    def parse(self, word):
        self.word = word
        self.initTables()
        for rulesTable in self.rules:
            table = copy.deepcopy(self.emptyTable)
            self.fillStart(table, rulesTable)
            tableHistory = []
            # This will start first step, need to use all tables again
            for rulesTable2 in self.rules:
                if self.CYK_loop(table, rulesTable2, False, tableHistory, set(), True):
                    return True
        return False

# print(ET0LParserCYK("testRulesET0L.txt").parse("bcbcbcbcbcbcbcbcbc"))
