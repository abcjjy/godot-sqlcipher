#!/usr/bin/env bash

set -e

VERSION=v4.5.5

git clone -b ${VERSION} --depth 1 https://github.com/sqlcipher/sqlcipher.git
cd sqlcipher

./configure --with-pic --disable-tcl --enable-tempstore --enable-threadsafe --with-crypto-lib=commoncrypto CFLAGS="-DSQLITE_HAS_CODEC -DSQLITE_THREADSAFE=1 -DSQLITE_TEMP_STORE=2"

make sqlite3.c

cd ..

cp sqlcipher/sqlite3.c src/sqlite
cp sqlcipher/sqlite3.h src/sqlite
cp sqlcipher/sqlite3ext.h src/sqlite

