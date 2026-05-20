/* Pegasus cart — persisted in localStorage, drawer UI, global `window.cart` API.
   Loaded on every page so the cart icon + drawer are available site-wide. */
(function () {
  const STORAGE_KEY = "pegasusCart_v1";

  // ── State ────────────────────────────────────────────────────────────────
  let cart = loadCart();

  function loadCart() {
    try { return JSON.parse(localStorage.getItem(STORAGE_KEY)) || []; }
    catch { return []; }
  }
  function saveCart() {
    localStorage.setItem(STORAGE_KEY, JSON.stringify(cart));
  }
  function totalQty() {
    return cart.reduce((s, i) => s + (i.qty || 0), 0);
  }
  function productSubtotal() {
    return cart
      .filter(i => i.type === "product" && i.price)
      .reduce((s, i) => s + i.price * i.qty, 0);
  }
  function hasServices() {
    return cart.some(i => i.type === "service");
  }
  function hasProducts() {
    return cart.some(i => i.type === "product");
  }
  function fmtZAR(n) {
    return "R " + Math.round(n).toLocaleString("en-ZA");
  }
  function escapeHtml(s) {
    return String(s).replace(/[&<>"']/g, c => ({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"}[c]));
  }

  // ── DOM injection ────────────────────────────────────────────────────────
  function injectUI() {
    // Cart icon — use pre-rendered button if present (no FOUC), else inject
    let btn = document.querySelector(".cart-icon-btn");
    if (!btn) {
      const navIcons = document.querySelector(".nav-icons");
      if (navIcons) {
        btn = document.createElement("button");
        btn.className = "cart-icon-btn";
        btn.setAttribute("aria-label", "Open cart");
        btn.type = "button";
        btn.innerHTML = `
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">
            <path d="M6 6h15l-2 10H8L6 6Z"/>
            <path d="M6 6L4 2H2"/>
            <circle cx="10" cy="20" r="1.4" fill="currentColor"/>
            <circle cx="18" cy="20" r="1.4" fill="currentColor"/>
          </svg>
          <span class="cart-icon-count" aria-live="polite"></span>
        `;
        navIcons.appendChild(btn);
      }
    }
    if (btn && !btn.dataset.cartWired) {
      btn.addEventListener("click", openDrawer);
      btn.dataset.cartWired = "1";
    }

    // Drawer + overlay
    if (!document.getElementById("cart-drawer")) {
      const wrap = document.createElement("div");
      wrap.id = "cart-drawer";
      wrap.className = "cart-drawer";
      wrap.innerHTML = `
        <div class="cart-drawer-overlay" id="cart-overlay"></div>
        <aside class="cart-drawer-panel" role="dialog" aria-label="Your cart">
          <header class="cart-drawer-head">
            <h3 class="cart-drawer-title">Your Cart</h3>
            <button class="cart-drawer-close" id="cart-close" aria-label="Close cart" type="button">×</button>
          </header>
          <div class="cart-drawer-body" id="cart-drawer-body"></div>
          <footer class="cart-drawer-foot" id="cart-drawer-foot"></footer>
        </aside>
      `;
      document.body.appendChild(wrap);
      document.getElementById("cart-close").addEventListener("click", closeDrawer);
      document.getElementById("cart-overlay").addEventListener("click", closeDrawer);
      document.addEventListener("keydown", e => {
        if (e.key === "Escape" && wrap.classList.contains("is-open")) closeDrawer();
      });
    }

    refreshUI();
  }

  function refreshUI() {
    const count = totalQty();
    document.querySelectorAll(".cart-icon-count").forEach(el => {
      el.textContent = count > 0 ? count : "";
      el.classList.toggle("is-visible", count > 0);
    });
    renderDrawer();
  }

  function renderDrawer() {
    const body = document.getElementById("cart-drawer-body");
    const foot = document.getElementById("cart-drawer-foot");
    if (!body || !foot) return;

    if (cart.length === 0) {
      body.innerHTML = `
        <div class="cart-empty">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.4" aria-hidden="true">
            <path d="M6 6h15l-2 10H8L6 6Z"/><path d="M6 6L4 2H2"/>
          </svg>
          <p>Your cart is empty.</p>
          <p class="cart-empty-sub">Browse the catalogue to add products or services.</p>
        </div>`;
      foot.innerHTML = `<a href="products.html" class="cta-button" style="width:100%;justify-content:center;">Browse the Catalogue</a>`;
      return;
    }

    body.innerHTML = cart.map((item, idx) => {
      const isService = item.type === "service";
      const priceHtml = isService
        ? `<span class="cart-row-quote">Quote required</span>`
        : `<span class="cart-row-price">${fmtZAR(item.price)} <small>/ ${escapeHtml(item.unit || "ea")}</small></span>`;
      const lineTotal = isService ? "" :
        `<span class="cart-row-linetotal">${fmtZAR(item.price * item.qty)}</span>`;
      return `<div class="cart-row" data-idx="${idx}">
        <a class="cart-row-img" href="${item.href}"><img src="${escapeHtml(item.image)}" alt=""></a>
        <div class="cart-row-info">
          <span class="cart-row-meta">${escapeHtml(item.brand)} · ${escapeHtml(item.categoryLabel)}</span>
          <a class="cart-row-title" href="${item.href}">${escapeHtml(item.title)}</a>
          ${priceHtml}
        </div>
        <div class="cart-row-controls">
          <div class="qty-stepper qty-stepper--sm">
            <button data-act="dec" aria-label="Decrease" type="button">−</button>
            <input type="number" value="${item.qty}" min="1" data-act="set" aria-label="Quantity">
            <button data-act="inc" aria-label="Increase" type="button">+</button>
          </div>
          ${lineTotal}
          <button class="cart-row-remove" data-act="remove" type="button" aria-label="Remove">Remove</button>
        </div>
      </div>`;
    }).join("");

    const subtotal = productSubtotal();
    const vat = subtotal * 0.15;
    const grand = subtotal + vat;
    const hasSvc = hasServices();
    const hasProd = hasProducts();

    let totalsHtml = "";
    if (subtotal > 0) {
      totalsHtml += `
        <div class="cart-totals">
          <div class="cart-total-row"><span>Subtotal</span><span>${fmtZAR(subtotal)}</span></div>
          <div class="cart-total-row"><span>VAT (15%)</span><span>${fmtZAR(vat)}</span></div>
          <div class="cart-total-row cart-total-row--grand"><strong>Total</strong><strong>${fmtZAR(grand)}</strong></div>
          <div class="cart-total-foot">Delivery quoted at checkout.</div>
        </div>`;
    }
    if (hasSvc) {
      totalsHtml += `<p class="cart-quote-note">Services require a written quote — final pricing confirmed after technical scoping.</p>`;
    }
    const btnLabel = hasSvc && hasProd ? "Submit Order &amp; Quote"
                    : hasProd ? "Proceed to Checkout"
                    : "Submit Quote Request";

    foot.innerHTML = `${totalsHtml}<a href="checkout.html" class="cta-button" style="width:100%;justify-content:center;margin-top:16px;">${btnLabel}</a>`;

    // Wire row controls
    body.querySelectorAll(".cart-row").forEach(row => {
      const idx = parseInt(row.dataset.idx);
      row.querySelector('[data-act="dec"]').onclick = () => updateQty(idx, cart[idx].qty - 1);
      row.querySelector('[data-act="inc"]').onclick = () => updateQty(idx, cart[idx].qty + 1);
      row.querySelector('[data-act="set"]').addEventListener("change", e =>
        updateQty(idx, parseInt(e.target.value) || 1));
      row.querySelector('[data-act="remove"]').onclick = () => remove(idx);
    });
  }

  function openDrawer() {
    document.getElementById("cart-drawer").classList.add("is-open");
    document.body.classList.add("cart-locked");
  }
  function closeDrawer() {
    document.getElementById("cart-drawer").classList.remove("is-open");
    document.body.classList.remove("cart-locked");
  }

  // ── Public API ───────────────────────────────────────────────────────────
  function add(item, qty) {
    qty = Math.max(1, parseInt(qty) || 1);
    const i = cart.findIndex(c => c.id === item.id);
    if (i >= 0) {
      cart[i].qty += qty;
    } else {
      cart.push({
        id: item.id, type: item.type, brand: item.brand,
        brandSlug: item.brandSlug, title: item.title,
        categoryLabel: item.categoryLabel, image: item.image,
        href: item.href, price: item.price, unit: item.unit,
        qty,
      });
    }
    saveCart();
    refreshUI();
    openDrawer();
    flashIcon();
  }
  function updateQty(idx, qty) {
    qty = parseInt(qty) || 1;
    if (qty < 1) qty = 1;
    if (cart[idx]) {
      cart[idx].qty = qty;
      saveCart();
      refreshUI();
    }
  }
  function remove(idx) {
    cart.splice(idx, 1);
    saveCart();
    refreshUI();
  }
  function clear() {
    cart = [];
    saveCart();
    refreshUI();
  }
  function flashIcon() {
    const el = document.querySelector(".cart-icon-btn");
    if (!el) return;
    el.classList.remove("is-pulse");
    void el.offsetWidth;
    el.classList.add("is-pulse");
  }

  window.cart = {
    add, remove, updateQty, clear,
    open: openDrawer, close: closeDrawer,
    getCart: () => cart.slice(),
    getProductSubtotal: productSubtotal,
    hasServices, hasProducts,
    fmtZAR,
  };

  // ── Boot ─────────────────────────────────────────────────────────────────
  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", injectUI);
  } else {
    injectUI();
  }
})();
