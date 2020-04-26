# Author:   Tomáš Kožár, xkozar02
#           Faculty of Information Technology, Brno University of Technology
# Bachelor's Thesis: Parsing for ET0L systems

import getopt
import sys, os
from parserCFG import CFGParserCYK
from parserE0L import E0LParserCYK
from parserET0L import ET0LParserCYK
from topDownCFGParser import TopDownCFGParser
from topDownE0LParser import TopDownE0LParser
from topDownET0LParser import TopDownET0LParser

def blockPrint():
    sys.stdout = open(os.devnull, 'w')

def enablePrint():
    sys.stdout = sys.__stdout__

CFGWords = TopDownCFGParser("testRules.txt").generate(4)
CFGCounter = 0
for word in CFGWords:
    blockPrint()
    if CFGParserCYK(word, "testRules.txt").parse():
        CFGCounter = CFGCounter + 1
    else:
        enablePrint()
        print("CFG parser failed on: ", word)


E0LWordsGenerated = TopDownE0LParser("testRules.txt").generate(4, startWord="S")
E0LCounter = 0
E0LCounterFail = 0
for word in E0LWordsGenerated[0]:
    blockPrint()
    if E0LParserCYK(word, "testRules.txt").parse():
        enablePrint()
        E0LCounter = E0LCounter + 1
    else:
        enablePrint()
        print("E0L parser failed on: ", word)
for word in E0LWordsGenerated[1]:
    blockPrint()
    if E0LParserCYK(word, "testRules.txt").parse() == False:
        enablePrint()
        E0LCounterFail = E0LCounterFail + 1
    else:
        enablePrint()
        print("E0L parser should fail on: ", word)

ET0LWords = TopDownET0LParser("testRulesET0L.txt").generate(8, startWord="S")
ET0LCounter = 0

for word in ET0LWords:
    blockPrint()
    if ET0LParserCYK(word, "testRulesET0L.txt").parse():
        ET0LCounter = ET0LCounter + 1
    else:
        enablePrint()
        print("ET0L parser failed on: ", word)


enablePrint()
print("Test result for CFG: ", CFGCounter, "/", CFGWords.__len__())
print("Test result for E0L: ", E0LCounter, "/", E0LWordsGenerated[0].__len__())
print("Test result for E0L false words: ", E0LCounterFail, "/", E0LWordsGenerated[1].__len__())
print("Test result for ET0L: ", ET0LCounter, "/", ET0LWords.__len__())