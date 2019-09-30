#!/bin/bash

images=()
for i in input/*.pgm
do
    images+=($(basename $i .pgm))
done

modes=(global bernsen niblack sp pms contraste media mediana)

for name in "${images[@]}"; do
    ./histogram.py input/${name}.pgm output/${name}-histogram.png ${name}
    for mode in "${modes[@]}"; do
        echo "${name}-${mode}"
        time ./threshold.py $mode input/${name}.pgm output/${name}-${mode}.png
        ./proportion.py output/${name}-${mode}.png
        echo ""
    done
done