# Author:   Tomáš Kožár, xkozar02
#           Faculty of Information Technology, Brno University of Technology
# Bachelor's Thesis: Parsing for ET0L systems

from ruleReader import RuleReader
from pprint import pprint
import copy

class E0LParserCYK:

    def __init__(self, rules):
        self.word = ""
        self.reader = RuleReader(rules)
        self.rules = self.reader.contentToRules(True)
        self.modified = True # Determines whether rules table was modified
        self.tableHistory = []
        self.emptySet = set()
        self.initTables()
        
    # Reset all variables that could be modified when parse was lastly run
    def initTables(self):
        self.modified = True # Determines whether rules table was modified
        self.table = [[set() for i in range(self.word.__len__())] for j in range(self.word.__len__())]
        self.new_table = [[set() for i in range(self.word.__len__())] for j in range(self.word.__len__())]
        self.tableHistory = []
        self.emptySet = set()

    # Fill set of empty symbols that can be used during reduction of rules
    def fillEmptyRules(self):
        newlyReduced = set()
        updateEmptySet = set()

        # Direct deletion
        updateEmptySet.update(self.findRule("-"))

        # Unary rules that can lead to deletion
        for empty in self.emptySet:
            newEmpty = self.findRule(empty)
            updateEmptySet.update(newEmpty)
        newlyReduced.update(updateEmptySet)

        # Pairs that can lead to deletion
        for empty1 in self.emptySet:
            for empty2 in self.emptySet:
                newEmpty = self.findRule(empty1 + empty2)
                if self.emptySet.intersection(newEmpty).__len__() < newEmpty.__len__():
                    updateEmptySet.update(newEmpty)
        newlyReduced.update(updateEmptySet)

        self.emptySet = newlyReduced.copy()

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
    def findInHistory(self):
        for x in self.tableHistory:
            if self.compareTables(self.new_table, x[0]) and x[1] == self.emptySet:
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

    # Fill diagonal with symbols
    def fillStart(self, word, table):
        for diag, character in enumerate(self.word):
            table[diag][diag] = self.findRule(character)

    # Find all symbols that can be rewriten to passed argument
    def findRule(self, rightSide):
        result = set()
        for leftSide in self.rules:
            if rightSide in self.rules[leftSide]:
                result.add(leftSide)
        return result

    # Does reduction of rules for symbol on [row, col] position
    def reduceRules(self, row, column, symbol):
        if symbol == "":
            return
        
        # Reduce unary rules
        unaryRuleFound = self.findRule(symbol)
        for unaryRule in unaryRuleFound:
            if symbol in self.table[row][column]:
                self.modified = True
                self.new_table[row][column].update(unaryRule)

        # Reduce rules where 1 nonterminal can be erased
        if symbol in self.table[row][column]:
            for first in set(symbol) | self.emptySet:
                for second in set(symbol) | self.emptySet:
                    if first in self.table[row][column] or second in self.table[row][column]:
                        rule = self.findRule(first + second)
                        if rule.__len__() == 0:
                            continue
                        self.modified = True
                        self.new_table[row][column].update(rule)

        # This column cannot be reduced using pairs,
        # since it looks for row = column + 1 and that is out of bounds
        if column == self.word.__len__()-1:
            return

        # Reduce normal pairs
        for col, tRules in enumerate(self.table[column+1]):
            if tRules == '':
                continue
            for nTerm in tRules:
                result = self.findRule(symbol + nTerm)
                for character in result:
                    self.new_table[row][col].add(character)
                    self.modified = True

    # Runs modified CYK algorithm for word
    def parse(self, word): 
        self.word = word
        self.initTables()
        print("Word: " + self.word)
        self.fillStart(self.word, self.table)

        # While we got some unique reduction
        while self.modified:
            self.fillEmptyRules()
            self.modified = False
            self.printTable(self.table)
            
            # Loop through table
            for idr, row in enumerate(self.table):
                for idc, tableRules in enumerate(row):
                    # Empty or invalid position
                    if(tableRules is '' or idc < idr):
                        continue
                    # Do reduction for each symbol on position
                    for nonTerminal in tableRules:
                        self.reduceRules(idr, idc, nonTerminal)

            # Check for loop
            if self.findInHistory():
                print("Loop detected")
                return False
            self.tableHistory.append((self.new_table, self.emptySet))

            # Check result
            if "S" in self.new_table[0][self.word.__len__()-1]:
                self.printTable(self.new_table)
                return True

            # Swap tables
            self.table = copy.deepcopy(self.new_table)
            self.new_table = [[set() for i in range(self.word.__len__())] for j in range(self.word.__len__())]
        return False

# print(E0LParserCYK("newTestRules.txt").parse("bcbc"))
