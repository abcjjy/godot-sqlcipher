#!/usr/bin/env python

import os
import platform
import sys
import argparse


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('-V', '--sqlcipher-version', default='v4.5.5')
    ap.add_argument('-s', '--openssl', default='openssl/build/android-arm64')
    ap.add_argument('-L', '--skip-build-library', action='store_true')
    ap.add_argument('-p', '--platform', default='android', choices=['ios', 'android', 'macos'])
    ap.add_argument('-a', '--arch', nargs='+', default=['arm64', 'x86_64'])
    ap.add_argument('-t', '--target', nargs='+', default=['template_debug', 'template_release'])
    ap.add_argument('-m', '--ios-simulator', action='store_true')


    args = ap.parse_args()
    
    get_sqlcipher_source(args)

    run('''
cp sqlcipher/sqlite3.c src/sqlite
cp sqlcipher/sqlite3.h src/sqlite
cp sqlcipher/sqlite3ext.h src/sqlite
''')

    opts = []
    opts.append(f'build_library={"no" if args.skip_build_library else "yes"}')
    opts.append(f'ios_simulator={"yes" if args.ios_simulator else "no"}')
        
    if args.platform == 'ios':
        args.arch = filter(lambda x: x.startswith('arm'), args.arch)

    for arch in args.arch:
        for target in args.target:
            run(f'scons platform={args.platform} arch={arch} target={target} ' + ' '.join(opts))
        
    if args.platform == 'ios':
        dst = "demo/addons/godot-sqlite/bin"
        for target in args.target:
            run(f'rm -rf {dst}/libgdsqlite.ios.{target}.xcframework')
            run(f'rm -rf {dst}/libgodot-cpp.ios.{target}.xcframework')
            run(f'xcodebuild -create-xcframework -library {dst}/libgdsqlite.ios.{target}.a -output {dst}/libgdsqlite.ios.{target}.xcframework')
            run(f'xcodebuild -create-xcframework -library godot-cpp/bin/libgodot-cpp.ios.{target}.arm64.a -output {dst}/libgodot-cpp.ios.{target}.xcframework')


def run(cmd):
    print(cmd)
    r = os.system(cmd)
    if r != 0:
        exit(r)


def get_sqlcipher_source(args):
    if not os.path.exists('sqlcipher'):
        run(f'git clone -b {args.sqlcipher_version} --depth 1 https://github.com/sqlcipher/sqlcipher.git')
 
    openssl = os.path.abspath(args.openssl)

    os.chdir('sqlcipher')
    
    # The amalgamated source is same
    if args.platform == 'ios' or True:
        run(f'./configure --with-pic --disable-tcl --enable-tempstore --enable-threadsafe --with-crypto-lib=commoncrypto CFLAGS="-DSQLITE_HAS_CODEC -DSQLITE_THREADSAFE=1 -DSQLITE_TEMP_STORE=2"')
    elif args.platform == 'android':
        ndk = os.environ['ANDROID_NDK_ROOT']
        sys_name = platform.system().lower()
        host_arch = platform.machine()
        host_tag = f'{sys_name}-{host_arch}'

        toolchain = os.path.join(ndk, 'toolchains/llvm/prebuilt', host_tag, 'bin')

        cprefix = os.path.join(toolchain, 'aarch64-linux-android21-')
        os.environ['CC'] = cprefix + 'clang'
        os.environ['LD'] = os.path.join(toolchain, 'ld')
        os.environ['AS'] = os.environ['CC']
        run(f'./configure --with-pic --disable-tcl --enable-tempstore --enable-threadsafe --with-crypto-lib=openssl \
            CFLAGS="-DSQLITE_HAS_CODEC -DSQLITE_THREADSAFE=1 -DSQLITE_TEMP_STORE=2 -I{openssl}/include" \
            LDFLAGS="-L{openssl}/lib -lcrypto" --host="{host_arch}-{sys_name}"')
    run('make sqlite3.c')
    os.chdir('..')


main()
