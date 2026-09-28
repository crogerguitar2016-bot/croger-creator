[app]

title = Croger Creator

package.name = creator
package.domain = com.croger

source.dir = .

source.include_exts = py,png,jpg,jpeg,kv,atlas,txt,json

source.exclude_dirs = .git,.buildozer,bin,__pycache__

version = 1.0.0

requirements = python3,kivy

orientation = portrait

fullscreen = 0


# ==========================================================
# ANDROID
# ==========================================================

android.api = 36
android.minapi = 24

android.ndk = 29

android.archs = arm64-v8a

android.accept_sdk_license = True

p4a.branch = develop
p4a.source_dir = /home/runner/p4a


[buildozer]

log_level = 2

warn_on_root = 1
