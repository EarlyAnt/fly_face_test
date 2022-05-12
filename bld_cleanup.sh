#!/bin/bash

echo $PWD
if grep -q "bld_cmd" <<< "$PWD"; then
  cd ..
fi
echo $PWD

# find . -name "*.blend1" -exec rm -rf {} \;
# find . -name "*.pyc" -exec rm -rf {} \;
find . -name "__pycache__" -exec rm -rf {} \;

