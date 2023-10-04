#!/bin/sh

sudo apt-get update
sudo apt-get install python3.6
sudo apt update
sudo apt install build-essential
sudo apt-get install manpages-dev

gcc --version
python3 --version

gcc -shared -fPIC -m64 -o clibrary.dll clibrary.c   # Windows OS
gcc -shared -fPIC -m64 -o clibrary.so clibrary.c    # Linux OS