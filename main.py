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
import settings


class MinecraftRemote():
    '''
    you can add more colors if you want
    just add another entry:
    
    (blockID, metaData): (r, g, b)
    '''
    colors = settings.colors
    
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

        self.output_message("Processing request...")

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

        self.output_message("Processing request...")

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

                self.mc.setBlock(-settings.resolution + x, 1, -settings.resolution + y, blockID, blockMeta)


    def clearArea(self):
        size = 512
        self.mc.setBlocks(-size, 0, -size, size - 1, 255, size, block.AIR)
        self.mc.setBlocks(-size, 0, -size, size - 1, 0, size, block.WOOL, 0)

        size = settings.resolution / 2
        self.mc.setBlocks(-size, 1, -size, -size, 1, size, block.GOLD_BLOCK)
        self.mc.setBlocks(-size, 1, -size, size - 2, 1, -size, block.GOLD_BLOCK)
        self.mc.setBlocks(size, 1, size, -size, 1, size, block.GOLD_BLOCK)
        self.mc.setBlocks(size, 1, size, size - 2, 1, -size, block.GOLD_BLOCK)


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
