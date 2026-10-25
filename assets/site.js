/* saez24.github.io — Hell/Dunkel-Schalter, Nav beim Scrollen, Menü auf dem Handy.
   Wird ohne defer im <head> geladen, damit das gespeicherte Theme vor dem ersten
   Zeichnen gesetzt ist. Einzige gespeicherte Angabe: „saez24-theme“ im localStorage. */
(function () {
  var KEY = 'saez24-theme';
  var root = document.documentElement;

  function saved() {
    try {
      return localStorage.getItem(KEY);
    } catch (e) {
      return null;
    }
  }

  function apply(theme) {
    root.setAttribute('data-theme', theme);
  }

  root.classList.add('js');
  apply(saved() === 'light' ? 'light' : 'dark');

  document.addEventListener('DOMContentLoaded', function () {
    var nav = document.querySelector('.nav');
    var toggle = document.querySelector('.nav__theme');
    var burger = document.querySelector('.nav__hamburger');
    var drawer = document.getElementById('nav-drawer');

    function label() {
      var dark = root.getAttribute('data-theme') === 'dark';
      toggle.setAttribute('aria-label', dark ? 'Helles Design aktivieren' : 'Dunkles Design aktivieren');
    }

    if (toggle) {
      label();
      toggle.addEventListener('click', function () {
        var next = root.getAttribute('data-theme') === 'dark' ? 'light' : 'dark';
        try {
          localStorage.setItem(KEY, next);
        } catch (e) {
          /* ohne Speicher gilt die Wahl nur für diese Seite */
        }
        if (document.startViewTransition) {
          document.startViewTransition(function () {
            apply(next);
          });
        } else {
          apply(next);
        }
        label();
      });
    }

    if (nav) {
      var onScroll = function () {
        nav.classList.toggle('nav--scrolled', window.scrollY > 24);
      };
      onScroll();
      window.addEventListener('scroll', onScroll, { passive: true });
    }

    if (burger && drawer) {
      var setOpen = function (open) {
        drawer.hidden = !open;
        nav.classList.toggle('nav--open', open);
        burger.setAttribute('aria-expanded', String(open));
        burger.setAttribute('aria-label', open ? 'Navigation schließen' : 'Navigation öffnen');
      };
      burger.addEventListener('click', function () {
        setOpen(drawer.hidden);
      });
      document.addEventListener('keydown', function (e) {
        if (e.key === 'Escape' && !drawer.hidden) {
          setOpen(false);
          burger.focus();
        }
      });
    }
  });
})();
