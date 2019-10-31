#!/usr/bin/python3

from sys import argv
import cv2

def _args():
    if len(argv) != 4:
        print("Usage: python3 decodificar.py image-input bit-plane text-output")
        exit(1)

    bit_plane = int(argv[2])

    if bit_plane not in range(0, 3):
        print("Bit plane value must be 0, 1 or 2")
        exit(1)

    return argv[1], bit_plane, argv[3]

def reveal(img, bit_plane):

    text = ''
    img = img.reshape(-1)

    mask = 1 << bit_plane

    text_bits = ''
    end = False

    for byte in img:
        bit = (byte & mask) >> bit_plane
        text_bits += str(bit)

        if len(text_bits) == 8:
            character = chr(int(text_bits, 2))

            # End Of Text character
            if character == '\x03':
                end = True
                break

            text += character
            text_bits = ''

    if end is False:
        print("Error: hidden text not found")
        exit(1)

    return text

def main():
    input, bit_plane, text_file = _args()

    # np.set_printoptions(threshold=np.inf)

    img = cv2.imread(input)

    text = reveal(img, bit_plane)

    f = open(text_file, "w")
    f.write(text)
    f.close()

if __name__ == '__main__':
    main()
