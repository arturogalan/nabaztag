#!/bin/bash

# SWIG is a tool to compile c++ code into Python.

echo "Installing SWIG"

if [ ! -e swig-3.0.7.tar.gz ]; then
  wget -T 10 -t 3 \
    http://prdownloads.sourceforge.net/swig/swig-3.0.7.tar.gz || exit 1;
fi

tar -xovzf swig-3.0.7.tar.gz || exit 1
ln -s swig-3.0.7 swig

cd swig

# We first have to install PCRE.
if [ ! -e pcre-8.37.tar.gz ]; then
  wget -T 10 -t 3 \
    ftp:// ftp.pcre.org/pub/pcre/pcre-8.37.tar.gz|| exit 1;
fi
Tools/pcre-build.sh

./configure --prefix=`pwd` --with-pic
make
make install

cd ..