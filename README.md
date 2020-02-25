# Minecraft Printer

## ATTENTION!
This project will not be maintained anylonger due to missing hardware on my side.
Maybe I'll get back to it when I get a Raspberry Pi in the future.
*
These scripts require a Raspberry Pi to execute correctly.
They do NOT work with a normal Minecraft installation.

## Description
These scripts enable you to print an imported image into your Minecraft world.
Currently the produced pixel art is locked to a maximum in-game resolution of 64 by 64 blocks.

You can change this resolution if needed in the [Image.py](https://github.com/rrleo/minecraft_printer/blob/136fef1abf0cb8bbcbdb173402e3cd17497e6b90/Image.py#L16) file.

    maxRes = 64

## Instructions
1. Open the program:
    python3 main.py

2. In the Input box you have the options:
    - type your inserted message to the chat
    - execute the commands "/print <filename>" and "/clear"
    
    - Pictures are added by putting some into the "pictures" directory

3. Press "Send"

4. Enjoy the magic! :)

## Requirements

    python3 -m install mcpi
    python3 -m install appJar
    python3 -m install Pillow

- [x] Minecraft Pi (usually ONLY on Raspberry Pi)
- [x] Python 3.x
- [x] Pictures in your "pictures" directory
