from ruleReader import RuleReader
from pprint import pprint

class E0LParser:

    def __init__(self, word, rules):
        self.word = word
        self.reader = RuleReader(rules)
        self.rules = self.reader.contentToPairs()
        self.table = [['' for i in range(word.__len__())] for j in range(word.__len__())]
        self.newTable = [['' for i in range(word.__len__())] for j in range(word.__len__())]
        self.modified = True # Determines whether rules table was modified
        self.firstStep = True
        self.tableUsedMap = [['' for i in range(word.__len__())] for j in range(word.__len__())]

    def printTable(self):
        temp = self.table.copy()
        temp.reverse()
        for row in temp:
            pprint(row)

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
                    firstIndex = self.findIndexInCell(row, column, nTerminal)
                    secondIndex = self.findIndexInCell(column+1, col, nTerm)
                    self.tableUsedMap[row][column] = self.tableUsedMap[row][column][0:firstIndex] + "1" + self.tableUsedMap[row][column][firstIndex+1:self.tableUsedMap[row][column].__len__()]
                    self.tableUsedMap[column+1][col] = self.tableUsedMap[column+1][col][0:secondIndex] + "1" + self.tableUsedMap[column+1][col][secondIndex+1:self.tableUsedMap[column+1][col].__len__()]
                    if self.table[row][col].find(character) < 0:
                        if row == column and col == column + 1 and not self.firstStep:
                            continue

                        self.newTable[row][col] = self.newTable[row][col] + character
                        self.modified = True

    def findIndexInCell(self, row, column, symbol):
        for id, symb in enumerate(self.table[row][column]):
            if symb == symbol:
                return id
        raise IndexError

    def fillUsedMap(self):
        for idr, row in enumerate(self.table):
            for idc, cell in enumerate(row):
                self.tableUsedMap[idr][idc] = "0" * cell.__len__()

    def fillNewTableWithUnused(self):
        for idr, row in enumerate(self.tableUsedMap):
            for idc, cell in enumerate(row):
                for ids, sym in enumerate(cell):
                    if sym == "0":
                        symbol = self.table[idr][idc][ids]
                        if self.newTable[idr][idc].find(symbol) < 0:
                            self.newTable[idr][idc] = self.newTable[idr][idc] + symbol

    def parse(self):

        self.fillStart(self.word, self.table)

        while self.modified:
            self.fillUsedMap()
            self.modified = False
            self.printTable()
            print('-----------------------------------------')
            for idr, row in enumerate(self.table):
                for idc, tableRules in enumerate(row):
                    if(tableRules is not ''):
                        for nonTerminal in tableRules:
                            self.findPairForRule(idr, idc, nonTerminal)

            self.fillNewTableWithUnused()
            self.table = self.newTable.copy()
            self.fillStart(self.word, self.table)
            self.newTable = [['' for i in range(self.word.__len__())] for j in range(self.word.__len__())]
            if self.table[0][self.word.__len__()-1].find('S') >= 0:
                self.printTable()
                print('Success')
                exit()
                
            # print('end of loop')
            
        print("Failed")
