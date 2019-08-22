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


