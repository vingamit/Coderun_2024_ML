with open('answer.txt', 'r') as file:
    ans = [line.strip().split() for line in file]

with open('dict.txt', 'r') as file:
    dictionary = set(line.strip() for line in file)


with open('queries.txt', 'r') as file:
    queries = [line.strip() for line in file]


for i, (query, an) in enumerate(zip(queries, ans)):
    if query != an[0]:
        print(query, an)
        print(i)


for an in ans:
    if an[1] == '0' and an[0] not in dictionary:
        print(an)