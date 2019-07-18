from mcpi.minecraft import Minecraft
from mcpi import block
from mcpi.block import Block

from appJar import gui

import sys
import math
import os
import time

import Image


def init():
    global mc
    mc = Minecraft.create()

    # app interface
    global app
    app = gui("Minecraft")
    app.addLabelEntry("ChatBox", 0, 0)
    app.addButton("Send", handleRequests, 0, 1)
    app.go()
    #


def clearArea():
    mc.setBlocks(-320, -1, -320, 320, 25, 320, 0)
    mc.setBlocks(-320, -1, -320, 320, -1, 320, 9)


def handleRequests(btn):
    msg = app.getEntry("ChatBox")

    if msg[0] != "/":
        mc.postToChat(msg)

    # RESET
    print("Setting default position")
    mc.player.setPos(50.5, 48, 45.5)
    # RESET END

    args = msg.split(" ")
    command = args[0]

    if command == "/print":
        clearArea()
        mc.postToChat("Executing print command...")

        for i in os.listdir("./pictures/"):
            if i[0:len(args[1])] == args[1]:
                 args[1] = i

        try:
            main("pictures/" + args[1])
        except FileNotFoundError:
            mc.postToChat("File does not exist")

    elif command == "/clear":
        print("clearing..")
        clearArea()
    

def main(filename):
    img = Image.resize(filename)

    for y in range(Image.getSize(img)[1]):
        for x in range(Image.getSize(img)[0]):
            r, g, b, a = Image.getRGB(img, x, y)
            if a == 255:
                blockID, blockMeta = getBlockID(r, g, b)
            else:
                blockID, blockMeta = 0, 0
                
            mc.setBlock(10 + x, 1, 10 + y, blockID, blockMeta)

    mc.postToChat("Finished")


def getBlockID(r, g, b):
    blockColor = {
        (35, 0): (228, 228, 228), # white
        (35, 8): (160, 167, 167), # light gray
        (35, 7): (65, 65, 65), # dark gray
        (35, 15): (24, 20, 20), # black
        (35, 14): (158, 43, 39), # red
        (35, 1): (234, 126, 53), # orange
        (35, 4): (194, 181, 28), # yellow
        (35, 5): (57, 186, 46), # lime green
        (35, 3): (99, 135, 210), # light blue
        (35, 9): (38, 113, 145), # cyan
        (35, 11): (37, 49, 147), # blue
        (35, 10): (126, 52, 191), # purple
        (35, 2): (190, 73, 201), # magenta
        (35, 6): (217, 129, 153), # pink
        (35, 12): (86, 51, 28), # brown
        (35, 13): (54, 75, 24), # green     ### WOOL END ###
        (17, 2): (88, 70, 43), # log
        (3, 0): (117, 84, 58), # dirt
        (5, 0): (140, 114, 70), # planks
        (18, 0): (33, 125, 22), # leaves
        (89, 0): (128, 105, 63), # glowstone
        (24, 0): (84, 84, 84), # sandstone
        (87, 0): (98, 47, 46), # netherrack
        (7, 0): (74, 74, 74), # bedrock
        (41, 0): (220, 211, 72), # goldblock
        (1, 0): (110, 110, 110), # stone
        (45, 0): (127, 83, 71), # bricks
        (42, 0): (196, 196, 196), # ironblock
        (57, 0): (97, 196, 191), # diamondblock
        (103, 0): (131, 134, 32), # melon
    }

    currColor = ()

    for color in blockColor:
        vec3Distance = math.sqrt((r - blockColor[color][0]) ** 2 + (g - blockColor[color][1]) ** 2 + (b - blockColor[color][2]) ** 2)

        if len(currColor) == 0 or vec3Distance < currColor[0]:
            currColor = (vec3Distance, color)

    ID = currColor[1]
    
    return ID


if __name__ == "__main__":
    try:
        #filename = sys.argv[1]
        pass
        
    except IndexError:
        sys.exit(print("Usage: python3 {} [filename]".format(__file__)))

    init()
