#!/bin/sh
set -x

mkdir -p bin

dst="demo/addons/godot-sqlite/bin"
rm -rf $dst/libgdsqlite.ios.$1.xcframework
rm -rf $dst/libgodot-cpp.ios.$1.xcframework

#scons arch=universal ios_simulator=yes platform=ios target=$1 $2
if [ $1 == "template_debug" ]
    then
        scons arch=arm64 ios_simulator=no platform=ios debug_symbols=yes target=$1 $2
    else
        scons arch=arm64 ios_simulator=no platform=ios target=$1 $2
fi

xcodebuild -create-xcframework -library $dst/libgdsqlite.ios.$1.a -output $dst/libgdsqlite.ios.$1.xcframework
xcodebuild -create-xcframework -library godot-cpp/bin/libgodot-cpp.ios.$1.arm64.a -output $dst/libgodot-cpp.ios.$1.xcframework
