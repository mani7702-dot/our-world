/* Our World — shared behaviour (kept tiny on purpose) */
(function () {
  "use strict";

  // Mobile navigation
  var toggle = document.querySelector(".nav-toggle");
  var nav = document.querySelector("#site-nav");
  if (toggle && nav) {
    toggle.addEventListener("click", function () {
      var open = nav.classList.toggle("open");
      toggle.setAttribute("aria-expanded", open ? "true" : "false");
    });
    document.addEventListener("keydown", function (e) {
      if (e.key === "Escape" && nav.classList.contains("open")) {
        nav.classList.remove("open");
        toggle.setAttribute("aria-expanded", "false");
        toggle.focus();
      }
    });
    document.addEventListener("click", function (e) {
      if (!nav.contains(e.target) && !toggle.contains(e.target)) {
        nav.classList.remove("open");
        toggle.setAttribute("aria-expanded", "false");
      }
    });
  }

  // Footer year
  var year = document.querySelector("#year");
  if (year) year.textContent = String(new Date().getFullYear());

  // Theme toggle (dark mode)
  var themeBtn = document.getElementById("theme-toggle");
  function applyTheme(mode) {
    document.documentElement.dataset.theme = mode;
    if (themeBtn) {
      themeBtn.setAttribute("aria-pressed", mode === "dark" ? "true" : "false");
      themeBtn.setAttribute("aria-label", mode === "dark" ? "Switch to light mode" : "Switch to dark mode");
    }
    try { window.localStorage.setItem("ow-theme", mode); } catch (e) { /* private mode */ }
  }
  if (themeBtn) {
    themeBtn.addEventListener("click", function () {
      applyTheme(document.documentElement.dataset.theme === "dark" ? "light" : "dark");
    });
    applyTheme(document.documentElement.dataset.theme || "light");
  }
})();
