import json
import datetime

class Node:

    def __init__(self, left, right):
        self.left = left
        self.right = right

text = 'abcde'
letters = set(text)
frequences = []
for letter in letters:
    frequences.append((text.count(letter), letter))
print(frequences)

while len(frequences) > 1:
    frequences = sorted(frequences, key=lambda x: x[0], reverse=True)
    first = frequences.pop()
    second = frequences.pop()
    freq = first[0]+second[0]
    frequences.append((freq, Node(first[1], second[1])))
    print(frequences)

code = {letter: '' for letter in letters}

def walk(node, path=''):
    if isinstance(node, str):
        code[node] = path
        return
    walk(node.left, path + '0')
    walk(node.right, path + '1')
    
walk(frequences[0][1])




print(code)