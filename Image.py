from PIL import Image
import sys
import math

def getRGB(img, x, y):
    img = img.convert("RGBA")
    r, g, b, a = img.getpixel((x, y))

    return r, g, b, a


def resize(img):
    img = Image.open(img)

    x, y = getSize(img)

    maxRes = 64

    aspectRatio = max(x, y) / min(x, y)
    if x == max(x, y):
        x = maxRes
        y = int(maxRes / aspectRatio)

    else:
        x = int(maxRes / aspectRatio)
        y = maxRes
    

    return img.resize((int(x), int(y)))


def getSize(img):
    return img.size
