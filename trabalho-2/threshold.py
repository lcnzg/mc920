#!/usr/bin/python3

from sys import argv
import cv2
import numpy as np

def _args():
    if len(argv) != 4:
        print("Usage: python3 threshold.py mode input output")
        exit(1)

    mode = argv[1]

    modes = ["global", "bernsen", "niblack", "sp", "pms", "contraste", "media", "mediana"]

    if mode not in modes:
        print('The mode must be one of the following:')
        print(*modes, sep=", ")
        exit(1)

    return mode, argv[2], argv[3]

def get_threshold_value(mode, image, pos):
    # return: threshold_value

    x, y = pos

    n = 5

    min_y = max(0, int(y-(n/2)))
    max_y = min(int(min_y+n), image.shape[0])
    min_y = max(0, int(max_y-n))
    min_x = max(0, int(x-(n/2)))
    max_x = min(int(min_x+n), image.shape[1])
    min_x = max(0, int(max_x-n))

    section = image[min_y:max_y, min_x:max_x]

    if mode == "bernsen":
        return (np.min(section).astype(float) + np.max(section).astype(float))/2

    if mode == "niblack":
        k_niblack = 1.5
        return np.mean(section) + k_niblack*np.std(section)

    if mode == "sp":
        k_sp = 0.5
        r_sp = 128
        return np.mean(section) * (1 + k_sp*(np.std(section)/r_sp - 1))

    if mode == "pms":
        k_pms = 0.25
        r_pms = 0.5
        p_pms = 2
        q_pms = 10
        return np.mean(section) * (1 + p_pms*np.exp(-1*q_pms*np.mean(section)) + \
               k_pms*(np.std(section)/r_pms - 1))

    if mode == "contraste":
        return 0 if np.max(section)-image[y][x] < image[y][x]-np.min(section) else 255

    if mode == "media":
        return np.mean(section)

    if mode == "mediana":
        return np.median(section)

    return None

def threshold(image, mode):

    h, w = image.shape

    result = np.empty_like(image)

    if mode == "global":
        threshold_value = 128
        for y in range(0, h):
            for x in range(0, w):
                result[y][x] = 255 if image[y][x] > threshold_value else 0

    else:
        for y in range(0, h):
            for x in range(0, w):
                threshold_value = get_threshold_value(mode, image, (x, y))
                result[y][x] = 255 if image[y][x] > threshold_value else 0

    return result

def main():
    mode, input, output = _args()

    img = cv2.imread(input, 0)
    img = threshold(img, mode)

    cv2.imwrite(output, img)

if __name__ == '__main__':
    main()
