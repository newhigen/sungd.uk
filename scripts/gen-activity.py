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

# 주제 아이콘(Lucide, 선)과 발행처 로고(Simple Icons, 면). 모두 currentColor 한 색
SV = '<svg class="act-ic" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.75" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">'
LG = lambda d, name: f'<svg class="act-logo" viewBox="0 0 24 24" fill="currentColor" role="img" aria-label="{name}"><path d="{d}"/></svg>'
IC = {
    'tech': SV + '<path d="m18 16 4-4-4-4"/><path d="m6 8-4 4 4 4"/><path d="m14.5 4-5 16"/></svg>',  # code-xml
    'med': SV + '<path d="M11 2v2"/><path d="M5 2v2"/><path d="M5 3H4a2 2 0 0 0-2 2v4a6 6 0 0 0 12 0V5a2 2 0 0 0-2-2h-1"/><path d="M8 15a6 6 0 0 0 12 0v-3"/><circle cx="20" cy="10" r="2"/></svg>',  # stethoscope
    'cert': SV + '<path d="M3.85 8.62a4 4 0 0 1 4.78-4.77 4 4 0 0 1 6.74 0 4 4 0 0 1 4.78 4.78 4 4 0 0 1 0 6.74 4 4 0 0 1-4.77 4.78 4 4 0 0 1-6.75 0 4 4 0 0 1-4.78-4.77 4 4 0 0 1 0-6.76Z"/><path d="m9 12 2 2 4-4"/></svg>',  # badge-check
    'topic': SV + '<path d="M12.83 2.18a2 2 0 0 0-1.66 0L2.6 6.08a1 1 0 0 0 0 1.83l8.58 3.91a2 2 0 0 0 1.66 0l8.58-3.9a1 1 0 0 0 0-1.83z"/><path d="M2 12a1 1 0 0 0 .58.91l8.6 3.91a2 2 0 0 0 1.65 0l8.58-3.9A1 1 0 0 0 22 12"/><path d="M2 17a1 1 0 0 0 .58.91l8.6 3.91a2 2 0 0 0 1.65 0l8.58-3.9A1 1 0 0 0 22 17"/></svg>',  # layers
    'year': SV + '<path d="M8 2v4"/><path d="M16 2v4"/><rect width="18" height="18" x="3" y="4" rx="2"/><path d="M3 10h18"/></svg>',  # calendar
    'Anthropic': LG('M17.3041 3.541h-3.6718l6.696 16.918H24Zm-10.6082 0L0 20.459h3.7442l1.3693-3.5527h7.0052l1.3693 3.5528h3.7442L10.5363 3.5409Zm-.3712 10.2232 2.2914-5.9456 2.2914 5.9456Z', 'Anthropic'),
    'MongoDB': LG('M17.193 9.555c-1.264-5.58-4.252-7.414-4.573-8.115-.28-.394-.53-.954-.735-1.44-.036.495-.055.685-.523 1.184-.723.566-4.438 3.682-4.74 10.02-.282 5.912 4.27 9.435 4.888 9.884l.07.05A73.49 73.49 0 0111.91 24h.481c.114-1.032.284-2.056.51-3.07.417-.296.604-.463.85-.693a11.342 11.342 0 003.639-8.464c.01-.814-.103-1.662-.197-2.218zm-5.336 8.195s0-8.291.275-8.29c.213 0 .49 10.695.49 10.695-.381-.045-.765-1.76-.765-2.405z', 'MongoDB'),
}

def page(lang, head):
    t = T[lang]; ko = lang == 'ko'
    def item(r, logo=False):
        y, m, cat, nko, nen, place, url = r
        name = nko if ko else nen
        if url: name = f'<a href="{url}" target="_blank" rel="noopener noreferrer">{name}</a>'
        if cat == 'cert': tail = f'<span class="act-issuer">{IC[place]}</span>' if logo else ''  # 주제별 보기에선 발행처가 소제목이다
        elif place is None: tail = f'<sup class="act-online">{t["online"]}</sup>'
        else: tail = f'<span class="act-place">{PIN}{PLACE[place][0 if ko else 1]}</span>'
        return f'<div class="act-name">{name}{tail}</div>'

    def grid(rows, label=None):
        """주제별 보기: 연도 | 월 | 이름. label 을 주면 연도별 보기: 주제 | 월 | 이름."""
        h, py, pm = '<div class="act-grid' + (' by-topic' if label else '') + '">', None, None
        first = True
        for r in rows:
            y, m = r[0], r[1]
            newy = y != py
            cls = ' act-newyear' if newy and py is not None else (' act-newmonth' if (m != pm) else '')
            mcell = t['month'](m) if (newy or m != pm) else ''
            if label: h += f'<div class="act-t{cls}">{(IC[label] + t[label]) if first else ""}</div>'
            else: h += f'<div class="act-y{cls}">{y if newy else ""}</div>'
            first = False
            h += f'<div class="act-m{cls}">{mcell}</div><div class="act-i{cls}">{item(r, logo=bool(label))}</div>'
            py, pm = y, m
        return h + '</div>'

    sel = lambda c: [r for r in ROWS if r[2] == c]
    sub = lambda icon, name, rows: f'<div class="act-grp">{IC[icon]}{name}</div>' + grid(rows)
    certs = ''.join(sub(iss, iss, [r for r in sel('cert') if r[5] == iss]) for iss in ['Anthropic', 'MongoDB'])
    topic = f'''
  <main class="cv-sections act-view" data-view="topic">
    <section id="conferences">
      <div class="sec-head"><h2 class="sec-title">{t['conf']}</h2></div>
      <div class="sec-content">
        {sub('tech', t['tech'], sel('tech'))}
        {sub('med', t['med'], sel('med'))}
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
            year += grid(rs, label=c)
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

  <header class="profile-header act-head">
    <div class="profile-left">
      <div class="meta">
        <div class="name-row">
          <h1 class="name-ko">{t['h1']}</h1>
          <span class="name-en">{t['sub']}</span>
        </div>
        <div class="role-line"><span>{t['lead']}</span></div>
      </div>
    </div>
    <div class="act-toggle" role="group" aria-label="{t['seg']}">
      <button type="button" data-v="topic" aria-pressed="true">{IC['topic']}{t['topic']}</button>
      <button type="button" data-v="year" aria-pressed="false">{IC['year']}{t['year']}</button>
    </div>
  </header>
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
