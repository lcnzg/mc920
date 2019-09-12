#!/usr/bin/python3

from sys import argv
import cv2
import numpy as np

def _args():
    if len(argv) != 6:
        print("Usage: python3 dithering.py mode direction color input output")
        exit(1)

    mode = argv[1]

    if mode < "a" or mode > "f":
        print('The mode must be a letter between "a" and "f"')
        exit(1)

    direction = argv[2]
    if (direction != "straight") and (direction != "zigzag"):
        print('The direction must be "straight" or "zigzag"')
        exit(1)

    direction = (direction == "straight")

    color = argv[3]
    if (color != "rgb") and (color != "mono"):
        print('The color must be "rgb" or "mono"')
        exit(1)

    color = (color == "rgb")

    return mode, direction, color, argv[4], argv[5]

def get_matrix(mode):
    # return: matrix, center

    switch = {
        # Floyd e Steinberg
        "a": (np.array([[0, 0, 7/16], [3/16, 5/16, 1/16]]), (0, 1)),

        # Stevenson e Arce
        "b": (np.array([[0, 0, 0, 0, 0, 32/200, 0],
                        [12/200, 0, 26/200, 0, 30/200, 0, 16/200],
                        [0, 12/200, 0, 26/200, 0, 12/200, 0],
                        [5/200, 0, 12/200, 0, 12/200, 0, 5/200]]), (0, 3)),

        # Burkes
        "c": (np.array([[0, 0, 0, 8/32, 4/32], [2/32, 4/32, 8/32, 4/32, 2/32]]), (0, 2)),

        # Sierra
        "d": (np.array([[0, 0, 0, 5/32, 3/32],
                        [2/32, 4/32, 5/32, 4/32, 2/32],
                        [0, 2/32, 3/32, 2/32, 0]]), (0, 2)),

        # Stucki
        "e": (np.array([[0, 0, 0, 8/42, 4/42],
                        [2/42, 4/42, 8/42, 4/42, 2/42],
                        [1/42, 2/42, 4/42, 2/42, 1/42]]), (0, 2)),

        # Jarvis, Judice e Ninke
        "f": (np.array([[0, 0, 0, 7/48, 5/48],
                        [3/48, 5/48, 7/48, 5/48, 3/48],
                        [1/48, 3/48, 5/48, 3/48, 1/48]]), (0, 2))
    }

    return switch.get(mode, None)

def dithering(image, mode, direction):

    matrix, center = get_matrix(mode)

    # Flip matrix to use in reversed direction
    matrix_flipped = np.fliplr(matrix)

    # 0 / 255 output
    result = np.empty_like(image)

    # Add padding
    top, left = center
    bottom, right = tuple(np.subtract(matrix.shape, center) - 1)
    border = ((top, bottom), (left, right))
    image = np.pad(image, border, 'constant').astype(np.float)

    h, w = result.shape

    for y in range(0, h):

        to_right = (y%2 == 0) or direction

        # To the right
        if to_right:
            for x in range(0, w):
                new_y, new_x = (y + top, x + left)
                result[y][x] = 255 if image[new_y][new_x] >= 128 else 0
                error = (image[new_y][new_x]) - (result[y][x])
                section = image[y:(new_y + bottom + 1), x:(new_x + right + 1)]
                section += (error * matrix)

        # To the left
        else:
            for x in range(w-1, -1, -1):
                new_y, new_x = (y + top, x + left)
                result[y][x] = 255 if image[new_y][new_x] >= 128 else 0
                error = (image[new_y][new_x]) - (result[y][x])
                section = image[y:(new_y + bottom + 1), x:(new_x + right + 1)]
                section += (error * matrix_flipped)

    return result

def main():
    mode, direction, color, input, output = _args()

    # RGB output
    if color:
        img = cv2.imread(input)

        (r, g, b) = cv2.split(img)
        r = dithering(r, mode, direction)
        g = dithering(g, mode, direction)
        b = dithering(b, mode, direction)

        img = cv2.merge((r, g, b))

    # Monochrome output
    else:
        img = cv2.imread(input, 0)
        img = dithering(img, mode, direction)

    cv2.imwrite(output, img)

if __name__ == '__main__':
    main()
