/* Kixly BD pilot report — navigation behaviour */
(function () {
  'use strict';

  var sidebar = document.getElementById('sidebar');
  var menuBtn = document.getElementById('menuBtn');
  var scrim = document.getElementById('scrim');
  var toc = document.getElementById('toc');
  var search = document.getElementById('tocSearch');
  var progress = document.querySelector('#progress span');
  var content = document.getElementById('content');

  /* ---------- mobile drawer ---------- */
  function setNav(open) {
    document.body.classList.toggle('nav-open', open);
    scrim.hidden = !open;
    menuBtn.setAttribute('aria-expanded', String(open));
  }
  if (menuBtn) {
    menuBtn.addEventListener('click', function () {
      setNav(!document.body.classList.contains('nav-open'));
    });
    scrim.addEventListener('click', function () { setNav(false); });
    toc.addEventListener('click', function (e) {
      if (e.target.closest('a')) setNav(false);
    });
    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape') setNav(false);
    });
  }

  /* ---------- contents filtering ---------- */
  if (search) {
    search.addEventListener('input', function () {
      var q = search.value.trim().toLowerCase();
      var items = toc.querySelectorAll('li');
      items.forEach(function (li) {
        var link = li.querySelector(':scope > a');
        var own = link ? link.textContent.toLowerCase().indexOf(q) !== -1 : false;
        var childMatch = !!li.querySelector(':scope > ul > li:not(.hidden)');
        li.classList.toggle('hidden', !!q && !own && !childMatch);
        if (q) li.classList.add('open');
        else if (!li.querySelector('a.active')) li.classList.remove('open');
      });
    });
  }

  /* ---------- active heading tracking ---------- */
  var links = Array.prototype.slice.call(toc.querySelectorAll('a'));
  var byId = {};
  links.forEach(function (a) {
    var id = a.getAttribute('href').slice(1);
    if (id) (byId[id] = byId[id] || []).push(a);
  });

  var headings = Array.prototype.slice
    .call(content.querySelectorAll('h2[id], h3[id]'))
    .filter(function (h) { return byId[h.id]; });

  function activate(id) {
    links.forEach(function (a) {
      a.classList.toggle('active', a.getAttribute('href') === '#' + id);
    });
    links.forEach(function (a) {
      if (a.classList.contains('active')) {
        var li = a.closest('li');
        while (li && li !== toc) {
          li.classList.add('open');
          li = li.parentElement ? li.parentElement.closest('li') : null;
        }
        var top = a.parentElement;
        while (top && top.parentElement !== toc) top = top.parentElement;
        if (top) top.classList.add('open');
        scrollTocIntoView(a);
      }
    });
  }

  function scrollTocIntoView(el) {
    var box = toc.getBoundingClientRect();
    var r = el.getBoundingClientRect();
    if (r.top < box.top + 8 || r.bottom > box.bottom - 8) {
      toc.scrollTop += r.top - box.top - box.height / 2.4;
    }
  }

  if ('IntersectionObserver' in window && headings.length) {
    var visible = {};
    var observer = new IntersectionObserver(
      function (entries) {
        entries.forEach(function (en) {
          visible[en.target.id] = en.isIntersecting ? en.intersectionRatio : 0;
        });
        var best = null, bestRatio = 0;
        headings.forEach(function (h) {
          if ((visible[h.id] || 0) >= bestRatio) {
            bestRatio = visible[h.id] || 0;
            best = h;
          }
        });
        if (!best) {
          // Nothing intersecting (long section) — pick the last heading above the fold.
          for (var i = 0; i < headings.length; i++) {
            if (headings[i].getBoundingClientRect().top <= 120) best = headings[i];
          }
        }
        if (best) activate(best.id);
      },
      { rootMargin: '-70px 0px -65% 0px', threshold: [0, 0.15, 0.4, 1] }
    );
    headings.forEach(function (h) { observer.observe(h); });
  }

  /* ---------- reading progress ---------- */
  var ticking = false;
  function onScroll() {
    if (ticking) return;
    ticking = true;
    requestAnimationFrame(function () {
      var h = document.documentElement;
      var max = h.scrollHeight - h.clientHeight;
      progress.style.width = (max > 0 ? (h.scrollTop / max) * 100 : 0) + '%';
      ticking = false;
    });
  }
  window.addEventListener('scroll', onScroll, { passive: true });
  onScroll();

  /* ---------- print ---------- */
  var printBtn = document.getElementById('printBtn');
  if (printBtn) printBtn.addEventListener('click', function () { window.print(); });

  /* ---------- open the first section by default ---------- */
  var first = toc.querySelector('li');
  if (first) first.classList.add('open');
})();
