# Author:   Tomáš Kožár, xkozar02
#           Faculty of Information Technology, Brno University of Technology
# Bachelor's Thesis: Parsing for ET0L systems

from ruleReaderET0L import RuleReader
from pprint import pprint

class ET0LParser:

    def __init__(self, word, rules):
        self.word = word
        self.reader = RuleReader(rules)
        self.rules = self.reader.contentToRules(True)
        self.table = [['' for i in range(word.__len__())] for j in range(word.__len__())]
        self.new_table = [['' for i in range(word.__len__())] for j in range(word.__len__())]
        # self.modified = True # Determines whether rules table was modified


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
                rowToPrint += " " + value + spacePadding + " "
            rowToPrint += "]"
            if x == 0:
                print()
            print(rowToPrint)
            if x == row.__len__() - 1:
                print(rowToPrint.__len__() * "_")

    def findRule(self, rightSide, rules):
        result = ''
        for leftSide in rules:
            if rightSide in rules[leftSide]:
                result = result + leftSide
        return(result)

    def findPairForRule(self, row, column, nTerminal, rules, CYKtable, newCYKtable, modifiedContainer, firstStep):
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
                    if CYKtable[row][col].find(character) < 0:
                        if row == column and col == column + 1 and not firstStep:
                            continue
                        newCYKtable[row][col] = newCYKtable[row][col] + character
                        modifiedContainer[0] = True

    def set_initial_rules(self, table, rules):
        for i in range(self.word.__len__()):
            for lSide in rules:
                if self.word[i] in rules[lSide]:
                    table[i][i] = table[i][i] + lSide

    def CYK_loop(self, CYKtable, ruleTable, firstTime, firstStep, toCopyTable):
        newCYKtable = toCopyTable.copy()
        for diagonal in range(CYKtable.__len__()):
            newCYKtable[diagonal][diagonal] = CYKtable[diagonal][diagonal]
        # while modified:
        modifiedContainer = [firstTime]
        self.printTable(CYKtable)
        for idr, row in enumerate(CYKtable):
            for idc, tableRules in enumerate(row):
                if(tableRules is not ''):
                    for nonTerminal in tableRules:
                        self.findPairForRule(idr, idc, nonTerminal, ruleTable, CYKtable, newCYKtable, modifiedContainer, firstStep)

        if firstStep:
            tableToCopy = newCYKtable.copy()
        else:
            tableToCopy = toCopyTable
        # table = new_table.copy()
        # new_table = [['' for i in range(word.__len__())] for j in range(word.__len__())]
        if newCYKtable[0][self.word.__len__()-1].find('S') >= 0:
            self.printTable(newCYKtable)
            return True
            
        if modifiedContainer[0]:
            for rulesTable in self.rules:
                if self.CYK_loop(newCYKtable.copy(), rulesTable, False, False, tableToCopy):
                    return True

    def parse(self):
        for rulesTable in self.rules:
            self.table = [['' for i in range(self.word.__len__())] for j in range(self.word.__len__())]
            self.set_initial_rules(self.table, rulesTable)
            newTable = [['' for i in range(self.word.__len__())] for j in range(self.word.__len__())]
            for rulesTable2 in self.rules:
                if self.CYK_loop(self.table.copy(), rulesTable2, True, True, newTable):
                    return True
            
        return False

# print(ET0LParser("bccb", "testRulesET0L.txt").parse())