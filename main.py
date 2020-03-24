from mcpi.minecraft import Minecraft
from mcpi import block
from mcpi.block import Block

from appJar import gui

import sys
import math
import os
import time
import threading

import Image # reference to Image.py


class MinecraftRemote():
    '''
    you can add more colors if you want
    just add another entry:
    
    (blockID, metaData): (r, g, b)
    '''

    colors = { \
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
            (103, 0): (131, 134, 32) # melon
        }


    def __init__(self):
        '''
        Setup for the Minecraft instance and the Application GUI
        '''
        try:
            self.mc = Minecraft.create()

        except ConnectionRefusedError:
            sys.exit(print("[MCWorldNotFound] Make sure the world is running before starting the script."))

        # app interface
        self.app = gui("Minecraft")
        self.app.addLabelEntry("ChatBox", 0, 0)
        self.app.addButton("Send", self.handleRequests, 0, 1)
        self.app.go()


    def output_message(self, msg):
        '''
        Present a given message to the user via terminal and in-game chat
        '''
        self.mc.postToChat(msg)
        print(msg)


    def handleRequests(self, btn):
        '''
        Accepts and handles requests by commands
        '''
        msg = self.app.getEntry("ChatBox")

        # Resetting to default vantage point
        print("Setting default position")
        self.mc.player.setPos(0, 134, 0)
        self.clearArea()

        #msg.replace("§", "")
        if len(msg) == 0:
            return

        args = msg.split(" ")
        if msg[0] != "/": # checks the input for unsupported characters / commands
            try:
                self.mc.postToChat(msg)
            except UnicodeEncodeError:
                self.mc.postToChat("[ERROR] You entered unsupported characters")
            return

        commands = ["/print", "/gif", "/clear"]
        if args[0] not in commands:
            self.output_message("[ERROR] Command not found")
            return

        switch = \
        {
            0 : threading.Thread(target=self.initiate_printing, args=args),
            1 : threading.Thread(target=self.output_gif, args=args),
            2 : threading.Thread(target=self.clearArea)
        }

        process = switch.get(commands.index(args[0]))
        process.start()
        

    def initiate_printing(self, command, name=None):
        if name == None:
            output_message("[ERROR] Filename must be provided")
            return

        was_not_found = True
        for i in os.listdir("./pictures/"):
            filename = i[0:i.rfind(".")] # separates filename and extension

            if filename == name and os.path.isfile("./pictures/" + i):
                was_not_found = True
                name = i
                break

        if was_not_found == False:
            self.output_message("[ERROR] File '{}' does not exist. Try again without the extension".format(name))
            return

        self.output_message("Now printing: {}".format(name))
        self.clearArea()
        self.outputImage(name)
        self.output_message("Finished")


    def output_gif(self, command, name=None):
        if name == None:
            self.output_message("[ERROR] Filename must be provided")

        Image.extractFrames("./pictures/" + name + ".gif")
        framePath = "./pictures/frames/"
        for frame in os.listdir(framePath):
            self.outputImage(frame, True)

        self.output_message("Finished")
        self.deleteFrames()


    def deleteFrames(self):
        framePath = "./pictures/frames/"
        for frame in os.listdir(framePath):
            os.remove(framePath + frame)


    def outputImage(self, filename, frame=False):
        try:
            outDir = "./pictures/"
            if frame:
                outDir += "frames/"
            img = Image.resize(outDir + filename)

        except OSError as e:
            self.output_message("File format not supported")
            return

        imageSize = Image.getSize(img)
        for y in range(imageSize[1]):
            for x in range(imageSize[0]):
                r, g, b, a = Image.getRGB(img, x, y)
                if a == 255:
                    blockID, blockMeta = self.getBlockID(r, g, b)
                else:
                    blockID, blockMeta = 0, 0

                self.mc.setBlock(-128 + x, 1, -128 + y, blockID, blockMeta)


    def clearArea(self):
        self.output_message("Processing request...")
        self.mc.setBlocks(-128, 0, -128, 128, 255, 128, block.AIR)
        self.mc.setBlocks(-128, 0, -128, 128, 0, 128, block.WOOL, 0)

        self.mc.setBlocks(-129, 1, -129, -129, 1, 129, block.GOLD_BLOCK)
        self.mc.setBlocks(-129, 1, -129, 129, 1, -129, block.GOLD_BLOCK)
        self.mc.setBlocks(129, 1, 129, -129, 1, 129, block.GOLD_BLOCK)
        self.mc.setBlocks(129, 1, 129, 129, 1, -129, block.GOLD_BLOCK)


    def getBlockID(self, r, g, b):
        currColor = []

        for color in self.colors:
            vec3Distance = math.sqrt((r - self.colors[color][0]) ** 2 + (g - self.colors[color][1]) ** 2 + (b - self.colors[color][2]) ** 2)

            if len(currColor) == 0 or vec3Distance < currColor[0]:
                currColor = [vec3Distance, color]

        block_id = currColor[1]
        
        return block_id


if __name__ == "__main__":
    MinecraftRemote()
