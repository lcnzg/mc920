#!/usr/bin/python3

from sys import argv
import cv2
import numpy as np

def _args():
    if len(argv) != 5:
        print("Usage: python3 combine.py percentage input_a input_b output")
        exit(1)

    percentage = float(argv[1])

    if percentage < 0 or percentage > 1:
        print("The percentage value must be a number between 0 and 1, like 0.3")
        exit(1)

    return percentage, argv[2], argv[3], argv[4]

def combine(percentage, img_a, img_b):

    img_a = percentage*img_a + (1-percentage)*img_b
    img_a = img_a.astype(int)

    return img_a


def main():
    percentage, input_a, input_b, output = _args()
    img_a = cv2.imread(input_a, 0)
    img_b = cv2.imread(input_b, 0)

    img_a = combine(percentage, img_a, img_b)

    cv2.imwrite(output, img_a)

if __name__ == '__main__':
    main()
