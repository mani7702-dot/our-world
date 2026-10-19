/* Our World — motion layer (premium feel, motion as discipline)
   Every effect below is skipped when prefers-reduced-motion is set. */
(function () {
  "use strict";

  var reduceMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  var finePointer = window.matchMedia("(pointer: fine)").matches;

  var progressBar = document.getElementById("progress-bar");
  var backToTop = document.getElementById("back-to-top");
  var heroTexture = document.querySelector(".hero-texture");

  /* ---- scroll: progress bar, back-to-top, hero parallax ---- */
  var ticking = false;
  function onScroll() {
    if (ticking) return;
    ticking = true;
    window.requestAnimationFrame(function () {
      var y = window.scrollY || window.pageYOffset || 0;
      var max = document.documentElement.scrollHeight - window.innerHeight;
      if (progressBar) {
        progressBar.style.width = (max > 0 ? (y / max) * 100 : 0) + "%";
      }
      if (backToTop) {
        backToTop.classList.toggle("show", y > 600);
      }
      if (heroTexture && !reduceMotion && y < 1600) {
        heroTexture.style.transform = "translateY(" + (y * 0.12).toFixed(1) + "px)";
      }
      ticking = false;
    });
  }
  window.addEventListener("scroll", onScroll, { passive: true });
  onScroll();

  if (backToTop) {
    backToTop.addEventListener("click", function () {
      window.scrollTo({ top: 0, behavior: reduceMotion ? "auto" : "smooth" });
    });
  }

  /* ---- scroll reveal with per-group stagger ---- */
  var revealEls = Array.prototype.slice.call(document.querySelectorAll("[data-reveal]"));
  if (reduceMotion || !("IntersectionObserver" in window)) {
    revealEls.forEach(function (el) { el.classList.add("in"); });
  } else {
    var groups = new Map();
    revealEls.forEach(function (el) {
      var key = el.parentElement;
      if (!groups.has(key)) groups.set(key, []);
      groups.get(key).push(el);
    });
    groups.forEach(function (els) {
      els.forEach(function (el, i) {
        el.style.transitionDelay = Math.min(i, 5) * 80 + "ms";
      });
    });
    var io = new IntersectionObserver(
      function (entries) {
        entries.forEach(function (entry) {
          if (entry.isIntersecting) {
            entry.target.classList.add("in");
            io.unobserve(entry.target);
          }
        });
      },
      { threshold: 0.12, rootMargin: "0px 0px -40px 0px" }
    );
    revealEls.forEach(function (el) { io.observe(el); });
  }

  /* ---- gentle pointer tilt on game cards (desktop only) ---- */
  if (finePointer && !reduceMotion) {
    Array.prototype.forEach.call(document.querySelectorAll(".game-card"), function (card) {
      card.addEventListener("pointermove", function (e) {
        var r = card.getBoundingClientRect();
        var px = (e.clientX - r.left) / r.width - 0.5;
        var py = (e.clientY - r.top) / r.height - 0.5;
        card.style.setProperty("--ry", (px * 5).toFixed(2) + "deg");
        card.style.setProperty("--rx", (-py * 5).toFixed(2) + "deg");
      });
      card.addEventListener("pointerleave", function () {
        card.style.setProperty("--rx", "0deg");
        card.style.setProperty("--ry", "0deg");
      });
    });
  }
})();
