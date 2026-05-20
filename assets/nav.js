/* Mobile navigation drawer — clones the desktop .nav-primary into a slide-in
   panel and wires up the hamburger button. Runs on every page. */
(function () {
  function init() {
    const hamburger = document.querySelector(".nav-hamburger");
    if (!hamburger) return;

    if (!document.getElementById("nav-mobile")) injectDrawer();

    if (!hamburger.dataset.navWired) {
      hamburger.addEventListener("click", openMenu);
      hamburger.dataset.navWired = "1";
    }
  }

  function injectDrawer() {
    const navPrimary = document.querySelector(".nav-primary");
    const linksHtml = navPrimary
      ? Array.from(navPrimary.querySelectorAll("a"))
          .map(a => `<a href="${a.getAttribute("href")}"${a.classList.contains("is-active") ? ' class="is-active"' : ""}>${a.textContent}</a>`)
          .join("")
      : "";

    const wrap = document.createElement("div");
    wrap.id = "nav-mobile";
    wrap.className = "nav-mobile";
    wrap.innerHTML = `
      <div class="nav-mobile-overlay" data-close></div>
      <aside class="nav-mobile-panel" role="dialog" aria-label="Site menu">
        <header class="nav-mobile-head">
          <span class="nav-mobile-title">Menu</span>
          <button class="nav-mobile-close" data-close aria-label="Close menu" type="button">×</button>
        </header>
        <nav class="nav-mobile-links" aria-label="Mobile primary">${linksHtml}</nav>
        <div class="nav-mobile-foot">
          <a href="contact.html" class="cta-button" style="width:100%;justify-content:center;">Request Quote</a>
          <div class="nav-mobile-contact">
            <a href="tel:+27132431390">013 243 1390</a>
            <a href="mailto:accounts@pegasuseng.co.za">accounts@pegasuseng.co.za</a>
            <span>Mon – Fri · 07h00 – 17h00 · Boksburg</span>
          </div>
        </div>
      </aside>
    `;
    document.body.appendChild(wrap);

    wrap.querySelectorAll("[data-close]").forEach(el => el.addEventListener("click", closeMenu));
    wrap.querySelectorAll(".nav-mobile-links a").forEach(a => a.addEventListener("click", closeMenu));
    document.addEventListener("keydown", e => {
      if (e.key === "Escape" && wrap.classList.contains("is-open")) closeMenu();
    });
  }

  function openMenu() {
    const m = document.getElementById("nav-mobile");
    if (!m) return;
    m.classList.add("is-open");
    document.body.classList.add("nav-locked");
    document.querySelector(".nav-hamburger")?.classList.add("is-active");
  }
  function closeMenu() {
    const m = document.getElementById("nav-mobile");
    if (!m) return;
    m.classList.remove("is-open");
    document.body.classList.remove("nav-locked");
    document.querySelector(".nav-hamburger")?.classList.remove("is-active");
  }

  // Remove the hero video entirely on mobile so the 23MB MP4 never downloads.
  // The poster image (CSS background) takes over for small screens.
  function killHeroVideoOnMobile() {
    if (window.innerWidth > 760) return;
    const v = document.getElementById("heroVideo");
    if (!v) return;
    v.pause();
    v.removeAttribute("autoplay");
    v.removeAttribute("src");
    v.querySelectorAll("source").forEach(s => s.remove());
    v.load();
    v.style.display = "none";
  }

  // Toggle a class on the sticky header once the user scrolls past the top —
  // gives it a subtle drop-shadow so it lifts off the page.
  function initStickyShadow() {
    const header = document.querySelector(".header");
    if (!header) return;
    function update() {
      header.classList.toggle("is-scrolled", window.scrollY > 4);
    }
    update();
    window.addEventListener("scroll", update, { passive: true });
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", () => { init(); initStickyShadow(); killHeroVideoOnMobile(); });
  } else {
    init();
    initStickyShadow();
    killHeroVideoOnMobile();
  }
})();
