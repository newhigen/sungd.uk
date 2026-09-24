#!/bin/zsh
# 홈에 쓰는 한글 글꼴(마루부리, SUIT)을 KS X 1001 한글 2,350자 + ASCII로 잘라 public/fonts 에 둔다.
# 둘 다 OFL 이라 잘라서 올려도 된다. 필요: pip install fonttools brotli
set -e
cd "$(dirname "$0")/.."
tmp=$(mktemp -d)
python3 - > "$tmp/chars.txt" <<'EOF'
import sys
s = ''.join(chr(c) for c in range(0xAC00, 0xD7A4) if len(chr(c).encode('euc-kr', 'ignore')) == 2)
s += ''.join(chr(c) for c in range(0x20, 0x7F)) + '·“”‘’…–—→←↑↓※○●■□'
sys.stdout.write(s)
EOF
curl -sL -o "$tmp/MaruBuri-Regular.ttf" https://hangeul.pstatic.net/hangeul_static/webfont/MaruBuri/MaruBuri-Regular.ttf
curl -sL -o "$tmp/MaruBuri-SemiBold.ttf" https://hangeul.pstatic.net/hangeul_static/webfont/MaruBuri/MaruBuri-SemiBold.ttf
curl -sL -o "$tmp/SUIT-Bold.woff2" https://cdn.jsdelivr.net/gh/sun-typeface/SUIT@2/fonts/static/woff2/SUIT-Bold.woff2
curl -sL -o "$tmp/SUIT-ExtraBold.woff2" https://cdn.jsdelivr.net/gh/sun-typeface/SUIT@2/fonts/static/woff2/SUIT-ExtraBold.woff2
mkdir -p public/fonts
for f in MaruBuri-Regular.ttf MaruBuri-SemiBold.ttf SUIT-Bold.woff2 SUIT-ExtraBold.woff2; do
  pyftsubset "$tmp/$f" --text-file="$tmp/chars.txt" --flavor=woff2 --layout-features='*' \
    --output-file="public/fonts/${f%.*}.subset.woff2"
done
rm -rf "$tmp"
ls -l public/fonts
