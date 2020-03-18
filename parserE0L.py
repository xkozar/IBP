from ruleReader import RuleReader
from pprint import pprint

class E0LParser:

    def __init__(self, word, rules):
        self.word = word
        self.reader = RuleReader(rules)
        self.rules = self.reader.contentToPairs()
        self.table = [['' for i in range(word.__len__())] for j in range(word.__len__())]
        self.new_table = [['' for i in range(word.__len__())] for j in range(word.__len__())]
        self.modified = True # Determines whether rules table was modified

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
                    if self.table[row][col].find(character) < 0:
                        self.new_table[row][col] = self.new_table[row][col] + character
                        self.modified = True

    def parse(self):

        self.fillStart(self.word, self.table)

        while self.modified:
            self.modified = False
            self.printTable()
            print('-----------------------------------------')
            for idr, row in enumerate(self.table):
                for idc, tableRules in enumerate(row):
                    if(tableRules is not ''):
                        for nonTerminal in tableRules:
                            self.findPairForRule(idr, idc, nonTerminal)

            self.table = self.new_table.copy()
            self.fillStart(self.word, self.table)
            self.new_table = [['' for i in range(self.word.__len__())] for j in range(self.word.__len__())]
            if self.table[0][self.word.__len__()-1].find('S') >= 0:
                self.printTable()
                return True                
        return False
