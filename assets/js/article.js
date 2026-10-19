/* Our World — reading comfort controls (article pages only).
   Text size + easy-read mode, remembered in localStorage per device. */
(function () {
  "use strict";

  var prose = document.getElementById("article-body");
  if (!prose) return;

  var smaller = document.getElementById("text-smaller");
  var larger = document.getElementById("text-larger");
  var easyRead = document.getElementById("dyslexia-toggle");

  var SIZES = ["prose-sm", "prose-md", "prose-lg"];
  var current = "prose-md";
  var easy = false;

  function readStore(key) {
    try { return window.localStorage.getItem(key); } catch (e) { return null; }
  }
  function writeStore(key, value) {
    try { window.localStorage.setItem(key, value); } catch (e) { /* private mode — fine */ }
  }

  function applySize() {
    SIZES.forEach(function (c) { prose.classList.remove(c); });
    prose.classList.add(current);
    writeStore("ow-reading-size", current);
  }
  function applyEasy() {
    prose.classList.toggle("dyslexia", easy);
    if (easyRead) easyRead.setAttribute("aria-pressed", easy ? "true" : "false");
    writeStore("ow-dyslexia", easy ? "1" : "0");
  }

  var savedSize = readStore("ow-reading-size");
  if (savedSize && SIZES.indexOf(savedSize) !== -1) current = savedSize;
  easy = readStore("ow-dyslexia") === "1";
  applySize();
  applyEasy();

  if (smaller) {
    smaller.addEventListener("click", function () {
      current = SIZES[Math.max(0, SIZES.indexOf(current) - 1)];
      applySize();
    });
  }
  if (larger) {
    larger.addEventListener("click", function () {
      current = SIZES[Math.min(SIZES.length - 1, SIZES.indexOf(current) + 1)];
      applySize();
    });
  }
  if (easyRead) {
    easyRead.addEventListener("click", function () {
      easy = !easy;
      applyEasy();
    });
  }
})();
