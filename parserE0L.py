from ruleReader import RuleReader
from pprint import pprint

def printTable(tab):
    temp = table.copy()
    temp.reverse()
    for row in temp:
        pprint(row)

def fillStart(word, table):
    for i in range(word.__len__()):
        for lSide in rules:
            if word[i] in rules[lSide]:
                table[i][i] = table[i][i] + lSide

def findRule(rightSide):
    result = ''
    global modified
    for leftSide in rules:
        if rightSide in rules[leftSide]:
            result = result + leftSide
    
    return(result)

def findPairForRule(row, column, nTerminal):
    global modified
    if column == word.__len__()-1:
        return

    for col, tRules in enumerate(table[column+1]):
        if tRules == '':
            continue
        for nTerm in tRules:
            result = findRule(nTerminal + nTerm)
            # if result == '':
            #     continue
            for character in result:
                if table[row][col].find(character) < 0:
                    new_table[row][col] = new_table[row][col] + character
                    modified = True

#word = 'bcbc'
word = 'bcbc'
print("WORD: ", word)

modified = True # Determines whether rules table was modified

reader = RuleReader("rules.txt")
rules = reader.contentToPairs()
# Context free grammar
table = [['' for i in range(word.__len__())] for j in range(word.__len__())]
new_table = [['' for i in range(word.__len__())] for j in range(word.__len__())]


fillStart(word, table)


while modified:
    modified = False
    printTable(table)
    print('-----------------------------------------')
    for idr, row in enumerate(table):
        for idc, tableRules in enumerate(row):
            if(tableRules is not ''):
                for nonTerminal in tableRules:
                    findPairForRule(idr, idc, nonTerminal)

    table = new_table.copy()
    fillStart(word, table)
    new_table = [['' for i in range(word.__len__())] for j in range(word.__len__())]
    if table[0][word.__len__()-1].find('S') >= 0:
        printTable(table)
        print('Success')
        exit()
        
    # print('end of loop')
    
print("Failed")
