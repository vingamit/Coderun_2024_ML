ik = []

with open('bknp_public_queries.txt', 'r') as file:
    for line in file:
        i, k = map(int, line.rstrip().split()[:2])
        ik.append([i, k])


with open('queries.txt', 'w') as file:
    for i, k in ik:
        file.write(f"{i} {k}\n")