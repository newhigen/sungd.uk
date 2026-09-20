# resume.sungd.uk

이력서와 만든 것들(Projects). Astro 정적 사이트, GitHub Actions 가 빌드해 Pages 로 배포한다.

```sh
npm install
npm run dev
```

## 어디를 고치나

```
public/index.html      이력서 (한국어) — 손으로 관리, 빌드에 안 태운다
public/en/index.html   이력서 (영문)
public/style.css       이력서 전용 스타일
public/script.js       재직 기간 자동 계산 + 사이드바 현재 섹션 표시
src/content/projects/  프로젝트 14개 (마크다운)
src/pages/projects/    프로젝트 목록·상세
```

## 이력서를 고칠 때

- **두 쪽을 같이 고친다.** 한국어·영문이 같은 구조·같은 클래스를 쓴다.
- 경력 기간은 `data-from` / `data-to` 만 넣으면 오늘 날짜 기준으로 자동 계산된다.
- 내용은 **본인 확인 없이 바꾸지 않는다.** `resume-studio` 의 master 데이터에 더 최신·상세한 이력이
  있지만, 무엇을 반영할지는 항목별로 정한다.

## 옛 주소

이 사이트는 `tech.sungd.uk` 였다. 2026-08-09 재편 때 기술 글은 `writing.sungd.uk` 로 보내고
프로젝트만 남긴 뒤, 이력서를 첫 쪽으로 들여왔다. 넘김(리다이렉트)은 안 걸었다.

배경과 결정 과정은 `docs/reorg/` 참고. 다른 사이트는 [sungd.uk](https://sungd.uk) 에서.
