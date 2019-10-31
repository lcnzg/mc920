#!/bin/bash

images=()
for i in input/*.png
do
    images+=($(basename $i .png))
done

texts=()
for i in input/*.txt
do
    texts+=($(basename $i .txt))
done

bits=(0 1 2)

for image in "${images[@]}"; do
    for text in "${texts[@]}"; do
        for bit in "${bits[@]}"; do
            echo "${image}-${text}-${bit}"
            time ./codificar.py input/${image}.png input/${text}.txt ${bit} output/${image}-${text}-${bit}.png
            time ./decodificar.py output/${image}-${text}-${bit}.png ${bit} output/${image}-${text}-${bit}.txt
            if cmp -s input/${text}.txt output/${image}-${text}-${bit}.txt; then
                echo "Test OK: The input and output texts matches"
                ./bits.py 0 output/${image}-${text}-${bit}.png output/${image}-${text}-${bit}-plane0.png
                ./bits.py 1 output/${image}-${text}-${bit}.png output/${image}-${text}-${bit}-plane1.png
                ./bits.py 2 output/${image}-${text}-${bit}.png output/${image}-${text}-${bit}-plane2.png
                ./bits.py 7 output/${image}-${text}-${bit}.png output/${image}-${text}-${bit}-plane7.png
            else
                echo "Test FAILED: The input and output texts are different"
            fi
            echo ""
        done
    done
done