s = set()
with open('dict.txt') as file:
    s.update(set(file.read()))
with open('queries.txt') as file:
    s.update(set(file.read()))
print(s)