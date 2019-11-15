#!/usr/bin/python3

from sys import argv
from os.path import getsize
import cv2
import numpy as np

def _args():
    if len(argv) != 4:
        print("Usage: python3 compression.py image k output")
        exit(1)

    k = int(argv[2])

    if k < 0:
        print("The number of components k must be a positive integer")
        exit(1)

    return argv[1], k, argv[3]

def compression(img, k):
    _, _, c = img.shape
    img = img.astype(np.float64)

    for i in range(c):
        u, s, vh = np.linalg.svd(img[:, :, i], full_matrices=False)

        u = u[:, :k]
        s = s[:k]
        vh = vh[:k, :]

        img[:, :, i] = (u * s) @ vh

    return img

def evaluation(img_in, file_in, img_out, file_out):

    p = getsize(file_out) / getsize(file_in)

    rmse = np.sqrt(np.mean((img_in - img_out)**2))

    return p, rmse

def main():
    input, k, output = _args()

    img = cv2.imread(input)

    img_out = compression(img, k)

    cv2.imwrite(output, img_out, [cv2.IMWRITE_PNG_COMPRESSION, 9])

    p, rmse = evaluation(img, input, img_out, output)

    print("Taxa de compressão: " + "%.2f" % p)
    print("RMSE: " + "%.2f" % rmse)

if __name__ == '__main__':
    main()
