with open('aswer.txt', 'r') as file:
    rows = list(map(lambda x: x.strip().split(), file.readlines()))

with open('dict.txt', 'r') as file:
    diction = list(map(lambda x: x.strip(), file.readlines()))
    dict_set = set(diction)

with open('queries.txt', 'r') as file:
    queries = list(map(lambda x: x.strip(), file.readlines()))


for i in range(100_000):
    if queries[i] != rows[i][0]:
        print(i)

for i in range(100_000):
    if rows[i][-1] != '5+' and rows[i][-1] != '0' and rows[i][-1] not in dict_set:
        print(i)

from workpiece import process_query

print(process_query('оэтекутр', ))