/**
 * BASF Theme Switcher for Reveal.js / Quarto presentations.
 * Adds a color swatch bar at the bottom of the slide deck.
 * Pressing a swatch instantly changes the brand color scheme
 * via CSS custom properties (no page reload required).
 *
 * Usage in Quarto YAML:
 *   include-after-body:
 *     - basf-theme-switcher.html
 *
 * Where basf-theme-switcher.html contains:
 *   <script src="basf-theme-switcher.js"></script>
 */
(function () {
  "use strict";

  var themes = [
    { name: "darkblue", color: "#004A96", label: "Dark Blue" },
    { name: "lightblue", color: "#21A0D2", label: "Light Blue" },
    { name: "darkgreen", color: "#007A33", label: "Dark Green" },
    { name: "orange", color: "#F37021", label: "Orange" },
    { name: "red", color: "#E4002B", label: "Red" },
    { name: "softblack", color: "#212427", label: "Soft Black" },
  ];

  function init() {
    var reveal = document.querySelector(".reveal");
    if (!reveal) return;

    var bar = document.createElement("div");
    bar.className = "basf-theme-switcher";
    bar.setAttribute("aria-label", "Theme color switcher");

    themes.forEach(function (theme) {
      var swatch = document.createElement("button");
      swatch.className = "basf-theme-swatch";
      swatch.style.backgroundColor = theme.color;
      swatch.setAttribute("data-theme", theme.name);
      swatch.setAttribute("aria-label", theme.label);
      swatch.setAttribute("title", theme.label);
      if (theme.name === "darkblue") swatch.classList.add("active");

      swatch.addEventListener("click", function () {
        reveal.setAttribute("data-theme", theme.name);

        bar.querySelectorAll(".basf-theme-swatch").forEach(function (s) {
          s.classList.remove("active");
        });
        swatch.classList.add("active");
      });

      bar.appendChild(swatch);
    });

    document.body.appendChild(bar);
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }
})();
