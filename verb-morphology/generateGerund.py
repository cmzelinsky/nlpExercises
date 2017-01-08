from fst import *

AZ = set("abcdefghijklmnopqrstuvwxyz")
VOWS = set("aeiou")
CONS = set("bcdfghjklmnprstvwxz")
E = set("e")
IE = set("ie")
EA = set("ea")
I = set("i")
P = set("p")
A = set("a")
T = set("t")
U = set("u")
Y = set("y")

# run like: python generateGerund.py 360verbs.txt

if __name__ == "__main__":
    file = sys.argv[1]

    #
    # States
    # ---------------------------------------

    f = FST("q0") # q0 is the initial (non-accepting) state
    f.addState("q1") # a non-accepting state
    f.addState("q2")
    f.addState("q3")
    f.addState("q4")
    f.addState("q5")
    f.addState("q6")
    f.addState("q7")
    f.addState("q8")
    f.addState("q9")
    f.addState("q10")
    f.addState("q11")
    f.addState("q_EOW", True) # accepting state

    #
    # The transitions
    # ---------------------------------------
    # My advice is to draw out the automaton first -- this helped me a lot

    f.addSetTransition("q0", AZ, "q1")
    f.addSetTransition("q1", CONS, "q6")
    f.addSetTransition("q6", CONS, "q6")
    f.addSetTransition("q1", VOWS-I, "q2")
    f.addSetTransition("q1", I, "q10")
    f.addSetTransition("q10", CONS, "q11")
    f.addSetTransition("q11", CONS, "q11")
    f.addTransition("q11", "", "ing", "q_EOW")
    f.addTransition("q11", "e", "ing", "q_EOW")
    f.addSetTransition("q2", E, "q7")
    f.addSetTransition("q2", Y, "q3")
    f.addSetTransition("q6", VOWS-I, "q2")
    f.addTransition("q7", "", "ing", "q_EOW")
    f.addSetTransition("q7", CONS, "q8")
    f.addTransition("q8", "", "ing", "q_EOW")
    f.addTransition("q6", "", "ing", "q_EOW")
    f.addSetTransition("q2", VOWS-E, "q2")
    f.addSetTransition("q2", CONS, "q6")
    f.addTransition("q6", "e", "", "q3")
    f.addSetTransition("q6", Y, "q3")
    f.addSetTransition("q6", I, "q9")
    f.addSetTransition("q9", CONS, "q6")
    f.addSetTransition("q2", VOWS-IE, "q3")
    f.addTransition("q1", "i", "", "q5")
    f.addTransition("q5", "e", "y", "q3")
    f.addTransition("q3", "", "ing", "q_EOW")
    f.parseInputFile(file)
