import sys
from PIL import Image, UnidentifiedImageError

def convert():
    if not len(sys.argv) == 4:
        print("Usage: " + sys.argv[0] + " convert <source> <output>")
        exit(1)

    try:
        source = Image.open(sys.argv[2]).convert('RGB')
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
            r, g, b = source.getpixel((x, y))
            
            if r == 10 or r == 13:
                data += chr(r + 1)
            else:
                data += chr(r)
            
            if g == 10 or g == 13:
                data += chr(g + 1)
            else:
                data += chr(g)
            
            if b == 10 or b == 13:
                data += chr(b + 1)
            else:
                data += chr(b)

    output.write("1," + str(width) + "," + str(height) + "\n" + data)

if __name__ == "__main__":
    print("Please run ./main.py")