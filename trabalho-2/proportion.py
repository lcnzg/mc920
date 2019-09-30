#!/usr/bin/python3

from sys import argv
import cv2
import matplotlib.pyplot as plt

def _args():
    if len(argv) != 2:
        print("Usage: python3 proportion.py input")
        exit(1)

    return argv[1]

def main():
    input = _args()

    img = cv2.imread(input, 0)

    black_count = 0
    white_count = 0

    h, w = img.shape

    for y in range(0, h):
        for x in range(0, w):
            if img[y][x] == 0:
                black_count += 1
            elif img[y][x] == 255:
                white_count += 1
            else:
                print("error")
    
    proportion_white = (white_count / (white_count+black_count))*100
    proportion_white = "%.2f" % proportion_white
    proportion_black = (black_count / (white_count+black_count))*100
    proportion_black = "%.2f" % proportion_black

    print("---")
    print(input)
    print("Black percentage: " + proportion_black + "%")
    print("White percentage: " + proportion_white + "%")
    print("---")


if __name__ == '__main__':
    main()