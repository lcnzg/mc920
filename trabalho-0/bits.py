#!/usr/bin/python3

from sys import argv
import cv2

def _args():
    if len(argv) != 4:
        print("Usage: python3 bits.py bits input output")
        exit(1)

    bits = int(argv[1])

    if (bits < 0) or (bits > 7):
        print("The number of bits must be an integer between 0 and 7")
        exit(1)

    return bits, argv[2], argv[3]

def bit_plane(image, bits):

    image = ((image >> bits) & 1)*255

    return image

def main():
    bits, input, output = _args()
    img = cv2.imread(input, 0)
    
    img = bit_plane(img, bits)   

    cv2.imwrite(output, img)

if __name__ == '__main__':
    main()
