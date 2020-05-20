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

    # Reset all variables that could be modified when parse was lastly run
    def initTables(self):
        self.emptyTable = [[set() for i in range(self.word.__len__())] for j in range(self.word.__len__())]
        self.new_table = [[set() for i in range(self.word.__len__())] for j in range(self.word.__len__())]
        self.CYKtableStack = []
        self.ruleTableStack = []
        self.modifiedStack = []
        self.tableHistoryStack = []
        self.emptyRulesStack = []
        self.emptyModifiedStack = []


    def fillEmptyRules(self, emptyRules, ruleTable):
        newlyReduced = set()
        updateEmptySet = set()

        # Direct deletion
        updateEmptySet.update(self.findRule("-", ruleTable))

        # Unary rules that can lead to deletion
        for empty in emptyRules:
            newEmpty = self.findRule(empty, ruleTable)
            updateEmptySet.update(newEmpty)
        newlyReduced.update(updateEmptySet)

        # Pairs that can lead to deletion
        for empty1 in emptyRules:
            for empty2 in emptyRules:
                newEmpty = self.findRule(empty1 + empty2, ruleTable)
                if emptyRules.intersection(newEmpty).__len__() < newEmpty.__len__():
                    updateEmptySet.update(newEmpty)
        newlyReduced.update(updateEmptySet)

        return newlyReduced

    # Compare CYK tables
    def compareTables(self, tab1, tab2):
        for row1, row2 in zip(tab1, tab2):
            for cell1, cell2 in zip(row1, row2):
                if cell1.__len__() != cell2.__len__():
                    return False
                for val in cell1:
                    if val not in cell2:
                        return False
        return True

    # Returns whether new table already existed. Used for loop detection
    def findInHistory(self, table, emptySet, tableHistory):
        for x in tableHistory:
            if self.compareTables(table, x[0]) and x[1] == emptySet:
                return True
        return False

    # Formats CYK table nicely
    def printTable(self, tab):
        temp = tab.copy()
        temp.reverse()
        
        # Contains max width of individual columns
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
    def findRule(self, rightSide, rules):
        result = set()
        for leftSide in rules:
            if rightSide in rules[leftSide]:
                result.add(leftSide)
        return result

    # Does reduction of rules for symbol on [row, col] position
    def reduceRules(self, row, column, nTerminal, ruleTable, CYKtable, newCYKtable, modifiedContainer, emptyRules):
        if nTerminal == "":
            return

        # Reduce unary rules
        unaryRuleFound = self.findRule(nTerminal, ruleTable)
        for unaryRule in unaryRuleFound:
            if nTerminal in CYKtable[row][column]:
                modifiedContainer[0] = True
                newCYKtable[row][column].update(unaryRule)

        # Reduce rules where 1 nonterminal can be erased
        if nTerminal in CYKtable[row][column]:
            for first in set(nTerminal) | emptyRules:
                for second in set(nTerminal) | emptyRules:
                    if first in CYKtable[row][column] or second in CYKtable[row][column]:
                        rule = self.findRule(first + second, ruleTable)
                        if rule.__len__() == 0:
                            continue
                        modifiedContainer[0] = True
                        newCYKtable[row][column].update(rule)

        # This column cannot be reduced using pairs,
        # since it looks for row = column + 1 and that is out of bounds
        if column == self.word.__len__()-1:
            return

        # Reduce normal pairs
        for col, tRules in enumerate(CYKtable[column+1]):
            if tRules == '':
                continue
            for nTerm in tRules:
                result = self.findRule(nTerminal + nTerm, ruleTable)
                for character in result:
                    # if not character in CYKtable[row][col]:
                    newCYKtable[row][col].add(character)
                    modifiedContainer[0] = True

    # Fill diagonal with symbols
    def fillStart(self, table, rules):
        for diag, character in enumerate(self.word):
            table[diag][diag] = self.findRule(character, rules)
    
    # Adds values to top of stacks
    def addToStacks(self, CYKtable, ruleTable, modified, tableHistory, emptyRules, emptyModified):
        self.CYKtableStack.append(CYKtable)
        self.ruleTableStack.append(ruleTable)
        self.modifiedStack.append(modified)
        self.tableHistoryStack.append(tableHistory)
        self.emptyRulesStack.append(emptyRules)
        self.emptyModifiedStack.append(emptyModified)

    # Step of modified CYK algorithm for ET0L systems
    def CYK_loop(self):

        while self.CYKtableStack.__len__() != 0:
            # Program is faster when values are taken from bottom of stacks
            CYKtable = self.CYKtableStack.pop(0)
            ruleTable = self.ruleTableStack.pop(0)
            modified = self.modifiedStack.pop(0)
            tableHistory = self.tableHistoryStack.pop(0)
            emptyRules = self.emptyRulesStack.pop(0)
            emptyModified = self.emptyModifiedStack.pop(0)

            emptyModifiedContainer = [emptyModified]
            currentHistory = copy.deepcopy(tableHistory)
            newCYKtable = copy.deepcopy(self.emptyTable)

            modifiedContainer = [modified]
            emptyRules = self.fillEmptyRules(emptyRules, ruleTable)

            # Loop through table
            for idr, row in enumerate(CYKtable):
                for idc, tableRules in enumerate(row):
                    # Empty or invalid position
                    if(tableRules is '' or idc < idr):
                        continue
                    # Do reduction for each symbol on position
                    for nonTerminal in tableRules:
                        self.reduceRules(idr, idc, nonTerminal, ruleTable, CYKtable, newCYKtable, modifiedContainer, emptyRules)

            # Check for loop
            if self.findInHistory(newCYKtable, emptyRules, currentHistory) == True:
                continue
            currentHistory.append((newCYKtable, emptyRules))

            # Check result
            if "S" in newCYKtable[0][self.word.__len__()-1]:
                # self.printTable(newCYKtable)
                for x in currentHistory:
                    self.printTable(x[0])
                    print(x[1])
                return True
            
            # Unique reduction was made
            if modifiedContainer[0]:
                for rulesTable in self.rules:
                    # This means recursion, but it is rewritten to iteration
                    self.addToStacks(newCYKtable, rulesTable, False, currentHistory, emptyRules, emptyModifiedContainer[0])
        
        return False

    # Runs modified CYK algorithm for word
    def parse(self, word):
        self.word = word
        self.initTables()
        for rulesTable in self.rules:
            table = copy.deepcopy(self.emptyTable)
            self.fillStart(table, rulesTable)
            tableHistory = [(table, self.fillEmptyRules({}, rulesTable))]
            # This will start first step, need to use all tables again
            for rulesTable2 in self.rules:
                self.addToStacks(table, rulesTable2, False, tableHistory, set(), True)
        if self.CYK_loop():
            return True
        return False

# print(ET0LParserCYK("testRulesET0L.txt").parse("bcbc"))
