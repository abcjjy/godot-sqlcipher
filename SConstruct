#!/usr/bin/env python
import os
import sys

target_path = ARGUMENTS.pop("target_path", "demo/addons/godot-sqlite/bin/")
target_name = ARGUMENTS.pop("target_name", "libgdsqlite")

env = SConscript("godot-cpp/SConstruct")

target = "{}{}".format(
    target_path, target_name
)

# For the reference:
# - CCFLAGS are compilation flags shared between C and C++
# - CFLAGS are for C-specific compilation flags
# - CXXFLAGS are for C++-specific compilation flags
# - CPPFLAGS are for pre-processor flags
# - CPPDEFINES are for pre-processor defines
# - LINKFLAGS are for linking flags

# tweak this if you want to use different folders, or more folders, to store your source code in.
env.Append(CPPPATH=["src/"])
env.Append(CFLAGS=['-DSQLITE_HAS_CODEC', '-DSQLITE_THREADSAFE=1', '-DSQLITE_TEMP_STORE=2', 
                   '-DSQLITE_OS_UNIX=1'
                   ])
sources = [Glob('src/*.cpp'), Glob('src/vfs/*.cpp'), 'src/sqlite/sqlite3.c']

if env['platform'] == 'ios':
    env.Append(CCFLAGS=["-miphoneos-version-min=" + env["ios_min_version"]])
    env.Append(LINKFLAGS=["-miphoneos-version-min=" + env["ios_min_version"]])

if env['platform'] in ['macos', 'ios']:
    env.Append(CFLAGS=['-DSQLCIPHER_CRYPTO_CC'])
    env.Append(LINKFLAGS=['-framework', 'Security', '-framework', 'Foundation'])

if env["platform"] == "android":
    arch_map = {
        'arm32': 'android-arm',
        'arm64': 'android-arm64',
        'x86_32': 'android-x86',
        'x86_64': 'android-x86_64',
    }
    openssl = os.path.join('openssl', arch_map[env['arch']])
    env.Append(CCFLAGS=[f'-I{openssl}/include', '-DSQLCIPHER_CRYPTO_OPENSSL'])
    env.Append(LINKFLAGS=[f'-L{openssl}/lib', # openssl lib path
                            '-lcrypto', # link openssl
                            '-llog', # why it needs to link log?
                            ])

if env["platform"] == "macos":
    target = "{}.{}.{}.framework/{}.{}.{}".format(
        target,
        env["platform"], 
        env["target"],
        target_name,
        env["platform"],
        env["target"]
    )
    library = env.SharedLibrary(target=target, source=sources)
elif env["platform"] == "ios":
    if env["ios_simulator"]:
        library = env.StaticLibrary(
            f"{target}.{env['platform']}.{env['target']}.simulator.a",
            source=sources,
        )
    else:
        library = env.StaticLibrary(
            f"{target}.{env['platform']}.{env['target']}.a",
            source=sources,
        )
else:
    target = "{}{}{}".format(
        target,
        env["suffix"],
        env["SHLIBSUFFIX"]
    )
    library = env.SharedLibrary(target=target, source=sources)

Default(library)
