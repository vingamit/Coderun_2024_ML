res = []

for i in range(10):
    with open(f'answer{i}.txt', 'r') as file:
        res.append(file.read())

with open('aswer.txt', 'w') as file:
    file.write('\n'.join(res))