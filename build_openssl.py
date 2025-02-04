#!/usr/bin/env python

import os
import argparse
import platform

cd = os.chdir

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('-V', '--version', default='openssl-3.4.0')
    ap.add_argument('-a', '--api-version', default=21, type=int)
    ap.add_argument('-i', '--install-dir', default='build')

    args = ap.parse_args()

    if not os.path.exists('openssl'):
        run(f'git clone -b {args.version} --depth 1 https://github.com/openssl/openssl.git')
    cd('openssl')

    ndk = os.environ['ANDROID_NDK_ROOT']
    sys_name = platform.system().lower()
    host_arch = platform.machine()
    host_tag = f'{sys_name}-{host_arch}'

    toolchain = os.path.join(ndk, 'toolchains/llvm/prebuilt', host_tag, 'bin')
    os.environ['PATH'] = ':'.join([toolchain, os.environ['PATH']])
    
    for tarch in ['android-arm64', 'android-arm', 'android-x86_64', 'android-x86']:
        outdir = os.path.abspath(os.path.join(args.install_dir, tarch))
        os.makedirs(outdir, exist_ok=True)
        run('make clean')
        run(f'./Configure {tarch} no-unit-test -D__ANDROID_API__={args.api_version} --prefix={outdir}')
        run('make && make install_sw')
    

def run(cmd):
    print(cmd)
    if os.system(cmd) != 0:
        raise Exception('Command failed')
    


main()
