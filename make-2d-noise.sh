#!/bin/zsh

# Create a 2D noise image

# loop from 1 to 20
for i in $(seq 0 1 20)
do
  echo "noise $i"
  just noise=$i r=3 generate-2d-noise
done
