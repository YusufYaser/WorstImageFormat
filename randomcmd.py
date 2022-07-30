import sys
import random

def rand():
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

if __name__ == "__main__":
    print("Please run ./main.py")