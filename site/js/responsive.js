(function () {
  'use strict';

  // --- Mobile detection ---
  var debounceTimer;
  function updateMobileFlag() {
    window.AKYRA_IS_MOBILE = window.innerWidth < 768;
  }
  updateMobileFlag();
  window.addEventListener('resize', function () {
    clearTimeout(debounceTimer);
    debounceTimer = setTimeout(updateMobileFlag, 250);
  });

  // --- Hamburger menu ---
  var nav = document.getElementById('nav');
  var hamburger = nav && nav.querySelector('.nav-hamburger');

  function setMenuOpen(open) {
    if (!nav) return;
    nav.classList.toggle('nav-open', open);
    if (hamburger) hamburger.setAttribute('aria-expanded', String(open));
    document.body.style.overflow = open ? 'hidden' : '';
  }

  if (hamburger) {
    hamburger.addEventListener('click', function () {
      setMenuOpen(!nav.classList.contains('nav-open'));
    });
  }

  if (nav) {
    nav.querySelectorAll('.nav-links a').forEach(function (link) {
      link.addEventListener('click', function () { setMenuOpen(false); });
    });
  }

  document.addEventListener('keydown', function (e) {
    if (e.key === 'Escape' && nav && nav.classList.contains('nav-open')) {
      setMenuOpen(false);
    }
  });

  // --- Stats bar scroll hint ---
  var statsBar = document.getElementById('live-stats-bar');
  if (statsBar) {
    var check = function () {
      statsBar.classList.toggle(
        'scroll-hint',
        statsBar.scrollWidth > statsBar.clientWidth
      );
    };
    check();
    window.addEventListener('resize', check);
  }
})();
