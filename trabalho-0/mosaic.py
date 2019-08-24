#!/usr/bin/python3

from sys import argv
import cv2
import numpy as np

def _args():
    if len(argv) != 4:
        print("Usage: python3 mosaic.py order input output")
        exit(1)

    order = np.array([int(number) for number in argv[1].split(',')])

    if len(order) != 16:
        print('The order must be a array with the format "1,2,...,16"')
        exit(1)
    for number in order:
        if number not in range(1,17):
            print("The numbers must be between 1 and 16")
            exit(1)

    return order, argv[2], argv[3]

def mosaic(image, order, qt):

    height, width = image.shape
    block_h = int(height / qt)
    block_w = int(width / qt)

    final = np.empty_like(image)

    for orig, new in enumerate(order):

        orig_row, orig_col = int(orig/qt), int(orig%qt)
        new_row, new_col = int(new/qt), int(new%qt)

        orig_x_start, orig_x_end = orig_col*block_w, (orig_col+1)*block_w
        orig_y_start, orig_y_end = orig_row*block_h, (orig_row+1)*block_h

        new_x_start, new_x_end = new_col*block_w, (new_col+1)*block_w
        new_y_start, new_y_end = new_row*block_h, (new_row+1)*block_h

        final[orig_y_start:orig_y_end, orig_x_start:orig_x_end] = image[new_y_start:new_y_end, new_x_start:new_x_end]

    return final


def main():
    order, input, output = _args()
    img = cv2.imread(input, 0)

    order = order - 1

    img = mosaic(img, order, 4)

    cv2.imwrite(output, img)

if __name__ == '__main__':
    main()
