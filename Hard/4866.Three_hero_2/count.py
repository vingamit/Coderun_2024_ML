import os

mas = os.listdir('dataset')
num = []

for el in mas:
    num.append(int(el.strip(".png")))

num.sort()

for i in range(1, len(num)):
    if num[i - 1] + 1 != num[i]:
        print(num[i - 1], num[i])

print(len(num))
print(max(num))