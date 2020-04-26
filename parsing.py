# Author:   Tomáš Kožár, xkozar02
#           Faculty of Information Technology, Brno University of Technology
# Bachelor's Thesis: Parsing for ET0L systems

import getopt
import sys
from parserCFG import CFGParserCYK
from parserE0Lnew import E0LParserCYK
from parserET0Lnew import ET0LParserCYK
from topDownCFGParser import TopDownCFGParser
from topDownE0LParser import TopDownE0LParser
from topDownET0LParser import TopDownET0LParser

def printHelp():
    print("")
    print("Hello and welcome to parser for Context Free Grammars, E0L and ET0L systems.")
    print("Available commands:")
    print("-C -> use parser for context free grammar")
    print("-E -> use parser for E0L system")
    print("-T -> use parser for ET0L system")
    print("Exactly 1 command above have to be used.")
    print("-w <word> -> specifies word to be parsed !MANDATORY!")
    print("-r <rules> -> specifies file with rules for parser !MANDATORY!")
    print("")
    print("Rules are in format: '[A-Z] -> [A-Z][A-Z]' or '[A-Z] -> [a-z]'")
    print("Each rule needs to be on separate line!")
    print("Each rule set needs at least one rule with starting symbol 'S'")
    print("For ET0L systems, tables of rule sets needs to be divided by '#' on separate line")

helpFlag = "-h"

CFGParserFlag = "-C"
E0LParserFlag = "-E"
ET0LParserFlag = "-T"

wordToParseFlag = "-w"
rulesForParserFlag = "-r"

topDownParserFlag = "--top-down"

parserOptions = [CFGParserFlag, E0LParserFlag, ET0LParserFlag]

try:
    opts, args = getopt.getopt(sys.argv[1:], "CETr:w:h", ["top-down"])
except getopt.GetoptError as err:
    print("Incorrect use of commands", file=sys.stderr)
    print(err, file=sys.stderr)
    sys.exit(10)

# Print help and exit
if [item for item in opts if item[0] == helpFlag].__len__() > 0:
    printHelp()
    sys.exit(0)

# Check single selection of parser type
if [item for item in opts if item[0] in parserOptions].__len__() != 1:
    print("Exactly one parser type must be specified", file=sys.stderr)
    printHelp()
    sys.exit(0)

# Check that word to be parsed is specified
if [item for item in opts if item[0] == wordToParseFlag].__len__() == 0:
    print("Word to be parsed must be specified!", file=sys.stderr)
    printHelp()
    sys.exit(0)

# Check that file with rules was specified
if [item for item in opts if item[0] == rulesForParserFlag].__len__() == 0:
    print("File containing rules must be specified!", file=sys.stderr)
    printHelp()
    sys.exit(0)

# Get values for word and rule input file
word = [item for item in opts if item[0] == wordToParseFlag][0][1]
rulesFile = [item for item in opts if item[0] == rulesForParserFlag][0][1]

useTopDownParser = topDownParserFlag in dict(opts)

# Run specified parser
for flag, value in opts:
    if flag == CFGParserFlag:
        if useTopDownParser:
            print("Using context free grammar parser (Top-Down)")
            if TopDownCFGParser(rulesFile).parse(word):
                print("Success")
            else:
                print("Fail")
        else:
            print("Using context free grammar parser (Cocke-Younger-Kasami)")
            if CFGParserCYK(word, rulesFile).parse():
                print("Success")
            else:
                print("Fail")
    if flag == E0LParserFlag:
        if useTopDownParser:
            print("Using E0L parser (Top-Down)")
            if TopDownCFGParser(rulesFile).parse(word):
                print("Success")
            else:
                print("Fail")
        else:
            print("Using E0L parser (Cocke-Younger-Kasami)")
            if E0LParserCYK(word, rulesFile).parse():
                print("Success")
            else:
                print("Fail")
    if flag == ET0LParserFlag:
        if useTopDownParser:
            print("Using ET0L parser (Top-Down)")
            if TopDownCFGParser(rulesFile).parse(word):
                print("Success")
            else:
                print("Fail")
        else:
            print("Using ET0L parser (Cocke-Younger-Kasami)")
            if ET0LParserCYK(word, rulesFile).parse():
                print("Success")
            else:
                print("Fail")
