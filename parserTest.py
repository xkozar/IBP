# Author:   Tomáš Kožár, xkozar02
#           Faculty of Information Technology, Brno University of Technology
# Bachelor's Thesis: Parsing for ET0L systems

import getopt
import sys, os
from parserCFG import ContextFreeGrammarParser
from parserE0L import E0LParser
from parserET0L import ET0LParser
from wordGeneratorCFG import ContextFreeGrammarGenerator
from wordGeneratorE0L import E0LGenerator
from wordGeneratorET0L import ET0LGenerator

def blockPrint():
    sys.stdout = open(os.devnull, 'w')

def enablePrint():
    sys.stdout = sys.__stdout__

CFGWords = ContextFreeGrammarGenerator("testRules.txt").generate(6)
CFGCounter = 0
for word in CFGWords:
    blockPrint()
    if ContextFreeGrammarParser(word, "testRules.txt").parse():
        CFGCounter = CFGCounter + 1
    else:
        enablePrint()
        print("CFG parser failed on: ", word)


E0LWords = E0LGenerator("testRules.txt").generate(12)
E0LCounter = 0
for word in E0LWords:
    blockPrint()
    if E0LParser(word, "testRules.txt").parse():
        enablePrint()
        E0LCounter = E0LCounter + 1
    else:
        enablePrint()
        print("E0L parser failed on: ", word)

ET0LWords = ET0LGenerator("testRulesET0L.txt").generate(8)
print(ET0LWords)
ET0LCounter = 0

for word in ET0LWords:
    blockPrint()
    if ET0LParser(word, "testRulesET0L.txt").parse():
        ET0LCounter = ET0LCounter + 1
    else:
        enablePrint()
        print("ET0L parser failed on: ", word)


enablePrint()

print("Test result for CFG: ", CFGCounter, "/", CFGWords.__len__())
print("Test result for E0L: ", E0LCounter, "/", E0LWords.__len__())
print("Test result for ET0L: ", ET0LCounter, "/", ET0LWords.__len__())