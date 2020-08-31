# Minecraft Printer

## Description
These scripts enable you to print an imported image into your Minecraft world.
Currently the produced pixel art is set to a maximum in-game resolution of 256 by 256 blocks.

You can change this resolution if needed in the [settings.py](https://github.com/kraibse/minecraft_printer/blob/685e3468dc2b06cc70edc1fc6ab644d7e32c7090/settings.py#L1) file.

    resolution = 256

It is recommended to **use a new world for this script** and also change the resolution to **64** if you want to run the scripts on a RaspberryPi.
Minecraft Pi Edition wont allow any changes in the render distance (also the performance is very bad)
If you're on PC you can adjust the resolution to your liking.


Original photo:                                 
![Original photo](https://github.com/kraibse/minecraft_printer/blob/master/pictures/example/original.png)

In-game screenshot:
![Screenshot](https://github.com/kraibse/minecraft_printer/blob/master/pictures/example/ingame.png)

## Instructions
1. Start the world (RaspberryPi) or the server (desktop)
    start.bat / start.sh

2. Run the program:
    python3 main.py
    OR
    python main.py

3. In the Input box you have the options:
    - type your inserted message to the chat
    - insert a command (a list of commands will be down below)
        
    - pictures and gifs are added by putting some into the "pictures" directory

4. Press "Send"

5. Enjoy the magic! :)

## Commands
### Remember to insert the filename without the file extension
Removing any blocks in a 128 block radius (up to the build limit) 

    /clear
    
Printing a picture in Minecraft

    /print {filename}
    
Outputting a gif frame by frame:

    /gif {filename}

## Requirements

    python3 -m install mcpi
    python3 -m install appJar
    python3 -m install Pillow

- [x] Minecraft Pi
OR
- [x] Spigot Server with the "RaspberryJuice" plugin
    - the server is included in the files and just needs to be started

Additionally you need:
- [x] Python 3.x
- [x] Pictures in your "pictures" directory
