from PIL import Image

pos = set()

for i in range(9605):
    img = Image.open(f"dataset/{i:0>4}.png")
    w, h = img.width, img.height
    pos.add((h, w))

print(pos)