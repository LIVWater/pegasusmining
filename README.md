# Pegasus Engineering & Mining Supplies — Website

A modern, static rebuild of pegasuseng.co.za as a trade-supply marketplace for the South African mining and industrial sectors.

## Pages

- **Homepage** — `index.html` (hero, division carousel, shop divisions, services, fabrication, supplier-logo carousel, marketplace CTA)
- **Marketplace** — `marketplace.html` (full database: 228 products + 6 services, filterable + searchable, catalogue carousel, browse-by-division)
- **Products** — `products.html` (products-only database, 228 product lines)
- **Services** — `services.html`
- **Network** — `network.html` (38 OEM partner brands organised by division)
- **About** — `about.html`
- **Contact** — `contact.html`
- **Checkout** — `checkout.html` (cart + order/quote submission)
- **8 division pages** — `product-*.html`
- **38 partner pages** — `partner-*.html` (each with overview, range, and downloadable catalogue PDF)

## Stack

Pure static HTML / CSS / JS — no framework, no build step. Site is hosted by simply serving the folder.

- **Vanilla JS** for the cart (`assets/cart.js`) and mobile nav (`assets/nav.js`)
- **localStorage** persists the cart across sessions
- **Python generators** to keep all derived pages consistent:
  - `generate_partners.py` — emits all 38 partner pages from one data structure
  - `generate_shop.py` — emits products.html + marketplace.html with embedded product/catalogue data

## Generators

After editing brand data in `generate_partners.py` or `generate_shop.py`, re-run them:

```bash
python3 generate_partners.py
python3 generate_shop.py
```

Both scripts overwrite their target HTML files.

## Local preview

Serve the folder with any static server:

```bash
python3 -m http.server 8843
# → open http://localhost:8843
```

## Deployment

Hosted on Vercel via GitHub integration — every push to `main` triggers a redeploy.
