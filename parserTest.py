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

# parserCFGCYK = CFGParserCYK("testRules.txt")
# topDownCFGParser = TopDownCFGParser("testRules.txt")
# CFGWordsGenerated = topDownCFGParser.generateValidWords(5)
# CFGFalseWords = topDownCFGParser.generateAllCombinations(5) - CFGWordsGenerated
# CFGCounter = 0
# CFGCounterFail = 0
# for word in CFGWordsGenerated:
#     blockPrint()
#     if parserCFGCYK.parse(word):
#         CFGCounter = CFGCounter + 1
#     else:
#         enablePrint()
#         print("CFG parser failed on: ", word)

# for word in CFGFalseWords:
#     blockPrint()
#     if parserCFGCYK.parse(word) == False:
#         enablePrint()
#         CFGCounterFail = CFGCounterFail + 1
#     else:
#         enablePrint()
#         print("CFG parser should fail on: ", word)


parserE0LCYK = E0LParserCYK("newTestRules.txt")
topDownE0LParser = TopDownE0LParser("newTestRules.txt")
E0LWordsGenerated = topDownE0LParser.generateValidWords(5, startWord="S")
E0LFalseWords = topDownE0LParser.generateAllCombinations(5) - E0LWordsGenerated
E0LCounter = 0
E0LCounterFail = 0

for word in E0LWordsGenerated:
    blockPrint()
    if parserE0LCYK.parse(word):
        enablePrint()
        E0LCounter = E0LCounter + 1
    else:
        enablePrint()
        print("E0L parser failed on: ", word)

for word in E0LFalseWords:
    blockPrint()
    if parserE0LCYK.parse(word) == False:
        enablePrint()
        E0LCounterFail = E0LCounterFail + 1
    else:
        enablePrint()
        print("E0L parser should fail on: ", word)

parserET0LCYK = ET0LParserCYK("testRulesET0L.txt")
topDownET0LParser = TopDownET0LParser("testRulesET0L.txt")
ET0LWordsGenerated = topDownET0LParser.generateValidWords(5, startWord="S")
ET0LFalseWords = topDownET0LParser.generateAllCombinations(5) - ET0LWordsGenerated
ET0LCounter = 0
ET0LCounterFail = 0


for word in ET0LWordsGenerated:
    blockPrint()
    if parserET0LCYK.parse(word):
        ET0LCounter = ET0LCounter + 1
    else:
        enablePrint()
        print("ET0L parser failed on: ", word)

for word in ET0LFalseWords:
    blockPrint()
    if parserET0LCYK.parse(word) == False:
        enablePrint()
        ET0LCounterFail = ET0LCounterFail + 1
    else:
        enablePrint()
        print("ET0L parser should fail on: ", word)


enablePrint()
# print("Test passed for CFG: ", CFGCounter, "/", CFGWordsGenerated.__len__())
# print("Test passed for CFG false words: ", CFGCounterFail, "/", CFGFalseWords.__len__())
print("Test passed for E0L: ", E0LCounter, "/", E0LWordsGenerated.__len__())
print("Test passed for E0L false words: ", E0LCounterFail, "/", E0LFalseWords.__len__())
print("Test passed for ET0L: ", ET0LCounter, "/", ET0LWordsGenerated.__len__())
print("Test passed for ET0L false words: ", ET0LCounterFail, "/", ET0LFalseWords.__len__())
