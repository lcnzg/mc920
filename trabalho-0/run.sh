#!/bin/bash

images=()
for i in input/*.png
do
    images+=($(basename $i .png))
done

# Negative
for name in "${images[@]}"
do
    ./intensity.py 1 input/${name}.png output/${name}-negative.png
done

# Intensity reduction
for name in "${images[@]}"
do
    ./intensity.py 2 input/${name}.png output/${name}-reduced.png
done

# Brightness 1.5
for name in "${images[@]}"
do
    ./brightness.py 1.5 input/${name}.png output/${name}-brightness-1.5.png
done

# Brightness 2.5
for name in "${images[@]}"
do
    ./brightness.py 2.5 input/${name}.png output/${name}-brightness-2.5.png
done

# Brightness 3.5
for name in "${images[@]}"
do
    ./brightness.py 3.5 input/${name}.png output/${name}-brightness-3.5.png
done

# Bit plane
for bits in {0..7}
do
    ./bits.py ${bits} input/${images[0]}.png output/${images[0]}-plane-${bits}.png
done

# Mosaic
for name in "${images[@]}"
do
    ./mosaic.py "6,11,13,3,8,16,1,9,12,14,2,7,4,15,10,5" input/${name}.png output/${name}-mosaic.png
done

# Combine
for percentage in {2..8}
do
    ./combine.py 0.${percentage} input/${images[0]}.png input/${images[1]}.png output/${images[0]}-${images[1]}-0.${percentage}.png
done
