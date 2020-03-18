from ruleReaderET0L import RuleReader
from pprint import pprint

class ET0LParser:

    def __init__(self, word, rules):
        self.word = word
        self.reader = RuleReader(rules)
        self.rules = self.reader.contentToPairs()
        self.table = [['' for i in range(word.__len__())] for j in range(word.__len__())]
        self.new_table = [['' for i in range(word.__len__())] for j in range(word.__len__())]
        # self.modified = True # Determines whether rules table was modified


    def printTable(self, tab):
        temp = tab.copy()
        temp.reverse()
        for row in temp:
            pprint(row)

    def findRule(self, rightSide, rules):
        result = ''
        for leftSide in rules:
            if rightSide in rules[leftSide]:
                result = result + leftSide
        return(result)

    def findPairForRule(self, row, column, nTerminal, rules, CYKtable, newCYKtable, modifiedContainer):
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
                        newCYKtable[row][col] = newCYKtable[row][col] + character
                        modifiedContainer[0] = True

    def set_initial_rules(self, table, rules):
        for i in range(self.word.__len__()):
            for lSide in rules:
                if self.word[i] in rules[lSide]:
                    table[i][i] = table[i][i] + lSide

    def CYK_loop(self, CYKtable, ruleTable, firstTime):
        newCYKtable = [['' for i in range(self.word.__len__())] for j in range(self.word.__len__())]
        for diagonal in range(CYKtable.__len__()):
            newCYKtable[diagonal][diagonal] = CYKtable[diagonal][diagonal]
        # while modified:
        modifiedContainer = [firstTime]
        self.printTable(CYKtable)
        print('-----------------------------------------')
        for idr, row in enumerate(CYKtable):
            for idc, tableRules in enumerate(row):
                if(tableRules is not ''):
                    for nonTerminal in tableRules:
                        self.findPairForRule(idr, idc, nonTerminal, ruleTable, CYKtable, newCYKtable, modifiedContainer)

        # table = new_table.copy()
        # new_table = [['' for i in range(word.__len__())] for j in range(word.__len__())]
        if newCYKtable[0][self.word.__len__()-1].find('S') >= 0:
            self.printTable(newCYKtable)
            return True
            
        print('end of loop')
        if modifiedContainer[0]:
            for rulesTable in self.rules:
                if self.CYK_loop(newCYKtable.copy(), rulesTable, False):
                    return True

    def parse(self):
        for rulesTable in self.rules:
            self.table = [['' for i in range(self.word.__len__())] for j in range(self.word.__len__())]
            self.set_initial_rules(self.table, rulesTable)
            for rulesTable2 in self.rules:
                if self.CYK_loop(self.table.copy(), rulesTable2, True):
                    return True
            
        return False

# ET0LParser("abcc", "testRulesET0l.txt").parse()