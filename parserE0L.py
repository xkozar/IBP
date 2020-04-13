# Author:   Tomáš Kožár, xkozar02
#           Faculty of Information Technology, Brno University of Technology
# Bachelor's Thesis: Parsing for ET0L systems

from ruleReader import RuleReader
from pprint import pprint

class E0LParser:

    def __init__(self, word, rules):
        self.word = word
        self.reader = RuleReader(rules)
        self.rules = self.reader.contentToRules(True)
        self.table = [['' for i in range(word.__len__())] for j in range(word.__len__())]
        self.new_table = [['' for i in range(word.__len__())] for j in range(word.__len__())]
        self.modified = True # Determines whether rules table was modified
        self.firstStep = True
        self.tableToCopy = [['' for i in range(word.__len__())] for j in range(word.__len__())]

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
                rowToPrint += " " + value + spacePadding + " "
            rowToPrint += "]"
            if x == 0:
                print()
            print(rowToPrint)
            if x == row.__len__() - 1:
                print(rowToPrint.__len__() * "_")

    def fillStart(self, word, table):
        for i in range(word.__len__()):
            for lSide in self.rules:
                if word[i] in self.rules[lSide]:
                    table[i][i] = table[i][i] + lSide

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
                        if row == column and col == column + 1 and not self.firstStep:
                            continue
                        
                        self.new_table[row][col] = self.new_table[row][col] + character
                        self.modified = True



    def parse(self):
        self.fillStart(self.word, self.table)

        while self.modified:
            self.modified = False
            self.printTable()
            for idr, row in enumerate(self.table):
                for idc, tableRules in enumerate(row):
                    if(tableRules is not ''):
                        for nonTerminal in tableRules:
                            self.findPairForRule(idr, idc, nonTerminal)

            if self.firstStep:
                self.tableToCopy = self.new_table.copy()
                self.fillStart(self.word, self.tableToCopy)

            self.table = self.new_table.copy()
            self.fillStart(self.word, self.table)
            self.new_table = self.tableToCopy
            if self.table[0][self.word.__len__()-1].find('S') >= 0:
                self.printTable()
                return True
            self.firstStep = False
        return False
