#!/usr/bin/python3

from sys import argv
import cv2

def _args():
    if len(argv) != 4:
        print("Usage: python3 brightness.py gamma input output")
        exit(1)

    return float(argv[1]), argv[2], argv[3]

def brightness_adjust(image, gamma):

    # Reducing interval to [0,1]
    image = image / 2.55

    # Exponencial transformation
    image = image ** (1/gamma)

    # Expanding interval to 256 range
    range = image.max() - image.min()
    image = image * (255/range)

    # Moving interval to [0, 255]
    min = image.min()
    image = image - min
    image = image.astype(int)

    return image

def main():
    gamma, input, output = _args()
    img = cv2.imread(input, 0)
    
    img = brightness_adjust(img, gamma)   

    cv2.imwrite(output, img)

if __name__ == '__main__':
    main()
