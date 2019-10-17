#!/usr/bin/python3

from sys import argv
import cv2
import numpy as np
import matplotlib.pyplot as plt

def _args():
    if len(argv) != 6:
        print("Usage: python3 mesurement.py input output-mono output-contour output-regions output-histogram")
        exit(1)

    return argv[1], argv[2], argv[3], argv[4], argv[5]

def eccentricity(M):

    # Derivated central moments for covariance matrix
    dv_mu20 = M['mu20'] / M['m00']
    dv_mu02 = M['mu02'] / M['m00']
    dv_mu11 = M['mu11'] / M['m00']

    # Eigenvalues
    a = dv_mu20 + dv_mu02

    b = np.sqrt(4*(dv_mu11**2) + (dv_mu20 - dv_mu02)**2)

    # Eccentricity
    return np.sqrt(1 - ((a - b) / (a + b)))

def solidity(cnt):
    area = cv2.contourArea(cnt)
    hull = cv2.convexHull(cnt)
    hull_area = cv2.contourArea(hull)
    return float(area) / float(hull_area)

def main():
    input, output_mono, output_contour, output_regions, output_histogram = _args()

    img = cv2.imread(input, 0)

    # Mono output
    thresh = 250
    img_mono = cv2.threshold(img, thresh, 255, cv2.THRESH_BINARY)[1]
    cv2.imwrite(output_mono, img_mono)

    # Contour output
    img_contour = np.ones(img_mono.shape, np.uint8)*255
    contours, _ = cv2.findContours(img_mono, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    cv2.drawContours(img_contour, contours, -1, 0)
    cv2.imwrite(output_contour, img_contour)

    # Regions output
    hist_small = hist_medium = hist_large = 0
    area_list = []

    img_regions = cv2.imread(input)

    n_contours = len(contours)-1
    
    print("número de regiões: " + str(n_contours))
    print("")
    for region, c in enumerate(reversed(contours[1:])):

        M = cv2.moments(c)

        area = M['m00']
        area_list.append(area)
        perimeter = cv2.arcLength(c,True)
        eccen = eccentricity(M)
        solid = solidity(c)

        print("região %d:  área: %d  perímetro: %.6f  excentricidade: %.6f  solidez: %.6f"
            %(region, area, perimeter, eccen, solid))

        cX = int(M["m10"] / M["m00"])
        cY = int(M["m01"] / M["m00"])

        cv2.putText(img_regions, str(region), (cX-6, cY+6), cv2.FONT_HERSHEY_SIMPLEX,
                    0.5, (0, 0, 0), lineType=cv2.LINE_AA, thickness=2)

        cv2.putText(img_regions, str(region), (cX-6, cY+6), cv2.FONT_HERSHEY_SIMPLEX,
                    0.5, (255, 255, 255), lineType=cv2.LINE_AA, thickness=1)

        # Histogram area count
        if (area<1500):
            hist_small += 1
        elif(area<3000):
            hist_medium += 1
        else:
            hist_large += 1

    cv2.imwrite(output_regions, img_regions)

    # Histogram
    print("")
    print("número de regiõoes pequenas: " + str(hist_small))
    print("número de regiõoes médias: " + str(hist_medium))
    print("número de regiõoes grandes: " + str(hist_large))

    plt.hist(area_list, bins=[0, 1500, 3000, 4500], edgecolor='black', color="#3F5D7D")
    plt.xlim([0, 4500])
    plt.ylabel('Número de Objetos')
    plt.xlabel('Área')

    plt.savefig(output_histogram, bbox_inches='tight')

if __name__ == '__main__':
    main()
