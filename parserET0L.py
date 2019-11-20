from ruleReaderET0L import RuleReader
from pprint import pprint

def printTable(tab):
    temp = tab.copy()
    temp.reverse()
    for row in temp:
        pprint(row)

def findRule(rightSide, rules):
    result = ''
    global modified
    for leftSide in rules:
        if rightSide in rules[leftSide]:
            result = result + leftSide
    
    return(result)

def findPairForRule(row, column, nTerminal, rules, CYKtable, newCYKtable):
    global modified
    if column == word.__len__()-1:
        return

    for col, tRules in enumerate(CYKtable[column+1]):
        if tRules == '':
            continue
        for nTerm in tRules:
            result = findRule(nTerminal + nTerm, rules)
            # if result == '':
            #     continue
            for character in result:
                if CYKtable[row][col].find(character) < 0:
                    newCYKtable[row][col] = newCYKtable[row][col] + character
                    modified = True

def set_initial_rules(table, rules):
    for i in range(word.__len__()):
        for lSide in rules:
            if word[i] in rules[lSide]:
                table[i][i] = table[i][i] + lSide

def CYK_loop(CYKtable, ruleTable):
    global modified
    global rules
    newCYKtable = [['' for i in range(word.__len__())] for j in range(word.__len__())]
    # while modified:
    modified = False
    printTable(CYKtable)
    print('-----------------------------------------')
    for idr, row in enumerate(CYKtable):
        for idc, tableRules in enumerate(row):
            if(tableRules is not ''):
                for nonTerminal in tableRules:
                    findPairForRule(idr, idc, nonTerminal, ruleTable, CYKtable, newCYKtable)

    # table = new_table.copy()
    # new_table = [['' for i in range(word.__len__())] for j in range(word.__len__())]
    if newCYKtable[0][word.__len__()-1].find('S') >= 0:
        printTable(newCYKtable)
        print('Success')
        exit()
        
    print('end of loop')
    if modified:
        for rulesTable in rules:
            CYK_loop(newCYKtable.copy(), rulesTable)

word = 'bcbc'
modified = True # Determines whether rules table was modified

reader = RuleReader("rulesET0L.txt")
rules = reader.contentToPairs()
pprint(rules)



for rulesTable in rules:
    table = [['' for i in range(word.__len__())] for j in range(word.__len__())]
    set_initial_rules(table, rulesTable)
    CYK_loop(table, rulesTable)
    
print("Failed")
