def contained(string1, char1):  # check if there is any appearance of char1 in string1 outside of parentheses
    parentheses = 0  # opened
    for e in range(len(string1)):
        if string1[e] == '(':
            parentheses += 1
        elif string1[e] == ')':
            parentheses -= 1
        elif parentheses == 0 and string1[e] == char1:
            return 1
    return 0

# read automaton
with open("automaton.txt") as file:
    nodesNo = int(file.readline())  # number of nodes e.g.: nodes = {0, 1, 2, 3, 4} => nodesNo = 5, node counting must start at 0!
    alpha = file.readline().strip()+'#'  # '#' stands for lambda

    labels = [0] * nodesNo
    for i in range(nodesNo):
        labels[i] = [''] * nodesNo

    line = file.readline()  # the format is originNode-letter-destinationNode
    while line.find("-") > 0:
        origin, label, destination = line[:-1].split("-")
        labels[int(origin)][int(destination)] = (labels[int(origin)][int(destination)] + ' ' + label).strip()
        line = file.readline()
    startNode = int(line)
    endNode = tuple([int(x) for x in file.readline().split()])  # e.g.: 2 3
    print('\n', labels, 'step 0: automaton read')

# step 1: combine alternate labels
for org in range(nodesNo):
    for dest in range(nodesNo):
        labels[org][dest] = '+'.join(labels[org][dest].split())
print('\n', labels, 'step 1: combined alternate labels')

# step 2 & 3: create new start & end nodes
for org in range(nodesNo):
    labels[org].extend(['', ''])
nodesNo += 2
labels.append([''] *nodesNo)  # add new start node
labels[nodesNo-2][startNode] = '#'
startNode = nodesNo-2
labels.append([''] *nodesNo)  # add new end node
for org in endNode:
    labels[org][nodesNo-1] = '#'
endNode = nodesNo-1
print('\n', labels, 'step 2 & 3: created new start & end nodes')

# step 4: delete intermediate nodes
for nodeDeleted in range(nodesNo-2):
    for _from in range(nodeDeleted+1, nodesNo):  # for every pair (node1, node2) where exists labels[node1][nodeDeleted] x
        for _to in range(nodeDeleted+1, nodesNo):  # and labels[deletedNode][node2] y, labels[node1][node2] if exists, is alternated ( + or |)
            if len(labels[_from][nodeDeleted]) > 0 and len(labels[nodeDeleted][_to]) > 0:  # with xZy where Z is z*, z is labels[deletedNode][deletedNode] if exists or '#'
                before = labels[_from][nodeDeleted]  # x
                if before == '#':
                    before = ''
                middle = labels[nodeDeleted][nodeDeleted]  # z
                if middle == '#':
                    middle = ''
                after = labels[nodeDeleted][_to]  # y
                if after == '#':
                    after = ''
                if contained(before, '+') and (len(after) or len(middle)):  # perserve order or operation if there is any main alternation
                    before = '(' + before + ')'
                if contained(after, '+') and (len(before) or len(middle)):  # perserve order or operation if there is any main alternation
                    after = '(' + after + ')'
                if len(middle) > 1:   # perserve order or operation
                    middle = '(' + middle + ')'
                if len(middle) > 0:
                    if before == middle:  # if z exists and is equal to x, x becomes '#' and z becomes z` (=zz*)
                        before = ''
                        middle += '`'
                    elif middle == after:  # if z exists and is equal to y, y becomes '#' and z becomes z` (=z*z)
                        after = ''
                        middle += '`'
                    else:                  # if z exists and is neither equal to x neither equal to y, z becomes z*
                        middle += '*'
                new = before + middle + after  # new part of label is xZy
                if new == '':  # if x and z are '#' and z is '#' or doesn't exist the new part is '#'
                    new = '#'
                if contained(labels[_from][_to], '+') == 0 \
                        and len(labels[_from][_to]) > 0 \
                        and labels[_from][_to][-1] == '`' \
                        and new == "#'":  # if previous label has the form (x)` with any label x and the new part
                    labels[_from][_to] = labels[_from][_to][:-1] + '*'  # of the label is just # then it becomes (x)*
                elif contained(new, '+') == 0 \
                        and len(new) > 0 \
                        and new[-1] == '`' \
                        and labels[_from][_to] == '#': # new part of label has the form (x)` with any label x and
                    labels[_from][_to] = new[:-1] + '*'  # the previous label is just # then it becomes (x)*
                else:
                    labels[_from][_to] = labels[_from][_to] + '+' + new  # x+y where x is the previous label and
                labels[_from][_to] = labels[_from][_to].strip('+')  # y is the new part o the label

    for _to in range(nodesNo):  # clear labels[deletedNode][x] for any node x
        labels[nodeDeleted][_to] = ''
    for _from in range(nodesNo):  #clear labels[x][deletedNode] for any node x
        labels[_from][nodeDeleted] = ''

    print('\n', labels, 'step 4: deleted node', nodeDeleted)

print('\n', labels[startNode][endNode], 'step 5: equivalent regular expression')
