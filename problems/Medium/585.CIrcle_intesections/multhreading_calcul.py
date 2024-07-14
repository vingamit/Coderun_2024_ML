import numpy as np
from time import time
from concurrent.futures import ThreadPoolExecutor


with open("data/data.txt", 'r') as file:
    tripls = []
    for line in file.readlines():
        x1, y1, r1, x2, y2, r2, x3, y3, r3 = map(int, line.rstrip().split())
        tripls.append([(x1, y1, r1), (x2, y2, r2), (x3, y3, r3)])
with open("data/enrich.txt", "r") as file:
    area = []
    for line in file.readlines():
        mas = list(map(int, line.rstrip().split()))
        area.append(mas)
with open("time.txt", "w") as file:
    file.write("")
with open("results.txt", "w") as file:
    file.write("")

def calc_array(fi, se, th, centr):
    start = time() 
    min_x, min_y, delta_x, delta_y = centr
    num = 0
    for _ in range(100):
        x = min_x + np.random.random(100_000_000) * delta_x
        y = min_y + np.random.random(100_000_000) * delta_y
        fim = ((x - fi[0]) ** 2 + (y - fi[1]) ** 2) < fi[2] ** 2
        sem = ((x - se[0]) ** 2 + (y - se[1]) ** 2) < se[2] ** 2
        thm = ((x - th[0]) ** 2 + (y - th[1]) ** 2) < th[2] ** 2

        num  += (fim & sem & thm).sum()
    part = num / 10_000_000_000
    array = part * delta_x * delta_y
    print(part * delta_x * delta_y, time() - start)
    with open("time.txt" "a") as file:
        file.write(str(time() - start))
    with open("results.txt", "a") as file:
        file.write(str(array))
    return array

n = 5
with ThreadPoolExecutor(max_workers=n) as executor:
    futures = [executor.submit(calc_array, fi, se, th, centr) for (fi, se, th), centr in zip(tripls, area)]

    results = [future.result() for future in futures]
