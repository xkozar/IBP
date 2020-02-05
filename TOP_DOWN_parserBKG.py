from ruleReader import RuleReader
from pprint import pprint

word = 'bcbcc'
table = [['' for i in range(word.__len__())] for j in range(word.__len__())]
modified = True # Determines whether rules table was modified
reader = RuleReader("rules.txt")
rules = reader.contentToPairs()
table[0][word.__len__()-1] = 'S'

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
    for value in table[row][col]:
        expandNonTerminal(row,col,rules[value][0])

def expandNonTerminal(row, col, rule):
    if rule.__len__() != 2:
        return

    for x in range(row,col):
        if row == x:
            insertIntoResultTable( row,x,rule[0])
        else:
            insertIntoTable(row,x,rule[0])
        if col == x + 1:
            insertIntoResultTable( x+1,col,rule[1])
        else:
            insertIntoTable( x+1,col,rule[1])
        break


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

printTable(table)
if table[0][word.__len__()-1].find('S') >= 0:
    print('Success')
else:
    print("Failed")
