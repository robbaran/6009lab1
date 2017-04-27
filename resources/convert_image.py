#!/usr/bin/env python2.7

import os, sys, json
import Image

def convert(f):
    img = Image.open(f)

    (width, height) =  img.size

    px = img.load()
    pixels = []

    for y in range(height):
        for x in range(width):
            #print px[x,y]
            (r,g,b) = px[x,y]
            lum = int(round(0.2126*r + 0.7152*g + 0.0722*b))
            pixels.append(lum)

    # print JSON
    print "{"
    print "  \"width\" : %s," % width
    print "  \"height\": %s," % height
    print "  \"pixels\": ["
    for y in range(height):
        end = ("" if (y == (height-1)) else ",")
        row = pixels[y*width:(y+1)*width]
        print ",".join( [ (str(x)+"  ")[0:3] for x in row ] ) + end
    print "]}"

def print_usage():
    print(sys.argv[0] + " [relative path to image file to convert to JSON]")

def main():
    if len(sys.argv) < 2:
        print_usage()
        return 1
    name = sys.argv[1]
    convert(name)

if __name__ == "__main__":
    main()

