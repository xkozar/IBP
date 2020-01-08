from ruleReader import RuleReader
from pprint import pprint

word = 'bcbcc'
table = [['' for i in range(word.__len__())] for j in range(word.__len__())]
modified = True # Determines whether rules table was modified
reader = RuleReader("rules.txt")
rules = reader.contentToPairs()
table[0][word.__len__()-1] = 'S'
counter = 1

def printFormatedRow(row):
    for x in range(1, row[row.__len__()-1]+1):
        print('|', end='')
        try:
            pos = row.index(x)
            print(row[pos-1], end=''),
        except ValueError:
            print(' ',end=''),
    print('|')

def printTable(tab):
    temp = table.copy()
    temp.reverse()
    for row in temp:
        pprint(row)


def insertIntoTable( row, col, val):
    if table[row][col].find(val) < 0:
        table[row][col] = table[row][col] + val
        return True
    return False

def insertIntoResultTable( row, col, val):
    if table[row][col] == '':
        table[row][col] = val
        return
    table[row][col] = table[row][col] + val

def expandCell(row, col):
    global counter
    for value in table[row][col]:    
        for rule in rules[value]:
            expandNonTerminal(row,col,rule)
            counter = counter + 1

def expandNonTerminal(row, col, rule):
    global counter
    if rule.__len__() != 2:
        return

    for x in range(row,col):
        if row == x:
            insertIntoResultTable( row,x,(rule[0],counter))
        else:
            insertIntoTable(row,x,rule[0])
        if col == x + 1:
            insertIntoResultTable( x+1,col,(rule[1], counter))
        else:
            insertIntoTable( x+1,col,rule[1])


# Context free grammar

for i in range(word.__len__()):
    table[i][i] = ''


x = 0
y = 0

for cols in range(word.__len__()-1, 0, -1):
    x = 0
    y = cols
    while(x <= word.__len__()-1 and y <= word.__len__()-1):
        expandCell(x, y)
        x += 1
        y += 1

# while modified:
#     modified = False
#     printTable(table)
#     print('-----------------------------------------')
#     for idr, row in enumerate(table):
#         for idc, tableRules in enumerate(row):
#             if(tableRules is not ''):
#                 for nonTerminal in tableRules:
#                     findPairForRule(idr, idc, nonTerminal)

#     print('end of loop')



printTable(table)
if table[0][word.__len__()-1].find('S') >= 0:
    print('Success')
else:
    print("Failed")

for i in range(word.__len__()-1, -1, -1):
    printFormatedRow(table[i][i])
