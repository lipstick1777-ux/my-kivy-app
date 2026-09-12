[app]

title = My Application
package.name = myapp
package.domain = org.test
source.dir = .
version = 0.1
source.include_exts = py,png,jpg,kv,atlas

# تحديد النسخ المستقرة كلياً لمنع تعارض البناء
requirements = python3,kivy==2.3.0,kivymd,arabic-reshaper,python-bidi,pillow

orientation = portrait
fullscreen = 0

# تحديد إصدارات أندرويد المستقرة والمتوافقة مع python-for-android
android.api = 33
android.minapi = 21
android.ndk = 25b
android.ndk_api = 21
android.archs = arm64-v8a

[buildozer]

log_level = 2
warn_on_root = 1
