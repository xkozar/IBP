# Author:   Tomáš Kožár, xkozar02
#           Faculty of Information Technology, Brno University of Technology
# Bachelor's Thesis: Parsing for ET0L systems

import re, sys

class RuleReader:
    
    def __init__(self, name):
        self.filename = name
        self.content = []
        self.contentPairs = []
        self.getFileContent()
        self.rulesDictionary = {}
        self.rulesTables = []

    def getFileContent(self):
        with open(self.filename, 'r') as file:
            self.content = file.read()

    def contentToRules(self, chomskyNormalFormRules):
        for line in self.content.split('\n'):
            # Remove all whitespace from line
            line = "".join(line.split())
            if line == '':
                continue
            # Table split
            if line == '#':
                self.rulesTables.append(self.rulesDictionary)
                self.rulesDictionary = {}
                continue
            ruleInCNF = re.match("[A-Z]->([A-Z][A-Z]|[a-z])", line)
            ruleInRightFormat = re.match("[A-z]->[A-z]+", line)
            if chomskyNormalFormRules and not ruleInCNF:
                print("Rules need to be in Chomsky normal form", file=sys.stderr)
                print(line, file=sys.stderr)
                raise RuntimeError()
            elif not ruleInRightFormat:
                print("Rules need to be proper format", file=sys.stderr)
                print(line, file=sys.stderr)
                raise RuntimeError()
            # Remove whitespace and split
            rulePair = line.split('->')
            if rulePair[0] in self.rulesDictionary:
                self.rulesDictionary[rulePair[0]].append(rulePair[1])
            else:
                self.rulesDictionary[rulePair[0]] = [rulePair[1]]
        self.rulesTables.append(self.rulesDictionary)
        return self.rulesTables

    def getRulesDictionary(self, chomskyNormalFormRules=False):
        return self.contentToRules(chomskyNormalFormRules)
        
