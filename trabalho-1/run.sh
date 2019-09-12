#!/bin/bash

images=()
for i in input/*.png
do
    images+=($(basename $i .png))
done

modes=(a b c d e f)
directions=(straight zigzag)
colors=(rgb mono)

for name in "${images[@]}"; do
    for mode in "${modes[@]}"; do
        for direction in "${directions[@]}"; do
            for color in "${colors[@]}"; do
                echo "${name}-${mode}-${direction}-${color}"
                time ./dithering.py $mode $direction $color input/${name}.png output/${name}-${mode}-${direction}-${color}.png
                echo "-----"
                echo ""
            done
        done
    done
done