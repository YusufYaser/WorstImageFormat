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
import random
import re
import time

if len(sys.argv) < 2:
    print("Usage: " + sys.argv[0] + " <image_path> [scale]")
    print("       " + sys.argv[0] + " convert <source> <output>")
    print("       " + sys.argv[0] + " random <width> <height> <output>")
    exit(1)

if sys.argv[1] == "convert":
    if not len(sys.argv) == 4:
        print("Usage: " + sys.argv[0] + " convert <source> <output>")
        exit(1)

    try:
        source = Image.open(sys.argv[2])
    except FileNotFoundError:
        print("Source file not found!")
        exit(1)
    except UnidentifiedImageError:
        print("Source image is corrupt!")
        exit(1)

    width = source.width
    height = source.height
    data = ""

    output = open(sys.argv[3], "w")

    print("Converting...")

    print("=== Image Information ===")
    print(" - Width: " + str(width))
    print(" - Height: " + str(height))

    for x in range(width):
        for y in range(height):
            pixel = source.getpixel((x, y))
            for i in range(3):
                if pixel[i] == 10:
                    data += chr(11)
                elif pixel[i] == 13:
                    data += chr(14)
                else:
                    data += chr(pixel[i])

    output.write("1," + str(width) + "," + str(height) + "\n" + data)
    
    sys.exit(0)

if sys.argv[1] == "random":
    if not len(sys.argv) == 5:
        print("Usage: " + sys.argv[0] + " random <width> <height> <output>")
        exit(1)

    print("Creating image...")
    
    width = int(sys.argv[2])
    height = int(sys.argv[3])

    output = open(sys.argv[4], "w")

    data = ""

    for x in range(width):
        for y in range(height):
            r = int(random.randint(0, 255))
            g = int(random.randint(0, 255))
            b = int(random.randint(0, 255))
            data += chr(r) + chr(g) + chr(b)
    
    output.write("1," + str(width) + "," + str(height) + "\n" + data)

    sys.exit(0)

try:
    image = open(sys.argv[1], "r")
except FileNotFoundError:
    print("This file was not found!")
    exit(2)

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
    elif s > 0:
        return '{:02d}s'.format(s)


try:
    try:
        scale = int(sys.argv[2])
    except ValueError:
        scale = 1
    except IndexError:
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

        for sx in range(scale):
            for sy in range(scale):
                canvas.create_rectangle(
                    y * scale + sx, x * scale + sy, y * scale + sx, x * scale + sy,
                    outline = hex,
                    fill = hex
                )
        
        x += 1
        at += 1
        speed += 1
    
    window.protocol('WM_DELETE_WINDOW', window.destroy)
        
    print("Viewing image            ")

    window.mainloop()

except IndexError:
    window.mainloop()
except ValueError:
    window.mainloop()
except KeyboardInterrupt:
    print("\nCancelled")
    exit(3)
