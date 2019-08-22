#!/usr/bin/python3

from sys import argv
import cv2

def _args():
    if len(argv) != 4:
        print("Usage: python3 intensity.py type input output")
        exit(1)
    
    type = int(argv[1])

    if (type != 1) and (type != 2):
        print("Type must be 1 to tranform to negative or 2 to reduce the interval")
        exit(1)

    return type, argv[2], argv[3]

def negative(image):

    image = 255 - image

    return image


def reduce(image):

    # Reducing intensity interval to [100, 200]
    image = image / 2.56 + 100
    image = image.astype(int)

    return image


def main():
    type, input, output = _args()
    img = cv2.imread(input, 0)
    
    if type == 1:
        img = negative(img)
    elif type == 2:
        img = reduce(img)

    cv2.imwrite(output, img)

if __name__ == '__main__':
    main()
