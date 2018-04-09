#!/bin/sh

wget --recursive \
  --html-extension \
  --convert-links \
  --domains frida.re \
  --restrict-file-names=windows \
  --page-requisites \
  --reject pdf \
  --no-parent www.frida.re/docs/

rm www.frida.re/docs/index.html


contents=frida.docset/Contents
res=$contents/Resources
mkdir -p $res
cp frida.png frida.docset/icon.png
mv www.frida.re $res/Documents

rm $res/docSet.dsidx

cat > $contents/Info.plist <<- "EOF"
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
  <key>CFBundleIdentifier</key>
  <string>frida</string>
  <key>CFBundleName</key>
  <string>Frida</string>
  <key>DocSetPlatformFamily</key>
  <string>frida</string>
  <key>dashIndexFilePath</key>
  <string>docs/home/index.html</string>
  <key>isDashDocset</key>
  <true/>
</dict>
</plist>
EOF

python index.py

echo 'done'

open frida.docset