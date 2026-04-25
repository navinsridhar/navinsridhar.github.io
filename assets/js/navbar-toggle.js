/**
 * Vanilla-JS navbar toggle.
 *
 * The al-folio header uses Bootstrap-4 `data-toggle="collapse"`, which
 * depends on jQuery + bootstrap.bundle.js. If either of those CDN scripts
 * fails to load (CSP, network, integrity-hash drift, slow phone connection),
 * the hamburger button does nothing on mobile. This script provides a
 * dependency-free fallback that works either way: it intercepts clicks
 * on `.navbar-toggler` and toggles the `show` class on the controlled
 * `.collapse` element directly.
 *
 * It is also idempotent with the Bootstrap behaviour — Bootstrap will
 * toggle `show` itself if it is up, and our handler simply syncs the
 * aria-expanded attribute.
 */

(function () {
  function toggleCollapse(targetSelector, button) {
    var target = document.querySelector(targetSelector);
    if (!target) return;
    var isOpen = target.classList.contains("show");
    if (isOpen) {
      target.classList.remove("show");
      button.classList.add("collapsed");
      button.setAttribute("aria-expanded", "false");
    } else {
      target.classList.add("show");
      button.classList.remove("collapsed");
      button.setAttribute("aria-expanded", "true");
    }
  }

  function init() {
    var togglers = document.querySelectorAll(".navbar-toggler[data-target], .navbar-toggler[data-bs-target]");
    Array.prototype.forEach.call(togglers, function (button) {
      // Skip if Bootstrap's own JS is already wired up — but we want our
      // listener to run regardless, since BS-without-jQuery is a no-op.
      var sel = button.getAttribute("data-target") || button.getAttribute("data-bs-target");
      if (!sel) return;
      button.addEventListener("click", function (ev) {
        ev.preventDefault();
        ev.stopPropagation();
        toggleCollapse(sel, button);
      });
    });

    // Close the menu when clicking a nav link (sane mobile UX).
    var nav = document.getElementById("navbarNav");
    if (nav) {
      var links = nav.querySelectorAll("a.nav-link, a.dropdown-item");
      Array.prototype.forEach.call(links, function (a) {
        a.addEventListener("click", function () {
          if (nav.classList.contains("show")) {
            nav.classList.remove("show");
            var btn = document.querySelector(".navbar-toggler");
            if (btn) {
              btn.classList.add("collapsed");
              btn.setAttribute("aria-expanded", "false");
            }
          }
        });
      });
    }
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }
})();
