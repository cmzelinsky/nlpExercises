import random

text = 'C:/Users/courtney.zelinsky/Desktop/vocabAndRules.txt'

with open(text) as file:
    content = file.readlines()
newContent = []
newContent = "".join(content)
final = newContent.split('\n\n\n\n')
rulesList = final[0].split('\n\n')
lexiconList = final[1].split('\n\n')

rules = {}
lexicon = {}

def toDictionary(itemList, emptyDict):
    for item in itemList:
        individs = item.split(' ')
        parent = individs[0][:-1]
        del individs[0]
        siblings = [individ for individ in individs]
        emptyDict[parent] = siblings

toDictionary(rulesList, rules)
toDictionary(lexiconList, lexicon)


class Grammar():
    def __init__(self):
        self.rules = rules
        self.lexicon = lexicon

    def sentence(self):
        

class Node(Grammar):
    def __init__(self, tag, left, right):
        self.tag = tag
        self.left = left
        self.right = right
        
    def generatePOS(self):
        output = []
        components = rules[self.tag]
        for component in components:
            output.append(random.choice(lexicon[component]))
        return " ".join(output)
