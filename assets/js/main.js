/* Site behaviour: mobile nav, reading progress, timeline filters, glossary search. */
(function () {
  "use strict";

  /* ---- mobile navigation ------------------------------------------------ */
  var toggle = document.querySelector(".nav-toggle");
  var links = document.getElementById("nav-links");

  if (toggle && links) {
    toggle.addEventListener("click", function () {
      var open = links.classList.toggle("open");
      toggle.setAttribute("aria-expanded", open ? "true" : "false");
      toggle.textContent = open ? "Close" : "Menu";
    });
    document.addEventListener("keydown", function (e) {
      if (e.key === "Escape" && links.classList.contains("open")) {
        links.classList.remove("open");
        toggle.setAttribute("aria-expanded", "false");
        toggle.textContent = "Menu";
        toggle.focus();
      }
    });
  }

  /* ---- reading progress bar --------------------------------------------- */
  var bar = document.querySelector(".read-progress");
  if (bar) {
    var update = function () {
      var doc = document.documentElement;
      var scrollable = doc.scrollHeight - doc.clientHeight;
      var pct = scrollable > 0 ? (doc.scrollTop / scrollable) * 100 : 0;
      bar.style.width = Math.min(100, Math.max(0, pct)) + "%";
    };
    window.addEventListener("scroll", update, { passive: true });
    window.addEventListener("resize", update);
    update();
  }

  /* ---- timeline era filters --------------------------------------------- */
  var filterBar = document.querySelector("[data-filter-bar]");
  if (filterBar) {
    var items = Array.prototype.slice.call(document.querySelectorAll("[data-era]"));
    var counter = document.querySelector("[data-filter-count]");

    var apply = function (era) {
      var shown = 0;
      items.forEach(function (item) {
        var match = era === "all" || item.getAttribute("data-era") === era;
        item.hidden = !match;
        if (match) { shown++; }
      });
      if (counter) {
        counter.textContent = shown + (shown === 1 ? " moment" : " moments") + " shown";
      }
    };

    filterBar.addEventListener("click", function (e) {
      var btn = e.target.closest(".filter-btn");
      if (!btn) { return; }
      filterBar.querySelectorAll(".filter-btn").forEach(function (b) {
        b.setAttribute("aria-pressed", b === btn ? "true" : "false");
      });
      apply(btn.getAttribute("data-filter"));
    });

    apply("all");
  }

  /* ---- glossary live search --------------------------------------------- */
  var search = document.getElementById("glossary-search");
  if (search) {
    var entries = Array.prototype.slice.call(document.querySelectorAll(".glossary-item"));
    var empty = document.querySelector("[data-empty-state]");
    var count = document.querySelector("[data-glossary-count]");

    search.addEventListener("input", function () {
      var q = search.value.trim().toLowerCase();
      var hits = 0;
      entries.forEach(function (entry) {
        var match = q === "" || entry.textContent.toLowerCase().indexOf(q) !== -1;
        entry.hidden = !match;
        if (match) { hits++; }
      });
      if (empty) { empty.hidden = hits !== 0; }
      if (count) { count.textContent = hits + (hits === 1 ? " term" : " terms"); }
    });
  }
})();
