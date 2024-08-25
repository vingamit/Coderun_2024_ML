with open('answer.txt', 'r') as file:
    res = [line.rstrip() for line in file]


with open('answer_space.txt', 'w', encoding='utf-8') as file:
    file.write(' \n'.join(res))