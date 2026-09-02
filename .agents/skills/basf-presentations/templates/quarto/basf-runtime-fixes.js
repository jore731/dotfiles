(function () {
  "use strict";

  function setLogoCanvasMode(logo, slides) {
    if (logo.parentElement !== slides) {
      slides.appendChild(logo);
    }

    logo.style.position = "absolute";
    logo.style.left = "auto";
    logo.style.top = "auto";
    logo.style.right = "22px";
    logo.style.bottom = "18px";
    logo.style.zIndex = "20";
  }

  function setLogoViewportMode(logo, reveal) {
    if (logo.parentElement !== reveal) {
      reveal.appendChild(logo);
    }

    logo.style.removeProperty("position");
    logo.style.removeProperty("right");
    logo.style.removeProperty("bottom");
    logo.style.removeProperty("left");
    logo.style.removeProperty("top");
    logo.style.removeProperty("z-index");
  }

  function alignLogoToSlideCanvas() {
    var logo = document.querySelector(".reveal .slide-logo");
    var slides = document.querySelector(".reveal .slides");
    var reveal = document.querySelector(".reveal");
    var currentSlide = document.querySelector(
      ".reveal .slides section.present",
    );

    if (!logo || !slides || !reveal || !currentSlide) return;

    if (
      currentSlide.id === "title-slide" ||
      currentSlide.classList.contains("closing-slide")
    ) {
      setLogoViewportMode(logo, reveal);
      return;
    }

    setLogoCanvasMode(logo, slides);
  }

  function fitHighlightSlideTables() {
    var panels = document.querySelectorAll(
      ".reveal .slides section.highlight-slide .split-left",
    );

    panels.forEach(function (panel) {
      var table = panel.querySelector("table");
      if (!table) return;

      if (!table.dataset.basfBaseFontSize) {
        table.dataset.basfBaseFontSize = getComputedStyle(table).fontSize;
      }

      var baseSize = parseFloat(table.dataset.basfBaseFontSize);
      var nextSize = baseSize;
      var minSize = 18;

      table.style.fontSize = baseSize + "px";

      while (panel.scrollHeight > panel.clientHeight && nextSize > minSize) {
        nextSize -= 1;
        table.style.fontSize = nextSize + "px";
      }
    });
  }

  // ── Auto font scaler — fits every content slide to the canvas ──────────
  //
  // Temporarily lifts Reveal.js's `height: 100% !important` and
  // `overflow: hidden !important` (via setProperty) so scrollHeight reflects
  // the true content height.  If the content overflows the canvas, font-size
  // is reduced proportionally.  Two passes for accuracy.
  //
  // The operation is synchronous within a single browser frame — no flicker.

  var SKIP_SCALE_CLASSES = ["closing-slide", "divider-slide"];
  var MIN_FONT_PX = 18; // absolute readability floor
  var TOLERANCE_PX = 8; // headroom before scaling kicks in

  function isScalableSlide(slide) {
    if (!slide) return false;
    if (slide.id === "title-slide") return false;
    return !SKIP_SCALE_CLASSES.some(function (cls) {
      return slide.classList.contains(cls);
    });
  }

  function measureTrueContentHeight(slide) {
    slide.style.setProperty("overflow", "visible", "important");
    slide.style.setProperty("height", "auto", "important");
    slide.style.setProperty("max-height", "none", "important");
    var h = slide.scrollHeight;
    slide.style.removeProperty("overflow");
    slide.style.removeProperty("height");
    slide.style.removeProperty("max-height");
    return h;
  }

  function fitCurrentSlideFont() {
    var slide = document.querySelector(".reveal .slides section.present");
    if (!isScalableSlide(slide)) return;

    var canvasH = slide.clientHeight;
    if (canvasH < 10) return;

    // Store original font-size on first visit
    if (!slide.dataset.basfOrigFontPx) {
      slide.style.removeProperty("font-size");
      slide.dataset.basfOrigFontPx = window.getComputedStyle(slide).fontSize;
    }

    // Reset to original before each measurement
    var origPx = parseFloat(slide.dataset.basfOrigFontPx);
    slide.style.fontSize = origPx + "px";

    var contentH = measureTrueContentHeight(slide);

    if (contentH <= canvasH + TOLERANCE_PX) {
      updateDevBadge(slide, origPx, origPx);
      return;
    }

    // First pass: proportional reduction
    var ratio = (canvasH - TOLERANCE_PX) / contentH;
    var newPx = Math.max(Math.floor(origPx * ratio), MIN_FONT_PX);
    slide.style.fontSize = newPx + "px";

    // Second pass: verify (font-size change affects layout)
    var afterH = measureTrueContentHeight(slide);
    if (afterH > canvasH + TOLERANCE_PX) {
      var ratio2 = (canvasH - TOLERANCE_PX) / afterH;
      var finalPx = Math.max(Math.floor(newPx * ratio2), MIN_FONT_PX);
      slide.style.fontSize = finalPx + "px";
      newPx = finalPx;
    }

    updateDevBadge(slide, origPx, newPx);
  }

  // ── Developer overlay — append ?dev=1 to the URL to enable ─────────────
  //
  // Shows a small badge on every scaled slide with the scaling percentage
  // and resulting font size.  Green ≥ 80 %, yellow 60–79 %, red < 60 %.
  // Slides at 100 % get a faint green badge for confirmation.
  //
  // Example: open presentation.html?dev=1 during authoring.
  //          open presentation.html         for a clean presentation.

  var DEV_MODE = new URLSearchParams(window.location.search).get("dev") === "1";

  function updateDevBadge(slide, origPx, finalPx) {
    if (!DEV_MODE) return;

    var badge = slide.querySelector(".basf-dev-badge");
    if (!badge) {
      badge = document.createElement("div");
      badge.className = "basf-dev-badge";
      badge.style.cssText = [
        "position:absolute",
        "top:10px",
        "right:10px",
        "padding:3px 9px",
        "border-radius:3px",
        "font-size:13px",
        "font-family:monospace",
        "font-weight:700",
        "z-index:100",
        "pointer-events:none",
        "line-height:1.6",
      ].join(";");
      // The slide section is already position:relative via Reveal.js
      slide.appendChild(badge);
    }

    var pct = Math.round((finalPx / origPx) * 100);

    if (pct >= 100) {
      badge.textContent = "✓ 100%";
      badge.style.background = "rgba(0,122,51,0.4)";
      badge.style.color = "#fff";
    } else {
      badge.textContent = "⚠ " + pct + "% | " + Math.round(finalPx) + "px";
      if (pct >= 80) {
        badge.style.background = "rgba(0,122,51,0.85)";
      } else if (pct >= 60) {
        badge.style.background = "rgba(243,112,33,0.9)";
      } else {
        badge.style.background = "rgba(228,0,43,0.9)";
      }
      badge.style.color = "#fff";
    }
  }

  function applyRuntimeFixes() {
    // Order: scale first so table-fitter measures against the scaled layout.
    fitCurrentSlideFont();
    fitHighlightSlideTables();
    alignLogoToSlideCanvas();
  }

  function watchRevealChrome() {
    var attempts = 0;

    function retryApply() {
      applyRuntimeFixes();
      attempts += 1;

      if (attempts < 12) {
        window.setTimeout(retryApply, 120 * attempts);
      }
    }

    var observer = new MutationObserver(function () {
      window.requestAnimationFrame(applyRuntimeFixes);
    });

    observer.observe(document.body, {
      childList: true,
      subtree: true,
      attributes: true,
      attributeFilter: ["class", "style"],
    });

    window.addEventListener("load", applyRuntimeFixes);
    retryApply();
  }

  function bindRevealLifecycle() {
    if (window.Reveal && typeof window.Reveal.on === "function") {
      window.Reveal.on("ready", applyRuntimeFixes);
      window.Reveal.on("slidechanged", applyRuntimeFixes);
      window.Reveal.on("resize", applyRuntimeFixes);
    }

    window.addEventListener("resize", applyRuntimeFixes);
    window.requestAnimationFrame(applyRuntimeFixes);
    window.setTimeout(applyRuntimeFixes, 150);
    watchRevealChrome();
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", bindRevealLifecycle);
  } else {
    bindRevealLifecycle();
  }
})();
