/* Our World — client-side search.
 *
 * Reads search-index.json (written by build.py at the site root) and filters it
 * as the user types. No external requests of any kind: the only network call is
 * the fetch of our own JSON file. All DOM is built with createElement and
 * textContent — never innerHTML — so index text can never inject markup.
 */
(function () {
  "use strict";

  var input = document.getElementById("q");
  var results = document.getElementById("results");
  if (!input || !results) return;

  var HINT = "Type a word — titles, topics and tags.";
  var EMPTY = "No matches — try another word";
  var ERROR = "Search is not available right now — please try again later.";

  var index = null;   // loaded entries, null until the fetch settles
  var broken = false; // fetch failed

  function clear(node) {
    while (node.firstChild) node.removeChild(node.firstChild);
  }

  /* A plain text line inside the live region. */
  function line(text, className) {
    var p = document.createElement("p");
    p.className = className;
    p.textContent = text;
    return p;
  }

  /* Weighted containment scoring: a title hit beats a tag hit beats an excerpt hit. */
  function score(item, q) {
    var title = String(item.title || "").toLowerCase();
    var tags = (item.tags || []).join(" ").toLowerCase();
    var excerpt = String(item.excerpt || "").toLowerCase();
    var s = 0;
    if (title.indexOf(q) !== -1) s += 100;
    if (tags.indexOf(q) !== -1) s += 40;
    if (excerpt.indexOf(q) !== -1) s += 10;
    return s;
  }

  function rowLink(item) {
    var a = document.createElement("a");
    a.className = "search-result-title";
    // Index urls are root-relative; this page lives at /search/, so go up one level.
    a.href = "../" + item.url;
    a.textContent = item.title;
    return a;
  }

  function render(list, q) {
    clear(results);
    if (!list.length) {
      results.appendChild(line(EMPTY, "search-empty"));
      return;
    }
    results.appendChild(line(list.length + (list.length === 1 ? " result" : " results") + " for “" + q + "”", "search-count"));
    var ul = document.createElement("ul");
    ul.className = "search-results-list";
    for (var i = 0; i < list.length; i++) {
      var item = list[i];
      var li = document.createElement("li");
      li.className = "search-result";

      var head = document.createElement("div");
      head.className = "search-result-head";
      head.appendChild(rowLink(item));
      var section = document.createElement("span");
      section.className = "search-result-section search-result-section--" + item.section;
      section.textContent = item.section === "news" ? "News" : "Blog";
      head.appendChild(section);
      li.appendChild(head);

      var p = document.createElement("p");
      p.className = "search-result-excerpt";
      p.textContent = item.excerpt || "";
      li.appendChild(p);

      if (item.tags && item.tags.length) {
        var tags = document.createElement("p");
        tags.className = "search-result-tags";
        tags.textContent = "Tags: " + item.tags.join(", ");
        li.appendChild(tags);
      }

      ul.appendChild(li);
    }
    results.appendChild(ul);
  }

  function update() {
    if (broken) {
      clear(results);
      results.appendChild(line(ERROR, "search-error"));
      return;
    }
    if (!index) return; // still loading — the static hint stays put
    var q = input.value.trim().toLowerCase();
    if (!q) {
      clear(results);
      results.appendChild(line(HINT, "search-hint"));
      return;
    }
    var hits = [];
    for (var i = 0; i < index.length; i++) {
      var s = score(index[i], q);
      if (s > 0) hits.push({ item: index[i], s: s, i: i });
    }
    hits.sort(function (a, b) {
      return b.s - a.s || a.i - b.i;
    });
    var list = [];
    for (var j = 0; j < hits.length; j++) list.push(hits[j].item);
    render(list, q);
  }

  input.addEventListener("input", update);

  // The only request this page ever makes: our own generated JSON.
  fetch("../search-index.json")
    .then(function (res) {
      if (!res.ok) throw new Error("HTTP " + res.status);
      return res.json();
    })
    .then(function (data) {
      index = Array.isArray(data) ? data : [];
      update();
    })
    .catch(function () {
      broken = true;
      clear(results);
      results.appendChild(line(ERROR, "search-error"));
    });
})();
