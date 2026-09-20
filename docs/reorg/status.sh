#!/bin/bash
# 재편이 어디까지 왔는지 한 번에 본다. 각 단계 끝나고 돌려보면 된다.
#   bash docs/reorg/status.sh

HOSTS="sungd.uk writing.sungd.uk resume.sungd.uk ai.sungd.uk tech.sungd.uk"

echo "=== GitHub Pages 가 어느 도메인을 잡고 있나"
for r in blog-tech blog-writing resume ai-pick; do
  printf "  %-14s " "$r"
  gh api "repos/newhigen/$r/pages" --jq '.cname // "없음"' 2>/dev/null || echo "Pages 안 씀"
done

echo
echo "=== DNS"
for h in $HOSTS; do
  printf "  %-20s " "$h"
  c=$(dig +short "$h" CNAME | head -1)
  a=$(dig +short "$h" A | head -1)
  if [ -z "$c" ] && [ -z "$a" ]; then echo "없음"; else echo "CNAME=${c:-·}  A=${a:-·}"; fi
done

echo
echo "=== 응답 (cf-ray 있으면 주황 구름)"
for h in $HOSTS; do
  printf "  %-20s " "$h"
  out=$(curl -sSI --max-time 8 "https://$h/" 2>/dev/null)
  if [ -z "$out" ]; then echo "응답 없음"; continue; fi
  code=$(printf '%s' "$out" | head -1 | awk '{print $2}')
  loc=$(printf '%s' "$out" | grep -i '^location:' | head -1 | sed 's/[Ll]ocation: *//' | tr -d '\r')
  cf=$(printf '%s' "$out" | grep -ci '^cf-ray:')
  cloud=$([ "$cf" -gt 0 ] && echo "주황" || echo "회색")
  echo "$code  $cloud  ${loc:+→ $loc}"
done

echo
echo "=== 넘김 확인 (4단계 뒤에 다 301 이어야 함)"
check() {
  printf "  %-46s " "$1"
  out=$(curl -sSI --max-time 8 "$1" 2>/dev/null)
  code=$(printf '%s' "$out" | head -1 | awk '{print $2}')
  loc=$(printf '%s' "$out" | grep -i '^location:' | head -1 | sed 's/[Ll]ocation: *//' | tr -d '\r')
  echo "${code:-?}  ${loc:-·}"
}
check "https://sungd.uk/the-go-giver-1/"
check "https://tech.sungd.uk/claude-code-tips"
check "https://tech.sungd.uk/projects/claude-watch"
check "https://ai.sungd.uk/"
echo "  ── 아래는 넘어가면 안 된다 (200 이어야 함)"
check "https://sungd.uk/projects"
check "https://sungd.uk/about"
