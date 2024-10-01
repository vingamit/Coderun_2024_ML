with open('answer.txt', 'r') as file:
    fi = file.readlines()

with open('answer1.txt', 'r') as file:
    se = file.readlines()

with open('dict.txt') as file:
    print(min(len(line.strip()) for line in file))


# for s in se:
#     if len(s.split()[0]) < 3:
#         print(s)

i = 0

# for f, s in zip(fi, se):
#     if f != s:
#         print(f)
#         print(s)
#         i += 1
# print(i)