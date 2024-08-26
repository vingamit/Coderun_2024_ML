with open('ans.txt', 'r') as file:
    di = {"0": 0, "1": 0, "2": 0, "3": 0, "4": 0, "5+": 0}

    for line in file:
        line = line.strip().split()
        di[line[1]] += 1


for key, item in di.items():
    print(key, item)