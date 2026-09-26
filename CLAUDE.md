# sungd.uk

대표 사이트. 소개(첫 화면), 이력서(/cv), 활동(/activity). Astro.

## 실행

```sh
npm install
npm run dev       # localhost:4321
npm run cv-pdf    # 이력서 PDF 다시 굽기 (public/cv/sungduk-cho-cv.pdf)
```

## 어디를 고치나

```
src/pages/index.astro    첫 화면 (소개)
public/cv/               이력서 — 손으로 관리하는 HTML. 영문은 cv/en/
public/activity/         활동. 영문은 activity/en/
```

## 배포

main 에 머지하면 `.github/workflows/deploy.yml` 이 빌드해 GitHub Pages 로 올린다.

## ⚠ 경고

- 이력서 내용은 본인 확인 없이 바꾸지 않는다. `resume-studio` 의 master 데이터가 더 최신이어도 항목별로 묻는다.
- 이력서는 한국어와 영문을 같이 고친다. 같은 구조와 클래스를 쓴다.
- 경력 기간은 `data-from` / `data-to` 만 넣는다. 오늘 날짜 기준으로 자동 계산된다.
- 변천사는 `HISTORY.md`, 재편 배경은 `docs/reorg/`.
