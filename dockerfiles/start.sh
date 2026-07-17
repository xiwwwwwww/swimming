#!/bin/bash
set -e

if [[ $@ ]]; then
    # Pre-clone and patch p4a so buildozer finds it already in place
    mkdir -p .buildozer/android/platform
    if [ ! -d ".buildozer/android/platform/python-for-android" ]; then
        git clone --depth 1 --branch develop https://github.com/kivy/python-for-android.git .buildozer/android/platform/python-for-android
        RECIPE=".buildozer/android/platform/python-for-android/pythonforandroid/recipes/libthorvg/__init__.py"
        if [ -f "$RECIPE" ]; then
            sed -i "s/clang_lib_dir = glob(pattern)\[0\]/clang_lib_dirs = glob(pattern); clang_lib_dir = clang_lib_dirs[0] if clang_lib_dirs else None/" "$RECIPE"
            echo "Patched libthorvg"
        fi
    fi
    eval $@
else
    /bin/bash
fi