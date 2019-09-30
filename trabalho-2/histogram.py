#!/usr/bin/python3

from sys import argv
import cv2
import matplotlib.pyplot as plt

def _args():
    if len(argv) != 4:
        print("Usage: python3 histogram.py input output title")
        exit(1)

    return argv[1], argv[2], argv[3]

def main():
    input, output, title = _args()

    img = cv2.imread(input, 0)

    # num_bins = 5

    plt.hist(img.ravel(), bins=range(256), edgecolor='none', color="#3F5D7D")
    plt.xlim([-0.5, 255.5])
    plt.title(title.capitalize())

    plt.savefig(output, bbox_inches='tight')

if __name__ == '__main__':
    main()