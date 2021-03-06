#!/bin/sh
cd `dirname $0`
export GOPATH=$(pwd)/go
echo $GOPATH
sudo apt-get update
sudo apt-get install -y python-pygame libudev-dev
wget https://storage.googleapis.com/golang/go1.8.linux-armv6l.tar.gz
sudo tar -C /usr/local/ -xzf go1.8.linux-armv6l.tar.gz
mkdir -p go/src/github.com/riking
mv diff.patch go/src/github.com/riking
cd go/src/github.com/riking/
git clone https://github.com/riking/joycon.git
cd joycon/
patch -p1 < ../diff.patch
cd prog4
/usr/local/go/bin/go get ./...
