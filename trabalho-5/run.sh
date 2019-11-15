#!/bin/bash

images=()
for i in input/*.png
do
    images+=($(basename $i .png))
done

ks=(1 5 10 20 30 40 50)

for image in "${images[@]}"; do
    for k in "${ks[@]}"; do
        echo "------------"
        echo "${image}-${k}"
        time ./compression.py input/${image}.png ${k} output/${image}-${k}.png
        echo "------------"
    done
done