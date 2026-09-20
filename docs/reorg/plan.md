# sungd.uk 사이트 재편

> **2026-08-07 시점의 계획이다. 지금 상태와 다르다.**
>
> 세운 뒤에 전제가 세 번 바뀌었다 — 호스팅이 Netlify 가 아니라 GitHub Pages 였고,
> `today.sungd.uk` 는 `ai.sungd.uk` 로 되돌렸고, 넘김(리다이렉트)은 안 걸기로 했다.
> 결정 과정 기록으로 두는 문서라 그때 그대로 둔다. **고쳐 쓰지 말 것.**
>
> 지금 상태는 각 repo 의 README, 무슨 일이 있었는지는 [`log.md`](log.md),
> 실제로 쓰는 것은 [`cloudflare.md`](cloudflare.md)(넘김 조건식)와
> [`status.sh`](status.sh)(점검) 에 있다.

## 목표

사이트가 넷인데 서로 관계가 안 보이고, 루트 주소(sungd.uk)를 에세이 블로그가 쓰고 있어 나머지가 형제인지 자식인지 애매하다. tech 는 넉 달째 멈춰 있다. 루트를 "나"로 되찾고 멈춘 사이트를 해체해 관리 대상을 줄인다.

## 최종 모양

```
sungd.uk          나 — 소개 + 프로젝트 14개   (blog-tech repo)
├── resume.       이력서                      (그대로)
├── writing.      글 — 책·생각·기술            (blog-writing)
└── today.        Claude Code·Codex 큐레이션   (ai-pick, ai. 에서 개명)
```

넷 다 GitHub Pages 에 그대로 둔다. 옛 주소를 넘기는 일만 Cloudflare 가 맡는다 — 자세한 건 `cloudflare.md`.

tech. 는 없어진다. 프로젝트 소개 14개는 루트에 남고, 기술 글 12편은 writing 으로 갔다.

## 코드 작업 — 끝남

세 repo 모두 브랜치를 push 해뒀다. main 에는 안 합쳤다 — 합치는 순간 사이트가 바뀌므로 아래 순서에 맞춰야 한다.

| repo (GitHub)          | 로컬 폴더            | 브랜치                | 한 일                                                   |
| ---------------------- | -------------------- | --------------------- | ------------------------------------------------------- |
| newhigen/blog-tech     | `newhigen.github.io` | `worktree-reorg-plan` | blog 걷어내고 루트 사이트로 개조, CNAME 을 sungd.uk 로   |
| newhigen/blog-writing  | `blog-writing`       | `reorg-writing`       | 기술 글 12편 흡수, 기술 카테고리 추가, 도메인 표기 변경  |
| newhigen/ai-pick       | `ai-pick`            | `reorg-today`         | CNAME·sitemap·robots·README 를 today.sungd.uk 로         |

검증한 것: 두 Astro 사이트 모두 빌드 통과. writing 은 글 79편이 다 생성되고 옮겨온 12편의 주소가 예전 그대로(`/claude-code-tips/` 등). 루트는 18쪽이 나오고 내부 링크에 깨진 곳이 없다.

## 남은 일 — 사람이 해야 하는 것

GitHub 설정과 Cloudflare 는 웹에서만 되므로 직접 해야 한다. **순서대로** 해야 도메인이 겹치지 않는다.

### 1. writing 먼저 (여기는 안 깨진다)

1. Cloudflare 에 `writing.sungd.uk` CNAME → `newhigen.github.io` 추가, **회색 구름**
2. blog-writing repo: `git merge reorg-writing && git push`
3. blog-writing Settings → Pages → 커스텀 도메인을 `sungd.uk` 에서 `writing.sungd.uk` 로
4. 인증서 발급되고 열리는지 확인

이 시점에 `sungd.uk` 는 주인이 없어져 잠깐 뜨지 않는다. 3단계까지 이어서 가면 된다.

### 2. today (여기서 ai 가 잠깐 끊긴다)

1. Cloudflare 에 `today.sungd.uk` CNAME → `newhigen.github.io` 추가, **회색 구름**
2. ai-pick repo: `git merge reorg-today && git push`
3. ai-pick Settings → Pages → 커스텀 도메인을 `today.sungd.uk` 로
4. 열리는지 확인

GitHub Pages 는 repo 하나에 도메인 하나뿐이라 `ai` 와 `today` 를 같이 못 쓴다. `ai.sungd.uk` 는 여기서 끊기고 4단계에서 되살아난다.

### 3. 루트 사이트

1. blog-tech repo: `git merge worktree-reorg-plan && git push` — 워크플로가 Pages 로 배포한다
2. blog-tech Settings → Pages → 커스텀 도메인을 `tech.sungd.uk` 에서 `sungd.uk` 로
3. 인증서 발급되고 "Enforce HTTPS" 켜지는 것 확인
4. 소개+프로젝트 홈이 뜨는지 확인

apex 는 이미 GitHub Pages A 레코드를 갖고 있어서 DNS 는 안 건드려도 된다. 주인만 바뀐다.

### 4. Cloudflare 규칙 — 옛 주소 되살리기

`cloudflare.md` 대로 한다. 요약하면 구름 켜고(sungd.uk·tech·ai) 규칙 다섯 개를 넣는다.
이걸 넣어야 옛 글 주소·tech·ai 가 다 새 주소로 넘어간다.

⚠ `sungd.uk` 는 3단계에서 인증서가 발급된 뒤에 주황으로 바꾼다. 먼저 바꾸면 발급이 막힌다.

### 5. 폴더·repo 이름 정리 (선택, 나중에)

사이트가 다 살아난 걸 확인한 뒤에 한다. 폴더 이름 = 서브도메인 이름으로 맞추는 안:

```
newhigen.github.io → home       (repo: blog-tech → home)
blog-writing       → writing    (repo: blog-writing → writing)
ai-pick            → today      (repo: ai-pick → today)
resume             → 그대로
calc-tools         → 도메인 보류라 그대로
```

바꾸면 `dev/CLAUDE.md`, `tools/server-console` 의 registry·문서, claude-config 스킬 2개의 경로도 같이 고쳐야 한다. 참고로 registry 는 지금도 없는 경로(`sites/blog-tech`)를 가리키고 있다.

## 보류

- calc-tools — 도메인 안 붙임. 나중에 붙인다면 tools. 아래로 묶는 안이 있다.
- `package.json` 의 이름이 아직 `blog-tech` 다.
- Google Analytics 태그는 tech 시절 것을 그대로 쓴다. 성격이 바뀌었으니 나중에 볼 것.
- blog-writing 에 Netlify 어댑터·`netlify.toml` 이 남아 있는데 실제 배포는 GitHub Pages 다. 안 쓰는 설정이라 이번엔 안 건드렸다.
