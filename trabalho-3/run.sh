#!/bin/bash

images=()
for i in input/*.png
do
    images+=($(basename $i .png))
done

for name in "${images[@]}"; do
    echo "${name}"
    time ./measurement.py input/${name}.png output/${name}-mono.png output/${name}-contour.png output/${name}-regions.png  output/${name}-histogram.png
    echo ""
done