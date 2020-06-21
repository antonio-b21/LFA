import sys

def validate(word, currentState):
    if len(word) == 0:
        if currentState in finalStates:
            print('Cuvant acceptat')
            sys.exit()
    else:
        letter = word[0]
        if letter == '#':
            validate(word[1:], currentState)
        else:
            if letter in transitions:
                for dest in transitions[letter][currentState]:
                    validate(word[1:], dest)

with open("automaton.txt") as file:
    statesNo = int(file.readline())
    alpha = file.readline().strip()
    transitions = {}
    for letter in alpha:
        transitions[letter] = [() for i in range(statesNo)]
    line = file.readline()
    while line[0] in alpha:
        letter = line[0]
        position = int(line[2])
        destination = tuple([int(x) for x in line[4:].split()])
        transitions[letter][position] = destination
        line = file.readline()
    initialState = int(line)
    finalStates = tuple([int(x) for x in file.readline().split()])

word = input("Cuvant=")
validate(word, initialState)
print("Cuvant neacceptat")
