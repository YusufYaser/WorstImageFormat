#!/usr/bin/python3

#
# Worst Image Format
#
# Author: YusufYaser
# Date: 28/05/2022
#

import sys
from tkinter import *
from PIL import Image, UnidentifiedImageError
import re
import time

import convertcmd
import randomcmd

def GetUnixTime():
    return round(time.time())

def TimeFormat(seconds):
    d = seconds // (3600 * 24)
    h = seconds // 3600 % 24
    m = seconds % 3600 // 60
    s = seconds % 3600 % 60
    if d > 0:
        return '{:02d}d {:02d}h {:02d}m {:02d}s'.format(d, h, m, s)
    elif h > 0:
        return '{:02d}h {:02d}m {:02d}s'.format(h, m, s)
    elif m > 0:
        return '{:02d}m {:02d}s'.format(m, s)
    
    return '{:02d}s'.format(s)

def main():
    if len(sys.argv) < 2:
        print("Usage: " + sys.argv[0] + " <image_path> [scale]")
        print("       " + sys.argv[0] + " convert <source> <output>")
        print("       " + sys.argv[0] + " random <width> <height> <output>")
        exit(1)

    if sys.argv[1] == "convert":
        convertcmd.convert()
        sys.exit(0)
    elif sys.argv[1] == "random":
        randomcmd.rand()
        sys.exit(0)

    try:
        image = open(sys.argv[1], "r")
    except FileNotFoundError:
        print("This file was not found!")
        exit(2)

    try:
        try:
            scale = int(sys.argv[2])
        except ValueError or IndexError:
            scale = 1


        print("Reading image")

        dim = image.readline().replace("\n", "").split(",")
        dim[0] = int(dim[2])
        dim[1] = int(dim[1])

        window = Tk()
        window.resizable(False, False)
        window.title(image.name + " - " + str(int(dim[1])) + "x" + str(int(dim[0])) + " scaled by " + str(scale))
        window.geometry(str(int(dim[1] * scale)) + "x" + str(int(dim[0] * scale)))

        data = image.read()
        pixels = re.findall(".{3}", data)

        canvas = Canvas(
            window,
            width = int(dim[1] * scale),
            height = int(dim[0] * scale),
            bg="#000"
        )

        canvas.pack()

        x = 1
        y = 1
        at = 0
        max = dim[0] * dim[1]
        speed = 0
        lastsecond = GetUnixTime()
        remaining = "unknown"
        print("Rendering image")
        print(" 0%\r", end="")
        for pixel in pixels:
            rgb = (ord(pixel[0]), ord(pixel[1]), ord(pixel[2]))
            hex = '#%02x%02x%02x' % rgb
            if not lastsecond == GetUnixTime():
                remaining = TimeFormat(round((max - at) / speed))
                speed = 0
                lastsecond = GetUnixTime()
            print(" " + str(round(at / max * 100, 1)) + "% - " + str(remaining) + " remaining                      \r", end="")

            if x > dim[0]:
                x = 1
                y += 1

            canvas.create_rectangle(
                y * scale, x * scale,
                y * pow(scale, 2), x * pow(scale, 2),
                outline = hex,
                fill = hex
            )
            
            x += 1
            at += 1
            speed += 1
        
        window.protocol('WM_DELETE_WINDOW', window.destroy)
        
        if at < max:
            print("Unexpected EOF, showing image anyways")

        print("Showing image                   ")

        window.mainloop()

    except IndexError or ValueError as e:
        print("There was an error, attempting showing image anyways")
        print(e)
        window.mainloop()
    except KeyboardInterrupt:
        print("\nCancelled")
        exit(3)

if __name__ == "__main__":
    main()