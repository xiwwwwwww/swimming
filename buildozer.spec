[app]

title = Swim Pool Manager
package.name = swimpool
package.domain = org.local

source.dir = .
source.include_exts = py,png,jpg,kv,atlas

version = 1.0.0

requirements = python3,kivy,pillow,qrcode,pyzbar,plyer

orientation = portrait
fullscreen = 0

android.permissions = CAMERA
android.api = 34
android.minapi = 24
android.ndk = 25b
android.arch = arm64-v8a
p4a.branch = release-2026.05.09
android.accept_sdk_license = True

[buildozer]

log_level = 2
warn_on_root = 1