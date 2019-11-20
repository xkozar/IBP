import re

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

    def contentToPairs(self):
        # TODO use regex to check if rule is in proper format!!!
        for line in self.content.split('\n'):
            # Remove empty spaces from file
            if line == '':
                continue
            if line == '#':
                self.rulesTables.append(self.rulesDictionary)
                self.rulesDictionary = {}
                continue
            # Remove whitespace and split
            rulePair = ''.join(line.split()).split('->')
            if rulePair[0] in self.rulesDictionary:
                self.rulesDictionary[rulePair[0]].append(rulePair[1])
            else:
                self.rulesDictionary[rulePair[0]] = [rulePair[1]]
        self.rulesTables.append(self.rulesDictionary)
        return self.rulesTables

    def getRulesDictionary(self):
        return 0
        
