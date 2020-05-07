def islower(letter):
    return letter.islower()

def generate(maxLen, word = "S"):
    if len("".join(filter(islower, word))) > maxLen:
        return
    if word == "":
        solution.add("#")
    elif word.islower() and len(word) <= maxLen:
        solution.add(word)
    else:
        for (index, letter) in enumerate(word):
            if letter.isupper():
                for production in productions[letter]:
                    generate(maxLen, word[:index] + production + word[index+1:])


with open("grammar.txt") as file:
    productions = {}
    for line in file.readlines():
        if line == "\n":
            break
        left, right = line[:-1].split("-")
        if right == "#":
            right = ""
        if left not in productions:
            productions[left] = []
        productions[left].append(right)

n = int(input("n="))
solution = set()
generate(n)
print("Solutie:", ", ".join(sorted(solution)))
