#!/bin/env bash

echo "run make main && ./main"
make main
printf '%*s\n' "${COLUMNS:-$(tput cols)}" '' | tr ' ' -
./main
printf '%*s\n' "${COLUMNS:-$(tput cols)}" '' | tr ' ' -
echo "✨ Done"