#!/bin/bash

# Script for installing Ta-Lib dependencies and the Python module itself

# Tarball found in linux section https://mrjbq7.github.io/ta-lib/install.html
tar -xvf libs/ta-lib-0.4.0-src.tar.gz
cd ta-lib
make
sudo make install
cd ..
rm -r ta-lib
pip install Ta-Lib