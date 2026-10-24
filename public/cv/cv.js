// cv 보기: 820px 이상은 A4 종이, 그 아래는 웹. 폭으로만 정하고 전환 단추는 두지 않는다.
// A4 는 본문 블록(.b)을 재서 쪽 높이(297mm − 위아래 15mm)를 넘는 블록을 통째로 다음 쪽으로 넘긴다.
// 섹션 제목처럼 data-keep 이 붙은 블록은 다음 블록과 같은 쪽에 둔다. 인쇄와 PDF 는 cv.css 의 print 규칙이 맡는다.
(function () {
  var PAGE_H = 1123 - 114; // A4 높이 − 위아래 여백
  var root = document.documentElement;
  var flow = document.getElementById('cvp-flow');
  var stage = document.getElementById('cvp-stage');
  var viewer = document.getElementById('cvp-viewer');
  var narrow = window.matchMedia('(max-width: 819px)');
  try { localStorage.removeItem('cvView'); } catch (e) {} // 단추가 있던 때 저장한 값

  function mode() { return narrow.matches ? 'web' : 'a4'; }

  function paginate() {
    var m = document.createElement('div');
    m.className = 'cvp-measure';
    var c = flow.cloneNode(true);
    c.removeAttribute('id');
    c.className = 'cv';
    m.appendChild(c);
    document.body.appendChild(m);
    var els = Array.prototype.slice.call(c.children);
    var top0 = els[0].getBoundingClientRect().top;
    var box = els.map(function (el) {
      var r = el.getBoundingClientRect();
      var mt = parseFloat(getComputedStyle(el).marginTop) || 0;
      return { top: r.top - top0, bot: r.bottom - top0, mt: mt, keep: el.hasAttribute('data-keep') };
    });
    document.body.removeChild(m);
    var pages = [[]], start = 0;
    for (var i = 0; i < els.length; i++) {
      var cur = pages[pages.length - 1];
      if (!cur.length) start = box[i].top;
      if (box[i].bot - start > PAGE_H && cur.length) {
        var carry = [];
        while (cur.length && box[cur[cur.length - 1]].keep) carry.unshift(cur.pop());
        pages.push(carry.concat([i]));
        start = box[carry.length ? carry[0] : i].top;
      } else cur.push(i);
    }
    return pages;
  }

  function build() {
    var blocks = Array.prototype.slice.call(flow.children);
    var pages = paginate();
    var wrap = document.createElement('div');
    wrap.className = 'cvp-pages';
    pages.forEach(function (ix, n) {
      var page = document.createElement('section');
      page.className = 'cvp-page';
      var cv = document.createElement('div');
      cv.className = 'cv';
      cv.lang = flow.lang;
      ix.forEach(function (i) { cv.appendChild(blocks[i].cloneNode(true)); });
      page.appendChild(cv);
      var no = document.createElement('span');
      no.className = 'cvp-pno';
      no.textContent = (n + 1) + ' / ' + pages.length;
      page.appendChild(no);
      wrap.appendChild(page);
    });
    stage.innerHTML = '';
    stage.appendChild(wrap);
    // 쪽 안 링크(논문 인용)는 흐름 쪽 id 와 겹치지 않게 떼어 낸다
    Array.prototype.forEach.call(wrap.querySelectorAll('[id]'), function (el) { el.id = 'p-' + el.id; });
    Array.prototype.forEach.call(wrap.querySelectorAll('a[href^="#"]'), function (a) { a.setAttribute('href', '#p-' + a.getAttribute('href').slice(1)); });
    fit();
  }

  function fit() {
    var wrap = stage.querySelector('.cvp-pages');
    if (!wrap) return;
    var cs = getComputedStyle(viewer);
    var avail = viewer.clientWidth - parseFloat(cs.paddingLeft) - parseFloat(cs.paddingRight);
    var s = Math.min(1, avail / 794);
    wrap.style.transform = 'scale(' + s + ')';
    stage.style.width = 794 * s + 'px';
    stage.style.height = wrap.offsetHeight * s + 'px';
  }

  function apply() {
    var m = mode();
    root.classList.toggle('cvp-a4', m === 'a4');
    if (m === 'a4') build(); else stage.innerHTML = '';
  }

  var t;
  window.addEventListener('resize', function () { clearTimeout(t); t = setTimeout(fit, 60); });
  if (narrow.addEventListener) narrow.addEventListener('change', apply);
  // 이메일은 링크 대신 눌러서 복사(쪽마다 복제되므로 문서에 한 번 건다)
  function copy(el) {
    var v = el.getAttribute('data-copy'), t = el.querySelector('span');
    if (!navigator.clipboard) return;
    navigator.clipboard.writeText(v).then(function () {
      t.textContent = el.getAttribute('data-done');
      setTimeout(function () { t.textContent = v; }, 1200);
    }).catch(function () {});
  }
  document.addEventListener('click', function (e) { var el = e.target.closest && e.target.closest('.em'); if (el) copy(el); });
  document.addEventListener('keydown', function (e) { var el = e.target.closest && e.target.closest('.em'); if (el && (e.key === 'Enter' || e.key === ' ')) { e.preventDefault(); copy(el); } });
  apply();
  if (document.fonts && document.fonts.ready) document.fonts.ready.then(function () { if (mode() === 'a4') build(); });
})();
