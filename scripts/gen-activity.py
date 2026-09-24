# 활동 페이지(/activity/, /activity/en/)를 만든다. 항목을 고치려면 ROWS 를 고치고 다시 돌린다.
#   python3 scripts/gen-activity.py
# <head> 는 지금 파일의 것을 그대로 두고 <body> 만 새로 쓴다. 스타일은 public/style.css 의 「활동 페이지」 절.
import os

# (연, 월, 분류, 한국어 이름, 영문 이름, 장소키 or None(온라인), 링크)
ROWS = [
    (2026, 9, 'tech', '2026 당근 Builder Meetup', '2026 Daangn Builder Meetup', 'seoul', 'https://ticketa.co/event/x0u2znh1'),
    (2026, 9, 'tech', 'Weights & Biases 서울 밋업 #12', 'Weights & Biases Seoul Meetup #12', 'seoul', 'https://wandb.ai/site/resources/events/seoul-meetup-12/'),
    (2026, 9, 'med', 'KCR, 대한영상의학회', 'KCR, Korean Congress of Radiology', 'goyang', 'https://2026.kcr4u.org/'),
    (2026, 6, 'tech', '토스 웨비나: AI 시대, 기술 조직에서 더 넓은 문제를 풀고 싶다면', 'Toss Webinar: Solving Broader Problems in Tech Organizations in the AI Era', None, ''),
    (2026, 5, 'tech', '토스 AI 웨비나: Data Engineer와 Data Analytics Engineer', 'Toss AI Webinar: Data Engineers and Data Analytics Engineers', None, 'https://youtube.com/live/h4ZEmEW5fe0'),
    (2026, 5, 'tech', '원티드 하이파이브 2026', 'Wanted HighFive 2026', 'seoul', 'https://event.wanted.co.kr/highfive/2026'),
    (2026, 4, 'tech', '토스 모닥불: 토스 FE는 AI를 이렇게 씁니다', 'Toss Modakbul: How Toss Frontend Uses AI', None, 'https://www.youtube.com/live/GfC-PcXO4ek'),
    (2026, 3, 'med', 'ECR, 유럽영상의학회', 'ECR, European Congress of Radiology', 'vienna', 'https://www.myesr.org/congress/'),
    (2025, 9, 'med', 'KCR, 대한영상의학회', 'KCR, Korean Congress of Radiology', 'seoul', 'https://2025.kcr4u.org/'),
    (2024, 10, 'med', 'KCR, 대한영상의학회', 'KCR, Korean Congress of Radiology', 'seoul', 'https://2024.kcr4u.org/'),
    (2023, 11, 'med', 'RSNA, 북미영상의학회', 'RSNA, Radiological Society of North America', 'chicago', 'https://www.rsna.org/annual-meeting'),
    (2023, 9, 'med', 'KCR, 대한영상의학회', 'KCR, Korean Congress of Radiology', 'seoul', 'https://2023.kcr4u.org/'),
    (2022, 6, 'med', 'KSSR, 대한영상의학회 춘계심포지엄', 'KSSR, Korean Spring Symposium of Radiology', 'busan', 'https://www.kssr.kr/'),
    (2021, 4, 'med', 'ISBI, IEEE 국제생체의학영상심포지엄', 'ISBI, IEEE International Symposium on Biomedical Imaging', None, 'https://biomedicalimaging.org/2021/'),
    (2020, 11, 'med', 'KOSOMBE, 대한의용생체공학회', 'KOSOMBE, Korean Society of Medical and Biological Engineering', None, 'https://kosombe.or.kr/'),
    # 수료 — resume-studio/master/certifications.yaml. 장소키 자리는 발행처
    (2026, 3, 'cert', 'Introduction to subagents', 'Introduction to subagents', 'Anthropic', 'https://verify.skilljar.com/c/aducvhf6396h'),
    (2026, 3, 'cert', 'Introduction to agent skills', 'Introduction to agent skills', 'Anthropic', 'https://verify.skilljar.com/c/fiqyk3xkq64r'),
    (2025, 12, 'cert', 'Claude Code in Action', 'Claude Code in Action', 'Anthropic', 'https://verify.skilljar.com/c/tq9qfui7nrwo'),
    (2025, 12, 'cert', 'Building AI Agents with MongoDB', 'Building AI Agents with MongoDB', 'MongoDB', 'https://www.credly.com/badges/4c1bebb2-029d-4340-b8d7-28dfd25b5d62'),
    (2025, 12, 'cert', 'Building RAG Apps Using MongoDB', 'Building RAG Apps Using MongoDB', 'MongoDB', 'https://www.credly.com/badges/e057697e-2d0f-4c11-9281-ac87191fc595'),
    (2025, 12, 'cert', 'Building AI-Powered Search with MongoDB Vector Search', 'Building AI-Powered Search with MongoDB Vector Search', 'MongoDB', 'https://www.credly.com/badges/2f4ee727-8eee-4906-812b-7e642861697b'),
]
# 한국어는 국내면 도시만, 해외면 도시와 나라. 영문은 늘 도시와 나라.
PLACE = {
    'seoul': ('서울', 'Seoul, Korea'), 'goyang': ('고양', 'Goyang, Korea'), 'busan': ('부산', 'Busan, Korea'),
    'vienna': ('비엔나, 오스트리아', 'Vienna, Austria'), 'chicago': ('시카고, 미국', 'Chicago, USA'),
}
T = {
    'ko': dict(title='조성덕 | 활동', desc='조성덕 — 학회 참석과 수료', h1='활동', sub='조성덕', lead='학회 참석과 수료',
               topic='주제별', year='연도별', conf='학회', tech='테크', med='의학', cert='수료', online='온라인',
               month=lambda m: f'{m}월', sw=('/activity/en/', 'EN'), cv=('/cv/', '이력서'), seg='보기'),
    'en': dict(title='Sungduk Cho | Activity', desc='Sungduk Cho — Conferences and courses', h1='Activity', sub='Sungduk Cho', lead='Conferences and courses',
               topic='By topic', year='By year', conf='Conferences', tech='Tech', med='Medical', cert='Courses', online='Virtual',
               month=lambda m: ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'][m-1], sw=('/activity/', 'KO'), cv=('/cv/en/', 'CV'), seg='View'),
}
PIN = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.75" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M20 10c0 4.99-5.54 10.19-7.4 11.8a1 1 0 0 1-1.2 0C9.54 20.19 4 14.99 4 10a8 8 0 0 1 16 0"/><circle cx="12" cy="10" r="3"/></svg>'

def page(lang, head):
    t = T[lang]; ko = lang == 'ko'
    def item(r):
        y, m, cat, nko, nen, place, url = r
        name = nko if ko else nen
        if url: name = f'<a href="{url}" target="_blank" rel="noopener noreferrer">{name}</a>'
        if cat == 'cert': tail = ''  # 발행처는 주제별 보기의 소제목과 이름에 드러난다
        elif place is None: tail = f'<sup class="act-online">{t["online"]}</sup>'
        else: tail = f'<span class="act-place">{PIN}{PLACE[place][0 if ko else 1]}</span>'
        return f'<div class="act-name">{name}{tail}</div>'

    def grid(rows, show_year=True, label=None):
        h, py, pm = '<div class="act-grid' + ('' if show_year or label else ' no-year') + (' by-topic' if label else '') + '">', None, None
        first = True
        for r in rows:
            y, m = r[0], r[1]
            newy = y != py
            cls = ' act-newyear' if newy and py is not None else (' act-newmonth' if (m != pm) else '')
            mcell = t['month'](m) if (newy or m != pm) else ''
            if label: h += f'<div class="act-t{cls}">{label if first else ""}</div>'
            elif show_year: h += f'<div class="act-y{cls}">{y if newy else ""}</div>'
            first = False
            h += f'<div class="act-m{cls}">{mcell}</div><div class="act-i{cls}">{item(r)}</div>'
            py, pm = y, m
        return h + '</div>'

    sel = lambda c: [r for r in ROWS if r[2] == c]
    certs = ''.join(f'<div class="act-grp">{iss}</div>' + grid([r for r in sel('cert') if r[5] == iss]) for iss in ['Anthropic', 'MongoDB'])
    topic = f'''
  <main class="cv-sections act-view" data-view="topic">
    <section id="conferences">
      <div class="sec-head"><h2 class="sec-title">{t['conf']}</h2></div>
      <div class="sec-content">
        <div class="act-grp">{t['tech']}</div>{grid(sel('tech'))}
        <div class="act-grp">{t['med']}</div>{grid(sel('med'))}
      </div>
    </section>
    <section id="courses">
      <div class="sec-head"><h2 class="sec-title">{t['cert']}</h2></div>
      <div class="sec-content">{certs}</div>
    </section>
  </main>'''
    year = '\n  <main class="cv-sections act-view" data-view="year" hidden>'
    for y in sorted({r[0] for r in ROWS}, reverse=True):
        year += f'\n    <section>\n      <div class="sec-head"><h2 class="act-year-title">{y}</h2></div>\n      <div class="sec-content">'
        for c in ['tech', 'med', 'cert']:
            rs = [r for r in ROWS if r[0] == y and r[2] == c]
            if not rs: continue
            year += grid(rs, show_year=False, label=t[c])
        year += '</div>\n    </section>'
    year += '\n  </main>'

    return f'''{head(t)}
<body>
<div class="cv-wrap">

  <nav class="nav-top">
    <a href="/" class="back-home">← sungd.uk</a>
    <div class="nav-right">
      <a href="{t['sw'][0]}" class="lang-switch">{t['sw'][1]}</a>
    </div>
  </nav>

  <header class="profile-header">
    <div class="profile-left">
      <div class="meta">
        <div class="name-row">
          <h1 class="name-ko">{t['h1']}</h1>
          <span class="name-en">{t['sub']}</span>
        </div>
        <div class="role-line"><span>{t['lead']}</span></div>
      </div>
    </div>
  </header>

  <div class="act-toggle" role="group" aria-label="{t['seg']}">
    <button type="button" data-v="topic" aria-pressed="true">{t['topic']}</button>
    <button type="button" data-v="year" aria-pressed="false">{t['year']}</button>
  </div>
{topic}{year}

  <footer>
    <a href="/" class="back-home">← sungd.uk</a>
    <a href="{t['cv'][0]}" class="sec-link">{t['cv'][1]}</a>
  </footer>

</div>
<script>
  document.querySelectorAll('.act-toggle button').forEach(function (btn) {{
    btn.addEventListener('click', function () {{
      document.querySelectorAll('.act-toggle button').forEach(function (b) {{ b.setAttribute('aria-pressed', b === btn); }});
      document.querySelectorAll('.act-view').forEach(function (v) {{ v.hidden = v.dataset.view !== btn.dataset.v; }});
    }});
  }});
</script>
</body>
</html>
'''

if __name__ == '__main__':
    pub = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'public', 'activity')
    for lang, out in [('ko', 'index.html'), ('en', 'en/index.html')]:
        path = os.path.join(pub, out)
        old = open(path).read()
        head = old[:old.index('</head>') + len('</head>')]
        open(path, 'w').write(page(lang, lambda t: head))
    print('ok')
