from PIL import Image

import os
import sys
import math

import settings

def getRGB(img, x, y):
    img = img.convert("RGBA")
    r, g, b, a = img.getpixel((x, y))

    return r, g, b, a


def resize(img):
    img = Image.open(img)
    x, y = getSize(img)
    maxRes = settings.resolution

    aspectRatio = max(x, y) / min(x, y)
    if x == max(x, y):
        x = maxRes
        y = int(maxRes / aspectRatio)
    else:
        x = int(maxRes / aspectRatio)
        y = maxRes

    return img.resize((int(x), int(y)))


# https://gist.github.com/revolunet/848913
def extractFrames(inGif):
    frame = Image.open(inGif)
    nframes = 0
    while frame:
        frame.save('pictures/frames/{}.png'.format(nframes), 'PNG')
        nframes += 1

        try:
            frame.seek(nframes)
        except EOFError:
            break
        
    return True


def getSize(img):
    return img.size
