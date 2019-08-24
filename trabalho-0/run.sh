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
