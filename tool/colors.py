'''
Returns the average color code of every texture in
the designated texture folder --> ./texture/

format:
filename: RGB

'''

from PIL import Image
import sys
import os


def init():
    inDir = "./textures/"
    if os.path.isdir() == False:
        os.mkdir(inDir)

    for texture in os.listdir(inDir):
        image = Image.open(inDir + texture)
        rgb = get_average_rgb(image)

        print("{}: RGB({}, {}, {})".format(texture, rgb[0], rgb[1], rgb[2]))


def get_average_rgb(image):
    image_size = image.size
    rgb = [0, 0, 0]

    for x in range(image_size[0]):
        for y in range(image_size[1]):
            values = image.getpixel((x, y))

            rgb[0] += values[0]
            rgb[1] += values[1]
            rgb[2] += values[2]

    total_pixel = image_size[0] * image_size[1]
    for value in range(3):
        rgb[value] = int(round(rgb[value] / total_pixel, 0))

    return rgb


if __name__ == "__main__":
    init()