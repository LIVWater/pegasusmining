"""
Build products.html + marketplace.html as a unified shop database.

Both pages share:
  - Filterable product/service database (Type pills + Category pills + search)
  - Catalogue carousel with category filter
  - "Browse by Division" grid at end

They differ only in hero + page framing.

Re-running is safe; both files are overwritten.
"""
import json
import hashlib
import re
from pathlib import Path


def gen_price(brand_slug: str, title: str, category: str) -> int:
    """Deterministic ZAR price per item based on category + title keywords."""
    seed = int(hashlib.md5(f"{brand_slug}|{title}".encode()).hexdigest()[:6], 16)
    t = title.lower()
    high  = ["equipment", "generator", "inverter", "welder", "toolkit", "specialist", "machine", "press", "rotary hammer", "demolition", "drill press"]
    midhi = ["plant", "sets", "platform", "system", "vice", "combo", "kit", "drill", "saw", "polisher"]
    low   = ["wheel", "disc", "glove", "spectacle", "file", "plug", "blade", "tape", "earplug", "burr", "tip", "nozzle", "filler"]
    cat_default = {
        "welding": (400, 5000), "abrasive": (100, 1500), "power-tools": (2000, 25000),
        "safety": (200, 3000), "hand-tools": (400, 8000), "electrical": (800, 12000),
        "paint": (450, 5500), "lubricants": (350, 7500),
    }

    if any(k in t for k in high):
        lo, hi = 5000, 75000
    elif any(k in t for k in midhi):
        lo, hi = 1500, 15000
    elif any(k in t for k in low):
        lo, hi = 30, 700
    else:
        lo, hi = cat_default.get(category, (300, 3500))

    price = lo + (seed % max(1, hi - lo))
    # Round to a nice number
    if price < 100:   return int(round(price / 5)) * 5
    if price < 1000:  return int(round(price / 10)) * 10
    if price < 10000: return int(round(price / 50)) * 50
    return int(round(price / 500)) * 500


def item_id(typ: str, brand_slug: str, title: str) -> str:
    """Stable, URL-safe id for cart matching."""
    slug = re.sub(r"[^a-z0-9]+", "-", title.lower()).strip("-")
    return f"{typ}-{brand_slug}-{slug}"[:80]

# Reuse the brand data + cat covers from the partner generator
import generate_partners as gp

OUT_DIR = Path(__file__).parent


# ── Engineering services (6 — from homepage Capability tiles) ────────────────
SERVICES = [
    {
        "num": "01",
        "slug": "fabrication",
        "title": "Bespoke Fabrication",
        "category": "Fabrication",
        "image": "welding-worker.jpg",
        "description": "Conveyor idlers, wear liners and structural sub-assemblies — cut, welded and finished to your drawing.",
    },
    {
        "num": "02",
        "slug": "shutdown",
        "title": "On-Site Shutdown Support",
        "category": "Shutdown",
        "image": "welding-blue.jpg",
        "description": "Crews that mobilise around your maintenance window — staging stock and managing OEM paperwork.",
    },
    {
        "num": "03",
        "slug": "refurb",
        "title": "Component Refurbishment",
        "category": "Refurbishment",
        "image": "powertools-workshop.jpg",
        "description": "Strip, inspect and recondition pumps, gearboxes and hydraulic cylinders — bench-tested before despatch.",
    },
    {
        "num": "04",
        "slug": "expediting",
        "title": "Expediting & Sourcing",
        "category": "Expediting",
        "image": "lubricants-truck-field.jpg",
        "description": "Obsolete OEM components, low-volume specials and imports against critical-path dates — found and delivered.",
    },
    {
        "num": "05",
        "slug": "consultation",
        "title": "Technical Consultation",
        "category": "Consultation",
        "image": "handtools-sockets.jpg",
        "description": "Cross-references, duty selection and substitution validation — engineering judgement on the desk.",
    },
    {
        "num": "06",
        "slug": "inventory",
        "title": "Managed Inventory",
        "category": "Managed Inventory",
        "image": "abrasive-bench.jpg",
        "description": "Consignment stock at agreed min/max levels, billed only when consumed — for Tier-1 standing accounts.",
    },
]


def build_items():
    """Build the unified product+service item list with pricing."""
    items = []
    # 38 brands × 6 range items = 228 product entries (priced)
    for brand in gp.BRANDS:
        cat_key = brand["cat"]
        cat_label = gp.CATEGORIES[cat_key]
        covers = gp.CAT_COVERS[cat_key]
        for i, (title, desc) in enumerate(brand["range"]):
            items.append({
                "id": item_id("p", brand["slug"], title),
                "type": "product",
                "category": cat_key,
                "categoryLabel": cat_label,
                "brand": brand["name"],
                "brandSlug": brand["slug"],
                "title": title,
                "description": desc,
                "image": f"assets/brand/{covers[i % len(covers)]}",
                "href": f"partner-{brand['slug']}.html",
                "price": gen_price(brand["slug"], title, cat_key),
                "unit": "ea",
            })
    # 6 services (quote-only, no price)
    for s in SERVICES:
        items.append({
            "id": item_id("s", "pegasus", s["slug"]),
            "type": "service",
            "category": s["slug"],
            "categoryLabel": s["category"],
            "brand": "Pegasus Engineering Services",
            "brandSlug": "pegasus",
            "title": s["title"],
            "description": s["description"],
            "image": f"assets/brand/{s['image']}",
            "href": f"services.html#{s['slug']}",
            "price": None,
            "unit": None,
        })
    return items


def build_catalogues():
    """Catalogue entries — every brand with a real PDF."""
    out = []
    for brand in gp.BRANDS:
        slug = brand["slug"]
        info = gp.CATALOGUE_PDFS.get(slug)
        if not info:
            continue
        pdf, pages = info
        cover = gp.CAT_COVERS[brand["cat"]][0]
        out.append({
            "brand": brand["name"],
            "brandSlug": slug,
            "category": brand["cat"],
            "categoryLabel": gp.CATEGORIES[brand["cat"]],
            "pdf": f"assets/catalogues/{pdf}",
            "pages": pages,
            "cover": f"assets/brand/{cover}",
        })
    # sort by category, then brand
    cat_order = list(gp.CATEGORIES.keys())
    out.sort(key=lambda x: (cat_order.index(x["category"]), x["brand"]))
    return out


PRODUCT_CATEGORIES = [
    ("welding",     "Welding & Cutting"),
    ("abrasive",    "Abrasive"),
    ("power-tools", "Power Tools"),
    ("safety",      "Safety & PPE"),
    ("hand-tools",  "Hand Tools"),
    ("electrical",  "Electrical"),
    ("paint",       "Paint Products"),
    ("lubricants",  "Lubricants & Fuel"),
]

SERVICE_CATEGORIES = [(s["slug"], s["category"]) for s in SERVICES]


def render_category_pills(cats, prefix):
    out = []
    for slug, label in cats:
        out.append(
            f'<button class="shop-pill" data-{prefix}="{slug}" type="button">'
            f'{label}</button>'
        )
    return "\n          ".join(out)


def render_division_grid():
    """Reuse the homepage division-card markup."""
    divisions = [
        ("welding",     "01", "Welding & Cutting",  "welding-portrait.jpg",    "product-welding.html"),
        ("abrasive",    "02", "Abrasive",            "abrasive-sparks.jpg",     "product-abrasive.html"),
        ("power-tools", "03", "Power Tools",         "powertools-drill.jpg",    "product-power-tools.html"),
        ("safety",      "04", "Safety & PPE",        "safety-face.jpg",         "product-safety.html"),
        ("hand-tools",  "05", "Hand Tools",          "handtools-pegboard.jpg",  "product-hand-tools.html"),
        ("electrical",  "06", "Electrical",          "electrical-low.jpg",      "product-electrical.html"),
        ("paint",       "07", "Paint Products",      "paint-roller.jpg",        "product-paint.html"),
        ("lubricants",  "08", "Lubricants & Fuel",   "lubricants-station.jpg",  "product-lubricants.html"),
    ]
    cards = []
    for _, num, label, img, href in divisions:
        label_html = label.replace("&", "&amp;")
        cards.append(f'''        <a class="division-card" href="{href}">
          <div class="division-card-media"><img src="assets/brand/{img}" alt="{label_html}"></div>
          <div class="division-card-overlay"></div>
          <div class="division-card-body">
            <span class="division-card-index">{num}</span>
            <h3 class="division-card-title">{label_html}</h3>
            <span class="division-card-cta">Shop
              <svg viewBox="0 0 24 24" aria-hidden="true"><path d="M5 12h14M13 6l6 6-6 6"/></svg>
            </span>
          </div>
        </a>''')
    return "\n".join(cards)


# ── Page templates ──────────────────────────────────────────────────────────

def head_block(title, description):
    return f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title}</title>
<meta name="description" content="{description}">
<link rel="icon" href="assets/brand/logo-emblem-transparent.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Raleway:ital,wght@0,300;0,400;0,500;0,700;1,300;1,400&family=Roboto+Condensed:ital,wght@0,300;0,400;0,500;0,700;1,400&display=swap" rel="stylesheet">
<link rel="stylesheet" href="assets/pegasus.css">
</head>
<body>

<div class="announce" id="announce">
  <a href="products.html">Browse our Engineering &amp; Mining Supply Catalogue</a>
  <button class="announce-close" aria-label="Close" onclick="document.getElementById('announce').style.display='none'">
    <svg viewBox="0 0 20 20" fill="currentColor"><path d="M17 4.4L15.6 3L10 8.6L4.4 3L3 4.4L8.6 10L3 15.6L4.4 17L10 11.4L15.6 17L17 15.6L11.4 10L17 4.4Z"/></svg>
  </button>
</div>
'''


def header_block(active):
    cls = lambda name: ' class="is-active"' if name == active else ''
    return f'''<header class="header">
  <div class="header-inner">
    <a href="index.html" class="brand" aria-label="Pegasus Engineering & Mining Supplies — Home">
      <img class="logo-emblem" src="assets/brand/logo-emblem-transparent.png" alt="Pegasus Engineering & Mining Supplies">
    </a>
    <nav class="nav-primary" aria-label="Primary">
      <a href="products.html"{cls('products')}>Products</a>
      <a href="services.html"{cls('services')}>Services</a>
      <a href="network.html"{cls('network')}>Network</a>
      <a href="marketplace.html"{cls('marketplace')}>Marketplace</a>
      <a href="about.html"{cls('about')}>About</a>
    </nav>
    <div class="nav-cta">
      <div class="nav-icons">
        <button aria-label="Search">
          <svg viewBox="0 0 24 24" stroke-width="1.5"><circle cx="11" cy="11" r="7"/><line x1="21" y1="21" x2="16.65" y2="16.65"/></svg>
        </button>
        <button class="cart-icon-btn" aria-label="Open cart" type="button">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">
            <path d="M6 6h15l-2 10H8L6 6Z"/>
            <path d="M6 6L4 2H2"/>
            <circle cx="10" cy="20" r="1.4" fill="currentColor"/>
            <circle cx="18" cy="20" r="1.4" fill="currentColor"/>
          </svg>
          <span class="cart-icon-count" aria-live="polite"></span>
        </button>
      </div>
      <a href="contact.html" class="cta-button">Request Quote</a>
      <button class="nav-hamburger" aria-label="Open menu" type="button">
        <span></span><span></span><span></span>
      </button>
    </div>
  </div>
</header>
'''


def footer_block():
    return '''<footer class="footer">
  <div class="footer-inner">
    <div class="footer-grid">
      <div class="footer-brand">
        <div class="wordmark">Pegasus</div>
        <div class="mark">Engineering &amp; Mining Supplies</div>
        <p>Trade supplier of engineered components, consumables and bespoke fabrication to the South African mining, industrial and infrastructure sectors.</p>
      </div>
      <div>
        <h5>Browse</h5>
        <ul>
          <li><a href="products.html">Products</a></li>
          <li><a href="services.html">Services</a></li>
          <li><a href="network.html">Network</a></li>
          <li><a href="marketplace.html">Marketplace</a></li>
          <li><a href="about.html">About</a></li>
        </ul>
      </div>
      <div>
        <h5>Divisions</h5>
        <ul>
          <li><a href="network.html#welding">Welding &amp; Cutting</a></li>
          <li><a href="network.html#abrasive">Abrasive</a></li>
          <li><a href="network.html#power-tools">Power Tools</a></li>
          <li><a href="network.html#safety">Safety &amp; PPE</a></li>
          <li><a href="network.html#hand-tools">Hand Tools</a></li>
          <li><a href="network.html#electrical">Electrical</a></li>
          <li><a href="network.html#paint">Paint Products</a></li>
          <li><a href="network.html#lubricants">Lubricants &amp; Fuel</a></li>
        </ul>
      </div>
      <div>
        <h5>Company</h5>
        <ul>
          <li><a href="about.html">About Pegasus</a></li>
          <li><a href="contact.html">Trade Accounts</a></li>
          <li><a href="about.html#quality">Quality &amp; SHEQ</a></li>
          <li><a href="about.html#bbbee">BBBEE Status</a></li>
        </ul>
      </div>
      <div>
        <h5>Contact</h5>
        <ul>
          <li><a href="mailto:accounts@pegasuseng.co.za">accounts@pegasuseng.co.za</a></li>
          <li><a href="tel:+27132431390">013 243 1390</a></li>
          <li><a href="contact.html">Boksburg, Gauteng</a></li>
          <li><a href="contact.html">Mon – Fri · 07h00 – 17h00</a></li>
        </ul>
      </div>
    </div>
    <div class="footer-bottom">
      <span>© 2025 Pegasus Engineering &amp; Mining Supplies (Pty) Ltd</span>
      <span>Reg. 2013/XXXXXX/07 · VAT 4XXXXXXXXX</span>
      <span>Privacy · Terms · Cookies</span>
    </div>
  </div>
</footer>

<div class="cookie" id="cookie">
  <h6>Our website uses cookies</h6>
  <p>We use cookies to remember your preferences, measure site traffic and personalise content. You can change or withdraw consent at any time.</p>
  <div class="cookie-actions">
    <button class="cookie-btn" onclick="document.getElementById('cookie').classList.add('is-hidden')">Reject all</button>
    <button class="cookie-btn primary" onclick="document.getElementById('cookie').classList.add('is-hidden')">Accept all</button>
  </div>
</div>

</body>
</html>
'''


def render_shop_page(active, hero):
    all_items = build_items()
    include_services = hero.get("include_services", True)
    if include_services:
        items = all_items
    else:
        items = [i for i in all_items if i["type"] == "product"]
    catalogues = build_catalogues()

    head = head_block(hero["title_attr"], hero["meta_desc"])
    header = header_block(active)

    # Hero
    n_prod = len([i for i in items if i["type"] == "product"])
    n_svc  = len([i for i in items if i["type"] == "service"])
    meta_parts = [f'<span><strong>{n_prod}</strong> product lines</span>']
    if n_svc > 0:
        meta_parts.append(f'<span><strong>{n_svc}</strong> engineering services</span>')
    meta_parts.append(f'<span><strong>{len(catalogues)}</strong> catalogues</span>')
    meta_html = "\n        ".join(meta_parts)

    hero_html = f'''<main>

  <section class="shop-hero">
    <div class="shop-hero-inner">
      <div class="suphead">{hero["eyebrow"]}</div>
      <h1 class="shop-hero-title">{hero["title_html"]}</h1>
      <p class="shop-hero-lead">{hero["lead"]}</p>
      <div class="shop-hero-meta">
        {meta_html}
      </div>
    </div>
  </section>
'''

    # Filter bar + product grid
    product_pills = render_category_pills(PRODUCT_CATEGORIES, "category")
    service_pills = render_category_pills(SERVICE_CATEGORIES, "category")

    type_filter_row = ""
    service_pill_group = ""
    if include_services:
        type_filter_row = (
            '<div class="shop-filter-row">\n'
            '          <span class="shop-filter-label">Type</span>\n'
            '          <div class="shop-pills" data-filter-group="type">\n'
            '            <button class="shop-pill is-active" data-type="all" type="button">All</button>\n'
            '            <button class="shop-pill" data-type="product" type="button">Products</button>\n'
            '            <button class="shop-pill" data-type="service" type="button">Services</button>\n'
            '          </div>\n'
            '        </div>'
        )
        service_pill_group = (
            '<div class="shop-pill-group" data-type-scope="service" hidden>\n'
            f'              {service_pills}\n'
            '            </div>'
        )

    db_html = f'''
  <section class="shop-section" id="shop">
    <div class="shop-section-inner">
      <div class="shop-section-head">
        <span class="suphead">{hero["db_eyebrow"]}</span>
        <h2>{hero["db_title"]}</h2>
      </div>

      <div class="shop-filters" role="region" aria-label="Filter products and services">
        {type_filter_row}

        <div class="shop-filter-row">
          <span class="shop-filter-label">Category</span>
          <div class="shop-pills" data-filter-group="category">
            <button class="shop-pill is-active" data-category="all" type="button">All</button>
            <div class="shop-pill-group" data-type-scope="product">
              {product_pills}
            </div>
            {service_pill_group}
          </div>
        </div>

        <div class="shop-filter-row shop-filter-search">
          <span class="shop-filter-label">Search</span>
          <div class="shop-search-wrap">
            <svg viewBox="0 0 24 24" aria-hidden="true" fill="none" stroke="currentColor" stroke-width="1.6"><circle cx="11" cy="11" r="7"/><line x1="21" y1="21" x2="16.65" y2="16.65"/></svg>
            <input type="search" id="shop-search" placeholder="Search products, brands, services…" autocomplete="off">
          </div>
          <span class="shop-result-count" id="shop-result-count"></span>
        </div>
      </div>

      <div class="shop-grid" id="shop-grid" aria-live="polite"></div>
      <div class="shop-empty" id="shop-empty" hidden>
        <p>No matches. Try clearing the search or selecting a different category.</p>
        <button class="btn btn-underline" id="shop-reset" type="button" style="margin-top:0;">Reset filters</button>
      </div>
    </div>
  </section>
'''

    # Catalogues carousel
    cat_pills = render_category_pills(PRODUCT_CATEGORIES, "cat-filter")
    catalogues_html = f'''
  <section class="shop-catalogues" id="catalogues">
    <div class="shop-section-inner">
      <div class="shop-section-head">
        <span class="suphead">Catalogues &amp; Datasheets</span>
        <h2>Download the full OEM library.</h2>
        <p>Browse the {len(catalogues)} OEM catalogues we stock against. Filter by division, then download as PDF.</p>
      </div>

      <div class="shop-filters shop-filters--inline">
        <div class="shop-filter-row">
          <span class="shop-filter-label">Division</span>
          <div class="shop-pills" data-filter-group="cat-filter">
            <button class="shop-pill is-active" data-cat-filter="all" type="button">All</button>
            {cat_pills}
          </div>
        </div>
      </div>

      <div class="catalogue-carousel-wrap">
        <button class="catalogue-carousel-nav is-prev" id="cat-prev" type="button" aria-label="Scroll catalogues left">‹</button>
        <div class="catalogue-carousel" id="catalogue-carousel"></div>
        <button class="catalogue-carousel-nav is-next" id="cat-next" type="button" aria-label="Scroll catalogues right">›</button>
      </div>
    </div>
  </section>
'''

    # Browse by Division (moved to end per request)
    division_cards = render_division_grid()
    division_html = f'''
  <section class="section">
    <div class="section-inner">
      <div class="section-head">
        <div class="suphead">Browse by Division</div>
        <h2>{hero["division_h2"]}</h2>
        <p>{hero["division_lead"]}</p>
      </div>
      <div class="division-grid">
{division_cards}
      </div>
    </div>
  </section>
'''

    # Closing CTA
    cta_html = f'''
  <section class="section is-dark" style="padding:96px 40px;">
    <div class="section-inner" style="text-align:center;">
      <div class="suphead" style="color:var(--c-accent);">{hero["cta_eyebrow"]}</div>
      <h2 style="color:var(--c-bg);font-size:clamp(28px,3vw,44px);margin:16px auto 24px;max-width:740px;">{hero["cta_title"]}</h2>
      <p style="color:rgba(227,227,225,0.85);max-width:560px;margin:0 auto 50px;">{hero["cta_lead"]}</p>
      <a href="contact.html" class="cta-button" style="padding:16px 32px;">Request a Quote</a>
    </div>
  </section>

</main>

'''

    # Embedded JS data + filter logic
    items_json = json.dumps(items, separators=(",", ":"))
    catalogues_json = json.dumps(catalogues, separators=(",", ":"))

    js_block = f'''<script>
const SHOP_ITEMS = {items_json};
const CATALOGUES = {catalogues_json};

(function initShop() {{
  const grid = document.getElementById('shop-grid');
  const empty = document.getElementById('shop-empty');
  const countEl = document.getElementById('shop-result-count');
  const search = document.getElementById('shop-search');
  const resetBtn = document.getElementById('shop-reset');
  const state = {{ type: 'all', category: 'all', q: '' }};

  function escapeHtml(s) {{
    return String(s).replace(/[&<>"']/g, c => ({{'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}}[c]));
  }}

  function fmtZAR(n) {{
    return 'R\\u00a0' + Math.round(n).toLocaleString('en-ZA');
  }}

  function card(item) {{
    const desc = escapeHtml(item.description);
    const isService = item.type === 'service';
    const buyBlock = isService
      ? `<div class="shop-card-buy shop-card-buy--service">
           <span class="shop-card-price-tag">Quote required</span>
           <button class="shop-card-add" data-add-id="${{item.id}}" type="button">
             <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M12 5v14M5 12h14"/></svg>
             Add to Quote
           </button>
         </div>`
      : `<div class="shop-card-buy">
           <span class="shop-card-price">${{fmtZAR(item.price)}}<small> / ${{item.unit || 'ea'}}</small></span>
           <div class="shop-card-buy-controls">
             <div class="qty-stepper">
               <button data-qty-dec="${{item.id}}" type="button" aria-label="Decrease">−</button>
               <input type="number" value="1" min="1" data-qty-input="${{item.id}}" aria-label="Quantity">
               <button data-qty-inc="${{item.id}}" type="button" aria-label="Increase">+</button>
             </div>
             <button class="shop-card-add" data-add-id="${{item.id}}" type="button">
               <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M6 6h15l-2 10H8L6 6Z"/><path d="M6 6L4 2H2"/><circle cx="10" cy="20" r="1.5"/><circle cx="18" cy="20" r="1.5"/></svg>
               Add
             </button>
           </div>
         </div>`;
    return `<div class="shop-card" data-item-id="${{item.id}}">
      <a class="shop-card-link" href="${{item.href}}">
        <div class="shop-card-media"><img src="${{item.image}}" alt="${{escapeHtml(item.title)}}" loading="lazy"></div>
        <div class="shop-card-body">
          <span class="shop-card-tag shop-card-tag--${{item.type}}">${{isService ? 'Service' : 'Product'}}</span>
          <span class="shop-card-meta">${{escapeHtml(item.categoryLabel)}}</span>
          <h4 class="shop-card-title">${{escapeHtml(item.title)}}</h4>
          <span class="shop-card-brand">${{escapeHtml(item.brand)}}</span>
          <p class="shop-card-desc">${{desc}}</p>
        </div>
      </a>
      ${{buyBlock}}
    </div>`;
  }}

  // Cart actions on the grid (delegated)
  grid.addEventListener('click', e => {{
    const addBtn = e.target.closest('[data-add-id]');
    if (addBtn) {{
      e.preventDefault();
      const id = addBtn.dataset.addId;
      const item = SHOP_ITEMS.find(x => x.id === id);
      if (!item) return;
      const qtyInput = grid.querySelector(`[data-qty-input="${{id}}"]`);
      const qty = qtyInput ? Math.max(1, parseInt(qtyInput.value) || 1) : 1;
      if (window.cart) window.cart.add(item, qty);
      return;
    }}
    const dec = e.target.closest('[data-qty-dec]');
    const inc = e.target.closest('[data-qty-inc]');
    if (dec || inc) {{
      e.preventDefault();
      const id = (dec || inc).dataset.qtyDec || (dec || inc).dataset.qtyInc;
      const input = grid.querySelector(`[data-qty-input="${{id}}"]`);
      if (!input) return;
      let v = parseInt(input.value) || 1;
      v = inc ? v + 1 : Math.max(1, v - 1);
      input.value = v;
    }}
  }});

  function render() {{
    const q = state.q.trim().toLowerCase();
    const filtered = SHOP_ITEMS.filter(it => {{
      if (state.type !== 'all' && it.type !== state.type) return false;
      if (state.category !== 'all' && it.category !== state.category) return false;
      if (q) {{
        const blob = (it.title + ' ' + it.brand + ' ' + it.description + ' ' + it.categoryLabel).toLowerCase();
        if (!blob.includes(q)) return false;
      }}
      return true;
    }});
    grid.innerHTML = filtered.map(card).join('');
    empty.hidden = filtered.length > 0;
    countEl.textContent = `${{filtered.length}} of ${{SHOP_ITEMS.length}}`;
  }}

  // Wire pill groups
  document.querySelectorAll('[data-filter-group]').forEach(group => {{
    const key = group.dataset.filterGroup;
    if (key !== 'type' && key !== 'category') return;
    group.addEventListener('click', e => {{
      const btn = e.target.closest('.shop-pill');
      if (!btn) return;
      if (key === 'type') {{
        state.type = btn.dataset.type;
        // toggle category scope
        document.querySelectorAll('.shop-pill-group[data-type-scope]').forEach(g => {{
          g.hidden = !(state.type === 'all' || g.dataset.typeScope === state.type);
        }});
        // reset category when switching type
        state.category = 'all';
        document.querySelectorAll('[data-filter-group="category"] .shop-pill').forEach(p => {{
          p.classList.toggle('is-active', p.dataset.category === 'all');
        }});
      }} else {{
        state.category = btn.dataset.category;
      }}
      group.querySelectorAll('.shop-pill').forEach(p => p.classList.remove('is-active'));
      btn.classList.add('is-active');
      render();
    }});
  }});

  search.addEventListener('input', e => {{ state.q = e.target.value; render(); }});

  resetBtn.addEventListener('click', () => {{
    state.type = 'all'; state.category = 'all'; state.q = '';
    search.value = '';
    document.querySelectorAll('.shop-pill').forEach(p => {{
      p.classList.toggle('is-active', p.dataset.type === 'all' || p.dataset.category === 'all');
    }});
    document.querySelectorAll('.shop-pill-group[data-type-scope]').forEach(g => g.hidden = false);
    render();
  }});

  render();
}})();

(function initCatalogues() {{
  const car = document.getElementById('catalogue-carousel');
  const pillGroup = document.querySelector('[data-filter-group="cat-filter"]');
  const prev = document.getElementById('cat-prev');
  const next = document.getElementById('cat-next');
  let activeFilter = 'all';

  function catCard(c) {{
    return `<a class="cat-card" href="${{c.pdf}}" target="_blank" rel="noopener" download>
      <div class="cat-card-img"><img src="${{c.cover}}" alt="${{c.brand}}" loading="lazy"></div>
      <div class="cat-card-overlay"></div>
      <span class="cat-card-badge">PDF · ${{c.pages}} pp</span>
      <div class="cat-card-meta">
        <span class="cat-card-eyebrow">${{c.categoryLabel}}</span>
        <h4 class="cat-card-title">${{c.brand}}</h4>
      </div>
      <div class="cat-card-action"><span class="cat-card-btn"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M12 3v13M5 11l7 7 7-7M5 21h14"/></svg>Download</span></div>
    </a>`;
  }}

  function renderCats() {{
    const visible = activeFilter === 'all' ? CATALOGUES : CATALOGUES.filter(c => c.category === activeFilter);
    car.innerHTML = visible.map(catCard).join('');
    car.scrollTo({{ left: 0, behavior: 'smooth' }});
  }}

  pillGroup.addEventListener('click', e => {{
    const btn = e.target.closest('.shop-pill');
    if (!btn) return;
    activeFilter = btn.dataset.catFilter;
    pillGroup.querySelectorAll('.shop-pill').forEach(p => p.classList.remove('is-active'));
    btn.classList.add('is-active');
    renderCats();
  }});

  function scrollByCards(dir) {{
    const card = car.querySelector('.cat-card');
    if (!card) return;
    const step = card.getBoundingClientRect().width + 24;
    car.scrollBy({{ left: dir * step * 2, behavior: 'smooth' }});
  }}
  prev.addEventListener('click', () => scrollByCards(-1));
  next.addEventListener('click', () => scrollByCards(1));

  renderCats();
}})();
</script>
'''

    site_tags = '<script src="assets/nav.js"></script>\n<script src="assets/cart.js"></script>\n'
    return head + header + hero_html + db_html + catalogues_html + division_html + cta_html + footer_block().replace("</body>", js_block + site_tags + "</body>")


# ── Page-specific framing ────────────────────────────────────────────────────

PRODUCTS_HERO = {
    "title_attr": "Products — Pegasus Engineering & Mining Supplies",
    "meta_desc":  "Browse 228 specification-grade product lines from 38 approved OEM partners. Filter by division, search by part — Pegasus Engineering & Mining Supplies.",
    "eyebrow": "Product Catalogue",
    "title_html": "Browse the <em>Product Catalogue.</em>",
    "lead": "228 specification-grade product lines from 38 approved OEM partners across welding, abrasive, power tools, safety, hand tools, electrical, paint and lubricants.",
    "db_eyebrow": "Product Database",
    "db_title": "Filter the catalogue.",
    "division_h2": "Eight engineered supply divisions.",
    "division_lead": "Pick a division to drill into its full product range, OEM partners and downloadable catalogues.",
    "cta_eyebrow": "Specify with Confidence",
    "cta_title": "Send us a line list. We'll respond with a written quote.",
    "cta_lead": "Mill certificates, OEM documentation, country-of-origin trace — all shipped with every order.",
    "include_services": False,
}

MARKETPLACE_HERO = {
    "title_attr": "Marketplace — Pegasus Engineering & Mining Supplies",
    "meta_desc":  "The Pegasus online trade counter — browse 228 product lines + 6 engineering services, build a quote and order from one online counter.",
    "eyebrow": "The Pegasus Marketplace",
    "title_html": "The online <em>trade counter.</em>",
    "lead": "228 product lines and 6 engineering services in one searchable database. Build a quote, place an order, schedule a despatch — all from one counter.",
    "db_eyebrow": "Marketplace Database",
    "db_title": "Search the trade counter.",
    "division_h2": "Shop by division.",
    "division_lead": "Each division opens to its full product range, OEM partners and downloadable catalogues.",
    "cta_eyebrow": "Open the Trade Counter",
    "cta_title": "Build a quote in five clicks. Get a written response within one working day.",
    "cta_lead": "Standing accounts, consignment stock, expediting on critical lines — all managed through one desk.",
    "include_services": True,
}


def main():
    (OUT_DIR / "products.html").write_text(render_shop_page("products", PRODUCTS_HERO), encoding="utf-8")
    print("  wrote products.html")
    (OUT_DIR / "marketplace.html").write_text(render_shop_page("marketplace", MARKETPLACE_HERO), encoding="utf-8")
    print("  wrote marketplace.html")


if __name__ == "__main__":
    main()
