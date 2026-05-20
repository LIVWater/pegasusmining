"""
Pegasus partner-page generator.
Builds individual partner-<slug>.html pages from a shared template + brand data.
Re-running the script is safe — it overwrites existing pages.
"""
import os
from pathlib import Path

OUT_DIR = Path(__file__).parent

# Category → anchor on network.html
CATEGORIES = {
    "welding":     "Welding & Cutting",
    "abrasive":    "Abrasive",
    "power-tools": "Power Tools",
    "safety":      "Safety & PPE",
    "hand-tools":  "Hand Tools",
    "electrical":  "Electrical",
    "paint":       "Paint Products",
    "lubricants":  "Lubricants & Fuel",
}

# Catalogue cover image per category — pulled from existing assets/brand/
CAT_COVERS = {
    "welding":     ["welding-portrait.jpg", "welding-blue.jpg", "welding-helmet.jpg", "welding-sparks.jpg"],
    "abrasive":    ["abrasive-sparks.jpg", "abrasive-cut.jpg", "abrasive-grinder.jpg", "abrasive-bench.jpg"],
    "power-tools": ["powertools-drill.jpg", "powertools-workshop.jpg", "powertools-bits.jpg", "welding-portrait.jpg"],
    "safety":      ["safety-face.jpg", "safety-glove-beam.jpg", "safety-glove-control.jpg", "welding-helmet.jpg"],
    "hand-tools":  ["handtools-pegboard.jpg", "handtools-sockets.jpg", "handtools-bits.jpg", "handtools-loose.jpg"],
    "electrical":  ["electrical-low.jpg", "powertools-workshop.jpg", "welding-blue.jpg", "handtools-bits.jpg"],
    "paint":       ["paint-roller.jpg", "abrasive-sanding.jpg", "powertools-workshop.jpg", "handtools-bits.jpg"],
    "lubricants":  ["lubricants-station.jpg", "lubricants-tanker.jpg", "lubricants-truck-field.jpg", "powertools-workshop.jpg"],
}

# Real catalogue PDFs retrieved from pegasuseng.co.za, with extracted page counts.
# slug → (pdf filename in /assets/catalogues/, page count)
# Brands not in this map have no published catalogue — they fall back to a "Request" card.
CATALOGUE_PDFS = {
    # Welding & Cutting
    "afrox": ("afrox.pdf", 112),
    "esab": ("esab.pdf", 113),
    "harris": ("harris.pdf", 212),
    "matweld": ("matweld.pdf", 64),
    "oerlikon": ("oerlikon.pdf", 406),
    "pinnacle": ("pinnacle.pdf", 70),
    "pioneer": ("pioneer.pdf", 56),
    "reflex-welding": ("reflex-welding.pdf", 8),
    # Abrasive
    "lukas": ("lukas.pdf", 12),
    "metabo": ("metabo.pdf", 12),
    "pferd": ("pferd.pdf", 60),
    "superflex": ("superflex.pdf", 20),
    # Power Tools
    "hikoki": ("hikoki.pdf", 60),
    "milwaukee": ("milwaukee.pdf", 51),
    # Safety & PPE
    "bestway": ("bestway.pdf", 4),
    "bova": ("bova.pdf", 32),
    "drager": ("drager.pdf", 48),
    "dupont": ("dupont.pdf", 132),
    "elvex": ("elvex.pdf", 39),
    "javlin": ("javlin.pdf", 54),
    "jonsson": ("jonsson.pdf", 224),
    "kaliber": ("kaliber.pdf", 2),
    "karam": ("karam.pdf", 47),
    "rebel": ("rebel.pdf", 32),
    "uvex": ("uvex.pdf", 52),
    "vulcan": ("vulcan.pdf", 34),
    "wayne": ("wayne.pdf", 16),
    # Hand Tools
    "gedore": ("gedore.pdf", 66),
    "groz": ("groz.pdf", 40),
    "matus": ("matus.pdf", 18),
    "stanley": ("stanley.pdf", 41),
    "wera": ("wera.pdf", 18),
    # Electrical
    "truco": ("truco.pdf", 2),
    # Paint
    "stoncor": ("stoncor.pdf", 16),
}

# All 38 brands — slug, name, category-key, logo filename in /assets/partners/, meta, content
BRANDS = [
    # ── Welding & Cutting ──────────────────────────────────────────────────
    {
        "slug": "afrox", "name": "Afrox", "cat": "welding", "logo": "afrox.png",
        "established": "1927", "origin": "South Africa", "since": "2013",
        "tagline": "South Africa's leading industrial gases and welding consumables manufacturer — supplied through Pegasus against trade accounts.",
        "lead": "Afrox supplies the welding consumables and industrial gases that keep South African fabrication shops, mines and EPC contractors moving — from MMA electrodes and MIG/MAG wires through to bulk argon, oxygen and acetylene.",
        "body": [
            "Pegasus carries the full Afrox range against standing trade accounts. Mill certificates, batch traceability and country-of-origin documentation ship with every order. Bulk-gas refills, cylinder swaps and consignment stock are arranged through our Boksburg branch.",
            "For specification cross-references, duty-cycle selection and substitution validation, our welding desk works directly with the Afrox technical team.",
        ],
        "range": [
            ("MMA Stick Electrodes",   "Mild-steel, low-hydrogen, stainless and hardfacing — full Afrox electrode portfolio with mill certs on request."),
            ("MIG / MAG Wires",        "Solid and flux-cored wires across mild-steel, low-alloy and stainless grades. 15kg, 18kg and bulk pack sizes."),
            ("TIG Filler Rods",        "Mild-steel, stainless and aluminium TIG rods to AWS specification. Tube and case quantities."),
            ("Industrial Gases",       "Argon, oxygen, acetylene, CO₂ and mixed shielding gases. Cylinder swaps and bulk refills via Boksburg."),
            ("Cutting Consumables",    "Oxy-fuel nozzles, plasma electrodes, tips and shields for HyPertherm-pattern and Afrox-OEM kit."),
            ("Welding Equipment",      "MMA, MIG, TIG inverters and engine-driven welders to Afrox spec — supplied with commissioning and warranty."),
        ],
        "catalogues": [
            ("Catalogue 2025", "Welding Consumables",  "Electrodes · MIG · TIG · Flux-cored", "184"),
            ("Reference Guide","Industrial Gases",      "Argon · Oxygen · Acetylene · CO₂",    "46"),
            ("Brochure",       "Welding Equipment",     "MMA · MIG · TIG · Engine-driven",     "28"),
            ("Datasheet",      "Cutting Consumables",   "Oxy-fuel · Plasma tips · Shields",    "12"),
        ],
    },
    {
        "slug": "esab", "name": "Esab", "cat": "welding", "logo": "esab.png",
        "established": "1904", "origin": "Sweden", "since": "2013",
        "tagline": "Global welding and cutting equipment manufacturer — Esab consumables and inverters supplied to South African operators through Pegasus.",
        "lead": "Founded in Gothenburg in 1904, Esab is a global welding technology leader producing premium consumables, inverter platforms and plasma cutting kit for heavy industry.",
        "body": [
            "Pegasus stocks the Esab range across MMA, MIG, TIG and submerged-arc applications. OK-series electrodes, Aristo wires and Cutmaster plasma sit on the shelf at Boksburg with full traceability documentation.",
            "Trade accounts cover consumables on consignment and OEM-spec inverters with commissioning, warranty and spares support managed in-house.",
        ],
        "range": [
            ("OK Series Electrodes",    "Premium MMA stick electrodes across mild, low-alloy, stainless and hardfacing — the Esab benchmark range."),
            ("Aristo Wires",            "Solid and flux-cored MIG/MAG wires for structural, pipeline and stainless fabrication."),
            ("TIG Filler Metals",       "OK Tigrod range — mild-steel, stainless and aluminium TIG rods to AWS spec."),
            ("Cutmaster Plasma",        "Inverter plasma cutters and consumables — manual and mechanised duty."),
            ("Submerged-Arc Consumables","Wires and fluxes for heavy structural and pressure-vessel work."),
            ("Welding Inverters",       "Rebel, Aristo and Origo welding power sources — MMA, MIG, TIG, multiprocess."),
        ],
        "catalogues": [
            ("Catalogue 2025", "Consumables Master",   "MMA · MIG · TIG · SAW",       "210"),
            ("Brochure",       "Welding Inverters",    "Rebel · Aristo · Origo",      "44"),
            ("Datasheet",      "Plasma Cutting",       "Cutmaster series and parts",  "22"),
            ("Reference",      "Welding Procedures",   "Process selection guide",     "36"),
        ],
    },
    {
        "slug": "harris", "name": "Harris", "cat": "welding", "logo": "harris.png",
        "established": "1898", "origin": "USA", "since": "2014",
        "tagline": "Brazing, soldering and gas equipment specialist — Harris consumables and regulators supplied via Pegasus.",
        "lead": "The Harris Products Group has manufactured brazing alloys, soldering products and gas distribution equipment for over 120 years — a default specification across refrigeration, HVAC and precision fabrication.",
        "body": [
            "Pegasus carries the Harris range of silver brazing alloys, lead-free solders, flux pastes and gas regulators against trade accounts in South Africa.",
            "OEM-grade documentation accompanies every order — mill certificates, datasheets and country-of-origin paperwork shipped with stock.",
        ],
        "range": [
            ("Silver Brazing Alloys", "Stay-Silv and Safety-Silv ranges — refrigeration, HVAC and industrial brazing."),
            ("Lead-Free Solders",     "Plumbing and electronics solders to RoHS spec."),
            ("Flux Pastes & Powders", "Brazing and soldering fluxes for ferrous and non-ferrous joining."),
            ("Gas Regulators",        "Single- and two-stage regulators for oxygen, acetylene, argon and propane."),
            ("Cutting Torches",       "Oxy-fuel cutting torches and tips — manual and mechanised."),
            ("Heating Equipment",     "Heating tips and accessories for shrink-fit and pre-heat applications."),
        ],
        "catalogues": [
            ("Catalogue 2025", "Brazing Alloys",         "Stay-Silv · Safety-Silv",       "96"),
            ("Brochure",       "Gas Equipment",          "Regulators · Torches · Tips",   "52"),
            ("Datasheet",      "Solders & Fluxes",       "Lead-free range",               "18"),
            ("Reference",      "Joining Process Guide",  "Brazing & soldering best-practice","24"),
        ],
    },
    {
        "slug": "matweld", "name": "Mat-Weld", "cat": "welding", "logo": "matweld.png",
        "established": "1985", "origin": "South Africa", "since": "2013",
        "tagline": "South African welding equipment manufacturer — Mat-Weld plant, generators and inverters from a local OEM via Pegasus.",
        "lead": "Mat-Weld designs and assembles welding plant locally — engine-driven welders, multi-operator units and field-grade inverters built for South African mining and construction conditions.",
        "body": [
            "Pegasus supplies Mat-Weld across the full local range, with Boksburg-based commissioning, warranty and spares support. Engine-driven sets ship configured to your duty and fuel preference.",
            "Standing-account customers can place Mat-Weld kit on long-term hire or hire-purchase via our finance partners.",
        ],
        "range": [
            ("Engine-Driven Welders",  "Diesel and petrol welding generators — single and multi-operator."),
            ("MMA Inverters",          "Field-grade MMA welding inverters to 400A duty."),
            ("MIG / MAG Sets",         "Workshop and site MIG/MAG platforms — separate and integrated wire feed."),
            ("TIG Welders",            "AC/DC TIG platforms for stainless and aluminium fabrication."),
            ("Welding Generators",     "Pure power generators and welder/generator combos."),
            ("Plant Spares & Service", "OEM spares, refurbishment and on-site service through Pegasus Engineering."),
        ],
        "catalogues": [
            ("Catalogue 2025", "Full Equipment Range",  "Generators · Inverters · MIG · TIG", "72"),
            ("Brochure",       "Engine-Driven Welders", "Diesel and petrol units",            "28"),
            ("Datasheet",      "MMA Inverters",         "Field-grade duty",                   "12"),
            ("Reference",      "Spares & Service",      "OEM parts catalogue",                "44"),
        ],
    },
    {
        "slug": "oerlikon", "name": "Oerlikon", "cat": "welding", "logo": "oerlikon.png",
        "established": "1906", "origin": "Switzerland", "since": "2014",
        "tagline": "Swiss-engineered premium welding consumables — Oerlikon electrodes and wires for critical-spec fabrication.",
        "lead": "Oerlikon (now part of voestalpine Böhler Welding) produces premium electrodes, wires and fluxes engineered for nuclear, pressure-vessel and pipeline work where specification deviation is not an option.",
        "body": [
            "Pegasus imports Oerlikon consumables against specific project specifications — Citochrome electrodes, Citorex wires and Fluxofil flux-cored ranges arrive with full mill paperwork.",
            "For nuclear, oil-and-gas or pressure-equipment fabrication, the Oerlikon catalogue is supplied with PED, ASME or AWS qualification trace as your project requires.",
        ],
        "range": [
            ("Citochrome Electrodes",   "Premium MMA electrodes for high-alloy, stainless and creep-resistant applications."),
            ("Citorex Wires",           "Solid MIG/MAG wires to AWS A5 spec — full mill paperwork."),
            ("Fluxofil Flux-cored",     "Self-shielded and gas-shielded FCAW wires for structural and pipeline work."),
            ("Fluxocord SAW",           "Submerged-arc wires and fluxes for heavy fabrication."),
            ("Tigrod Filler",           "TIG rods for stainless, nickel-alloy and titanium fabrication."),
            ("Specification Sourcing",  "Project-specific imports against PED, ASME or AWS qualifications."),
        ],
        "catalogues": [
            ("Catalogue 2025", "Premium Consumables",   "Citochrome · Citorex · Fluxofil",  "168"),
            ("Reference",      "PED & ASME Qualifications","Compliance documentation guide", "32"),
            ("Brochure",       "High-Alloy Welding",    "Stainless · Nickel · Creep",       "24"),
            ("Datasheet",      "SAW Range",             "Fluxocord wires and fluxes",       "16"),
        ],
    },
    {
        "slug": "pinnacle", "name": "Pinnacle", "cat": "welding", "logo": "pinnacle.png",
        "established": "1998", "origin": "South Africa", "since": "2013",
        "tagline": "Locally-stocked welding consumables, equipment and safety gear — Pinnacle's broad range backed by Pegasus on the floor.",
        "lead": "Pinnacle is a South African distributor of welding equipment, consumables and personal protective equipment for the mining, fabrication and construction trades — a workhorse brand on the toolbox.",
        "body": [
            "Pegasus stocks Pinnacle inverters, MMA electrodes, MIG wires and a complete safety range including welding helmets, gloves and screens.",
            "Standing-account customers benefit from Pinnacle PPE on consignment alongside their welding consumables.",
        ],
        "range": [
            ("Welding Inverters",     "MMA, MIG and TIG inverter platforms — workshop and field duty."),
            ("MMA Electrodes",        "Mild-steel and stainless stick electrodes — popular pack sizes always in stock."),
            ("MIG / MAG Wires",       "Standard and flux-cored wires for general fabrication."),
            ("Welding Helmets",       "Auto-darkening and passive helmets across the Pinnacle range."),
            ("Welding Gloves & Aprons","Leather PPE for welders — gauntlet, mitt and apron options."),
            ("Cutting Tables & Screens","Workshop cutting tables, screens and curtains."),
        ],
        "catalogues": [
            ("Catalogue 2025", "Welding Equipment",   "Inverters · MIG · TIG · Plasma", "88"),
            ("Brochure",       "Consumables",         "Electrodes · Wires · Tips",      "44"),
            ("Brochure",       "Welder Safety Gear",  "Helmets · Gloves · Aprons",      "32"),
            ("Datasheet",      "Workshop Accessories","Tables · Screens · Clamps",      "16"),
        ],
    },
    {
        "slug": "pioneer", "name": "Pioneer", "cat": "welding", "logo": "pioneer.png",
        "established": "1989", "origin": "USA / South Africa", "since": "2013",
        "tagline": "Welder safety specialists — Pioneer helmets, screens and protective gear supplied by Pegasus.",
        "lead": "Pioneer manufactures welding-focused PPE — auto-darkening helmets, leather aprons, gauntlets and welding screens — engineered specifically for arc-flash, spatter and UV protection.",
        "body": [
            "Pegasus stocks the Pioneer Safety Welding range across helmets, gloves, sleeves and curtains. Bulk orders for mine and shutdown crews ship from Boksburg in 24 hours.",
            "All Pioneer helmets are SANS- and ANSI-rated with sensor and shade-range certification supplied per unit.",
        ],
        "range": [
            ("Auto-Darkening Helmets", "Variable-shade helmets to SANS and ANSI Z87 standards."),
            ("Passive Welding Helmets","Standard fixed-shade helmets — popular sizes and tints."),
            ("Welding Gloves",         "Leather gauntlets, MIG mitts and TIG fingers."),
            ("Aprons & Sleeves",       "Split-leather aprons, jackets, sleeves and spats."),
            ("Welding Screens",        "PVC and canvas welding curtains and screens."),
            ("Spare Lenses & Parts",   "Replacement cover lenses, sweatbands and helmet spares."),
        ],
        "catalogues": [
            ("Catalogue 2025", "Welder Safety Range", "Helmets · Gloves · Aprons · Screens", "96"),
            ("Brochure",       "Auto-Darkening Helmets","Variable-shade range",              "28"),
            ("Datasheet",      "SANS / ANSI Compliance","Certifications and ratings",        "18"),
            ("Reference",      "Spare Parts Index",    "Lenses · Bands · Frames",            "12"),
        ],
    },
    {
        "slug": "reflex-welding", "name": "Reflex Welding", "cat": "welding", "logo": "reflex-welding.png",
        "established": "2002", "origin": "South Africa", "since": "2013",
        "tagline": "Locally-manufactured welding consumables — Reflex electrodes and wires from a South African OEM, on the shelf at Pegasus.",
        "lead": "Reflex Welding manufactures MMA electrodes and MIG/MAG wires in South Africa, supplying mining, fabrication and construction clients with locally-produced consumables to AWS spec.",
        "body": [
            "Pegasus is a Reflex distributor across Gauteng and the platinum belt. Trade accounts cover full electrode and wire range with mill certificates on every batch.",
            "Local OEM status means short lead-times on standing orders, bulk packaging and BBBEE-friendly procurement.",
        ],
        "range": [
            ("Mild-Steel Electrodes",  "E6013, E7018 and structural electrodes — locally manufactured."),
            ("Stainless Electrodes",   "308, 309, 316 and duplex stainless MMA range."),
            ("Hardfacing Electrodes",  "Wear-resistant electrodes for mining and earthmoving repair."),
            ("Solid MIG Wires",        "ER70S-6 and stainless solid wires in 15kg and 18kg packs."),
            ("Flux-Cored Wires",       "Self-shielded and gas-shielded FCAW wires."),
            ("Specials & Bulk",        "Custom batches, packaging and labelling for OEM and resale clients."),
        ],
        "catalogues": [
            ("Catalogue 2025", "Local Consumables",  "MMA · MIG · Hardfacing",        "68"),
            ("Brochure",       "Stainless Range",    "Austenitic · Duplex",           "22"),
            ("Datasheet",      "Hardfacing Guide",   "Wear application reference",    "14"),
            ("Reference",      "Mill Certificates",  "Documentation explainer",       "8"),
        ],
    },

    # ── Abrasive ───────────────────────────────────────────────────────────
    {
        "slug": "fox", "name": "Fox", "cat": "abrasive", "logo": "fox.jpg",
        "established": "1998", "origin": "India", "since": "2019",
        "tagline": "Industrial abrasive discs and wheels — Fox cut-off, grinding and flap discs supplied by Pegasus.",
        "lead": "Fox manufactures industrial bonded and coated abrasives — cut-off wheels, depressed-centre grinding discs and flap discs — engineered for steel fabrication and mining maintenance.",
        "body": [
            "Pegasus stocks the Fox range across 115mm, 125mm and 230mm angle-grinder formats. Bulk packaging is available for shutdown crews and standing accounts.",
            "Every box ships with EN12413 compliance documentation and expiry-date trace.",
        ],
        "range": [
            ("Cut-Off Wheels",      "1mm, 1.6mm and 2.5mm thin cut-off discs — steel and stainless variants."),
            ("Grinding Discs",      "6mm depressed-centre grinding wheels for general fabrication."),
            ("Flap Discs",          "Zirconia and ceramic flap discs across grit ranges."),
            ("Wire Cup Brushes",    "Twisted and crimped wire cup brushes for paint and rust removal."),
            ("Mounted Points",      "Aluminium-oxide mounted points for die-grinder duty."),
            ("Diamond Blades",      "Segmented diamond blades for cured concrete and masonry."),
        ],
        "catalogues": [
            ("Catalogue 2025", "Abrasive Master",   "Cut-off · Grinding · Flap",   "64"),
            ("Brochure",       "Coated Abrasives",  "Flap discs · Sandpaper",      "28"),
            ("Datasheet",      "EN12413 Compliance","Bonded-wheel standards",      "10"),
            ("Reference",      "Wheel Selection",   "Speed and duty guide",        "16"),
        ],
    },
    {
        "slug": "lukas", "name": "Lukas", "cat": "abrasive", "logo": "lukas.png",
        "established": "1934", "origin": "Germany", "since": "2014",
        "tagline": "German precision abrasives — Lukas burrs, mounted points and grinding wheels for die-makers, fabricators and mining maintenance.",
        "lead": "Founded in Engelskirchen in 1934, Lukas-Erzett produces precision rotary burrs, mounted points, files and grinding wheels to demanding German engineering tolerances.",
        "body": [
            "Pegasus stocks the Lukas range for die-makers, weld-shop finishers and mining-component refurbishers. Mill paperwork and DIN-compliance documentation ship with every order.",
            "Specialist die-maker kits, tungsten-carbide burrs and OEM-rebrand options available on request.",
        ],
        "range": [
            ("Tungsten-Carbide Burrs", "Die-maker rotary burrs — cylindrical, conical, ball and tree forms."),
            ("Mounted Points",         "Pink aluminium-oxide and silicon-carbide mounted points."),
            ("Files & Rifflers",       "Precision Swiss-pattern and rotary files."),
            ("Grinding Wheels",        "Straight, dish and cup grinding wheels for surface work."),
            ("Diamond Burrs",          "Plated diamond burrs for carbide and hardened-steel finishing."),
            ("Polishing Range",        "Felt bobs, mops and polishing compounds."),
        ],
        "catalogues": [
            ("Catalogue 2025", "Rotary Tools",      "Burrs · Files · Mounted Points","112"),
            ("Brochure",       "Tungsten-Carbide",  "Die-maker burr range",          "44"),
            ("Datasheet",      "DIN Compliance",    "Standards reference",           "12"),
            ("Reference",      "Application Guide", "Burr/material selector",        "20"),
        ],
    },
    {
        "slug": "metabo", "name": "Metabo", "cat": "abrasive", "logo": "metabo.png",
        "established": "1924", "origin": "Germany", "since": "2013",
        "tagline": "German-engineered power tools and abrasives — Metabo grinders, drills and bonded abrasives from a 100-year OEM, via Pegasus.",
        "lead": "Metabo manufactures professional power tools and matched abrasives in Nürtingen — angle grinders, drills, polishers and the bonded wheels designed to run on them.",
        "body": [
            "Pegasus supplies the Metabo combined range — corded and cordless power tools, plus matched cut-off wheels, grinding discs, flap discs and diamond blades for them.",
            "Trade accounts include OEM commissioning, warranty and a workshop spares network across the platinum belt.",
        ],
        "range": [
            ("Angle Grinders",         "115mm – 230mm corded and cordless angle grinders."),
            ("Cordless Drill / Driver","18V LiHD platform — drills, impact drivers and combi sets."),
            ("Metal Polishers",        "Variable-speed polishers and finishing sanders."),
            ("Cut-Off & Grinding",     "Matched bonded wheels for the Metabo platform."),
            ("Flap & Fibre Discs",     "Coated abrasives for finishing and stock-removal work."),
            ("Diamond Blades",         "Concrete and masonry diamond blades for the Metabo cut-off range."),
        ],
        "catalogues": [
            ("Catalogue 2025", "Power Tools Master","Corded · Cordless · Accessories","244"),
            ("Brochure",       "Abrasives Range",   "Bonded · Coated · Diamond",      "88"),
            ("Datasheet",      "LiHD Battery Platform","18V technology guide",        "20"),
            ("Reference",      "Service Network",   "Warranty and spares index",      "16"),
        ],
    },
    {
        "slug": "pferd", "name": "Pferd", "cat": "abrasive", "logo": "pferd.png",
        "established": "1799", "origin": "Germany", "since": "2014",
        "tagline": "Heritage German abrasives — Pferd files, burrs and bonded wheels since 1799, on the shelf at Pegasus.",
        "lead": "Pferd has been manufacturing files, burrs and bonded abrasives in Marienheide since 1799 — a default specification across high-precision tool-rooms, weld-shops and aerospace finishing.",
        "body": [
            "Pegasus carries the Pferd portfolio across rotary burrs, mounted points, cut-off and grinding wheels, flap discs and engineer's files. Trade accounts cover the full range with mill paperwork.",
            "Specification consulting for tool-room and weld-finish work is supported through Pegasus's technical desk.",
        ],
        "range": [
            ("Engineer's Files",     "Swiss-pattern, machinist and rotary files — full Pferd portfolio."),
            ("Rotary Burrs",         "Tungsten-carbide and HSS burrs in all cutting geometries."),
            ("Mounted Points",       "Aluminium-oxide and silicon-carbide mounted points."),
            ("Cut-Off & Grinding",   "Bonded discs in 115mm to 230mm — steel, stainless and aluminium."),
            ("Flap Discs",           "Zirconia, ceramic and Polifan flap-disc range."),
            ("Diamond & CBN Tools",  "Plated and resin-bond diamond and CBN finishing tools."),
        ],
        "catalogues": [
            ("Catalogue 2025", "Tool Master Volume","Files · Burrs · Points · Wheels","356"),
            ("Brochure",       "Polifan Flap Discs","Premium finishing range",         "44"),
            ("Datasheet",      "Tungsten-Carbide Burrs","Die-maker reference",         "28"),
            ("Reference",      "Surface-Finish Guide","Ra-target selection table",     "24"),
        ],
    },
    {
        "slug": "superflex", "name": "Super Flex", "cat": "abrasive", "logo": "superflex.png",
        "established": "1985", "origin": "South Africa", "since": "2013",
        "tagline": "Locally-manufactured cut-off and grinding wheels — Super Flex value-grade abrasives via Pegasus.",
        "lead": "Super Flex manufactures bonded abrasives in South Africa — cut-off, grinding and flap discs aimed at value-tier procurement for mining, construction and general fabrication.",
        "body": [
            "Pegasus stocks Super Flex against bulk and standing-account orders. Local manufacture means short lead-times and BBBEE-friendly procurement for state-aligned clients.",
            "EN12413-compliant batch documentation ships with every consignment.",
        ],
        "range": [
            ("Cut-Off Wheels",  "115mm – 230mm thin cut-off discs for steel and stainless."),
            ("Grinding Discs",  "6mm depressed-centre grinding wheels."),
            ("Flap Discs",      "Zirconia flap discs across grit ranges."),
            ("Wire Brushes",    "Cup, wheel and end-brush wire products."),
            ("Diamond Blades",  "General-purpose diamond blades for concrete and brick."),
            ("Specials",        "Custom labelling and packaging for resale clients."),
        ],
        "catalogues": [
            ("Catalogue 2025", "Bonded Abrasives", "Cut-off · Grinding · Flap",  "48"),
            ("Brochure",       "Diamond Blades",   "Concrete and masonry range", "16"),
            ("Datasheet",      "EN12413",          "Compliance reference",       "8"),
            ("Reference",      "Wheel Selection",  "Application guide",          "12"),
        ],
    },

    # ── Power Tools ────────────────────────────────────────────────────────
    {
        "slug": "hikoki", "name": "Hikoki", "cat": "power-tools", "logo": "hikoki.png",
        "established": "1948", "origin": "Japan", "since": "2018",
        "tagline": "Japanese precision power tools — formerly Hitachi Koki, Hikoki tools supplied through Pegasus.",
        "lead": "Hikoki (the rebranded Hitachi Koki) builds professional-grade corded and cordless power tools in Japan — drills, drivers, grinders, saws and the MultiVolt 36V/18V slide platform.",
        "body": [
            "Pegasus stocks the Hikoki tradesman range with commissioning and warranty support. Cordless platforms are bundled as bare-tool, kit and combo options.",
            "Service is handled through Pegasus's workshop network in Boksburg — same-day spares on common consumables.",
        ],
        "range": [
            ("Cordless Drill / Driver","18V and 36V MultiVolt drills, impact drivers and rotary hammers."),
            ("Angle Grinders",         "Corded and cordless grinders 115mm – 230mm."),
            ("Saws",                   "Circular, recip, mitre and jigsaws — corded and cordless."),
            ("Rotary Hammers",         "SDS-plus and SDS-max rotary hammers for masonry and concrete."),
            ("Demolition Hammers",     "Chipping hammers and breakers for site work."),
            ("Combo Kits",             "MultiVolt 4- and 6-tool combo bundles with batteries and charger."),
        ],
        "catalogues": [
            ("Catalogue 2025", "Power Tools Master",  "Corded · Cordless · MultiVolt", "212"),
            ("Brochure",       "MultiVolt Platform",  "18V / 36V slide system",        "32"),
            ("Datasheet",      "SDS Hammers",         "Rotary and demolition range",   "16"),
            ("Reference",      "Warranty & Spares",   "Service network guide",         "12"),
        ],
    },
    {
        "slug": "milwaukee", "name": "Milwaukee", "cat": "power-tools", "logo": "milwaukee.png",
        "established": "1924", "origin": "USA", "since": "2014",
        "tagline": "US heavy-duty power tools — Milwaukee M18 FUEL cordless platform supplied by Pegasus.",
        "lead": "Milwaukee Tool builds heavy-duty professional power tools in Brookfield, Wisconsin — best known for the M18 FUEL cordless platform and Packout modular storage.",
        "body": [
            "Pegasus stocks the Milwaukee M18 and M12 cordless range with full kit, bare-tool and combo options. Packout storage, hand tools and personal lighting are sold alongside.",
            "Trade accounts cover bulk M18 battery and charger orders for site crews and mine maintenance teams.",
        ],
        "range": [
            ("M18 FUEL Cordless",    "Brushless 18V drills, impact drivers, grinders and saws."),
            ("M12 Sub-Compact",      "12V tools for trim work, electrical and HVAC trades."),
            ("Packout Storage",      "Modular toolboxes, organisers and trolleys."),
            ("Heavy-Duty Corded",    "Magnetic drill presses, breakers and core drills."),
            ("Hand Tools",           "Knives, pliers, tape measures and torque wrenches."),
            ("Personal Lighting",    "Cordless and rechargeable site lights and head torches."),
        ],
        "catalogues": [
            ("Catalogue 2025", "M18 FUEL Range",     "Cordless platform master",     "284"),
            ("Brochure",       "Packout Storage",    "Modular system",                "44"),
            ("Datasheet",      "M12 Sub-Compact",    "12V trade-tool range",          "24"),
            ("Reference",      "Battery Platform",   "RedLithium technology",         "16"),
        ],
    },

    # ── Safety & PPE ───────────────────────────────────────────────────────
    {
        "slug": "bestway", "name": "Bestway", "cat": "safety", "logo": "bestway.png",
        "established": "1992", "origin": "South Africa", "since": "2014",
        "tagline": "South African PPE specialist — Bestway helmets, harnesses and protective footwear supplied by Pegasus.",
        "lead": "Bestway manufactures and distributes a broad PPE range in South Africa — hard hats, fall-arrest harnesses, hi-vis garments and protective footwear to SANS and EN standards.",
        "body": [
            "Pegasus carries Bestway against trade accounts for mining, construction and contractor clients. Bulk and contract-pack pricing available.",
            "All harnesses and lanyards are SANS50361-compliant with batch documentation supplied per consignment.",
        ],
        "range": [
            ("Hard Hats",         "Type-1 and Type-2 helmets to SANS1397."),
            ("Fall-Arrest",       "Harnesses, lanyards and shock absorbers to SANS50361."),
            ("Hi-Vis Garments",   "Class-2 reflective vests, jackets and bibs."),
            ("Safety Footwear",   "Steel- and composite-toe boots to SANS20345."),
            ("Eye Protection",    "Spectacles, goggles and chemical splash visors."),
            ("Hand Protection",   "General-purpose and chemical-resistant gloves."),
        ],
        "catalogues": [
            ("Catalogue 2025", "PPE Master",      "Head · Body · Hand · Foot",  "120"),
            ("Brochure",       "Fall-Arrest",     "Harness and lanyard range",  "32"),
            ("Datasheet",      "Hard Hat",        "SANS1397 compliance",        "12"),
            ("Reference",      "PPE Standards",   "SANS / EN cross-reference",  "20"),
        ],
    },
    {
        "slug": "bova", "name": "Bova", "cat": "safety", "logo": "bova.png",
        "established": "1976", "origin": "South Africa", "since": "2013",
        "tagline": "South African safety footwear OEM — Bova boots manufactured locally, on the shelf at Pegasus.",
        "lead": "Bova is one of South Africa's largest safety-footwear manufacturers — locally produced boots, shoes and gumboots to SANS20345 for mining, industrial and construction wear.",
        "body": [
            "Pegasus stocks the Bova range with bulk pricing for site standing-account customers. Sizing kits and try-on stock can be arranged for procurement teams.",
            "BBBEE-friendly local-content procurement makes Bova a default specification for state-aligned and EPC projects.",
        ],
        "range": [
            ("Steel-Toe Boots",  "Standard work boots to SANS20345 SB / S1P / S3."),
            ("Composite Toe",    "Non-metallic safety footwear for electrical and airport work."),
            ("Metatarsal Range", "External-met-guard boots for high-impact applications."),
            ("Gumboots",         "Steel- and composite-toe PVC gumboots."),
            ("Heat-Resistant",   "Foundry, smelter and high-temperature footwear."),
            ("Specialist Boots", "Chainsaw, snake-protection and high-leg variants."),
        ],
        "catalogues": [
            ("Catalogue 2025", "Safety Footwear",  "Full Bova range",            "76"),
            ("Brochure",       "Heat-Resistant",   "Foundry and smelter range",  "20"),
            ("Datasheet",      "SANS20345",        "Footwear standards guide",   "12"),
            ("Reference",      "Sizing Guide",     "Procurement sizing tables",  "8"),
        ],
    },
    {
        "slug": "drager", "name": "Drager", "cat": "safety", "logo": "drager.png",
        "established": "1889", "origin": "Germany", "since": "2013",
        "tagline": "Dräger respiratory and gas-detection technology — Lübeck-engineered safety kit supplied through Pegasus.",
        "lead": "Dräger has manufactured respiratory protection, gas detection and rescue equipment in Lübeck since 1889 — the global default specification across mining, oil-and-gas and industrial safety.",
        "body": [
            "Pegasus is an approved Dräger reseller across South Africa, supplying SCBAs, escape sets, gas monitors and the full respirator filter range with Lübeck-traceable documentation.",
            "Calibration, service and bump-test support for Dräger gas monitors is handled in-house at Boksburg.",
        ],
        "range": [
            ("Self-Contained Breathing Apparatus","PSS-series SCBAs for fire and confined-space rescue."),
            ("Escape Sets",                "Saver PP escape hoods for mining and confined-space exit."),
            ("Gas Detection",              "X-am 2500/5000/8000 portable gas monitors."),
            ("Respirators & Filters",      "Half-mask, full-mask and powered-air respirators."),
            ("Fixed Gas Monitoring",       "Polytron series for hazardous-area fixed monitoring."),
            ("Calibration & Service",      "On-site bump-test, calibration and service through Pegasus."),
        ],
        "catalogues": [
            ("Catalogue 2025", "Personal Protection","SCBAs · Escape · Respirators","148"),
            ("Brochure",       "Gas Detection",     "X-am portable monitors",      "44"),
            ("Datasheet",      "Polytron Fixed",    "Hazardous-area monitoring",   "28"),
            ("Reference",      "Service Manual",    "Maintenance schedule guide",  "32"),
        ],
    },
    {
        "slug": "dupont", "name": "DuPont", "cat": "safety", "logo": "dupont.png",
        "established": "1802", "origin": "USA", "since": "2014",
        "tagline": "DuPont protective fabrics — Tyvek, Tychem and Kevlar PPE supplied by Pegasus.",
        "lead": "DuPont Personal Protection manufactures the technical fabrics that protect against chemical, biological and high-energy hazards — Tyvek for particulate, Tychem for chemical, Kevlar and Nomex for cut and flame protection.",
        "body": [
            "Pegasus distributes the DuPont coverall range for mining, petrochemical and industrial-cleaning clients. Bulk procurement and contract-pack options available.",
            "All coveralls ship with EN ISO 13982-1 / 13034 compliance trace for hazardous-area work.",
        ],
        "range": [
            ("Tyvek Coveralls",   "Particulate and limited liquid-splash protection — disposable PPE."),
            ("Tychem Range",      "Chemical-resistant coveralls across hazard categories."),
            ("Kevlar Cut Gloves", "Cut-resistant gloves to EN388 standards."),
            ("Nomex Flame-Resistant","FR garments for arc-flash and flash-fire protection."),
            ("Accessories",       "Shoe covers, sleeves, aprons and overboots."),
            ("Specialist PPE",    "Asbestos, lead and biohazard coveralls for remediation work."),
        ],
        "catalogues": [
            ("Catalogue 2025", "Personal Protection","Tyvek · Tychem · Nomex",     "112"),
            ("Brochure",       "Chemical Resistance","Tychem hazard guide",        "44"),
            ("Datasheet",      "EN ISO 13982-1",    "Type 5/6 coverall standards", "16"),
            ("Reference",      "Fabric Selection",  "Hazard matrix",               "24"),
        ],
    },
    {
        "slug": "elvex", "name": "Elvex", "cat": "safety", "logo": "elvex.png",
        "established": "1979", "origin": "USA", "since": "2015",
        "tagline": "Elvex hearing protection and chainsaw safety wear — US-engineered PPE through Pegasus.",
        "lead": "Elvex manufactures hearing protection, chainsaw safety gear, eye protection and laser-safety eyewear — engineered specifically for high-noise, high-cut and visual-hazard environments.",
        "body": [
            "Pegasus supplies the Elvex range to mining, forestry and industrial-maintenance clients. Custom-moulded earplug fitment available on request.",
            "Trade accounts include bulk earmuff and earplug consumable orders for shutdown crews.",
        ],
        "range": [
            ("Earmuffs",           "Passive and electronic earmuffs across NRR ratings."),
            ("Earplugs",           "Disposable foam, reusable silicone and custom-moulded plugs."),
            ("Chainsaw Trousers",  "Cut-resistant trousers to EN381 standards."),
            ("Safety Eyewear",     "Impact spectacles, OTG, sealed goggles and laser eyewear."),
            ("Face Shields",       "Visors and full-face shields for grinding and chemical work."),
            ("Welding Helmets",    "Auto-darkening and passive welding helmets."),
        ],
        "catalogues": [
            ("Catalogue 2025", "Safety Master",     "Hearing · Eye · Cut · Visor", "88"),
            ("Brochure",       "Hearing Protection","NRR-rated muff and plug range","32"),
            ("Datasheet",      "Chainsaw Safety",   "EN381 compliance",            "16"),
            ("Reference",      "Eyewear Standards", "ANSI Z87 / EN166",            "12"),
        ],
    },
    {
        "slug": "javlin", "name": "Javlin Workwear", "cat": "safety", "logo": "javlin.png",
        "established": "1995", "origin": "South Africa", "since": "2013",
        "tagline": "Locally manufactured workwear — Javlin overalls, conti-suits and contractor uniforms supplied by Pegasus.",
        "lead": "Javlin Workwear is a South African manufacturer of two-piece conti-suits, boilersuits, dust coats and contractor uniforms in poly-cotton and 100% cotton fabrics.",
        "body": [
            "Pegasus carries Javlin workwear stock against contractor and mine standing accounts. Custom branding, embroidery and contract sizing available.",
            "Local manufacture means short lead-times on bulk and BBBEE-friendly procurement for state-aligned clients.",
        ],
        "range": [
            ("Conti-Suit (Two-Piece)","Trouser + jacket workwear in poly-cotton across colour range."),
            ("Boilersuits",          "Single-piece work overalls — cotton and poly-cotton."),
            ("Dust Coats",           "Lab and warehouse dust coats."),
            ("Hi-Vis Range",         "Reflective conti-suits, vests and jackets."),
            ("Contractor Uniforms",  "Branded uniform programmes for site contractors."),
            ("Custom Branding",      "Embroidery, screen-print and heat-transfer branding service."),
        ],
        "catalogues": [
            ("Catalogue 2025", "Workwear Master",  "Conti · Overalls · Coats", "56"),
            ("Brochure",       "Hi-Vis Range",     "Reflective garments",      "20"),
            ("Datasheet",      "Fabric Guide",     "Cotton blends explained",  "10"),
            ("Reference",      "Branding Service", "Embroidery and print specs","12"),
        ],
    },
    {
        "slug": "jonsson", "name": "Jonsson Workwear", "cat": "safety", "logo": "jonsson.png",
        "established": "1873", "origin": "South Africa", "since": "2013",
        "tagline": "Jonsson Workwear — 150-year-old South African workwear manufacturer supplied through Pegasus.",
        "lead": "Founded in 1873, Jonsson Workwear is South Africa's oldest workwear manufacturer — designing and producing premium boilersuits, conti-suits, FR garments and corporate workwear.",
        "body": [
            "Pegasus supplies Jonsson against trade and contract accounts for mining, petrochemical and EPC clients. Custom branding, FR fabrics and contractor uniform programmes managed in-house.",
            "Local manufacture, BBBEE compliance and long-standing OEM heritage make Jonsson a default specification for state-aligned procurement.",
        ],
        "range": [
            ("Conti-Suits",          "Premium poly-cotton and 100%-cotton two-piece workwear."),
            ("Boilersuits",          "Single-piece overalls for general and mining duty."),
            ("Flame-Resistant Range","FR coveralls and conti-suits to EN ISO 11612."),
            ("Acid-Resistant",       "Acid-splash garments for chemical and battery duty."),
            ("Hi-Vis Garments",      "Reflective conti-suits, jackets and bibs."),
            ("Corporate Workwear",   "Branded uniform programmes for site crews and offices."),
        ],
        "catalogues": [
            ("Catalogue 2025", "Workwear Master",    "Conti · Boilersuit · FR · Acid","160"),
            ("Brochure",       "Flame-Resistant",    "FR fabrics and EN compliance",  "48"),
            ("Datasheet",      "Acid-Resistant",     "Chemical-splash protection",    "16"),
            ("Reference",      "Sizing & Branding",  "Procurement reference",         "20"),
        ],
    },
    {
        "slug": "kaliber", "name": "Kaliber", "cat": "safety", "logo": "kaliber.png",
        "established": "2008", "origin": "South Africa", "since": "2014",
        "tagline": "Kaliber safety footwear — locally distributed boots for industrial, mining and contractor wear via Pegasus.",
        "lead": "Kaliber distributes a broad safety-footwear range in South Africa — steel-toe boots, composite-toe boots and gumboots aimed at value-tier procurement.",
        "body": [
            "Pegasus stocks the Kaliber range against bulk and standing-account orders. Sizing kits available for procurement teams.",
            "All footwear is SANS20345-rated with batch documentation per consignment.",
        ],
        "range": [
            ("Steel-Toe Boots",   "Standard work boots to SANS20345 SB / S1P / S3."),
            ("Composite Toe",     "Non-metallic safety boots for electrical work."),
            ("Gumboots",          "PVC safety gumboots — steel-toe and plain."),
            ("Chukka Range",      "Lightweight chukka-style work shoes."),
            ("Hiker Range",       "High-leg lace-up hikers for mining and outdoor duty."),
            ("Specialist Boots",  "Heat-resistant and chemical-resistant footwear."),
        ],
        "catalogues": [
            ("Catalogue 2025", "Safety Footwear", "Full Kaliber range",   "44"),
            ("Brochure",       "Mining Range",    "High-leg and metatarsal","16"),
            ("Datasheet",      "SANS20345",       "Compliance overview",  "10"),
            ("Reference",      "Sizing Guide",    "Fitment tables",       "8"),
        ],
    },
    {
        "slug": "karam", "name": "Karam", "cat": "safety", "logo": "karam.png",
        "established": "1996", "origin": "India", "since": "2015",
        "tagline": "Fall-arrest and height-safety specialist — Karam harnesses, lanyards and lifelines supplied by Pegasus.",
        "lead": "Karam is one of the largest fall-protection manufacturers globally — full-body harnesses, energy-absorbing lanyards, self-retracting lifelines and rescue systems to EN, ANSI and CE standards.",
        "body": [
            "Pegasus distributes the Karam range across South African mining, construction and EPC clients. Rescue-system specification and rope-access kit available on project bid.",
            "Trade accounts cover bulk harness orders for shutdown crews with full EN361 / EN363 compliance trace.",
        ],
        "range": [
            ("Full-Body Harnesses","Standard and specialised harnesses — front, rear and side D-rings."),
            ("Lanyards",          "Single, twin-leg, energy-absorbing and adjustable lanyards."),
            ("SRLs",              "Self-retracting lifelines — webbing and cable platforms."),
            ("Anchorage Devices", "Temporary and permanent anchor points and lifeline systems."),
            ("Confined Space",    "Tripods, winches and rescue kit for confined-space entry."),
            ("Rescue Equipment",  "Descent devices and emergency-rescue systems."),
        ],
        "catalogues": [
            ("Catalogue 2025", "Height Safety Master","Harnesses · Lanyards · SRLs","176"),
            ("Brochure",       "Rescue Systems",    "Confined-space and rope access","40"),
            ("Datasheet",      "EN361 / EN363",     "Fall-arrest standards",         "16"),
            ("Reference",      "Inspection Guide",  "Pre-use inspection checklist",  "12"),
        ],
    },
    {
        "slug": "rebel", "name": "Rebel Safety Gear", "cat": "safety", "logo": "rebel.png",
        "established": "1995", "origin": "South Africa", "since": "2014",
        "tagline": "Rebel Safety Gear — South African PPE distributor with the value-tier range, supplied through Pegasus.",
        "lead": "Rebel Safety Gear is a South African PPE distributor with a broad value-tier range — gloves, eyewear, hard hats and hi-vis garments aimed at high-volume procurement.",
        "body": [
            "Pegasus carries Rebel against bulk standing-account orders for contractor and mine clients. Local stock means short lead-times on common PPE consumables.",
            "All garments and PPE ship with SANS compliance trace where applicable.",
        ],
        "range": [
            ("Work Gloves",     "Cotton, leather, latex-coated and nitrile-coated glove range."),
            ("Eye Protection",  "Spectacles, goggles and visors to SANS / EN166."),
            ("Hard Hats",       "Type-1 and Type-2 hard hats to SANS1397."),
            ("Hi-Vis Garments", "Reflective vests, bibs and jackets."),
            ("Ear Protection",  "Disposable plugs and basic earmuffs."),
            ("Wet-Weather Gear","PVC rain jackets, trousers and suits."),
        ],
        "catalogues": [
            ("Catalogue 2025", "PPE Master",       "Head · Eye · Hand · Body",   "92"),
            ("Brochure",       "Glove Range",      "Coated and uncoated options","28"),
            ("Datasheet",      "Hard Hat",         "SANS1397 compliance",        "8"),
            ("Reference",      "PPE Procurement",  "Bulk-buy guide",             "12"),
        ],
    },
    {
        "slug": "uvex", "name": "Uvex", "cat": "safety", "logo": "uvex.png",
        "established": "1926", "origin": "Germany", "since": "2013",
        "tagline": "Uvex German-engineered eye, head and hand protection — premium PPE supplied through Pegasus.",
        "lead": "Uvex Safety has manufactured precision eyewear, helmets and protective gloves in Fürth since 1926 — a premium PPE specification for industrial, mining and laboratory applications.",
        "body": [
            "Pegasus distributes the Uvex range — pheos spectacles, x-fit goggles, athletik helmets and the C500 / phynomic glove series — with full EN compliance trace.",
            "Custom prescription safety eyewear and laser-safety eyewear can be arranged on request.",
        ],
        "range": [
            ("Safety Spectacles",  "Pheos, sportstyle and i-3 spectacle ranges to EN166."),
            ("Goggles",            "X-fit and ultrasonic goggles — sealed and ventilated."),
            ("Welding Eyewear",    "Welding goggles, masks and auto-darkening helmets."),
            ("Hard Hats",          "Pheos, airwing and athletik helmet platforms."),
            ("Ear Protection",     "K-series earmuffs and com 4-in-1 protectors."),
            ("Protective Gloves",  "Phynomic, profi and C500 cut-protection glove range."),
        ],
        "catalogues": [
            ("Catalogue 2025", "Personal Protection","Eye · Head · Hand · Ear",      "168"),
            ("Brochure",       "Eyewear Master",    "Spectacles and goggles",       "56"),
            ("Datasheet",      "Cut-Protection",    "Phynomic glove range",         "20"),
            ("Reference",      "EN Standards",      "Compliance cross-reference",   "16"),
        ],
    },
    {
        "slug": "vulcan", "name": "Vulcan Workwear", "cat": "safety", "logo": "vulcan.png",
        "established": "1988", "origin": "South Africa", "since": "2014",
        "tagline": "South African workwear manufacturer — Vulcan boilersuits, conti-suits and FR garments via Pegasus.",
        "lead": "Vulcan Workwear is a South African manufacturer of two-piece conti-suits, boilersuits and FR-treated workwear for mining, petrochemical and EPC clients.",
        "body": [
            "Pegasus stocks Vulcan against contractor and mine standing accounts. Custom branding, sizing and FR-fabric options available.",
            "BBBEE-friendly local procurement with bulk and contract-pack pricing.",
        ],
        "range": [
            ("Conti-Suits",       "Two-piece poly-cotton conti-suits across colour range."),
            ("Boilersuits",       "Single-piece overalls — cotton and poly-cotton."),
            ("FR Workwear",       "Flame-resistant conti-suits to EN ISO 11612."),
            ("Acid-Resistant",    "Acid-splash garments for chemical work."),
            ("Hi-Vis Range",      "Reflective garments to EN20471."),
            ("Branding Service",  "Embroidery and screen-print branding."),
        ],
        "catalogues": [
            ("Catalogue 2025", "Workwear Master", "Conti · Boilersuit · FR", "64"),
            ("Brochure",       "FR Range",        "Flame-resistant garments","28"),
            ("Datasheet",      "Fabric Guide",    "Blends and treatments",   "12"),
            ("Reference",      "Branding Specs",  "Custom uniform service",  "10"),
        ],
    },
    {
        "slug": "wayne", "name": "Wayne", "cat": "safety", "logo": "wayne.png",
        "established": "1990", "origin": "South Africa", "since": "2015",
        "tagline": "Wayne safety footwear — South African boot specialist supplied by Pegasus.",
        "lead": "Wayne Safety Footwear is a South African distributor of work boots, gumboots and protective footwear across the mining, construction and warehouse sectors.",
        "body": [
            "Pegasus carries the Wayne range against bulk and contract orders. Sizing kits available for procurement teams.",
            "All footwear is SANS20345-rated with documentation per consignment.",
        ],
        "range": [
            ("Steel-Toe Boots",  "Standard work boots — SB / S1P / S3 ratings."),
            ("Composite Toe",    "Non-metallic safety footwear."),
            ("Metatarsal Boots", "External-met-guard footwear for high-impact work."),
            ("Gumboots",         "PVC and rubber safety gumboots."),
            ("Hikers",           "High-leg lace-up safety hikers."),
            ("Heat-Resistant",   "Foundry and high-temperature footwear."),
        ],
        "catalogues": [
            ("Catalogue 2025", "Safety Footwear",  "Wayne range overview", "40"),
            ("Brochure",       "Mining Footwear",  "High-leg and metatarsal","16"),
            ("Datasheet",      "SANS20345",        "Compliance reference", "10"),
            ("Reference",      "Sizing Guide",     "Procurement tables",   "8"),
        ],
    },

    # ── Hand Tools ─────────────────────────────────────────────────────────
    {
        "slug": "gedore", "name": "Gedore", "cat": "hand-tools", "logo": "gedore.png",
        "established": "1919", "origin": "Germany", "since": "2013",
        "tagline": "Gedore German precision hand tools — Remscheid-engineered spanners, sockets and torque wrenches via Pegasus.",
        "lead": "Gedore has manufactured precision hand tools in Remscheid since 1919 — a default specification across German automotive, aerospace and heavy-engineering workshops.",
        "body": [
            "Pegasus stocks the Gedore range across spanners, sockets, torque wrenches and assembly kits. Calibration and recertification of torque tools handled in-house.",
            "Trade accounts include OEM-spec maintenance toolkits for mine and contractor workshops.",
        ],
        "range": [
            ("Spanners",         "Combination, double-ended and ring spanners — DIN 3110 / 3113."),
            ("Sockets",          "1/4\", 3/8\", 1/2\", 3/4\", 1\" drive sockets and accessories."),
            ("Torque Wrenches",  "Click and electronic torque wrenches with calibration certs."),
            ("Pliers & Cutters", "VDE-insulated and standard pliers, side-cutters and snips."),
            ("Screwdrivers",     "Slotted, Phillips, Pozidriv, Torx and VDE-insulated drivers."),
            ("Toolkits",         "Pre-packed and custom maintenance toolkits in steel boxes."),
        ],
        "catalogues": [
            ("Catalogue 2025", "Hand Tools Master","Spanners · Sockets · Drivers", "356"),
            ("Brochure",       "Torque Range",     "Click and electronic wrenches","48"),
            ("Datasheet",      "VDE Insulated",    "Electrical safety tools",      "24"),
            ("Reference",      "Calibration",      "Torque-tool service guide",    "16"),
        ],
    },
    {
        "slug": "groz", "name": "Groz", "cat": "hand-tools", "logo": "groz.png",
        "established": "1968", "origin": "India", "since": "2014",
        "tagline": "Groz precision hand tools — Indian-manufactured engineer's tools and workshop equipment supplied by Pegasus.",
        "lead": "Groz manufactures precision hand tools, measuring instruments and workshop equipment for engineers, machinists and toolmakers — a value-tier alternative to premium European brands.",
        "body": [
            "Pegasus stocks the Groz range across measuring tools, clamps, vices and workshop equipment. Bulk and standing-account pricing for contractor and trade clients.",
            "All measuring tools ship with calibration documentation where applicable.",
        ],
        "range": [
            ("Measuring Tools",  "Vernier callipers, micrometers, height gauges and protractors."),
            ("Clamps & Vices",   "Bench vices, drill-press vices, C-clamps and quick-grip clamps."),
            ("Punches & Chisels","Pin, taper and centre punches; cold and brick chisels."),
            ("Pliers & Cutters", "Standard pliers, side-cutters and tin-snips."),
            ("Files",            "Engineer's, machinist's and Swiss-pattern files."),
            ("Workshop Equipment","Workbenches, tool trolleys and tool chests."),
        ],
        "catalogues": [
            ("Catalogue 2025", "Hand Tools Master","Measuring · Clamps · Files",   "240"),
            ("Brochure",       "Measuring Tools",  "Callipers and micrometers",    "44"),
            ("Datasheet",      "Workshop Vices",   "Bench and drill-press range",  "20"),
            ("Reference",      "Calibration Service","Measuring tool support",     "12"),
        ],
    },
    {
        "slug": "matus", "name": "Matus", "cat": "hand-tools", "logo": "matus.png",
        "established": "2000", "origin": "South Africa", "since": "2018",
        "tagline": "Matus general-purpose hand tools — value-tier toolkit and spanner sets via Pegasus.",
        "lead": "Matus distributes general-purpose hand tools across South Africa — toolkits, spanner sets, sockets and basic workshop tools aimed at value-tier procurement.",
        "body": [
            "Pegasus stocks Matus against contractor and bulk-buy standing-account orders. Local distribution means short lead-times on toolkits and consumables.",
            "BBBEE-friendly procurement available for state-aligned clients.",
        ],
        "range": [
            ("Toolkits",         "Multi-piece toolkits in steel cases — popular sizes always in stock."),
            ("Socket Sets",      "1/4\", 3/8\" and 1/2\" drive socket sets."),
            ("Spanner Sets",     "Combination spanner sets — metric and imperial."),
            ("Screwdriver Sets", "Standard and precision screwdriver sets."),
            ("Plier Sets",       "Combination plier and cutter sets."),
            ("Hammers",          "Claw, ball-pein, rubber and lump hammers."),
        ],
        "catalogues": [
            ("Catalogue 2025", "Hand Tools",      "Toolkits and sets",      "44"),
            ("Brochure",       "Socket Sets",     "Drive sizes overview",   "16"),
            ("Datasheet",      "Toolkit Contents","Standard kit list",      "8"),
            ("Reference",      "Procurement",     "Bulk-buy guide",         "10"),
        ],
    },
    {
        "slug": "mts", "name": "MTS", "cat": "hand-tools", "logo": "mts.png",
        "established": "2002", "origin": "South Africa", "since": "2019",
        "tagline": "MTS toolkit and general hand-tool distributor — supplied to South African contractors via Pegasus.",
        "lead": "MTS distributes general-purpose hand tools and toolkits across South Africa, supplying contractors, workshops and resale clients with value-tier procurement.",
        "body": [
            "Pegasus stocks the MTS range against bulk and standing-account orders. Custom packaging and contract-pack options available.",
            "Short lead-times on common toolkit configurations.",
        ],
        "range": [
            ("Toolkits",         "Multi-piece toolkits in plastic and steel cases."),
            ("Socket Sets",      "1/4\", 3/8\" and 1/2\" drive sockets and accessories."),
            ("Spanner Sets",     "Metric and imperial spanner sets."),
            ("Screwdriver Sets", "Slotted, Phillips and precision driver sets."),
            ("Plier Sets",       "Combination plier and cutter sets."),
            ("Tape Measures",    "5m, 8m and 10m tape measures."),
        ],
        "catalogues": [
            ("Catalogue 2025", "Hand Tools",      "Full MTS range",  "36"),
            ("Brochure",       "Toolkits",        "Kit configurations","14"),
            ("Datasheet",      "Tool Reference",  "Sizing tables",    "8"),
            ("Reference",      "Procurement",     "Bulk-buy options", "10"),
        ],
    },
    {
        "slug": "stanley", "name": "Stanley", "cat": "hand-tools", "logo": "stanley.png",
        "established": "1843", "origin": "USA", "since": "2013",
        "tagline": "Stanley hand tools — 180-year-old US workhorse brand from tape measures to knives via Pegasus.",
        "lead": "Stanley has manufactured hand tools since 1843 — tape measures, hammers, knives, hand planes and screwdrivers that are default specification on every contractor's toolkit.",
        "body": [
            "Pegasus stocks Stanley across the FatMax, Tradesman and standard ranges. Bulk and standing-account orders for contractor and EPC clients.",
            "Trade-account customers benefit from FatMax tool guarantees and the Stanley warranty network.",
        ],
        "range": [
            ("Tape Measures",   "FatMax, Tradesman and standard tape measures — 3m to 10m."),
            ("Hammers",         "Claw, ball-pein, lump and engineer's hammers."),
            ("Knives & Blades", "Trimming knives and replacement blades — FatMax retractable range."),
            ("Hand Planes",     "Bailey-pattern hand planes for joinery and finishing."),
            ("Screwdrivers",    "FatMax screwdriver sets and individual drivers."),
            ("Storage",         "Toolboxes, organisers and mobile tool chests."),
        ],
        "catalogues": [
            ("Catalogue 2025", "Hand Tools Master","FatMax · Tradesman · Standard","192"),
            ("Brochure",       "Knives & Blades", "Trimming and utility range",   "28"),
            ("Datasheet",      "Tape Measures",   "FatMax range specifications",  "16"),
            ("Reference",      "Warranty Network","Guarantee and service guide",  "12"),
        ],
    },
    {
        "slug": "wera", "name": "Wera", "cat": "hand-tools", "logo": "wera.png",
        "established": "1936", "origin": "Germany", "since": "2015",
        "tagline": "Wera Tool Rebels — German-engineered screwdrivers, bits and ratchets via Pegasus.",
        "lead": "Wera Werkzeuge has manufactured screwdrivers, bits and torque tools in Wuppertal since 1936 — the Tool Rebels brand engineered for precision, ergonomics and idiosyncratic colour-coded tooling.",
        "body": [
            "Pegasus stocks the Wera range — Kraftform screwdrivers, the Zyklop ratchet platform, the Joker spanner range and the full Belt bit set.",
            "Trade accounts include OEM-spec maintenance toolkits and Wera's lifetime guarantee on most product lines.",
        ],
        "range": [
            ("Kraftform Screwdrivers", "Ergonomic screwdrivers with patented multi-component grips."),
            ("Bit Range",              "Bit holders, bit sets and the Bit-Check series."),
            ("Zyklop Ratchets",        "Pivoting-head ratchets across 1/4\" – 1/2\" drive."),
            ("Joker Spanners",         "Hybrid open-end ratcheting spanners."),
            ("Torque Tools",           "Adjustable, fixed and preset-torque screwdrivers and wrenches."),
            ("Allen Keys",             "Hex-Plus L-keys and folding hex sets — colour-coded."),
        ],
        "catalogues": [
            ("Catalogue 2025", "Tool Rebels Master","Kraftform · Zyklop · Joker",  "320"),
            ("Brochure",       "Bit Range",        "Bit holders and sets",         "44"),
            ("Datasheet",      "Joker Spanners",   "Hybrid ratcheting range",      "20"),
            ("Reference",      "Lifetime Guarantee","Warranty and exchange policy","12"),
        ],
    },

    # ── Electrical ─────────────────────────────────────────────────────────
    {
        "slug": "truco", "name": "Truco", "cat": "electrical", "logo": "truco.png",
        "established": "1982", "origin": "South Africa", "since": "2013",
        "tagline": "Truco industrial hose and bellows manufacturer — South African OEM for petroleum, PVC, rubber and composite hose via Pegasus.",
        "lead": "Truco manufactures industrial hoses, bellows and ducting in South Africa — petroleum composite hose, rubber bellows, small-bore PVC and rubber hose for mining, petrochemical and water-handling applications.",
        "body": [
            "Pegasus stocks Truco against standing-account orders for mine slimes, dewatering and petroleum-handling clients. Custom fittings, lengths and crimping handled in-house at Boksburg.",
            "Local manufacture and BBBEE-friendly procurement make Truco a default specification for state-aligned and mining EPC projects.",
        ],
        "range": [
            ("Petroleum Composite Hose","Bulk fuel transfer hose — diesel, petrol and aviation fuel duty."),
            ("Rubber Bellows",          "Expansion joints and pump-connection bellows."),
            ("Small-Bore PVC Hose",     "Clear and reinforced PVC hose for water and air."),
            ("Small-Bore Rubber Hose",  "Air, water and oil rubber hose — standard and abrasion-resistant."),
            ("Industrial Ducting",      "Flexible ducting for fume, dust and gas extraction."),
            ("Custom Assemblies",       "Crimped and clamped hose assemblies to drawing."),
        ],
        "catalogues": [
            ("Catalogue 2025", "Industrial Hose Master","Petroleum · Rubber · PVC",   "108"),
            ("Brochure",       "Rubber Bellows",       "Pump connection range",      "32"),
            ("Datasheet",      "Petroleum Composite",  "Bulk fuel transfer hose",    "20"),
            ("Reference",      "Hose Assembly Guide",  "Crimping and fitment specs", "16"),
        ],
    },

    # ── Paint Products ─────────────────────────────────────────────────────
    {
        "slug": "ogradys", "name": "O'Grady's Paint", "cat": "paint", "logo": "ogradys.png",
        "established": "1985", "origin": "South Africa", "since": "2013",
        "tagline": "O'Grady's industrial coatings — South African paint manufacturer for mining, marine and structural applications via Pegasus.",
        "lead": "O'Grady's Paint manufactures industrial protective coatings in South Africa — epoxies, polyurethanes, zinc-rich primers and structural-grade enamels for mining, marine and infrastructure work.",
        "body": [
            "Pegasus stocks O'Grady's paints against contractor and EPC standing accounts. Bulk-pack, tinting and specification support available through the technical desk.",
            "Local manufacture means short lead-times on custom colours and BBBEE-friendly procurement.",
        ],
        "range": [
            ("Epoxy Coatings",     "Two-pack epoxy primers, build coats and floor systems."),
            ("Polyurethanes",      "Aliphatic and aromatic polyurethane top-coats."),
            ("Zinc-Rich Primers",  "Inorganic and organic zinc-rich primers for structural steel."),
            ("Enamels",            "Air-dry and stoving enamels for general industrial work."),
            ("Anti-Corrosive",     "Heavy-duty marine and offshore-grade coatings."),
            ("Specialist Systems", "High-temperature, heat-resistant and chemical-resistant coatings."),
        ],
        "catalogues": [
            ("Catalogue 2025", "Industrial Coatings","Epoxy · PU · Zinc · Enamel", "84"),
            ("Brochure",       "Marine Range",      "Offshore-grade systems",     "32"),
            ("Datasheet",      "Zinc-Rich Primers", "Steel-structure protection", "16"),
            ("Reference",      "Specification Guide","System selection matrix",   "20"),
        ],
    },
    {
        "slug": "stoncor", "name": "StonCor Africa", "cat": "paint", "logo": "stoncor.png",
        "established": "1924", "origin": "USA / South Africa", "since": "2014",
        "tagline": "StonCor (Stonhard) industrial flooring and protective lining — chemically resistant floor systems via Pegasus.",
        "lead": "StonCor Africa (part of the global Stonhard / RPM International group) manufactures seamless industrial flooring, chemical-resistant linings and decorative wall systems for food, pharma and heavy-industry sites.",
        "body": [
            "Pegasus supplies StonCor products against project specifications — Stonshield, Stonchem and Stonclad systems with full chemical-resistance trace and Stonhard certified installer network.",
            "On large-area floor projects, Pegasus can manage the StonCor-certified application crew from Boksburg.",
        ],
        "range": [
            ("Stonshield",        "Decorative quartz-broadcast epoxy floor systems."),
            ("Stonclad",          "Heavy-duty industrial epoxy and urethane floor systems."),
            ("Stonchem",          "Chemical-resistant tank linings and floor coatings."),
            ("Stonkote",          "Wall coatings and seamless decorative finishes."),
            ("Stonpark",          "Parking-deck and bridge waterproofing systems."),
            ("Certified Application","Stonhard-certified installer network for project-spec work."),
        ],
        "catalogues": [
            ("Catalogue 2025", "Flooring Master",   "Stonshield · Stonclad · Stonchem","132"),
            ("Brochure",       "Food & Pharma",     "HACCP-compliant flooring",       "44"),
            ("Datasheet",      "Chemical Resistance","Stonchem resistance chart",     "28"),
            ("Reference",      "Application Guide", "Installer certification process","16"),
        ],
    },

    # ── Lubricants & Fuel ──────────────────────────────────────────────────
    {
        "slug": "true-lubricants", "name": "True Lubricants", "cat": "lubricants", "logo": "true-lubricants.png",
        "established": "2005", "origin": "South Africa", "since": "2014",
        "tagline": "True Lubricants — South African industrial lubricants OEM supplying mining, transport and manufacturing via Pegasus.",
        "lead": "True Lubricants manufactures industrial oils, hydraulic fluids and greases in South Africa — engine oils, gear oils, slideway lubricants and mining-grade greases blended to OEM specification.",
        "body": [
            "Pegasus stocks the True Lubricants range against bulk and standing-account orders. Bulk drums, IBC and bulk-road-tanker supply arranged through Boksburg.",
            "OEM cross-references for Caterpillar, Komatsu and major mining-fleet specifications managed in-house.",
        ],
        "range": [
            ("Engine Oils",       "Mining and transport diesel engine oils — API CK-4 / CJ-4."),
            ("Hydraulic Fluids",  "Mineral and zinc-free hydraulic fluids for mobile and industrial duty."),
            ("Gear Oils",         "Industrial and mobile gear lubricants — EP and synthetic ranges."),
            ("Greases",           "Lithium, calcium-sulphonate and MoS₂-fortified greases."),
            ("Slideway Oils",     "Machine-tool slideway lubricants — ISO Vg 32 / 68 / 220."),
            ("Bulk Supply",       "Drum, IBC and road-tanker bulk lubricant supply."),
        ],
        "catalogues": [
            ("Catalogue 2025", "Industrial Lubricants","Engine · Hydraulic · Gear · Grease","144"),
            ("Brochure",       "Mining Range",        "Mining-fleet lubrication specs",      "48"),
            ("Datasheet",      "OEM Cross-Reference", "Caterpillar / Komatsu equivalencies", "32"),
            ("Reference",      "Bulk Supply",         "Drum / IBC / tanker logistics",       "16"),
        ],
    },
]


# ── HTML template ──────────────────────────────────────────────────────────
PAGE_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{name_attr} — Partner Portfolio · Pegasus Engineering &amp; Mining Supplies</title>
<meta name="description" content="{name_attr} — supplied by Pegasus Engineering & Mining Supplies. Full product portfolio and downloadable catalogues.">
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

<header class="header">
  <div class="header-inner">
    <a href="index.html" class="brand" aria-label="Pegasus Engineering & Mining Supplies — Home">
      <img class="logo-emblem" src="assets/brand/logo-emblem-transparent.png" alt="Pegasus Engineering & Mining Supplies">
    </a>
    <nav class="nav-primary" aria-label="Primary">
      <a href="products.html">Products</a>
      <a href="services.html">Services</a>
      <a href="network.html" class="is-active">Network</a>
      <a href="marketplace.html">Marketplace</a>
      <a href="about.html">About</a>
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

<main>

  <div class="partner-breadcrumb">
    <a href="network.html">← Back to Network</a>
    <span class="partner-breadcrumb-sep">·</span>
    <a href="network.html#{cat_anchor}">{cat_label}</a>
  </div>

  <section class="partner-hero">
    <div class="partner-hero-inner">
      <div class="partner-hero-logo">
        <img src="assets/partners/{logo}" alt="{name_attr}">
      </div>
      <div class="partner-hero-text">
        <div class="suphead">Approved Partner · {cat_label}</div>
        <h1 class="partner-hero-title">{name_html}</h1>
        <p class="partner-hero-tagline">{tagline}</p>
        <div class="partner-hero-meta">
          <div class="partner-hero-meta-item">
            <span class="partner-hero-meta-label">Established</span>
            <span class="partner-hero-meta-value">{established}</span>
          </div>
          <div class="partner-hero-meta-item">
            <span class="partner-hero-meta-label">Origin</span>
            <span class="partner-hero-meta-value">{origin}</span>
          </div>
          <div class="partner-hero-meta-item">
            <span class="partner-hero-meta-label">Pegasus Since</span>
            <span class="partner-hero-meta-value">{since}</span>
          </div>
        </div>
      </div>
    </div>
  </section>

  <section class="partner-section">
    <div class="partner-section-inner">
      <div class="partner-overview">
        <div class="partner-overview-side">
          <span class="suphead">Overview</span>
        </div>
        <div class="partner-overview-body">
          <p class="partner-lead">{lead}</p>
          {overview_paragraphs}
        </div>
      </div>
    </div>
  </section>

  <section class="partner-section is-soft">
    <div class="partner-section-inner">
      <div class="partner-section-head">
        <span class="suphead">Product Range</span>
        <h2>What we supply from {name_html}.</h2>
      </div>
      <div class="partner-range">
{range_items}
      </div>
    </div>
  </section>

  <section class="partner-section">
    <div class="partner-section-inner">
      <div class="partner-section-head">
        <span class="suphead">Catalogues &amp; Datasheets</span>
        <h2>Download the full {name_html} library.</h2>
        <p>Latest OEM catalogues, datasheets and reference material. PDFs open in a new tab.</p>
      </div>
      <div class="catalogue-gallery">
{catalogue_items}
      </div>
    </div>
  </section>

  <section class="section is-dark" style="padding:96px 40px;">
    <div class="section-inner" style="text-align:center;">
      <div class="suphead" style="color:var(--c-accent);">Speak to the desk</div>
      <h2 style="color:var(--c-bg);font-size:clamp(28px,3vw,44px);margin:16px auto 24px;max-width:740px;">Specifying {name_html}? Let's get your order on a trade account.</h2>
      <p style="color:rgba(227,227,225,0.85);max-width:560px;margin:0 auto 50px;">Standing accounts, consignment stock, project pricing — we'll set you up against your operational rhythm.</p>
      <a href="contact.html" class="cta-button" style="padding:16px 32px;">Request a Quote</a>
    </div>
  </section>

</main>

<footer class="footer">
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

<script src="assets/nav.js"></script>
<script src="assets/cart.js"></script>
</body>
</html>
"""

RANGE_ITEM_TEMPLATE = """        <div class="partner-range-item">
          <span class="partner-range-num">{num}</span>
          <h4>{title}</h4>
          <p>{desc}</p>
        </div>"""

CATALOGUE_ITEM_TEMPLATE = """        <a class="catalogue-cover" href="{href}" target="_blank" rel="noopener"{download_attr}>
          <div class="catalogue-cover-img">
            <img src="assets/brand/{cover}" alt="{title} — {name_attr}">
          </div>
          <div class="catalogue-cover-overlay"></div>
          <span class="catalogue-cover-badge">{badge}</span>
          <div class="catalogue-cover-meta">
            <span class="catalogue-cover-eyebrow">{eyebrow}</span>
            <h4 class="catalogue-cover-title">{title}</h4>
            <span class="catalogue-cover-sub">{sub}</span>
          </div>
          <div class="catalogue-cover-action" aria-hidden="true">
            <span class="catalogue-cover-btn">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="{icon_path}"/></svg>
              {btn_label}
            </span>
          </div>
        </a>"""

# SVG paths used for the button icon
ICON_DOWNLOAD = "M12 3v13M5 11l7 7 7-7M5 21h14"
ICON_ARROW    = "M5 12h14M13 6l6 6-6 6"


def html_escape_attr(s: str) -> str:
    return s.replace("&", "&amp;").replace('"', "&quot;").replace("<", "&lt;").replace(">", "&gt;")

def html_escape_body(s: str) -> str:
    # Body text — preserve common typographic chars, escape angle brackets and ampersands
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def build_page(brand: dict) -> str:
    cat_key = brand["cat"]
    cat_label = CATEGORIES[cat_key]
    covers = CAT_COVERS[cat_key]

    # Overview paragraphs (skip first; first is the lead)
    overview_html = "\n          ".join(
        f"<p>{html_escape_body(p)}</p>" for p in brand["body"]
    )

    # Range items
    range_html = "\n".join(
        RANGE_ITEM_TEMPLATE.format(
            num=f"{i+1:02d}",
            title=html_escape_body(title),
            desc=html_escape_body(desc),
        )
        for i, (title, desc) in enumerate(brand["range"])
    )

    # Catalogue card — ONE real PDF per brand from CATALOGUE_PDFS, else "Request" card
    pdf_info = CATALOGUE_PDFS.get(brand["slug"])
    cover = covers[0]
    name_attr = html_escape_attr(brand["name"])
    name_body = html_escape_body(brand["name"])

    if pdf_info:
        pdf_filename, pages = pdf_info
        catalogue_html = CATALOGUE_ITEM_TEMPLATE.format(
            href=f"assets/catalogues/{pdf_filename}",
            download_attr=" download",
            cover=cover,
            badge=f"PDF · {pages} pp",
            eyebrow="Product Catalogue",
            title=f"{name_body} Master Catalogue",
            sub=html_escape_body(f"Full {cat_label.lower()} range, datasheets and technical reference"),
            name_attr=name_attr,
            icon_path=ICON_DOWNLOAD,
            btn_label="Download PDF",
        )
    else:
        # No published catalogue — present as "Request via the desk" card
        catalogue_html = CATALOGUE_ITEM_TEMPLATE.format(
            href="contact.html",
            download_attr="",
            cover=cover,
            badge="ON REQUEST",
            eyebrow="Product Literature",
            title=f"{name_body} Reference",
            sub=html_escape_body("Catalogue available on request via the trade desk"),
            name_attr=name_attr,
            icon_path=ICON_ARROW,
            btn_label="Request via Desk",
        )

    return PAGE_TEMPLATE.format(
        name_attr=html_escape_attr(brand["name"]),
        name_html=html_escape_body(brand["name"]),
        cat_anchor=cat_key,
        cat_label=html_escape_body(cat_label),
        logo=brand["logo"],
        tagline=html_escape_body(brand["tagline"]),
        established=html_escape_body(brand["established"]),
        origin=html_escape_body(brand["origin"]),
        since=html_escape_body(brand["since"]),
        lead=html_escape_body(brand["lead"]),
        overview_paragraphs=overview_html,
        range_items=range_html,
        catalogue_items=catalogue_html,
    )


def main():
    for brand in BRANDS:
        path = OUT_DIR / f"partner-{brand['slug']}.html"
        path.write_text(build_page(brand), encoding="utf-8")
        print(f"  wrote {path.name}")
    print(f"\nDone — generated {len(BRANDS)} partner pages.")


if __name__ == "__main__":
    main()
