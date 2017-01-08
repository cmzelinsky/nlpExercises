from __future__ import division
import os.path
import sys

# Credit to Julia Hockenmaier for this FST implementation starter code
# https://courses.engr.illinois.edu/cs498jh/HW/hw1.pdf

class Transition:
    # string_in
    # string_out
    def __init__(self, inState, inString, outString, outState):
        self.state_in = inState
        self.string_in = inString
        self.string_out = outString
        self.state_out = outState

    def equals(self, t):
        if self.state_in == t.state_in \
                and self.string_in == t.string_in \
                and self.string_out == t.string_out \
                and self.state_out == t.state_out:
            return True
        else:
            return False

class FSTstate:
    # id: an integer ID of the state
    # isFinal: is this a final state?
    def __init__(self, n, isF, fst):
        self.id = n
        self.isFinal = isF
        self.transitions = dict() # map inStrings to a set of all possible transitions
        self.FST = fst

    def addTransition(self, inString, outString, outState):
        newTransition = Transition(self, inString, outString, outState)
        if inString in self.transitions:
            for t in self.transitions[inString]:
                if t.equals(newTransition):
                    return
            self.transitions[inString].add(newTransition)
        else:
            self.transitions[inString] = set([])
            self.transitions[inString].add(newTransition)

    def parseInputFromStartState(self, inString):
        parseTuple = ("", self.id)
        parses = []
        (accept, stringParses) = self.parseInput(inString)
        if accept:
            for p in stringParses:
                completeParse = [parseTuple]
                completeParse.extend(p)
                parses.append(completeParse)
        return (accept, parses)

    def parseInput(self, inString):
        parses = []
        isAccepted = True

        DEBUG = False
        if DEBUG:
            print "parseInput: state: ", self.id, " parsing: " , inString

        # Case 1: no suffix
        if inString == "":
            epsilonParses = []
            epsilonAccepted = False
            # try all epsilon transitions
            if "" in self.transitions:
                transSet = self.transitions[""]
                for t in transSet:
                    outString = t.string_out
                    toStateID = t.state_out
                    toState = self.FST.allStates[toStateID]
                    parseTuple = (outString, toStateID)
                    (suffixAccepted, suffixParses) = toState.parseInput(inString)
                    if suffixAccepted:
                        epsilonAccepted = True
                        if suffixParses == []: #accepts.
                            parse_s = [parseTuple]
                            epsilonParses.append(parse_s)
                        else:
                            for s in suffixParses:
                                parse_s = [parseTuple]
                                parse_s.extend(s)
                                epsilonParses.append(parse_s)
            # if epsilon is accepted, add all its parses
            if epsilonAccepted:
                parses.extend(epsilonParses)
            # if this is a final state, add an empty parse
            if self.isFinal or parses != []:
                if DEBUG:
                    print "Accepted in state ", self.id
                return (True, parses)
            else:
                if DEBUG:
                    print "Rejected in state ", self.id
                return (False, None)
        # case 2: non-empty suffix: there needs to be one suffix that parses!)
        hasAcceptedSuffix = False;
        for i in range(0,len(inString)+1):
            prefix = inString[0:i]
            suffix = inString[i:len(inString)]
            if DEBUG:
                print "\t prefix: \'", prefix, "\' I=", i
            if prefix in self.transitions:
                if DEBUG:
                     print "\t prefix: ", prefix,  "suffix: ", suffix, "I=", i
                transSet = self.transitions[prefix]
                for t in transSet:
                    outString = t.string_out
                    toStateID = t.state_out
                    toState = self.FST.allStates[toStateID]
                    parseTuple = (outString, toStateID)
                    (suffixAccepted, suffixParses) = toState.parseInput(suffix)
                    if suffixAccepted:
                        hasAcceptedSuffix = True
                        if suffixParses == []:
                            parse_s = [parseTuple]
                            parses.append(parse_s)
                            thisPrefixParses = True
                        for s in suffixParses:
                            parse_s = [parseTuple]
                            parse_s.extend(s)
                            parses.append(parse_s)
        if hasAcceptedSuffix:
            return (True, parses)
        else:
            return (False, None)



    def printState(self):
        if self.isFinal:
            FINAL = "FINAL"
        else: FINAL = ""
        print "State", self.id, FINAL
        for inString in self.transitions:
            transList = self.transitions[inString]
            for t in transList:
                print "\t", inString, ":", t.string_out, " => ", t.state_out




class FST:
    def __init__(self, initialStateName="q0"):
        self.nStates = 0
        self.initState = FSTstate(initialStateName, False, self)
        self.allStates = dict()
        self.allStates[initialStateName] = self.initState

    def addState(self, name, isFinal=False):
        if name in self.allStates:
            print "ERROR addState: state", name, "exists already"
            sys.exit()
        elif len(self.allStates) >= 30:
            print "ERROR addState: you can't have more than 30 states"
            sys.exit()
        else:
            newState = FSTstate(name, isFinal, self)
            self.allStates[name] = newState

    def addTransition(self, inStateName, inString, outString, outStateName):
        if (len(inString) > 1):
            print "ERROR: addTransition: input string ", inString, " is longer than one character"
            sys.exit()
        if inStateName not in self.allStates:
            print "ERROR: addTransition: state ", inStateName, " does not exist"
            sys.exit()
        if outStateName not in self.allStates:
            print "ERROR: addTransition: state ", outStateName, " does not exist"
            sys.exit()
        inState = self.allStates[inStateName]
        inState.addTransition(inString, outString, outStateName)

    # epsilon:epsilon
    def addEpsilonTransition(self, inStateName, outStateName):
        if inStateName not in self.allStates:
            print "ERROR: addEpsilonTransition: state ", inStateName, " does not exist"
            sys.exit()
        if outStateName not in self.allStates:
            print "ERROR: addEpsilonTransition: state ", outStateName, " does not exist"
            sys.exit()
        if inStateName == outStateName:
            print "ERROR: we don't allow epsilon loops"
            sys.exit()
        inState = self.allStates[inStateName]
        inState.addTransition("", "", outStateName)

    # map every element in inStringSet to itself
    def addSetTransition(self, inStateName, inStringSet, outStateName):
         if inStateName not in self.allStates:
            print "ERROR: addSetTransition: state ", inStateName, " does not exist"
            sys.exit()
         if outStateName not in self.allStates:
            print "ERROR: addSetTransition: state ", outStateName, " does not exist"
            sys.exit()
         for s in inStringSet:
            self.addTransition(inStateName, s, s, outStateName)

    # map string to itself
    def addSelfTransition(self, inStateName, inString, outStateName):
         if inStateName not in self.allStates:
            print "ERROR: addSetTransition: state ", inStateName, " does not exist"
            sys.exit()
         if outStateName not in self.allStates:
            print "ERROR: addSetTransition: state ", outStateName, " does not exist"
            sys.exit()
         self.addTransition(inStateName, inString, inString, outStateName)

    # map every element in inStringSet to outString
    def addSetToStringTransition(self, inStateName, inStringSet, outString, outStateName):
         if inStateName not in self.allStates:
            print "ERROR: addSetDummyTransition: state ", inStateName, " does not exist"
            sys.exit()
         if outStateName not in self.allStates:
            print "ERROR: addSetDummyTransition: state ", outStateName, " does not exist"
            sys.exit()
         for s in inStringSet:
            self.addTransition(inStateName, s, outString, outStateName)


    # map every element in inStirngSet to outString
    def addSetEpsilonTransition(self, inStateName, inStringSet, outStateName):
         if inStateName not in self.allStates:
            print "ERROR: addSetEpsilonTransition: state ", inStateName, " does not exist"
            sys.exit()
         if outStateName not in self.allStates:
            print "ERROR: addSetEpsionTransition: state ", outStateName, " does not exist"
            sys.exit()
         for s in inStringSet:
            self.addTransition(inStateName, s, "", outStateName)

    def parseInput(self, inString):
        SHOW_STATES = True
        inString = inString.rstrip('\n')
        (canParse, allParses)  = self.initState.parseInputFromStartState(inString)
        allParsesAsString = ""
        if canParse:
            for parse in allParses:
                for tuple in parse:
                    outString, outState = tuple
                    allParsesAsString += outString
                if SHOW_STATES:
                    allParsesAsString += "\t  States: "
                    i = 0
                    for tuple in parse:
                        i += 1
                        outString, outState = tuple
                        allParsesAsString += outState
                        if i < len(parse):
                            allParsesAsString += " => "
                    allParsesAsString += "; "

            print inString, " ==> ", allParsesAsString
            return True
        else:
            print inString, " ==> ", "FAIL"
            return False

    def printFST(self):
        print "Printing FST", str(self)
        for stateID in self.allStates:
            state = self.allStates[stateID]
            state.printState()

    def parseInputFile(self, fileName):
        if os.path.isfile(fileName):
            file = open(fileName, "r")
            nParses = 0
            totalStrings = 0
            for line in file:
                totalStrings += 1
                canParse = self.parseInput(line)
                if canParse:
                    nParses += 1
            fraction = nParses/totalStrings
            print "### ", fraction,  "(", nParses, " out of ", totalStrings, ") parsed"


if __name__ == "__main__":
    file = sys.argv[1]
    f = FST("q0")
    #f.addState("1", True)
    #f.addState("2", True)
    #f.addState("3", True)
    V = set("aeiou")
    Y = set ("y")
    C = set("bcdfghjklmnprstvwxyz")
    C1 = C-Y

    f.addState("V", False)
    f.addState("VV", False)
    f.addState("VVC", True)
    f.addState("VVCC", True)
    f.addState("VC", False)
    f.addState("VCV", True)
    f.addState("VCVC", True)
    f.addState("VCVCC", True)
    f.addState("VCVCV", True)
    f.addState("VCC", True)
    f.addState("VCCV", True)
    f.addState("VCCVC", True)
    f.addState("VCCVCC", True)
    f.addState("VCCVCV", True)

    f.addState("C", False)
    f.addState("CV", True)
    f.addState("CC", False)
    f.addState("CVV", True)
    f.addState("CCy", True)
    f.addState("CCC", False)
    f.addState("CVC", True)
    f.addState("CVCCV", True)
    f.addState("CVCCVC", True)
    f.addState("CVCV", True)
    f.addState("CVCVC", True)
    f.addState("CVCVCC", True)
    f.addState("CVCVCV", True)
    f.addState("CVCVV", False)
    f.addState("CVCVVC", True)
    f.addState("CVCC", True)
    f.addState("CVCCy", True)
    f.addState("CVCCC", True)
    f.addState("CVCCCV", True)
    f.addState("CVCCCy", True)
    f.addState("CVVC", True)
    f.addState("CVVCC", True)
    f.addState("CVVCCC", True)
    f.addState("CVVCV", True)
    f.addState("CVVCCC", True)
    f.addState("CVCCVV", True)
    f.addSetTransition("q0", C, "C")
    f.addSetTransition("q0", V, "V")
    f.addSetTransition("V", C, "VC")
    f.addSetTransition("V", V, "VV")
    f.addSetTransition("VV", C, "VVC")
    f.addSetTransition("VVC", C, "VVCC")
    f.addSetTransition("VC", V, "VCV")
    f.addSetTransition("VC", C, "VCC")
    f.addSetTransition("VCC", V, "VCCV")
    f.addSetTransition("VCCV", C, "VCCVC")
    f.addSetTransition("VCCV", V, "VCCVC")
    f.addSetTransition("VCCVC", C, "VCCVCC")
    f.addSetTransition("VCCVC", V, "VCCVCV")
    f.addSetTransition("C", V, "CV")
    f.addSetTransition("C", C, "CC")
    f.addSetTransition("CC", C, "CCC")
    f.addSetTransition("CC", Y, "CCy")
    f.addSetTransition("CVCC", Y, "CVCCy")
    f.addSetTransition("CVCCV", V, "CVCCVV")
    f.addSetTransition("CC", V, "CV")
    f.addSetTransition("CCC", V, "CV")
    f.addSetTransition("CV", C, "CVC")
    f.addSetTransition("CVC", V, "CVCV")
    f.addSetTransition("CVC", C, "CVCC")
    f.addSetTransition("CVCV", C, "CVCVC")
    f.addSetTransition("CVCVC", C, "CVCVCC")
    f.addSetTransition("CVCVC", V, "CVCVCV")
    f.addSetTransition("CV", V, "CVV")
    f.addSetTransition("CVV", C, "CVVC")
    f.addSetTransition("CVVC", C, "CVVCC")
    f.addSetTransition("CVVCC", C, "CVVCCC")
    f.addSetTransition("CVVC", V, "CVVCV")
    f.addSetTransition("CVCC", V, "CVCCV")
    f.addSetTransition("CVCC", C1, "CVCCC")
    f.addSetTransition("CVCCV", C, "CVCCVC")
    f.addSetTransition("CVCV", V, "CVCVV")
    f.addSetTransition("CVCVV", C, "CVCVVC")
    f.addSetTransition("VCV", C, "VCVC")
    f.addSetTransition("VCVC", C, "VCVCC")
    f.addSetTransition("VCVC", V, "VCVCV")
    f.addSetTransition("CVCCC", V, "CVCCCV")
    f.addSetTransition("CVCCC", Y, "CVCCCy")
    # f.printFST()
    #f.parseInput("mans")
    #f.parseInput("woman")
    #f.parseInput("aaaooouaoemans")
   # f.parseInputFile("SimpleVerbs1.txt")
    f.parseInputFile(file)
