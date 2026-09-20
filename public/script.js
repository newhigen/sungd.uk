// 1) 재직 기간을 오늘 기준으로 계산해 채운다. 표기는 문서 언어(<html lang>)를 따른다.
// 2) 스크롤 위치에 맞춰 섹션 이동줄의 현재 항목을 표시한다.
(function () {
  var EN = document.documentElement.lang === 'en';

  function months(start, end) {
    var s = start.split('.').map(Number);
    var e = end ? end.split('.').map(Number) : null;
    var now = new Date();
    var ey = e ? e[0] : now.getFullYear();
    var em = e ? e[1] : now.getMonth() + 1;
    return (ey - s[0]) * 12 + (em - s[1]) + 1;
  }

  function label(n) {
    var y = Math.floor(n / 12), m = n % 12;
    if (EN) {
      var yl = y + (y === 1 ? ' yr' : ' yrs');
      var ml = m + (m === 1 ? ' mo' : ' mos');
      if (y === 0) return ml;
      if (m === 0) return yl;
      return yl + ' ' + ml;
    }
    if (y === 0) return m + '개월';
    if (m === 0) return y + '년';
    return y + '년 ' + m + '개월';
  }

  document.querySelectorAll('[data-from]').forEach(function (el) {
    el.textContent = label(months(el.dataset.from, el.dataset.to));
  });

  // ── 현재 섹션 표시 ──
  // IntersectionObserver 의 rootMargin 은 화면 높이에 따라 결과가 널뛰어서,
  // 기준선(화면 위 1/3)을 지난 마지막 섹션을 고르는 방식으로 한다.
  var links = Array.prototype.slice.call(document.querySelectorAll('.nav a'));
  if (!links.length) return;

  var targets = links
    .map(function (a) { return { a: a, el: document.getElementById(a.getAttribute('href').slice(1)) }; })
    .filter(function (t) { return t.el; });
  if (!targets.length) return;

  var queued = false;
  function paint() {
    queued = false;
    var line = window.innerHeight * 0.3;
    var cur = targets[0];
    targets.forEach(function (t) {
      if (t.el.getBoundingClientRect().top <= line) cur = t;
    });
    targets.forEach(function (t) { t.a.classList.toggle('on', t === cur); });
  }
  function onScroll() {
    if (queued) return;
    queued = true;
    requestAnimationFrame(paint);
  }

  window.addEventListener('scroll', onScroll, { passive: true });
  window.addEventListener('resize', onScroll, { passive: true });
  paint();
})();
