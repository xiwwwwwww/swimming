[app]
title = Swim Pool Manager
package.name = swimpool
package.domain = org.local
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,ttf
source.include_patterns = assets/*,data/*
version = 1.0.0
requirements = python3,kivy,pillow,qrcode,pyzbar,plyer
orientation = portrait
fullscreen = 0
android.permissions = CAMERA,READ_EXTERNAL_STORAGE,WRITE_EXTERNAL_STORAGE
android.api = 33
android.minapi = 24
android.ndk = 25b
android.sdk = 34
android.gradle_dependencies = 
android.add_src =
android.archs = arm64-v8a
ios.kivy_ios_dir = 
ios.kivy_ios_url = 
ios.requirements =

[buildozer]
log_level = 2
warn_on_root = 1
android.accept_sdk_license = True
