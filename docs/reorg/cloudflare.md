# 옛 주소 넘기기 — Cloudflare 규칙

호스팅은 네 사이트 모두 GitHub Pages 그대로 두고, 주소를 넘기는 일만 Cloudflare 가 맡는다.
GitHub Pages 는 301 을 못 걸고, repo 하나에 도메인 하나만 붙일 수 있어서 tech·ai 를
자기 자리에서 넘겨줄 방법이 없기 때문이다.

## 먼저 알아둘 것

**규칙은 주황 구름을 거치는 요청에만 걸린다.** 지금 `sungd.uk`·`tech`·`ai` 는 전부
회색 구름(DNS 만)이라 요청이 Cloudflare 를 그냥 지나쳐 GitHub 으로 간다. 규칙을 넣어도
안 걸린다. 넘김이 필요한 세 이름은 주황 구름으로 바꿔야 한다.

**인증서 순서가 있다.** GitHub 이 커스텀 도메인 인증서를 발급하려면 그 이름이 회색 구름
상태여야 한다. 그래서 순서가 이렇다 — 회색으로 두고 도메인 붙이기 → GitHub 에서 인증서
발급되고 "Enforce HTTPS" 켜지는 것 확인 → 그때 주황으로 바꾸기. 먼저 주황으로 바꾸면
발급이 막힌다.

**SSL 모드는 Full 이상.** Flexible 로 두면 GitHub 이 HTTPS 로 다시 보내고 Cloudflare 가
다시 받아서 무한히 돈다. Full 또는 Full (strict) 로 둔다.

## DNS

```
sungd.uk          A 185.199.108~111.153     주황 (인증서 발급 후)
writing.sungd.uk  CNAME newhigen.github.io  회색
ai.sungd.uk       CNAME newhigen.github.io  회색
resume.sungd.uk   CNAME newhigen.github.io  회색 (그대로)
tech.sungd.uk     CNAME newhigen.github.io  주황 — 넘김 전용
ai.sungd.uk       CNAME newhigen.github.io  주황 — 넘김 전용
```

tech·ai 는 주황이면 요청이 GitHub 까지 안 가고 Cloudflare 에서 넘어가므로, CNAME 이
어디를 가리키든 상관없다. 지금 값 그대로 두고 구름만 켜면 된다.

## 규칙 다섯 개

Rules → Redirect Rules 에서 만든다. **위에서부터 순서대로** 걸리므로 순서가 중요하다.
전부 301(Permanent), 쿼리스트링 보존 켬.

### 1. 옛 글 주소 → writing

sungd.uk 은 원래 글 블로그였고 글이 루트 바로 아래(`/the-go-giver-1/`)에 있었다.
새 루트 사이트가 쓰는 주소만 빼고 나머지는 다 옛 글로 보고 넘긴다. 글 79편을
하나씩 적는 대신 "루트 사이트 것이 아니면"으로 뒤집었다.

조건:

```
http.host eq "sungd.uk"
and not starts_with(http.request.uri.path, "/_astro/")
and not starts_with(http.request.uri.path, "/about")
and not starts_with(http.request.uri.path, "/dashboards/")
and not starts_with(http.request.uri.path, "/fonts/")
and not starts_with(http.request.uri.path, "/projects")
and not starts_with(http.request.uri.path, "/resume")
and not http.request.uri.path in {"/" "/favicon.ico" "/favicon.svg" "/robots.txt" "/sitemap-0.xml" "/sitemap-index.xml"}
```

넘길 곳 — Dynamic:

```
concat("https://writing.sungd.uk", http.request.uri.path)
```

⚠ 이 규칙 때문에 루트 사이트는 자기 404 를 못 갖는다. 모르는 주소는 writing 으로 가고
거기서 404 가 난다. 옛 주소가 전부 글이었으니 대개는 맞는 동작이다.

⚠ 루트 사이트에 새 최상위 경로(예: `/notes`)를 만들면 이 목록에 추가해야 한다.
안 그러면 그 경로가 writing 으로 넘어간다.

### 2. tech 프로젝트 → 루트

조건:

```
http.host eq "tech.sungd.uk" and starts_with(http.request.uri.path, "/projects")
```

넘길 곳 — Dynamic:

```
concat("https://sungd.uk", http.request.uri.path)
```

### 3. tech 기술 글 → writing

조건:

```
http.host eq "tech.sungd.uk" and http.request.uri.path in {
  "/2026-conferences" "/2026-conferences/"
  "/claude-code-tips" "/claude-code-tips/"
  "/claude-directory-structure" "/claude-directory-structure/"
  "/claude-skill-md" "/claude-skill-md/"
  "/claude-subagents" "/claude-subagents/"
  "/code-review" "/code-review/"
  "/git-checkout" "/git-checkout/"
  "/github-project" "/github-project/"
  "/ide" "/ide/"
  "/macos" "/macos/"
  "/mongodb-data-versioning" "/mongodb-data-versioning/"
  "/tablet-dev-with-ngrok" "/tablet-dev-with-ngrok/"
}
```

넘길 곳 — Dynamic:

```
concat("https://writing.sungd.uk", http.request.uri.path)
```

### 4. tech 나머지 → 루트 홈

2·3 에 안 걸린 것(홈, `/about`, `/posts`, `/tags/*`)을 받는다. **반드시 2·3 아래.**

조건:

```
http.host eq "tech.sungd.uk"
```

넘길 곳 — Static: `https://sungd.uk/`

### 5. ai → today

조건:

```
http.host eq "ai.sungd.uk"
```

넘길 곳 — Dynamic:

```
concat("https://ai.sungd.uk", http.request.uri.path)
```

## 확인

주황 구름으로 바꾼 뒤 몇 분 기다렸다가 본다. `-I` 로 헤더만 받아서 301 과 location 을 본다.

```sh
curl -sSI https://sungd.uk/the-go-giver-1/      | grep -iE "^(HTTP|location|cf-ray)"
curl -sSI https://tech.sungd.uk/claude-code-tips | grep -iE "^(HTTP|location)"
curl -sSI https://tech.sungd.uk/projects/claude-watch | grep -iE "^(HTTP|location)"
curl -sSI https://ai.sungd.uk/                   | grep -iE "^(HTTP|location)"
curl -sSI https://sungd.uk/projects              | grep -iE "^(HTTP|location)"   # 넘어가면 안 됨
```

`cf-ray` 헤더가 보이면 주황 구름이 켜진 것이다. 안 보이면 아직 회색이라 규칙이 안 걸린다.
