#!/usr/bin/python3

from sys import argv
import cv2

def _args():
    if len(argv) != 5:
        print("Usage: python3 codificar.py image-input text-input bit-plane image-output")
        exit(1)

    bit_plane = int(argv[3])

    if bit_plane not in range(0, 3):
        print("Bit plane value must be 0, 1 or 2")
        exit(1)

    return argv[1], argv[2], bit_plane, argv[4]

def steganography(img, text, bit_plane):

    h, w, c = img.shape

    # End Of Text character at the end
    text += '\x03'

    img = img.reshape(-1)

    text_bits = ''.join(format(ord(i), 'b').zfill(8) for i in text)

    mask = 1 << bit_plane
    mask_inv = ~mask

    text_bitsize = len(text_bits)

    if text_bitsize > len(img):
        print("Error: this text is too large for this image")
        exit(1)

    for i in range(text_bitsize):
        img[i] = (img[i] & mask_inv) | (int(text_bits[i], 2) << bit_plane)

    img = img.reshape(h, w, c)

    return img

def main():
    input, text_file, bit_plane, output = _args()

    # np.set_printoptions(threshold=np.inf)

    img = cv2.imread(input)

    f = open(text_file, "r")
    text = f.read()
    f.close()

    img = steganography(img, text, bit_plane)

    cv2.imwrite(output, img)

if __name__ == '__main__':
    main()
