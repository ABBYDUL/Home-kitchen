from flask import Flask, render_template_string, jsonify, request

app = Flask(__name__)

# ── Menu Data ──────────────────────────────────────────────────────────────────
MENU = {
    "non_veg_rice": {
        "label": "Non-Veg Rice",
        "icon": "🍚",
        "color": "#c0392b",
        "dishes": [
            {"name": "Mutton Biryani", "qty": "1 kg", "price": 140},
            {"name": "Mutton Yakhni Pulao", "qty": "1 kg", "price": 130},
            {"name": "Mutton Tehari with Aloo", "qty": "1 kg", "price": 130},
            {"name": "Chicken Biryani", "qty": "15-18 pieces", "price": 120},
            {"name": "Chicken Pulao with Aloo", "qty": "", "price": 120},
            {"name": "Biriyani Rice", "qty": "1 kg", "price": 50},
            {"name": "Baghare Chawal", "qty": "1 kg", "price": 50},
        ],
    },
    "veg_starters": {
        "label": "Veg Starters",
        "icon": "🥗",
        "color": "#27ae60",
        "dishes": [
            {"name": "Chana Papdi Chaat", "qty": "", "price": 50},
            {"name": "Veg Cutlets", "qty": "12 pieces", "price": 45},
            {"name": "Onion Samosa", "qty": "12 pieces", "price": 35},
            {"name": "Paneer Springrolls", "qty": "12 pieces", "price": 45},
            {"name": "Dahi Vada", "qty": "12 pieces", "price": 25},
            {"name": "Namkeen Dahivada", "qty": "12 pieces", "price": 25},
        ],
    },
    "veg_main": {
        "label": "Veg Main Course",
        "icon": "🫕",
        "color": "#16a085",
        "dishes": [
            {"name": "Paneer Masala", "qty": "", "price": 80},
            {"name": "Methi Malai Mutter", "qty": "", "price": 50},
            {"name": "Chilli Milli Aloo", "qty": "", "price": 50},
            {"name": "Chole", "qty": "", "price": 50},
            {"name": "Dal Fry", "qty": "", "price": 40},
            {"name": "Veg Biryani", "qty": "1 kg", "price": 120},
        ],
    },
    "non_veg_starters": {
        "label": "Non-Veg Starters",
        "icon": "🍗",
        "color": "#e67e22",
        "dishes": [
            {"name": "Mutton Samosa", "qty": "12 pieces", "price": 40},
            {"name": "Beef/Mutton Shami Kebab", "qty": "12 pieces", "price": 50},
            {"name": "Beef/Mutton Resha Kebab", "qty": "12 pieces", "price": 50},
            {"name": "Beef/Mutton Shami Fingers", "qty": "12 pieces", "price": 50},
            {"name": "Chicken Shami Kebab", "qty": "12 pieces", "price": 50},
            {"name": "Chicken Croquets", "qty": "12 pieces", "price": 50},
            {"name": "Chicken Springrolls", "qty": "12 pieces", "price": 45},
            {"name": "Chicken Cutlets", "qty": "12 pieces", "price": 50},
            {"name": "Chicken Tikka Samosa", "qty": "12 pieces", "price": 50},
            {"name": "Chicken Pockets", "qty": "12 pieces", "price": 50},
            {"name": "Chicken Bread Rolls", "qty": "12 pieces", "price": 50},
            {"name": "Chicken Cheese Candy", "qty": "12 pieces", "price": 40},
            {"name": "Chicken 65", "qty": "1 kg", "price": 70},
            {"name": "Chicken Majestic", "qty": "1 kg", "price": 70},
            {"name": "Beef/Mutton Boti (Dry)", "qty": "1 kg", "price": 90},
        ],
    },
    "non_veg_main": {
        "label": "Non-Veg Main Course",
        "icon": "🥘",
        "color": "#8e44ad",
        "dishes": [
            {"name": "Mutton Qeema", "qty": "1 kg", "price": 80},
            {"name": "Mutton Qeema Methi", "qty": "1 kg", "price": 90},
            {"name": "Mutton Qeema Aloo", "qty": "1 kg", "price": 90},
            {"name": "Mutton Thecha", "qty": "1 kg", "price": 80},
            {"name": "Mutton Curry", "qty": "1 kg", "price": 80},
            {"name": "Aloo Gosht (Mutton)", "qty": "1 kg", "price": 90},
            {"name": "Mutton Khichda", "qty": "1 kg", "price": 130},
            {"name": "Mutton Paya", "qty": "1 dozen", "price": 80},
            {"name": "Mutton Nalli Nihari", "qty": "1 kg", "price": 100},
            {"name": "Beef Nihari", "qty": "1 kg", "price": 110},
            {"name": "Dum Ka Gosht (Mutton)", "qty": "1 kg", "price": 90},
            {"name": "Dal Gosht (Mutton)", "qty": "1 kg", "price": 90},
            {"name": "Mutton Raan", "qty": "", "price": 140},
            {"name": "Chicken Korma", "qty": "1 chicken (12 pcs)", "price": 70},
            {"name": "Green Chicken", "qty": "1 chicken (12 pcs)", "price": 70},
            {"name": "Chicken Maharani", "qty": "1 chicken (12 pcs)", "price": 70},
            {"name": "Butter Chicken", "qty": "1 chicken (12 pcs)", "price": 70},
        ],
    },
    "desserts": {
        "label": "Desserts",
        "icon": "🍮",
        "color": "#d35400",
        "dishes": [
            {"name": "Baked Yoghurt", "qty": "per cup", "price": 5},
            {"name": "Gulab Jamun", "qty": "per piece", "price": 3},
            {"name": "Sewaiyyan", "qty": "1 kg", "price": 60},
            {"name": "Shahi Tukda", "qty": "per piece", "price": 3},
            {"name": "Tilgud Laddoo", "qty": "per piece", "price": 4},
            {"name": "Sheerkhurma", "qty": "per litre", "price": 65},
            {"name": "Phirni", "qty": "per litre", "price": 50},
        ],
    },
}

HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8"/>
<meta name="viewport" content="width=device-width, initial-scale=1.0"/>
<title>Home Kitchen – Catering Service</title>
<link href="https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,500;0,700;1,500&family=Nunito:wght@300;400;600;700&display=swap" rel="stylesheet"/>
<style>
  /* ── Reset & Variables ── */
  *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

  :root {
    --cream: #fdf6ec;
    --dark: #1a0a00;
    --maroon: #7b1d1d;
    --gold: #c8922a;
    --gold-light: #e8b84b;
    --gold-pale: #f7e9c8;
    --card-bg: #fff9f0;
    --shadow: 0 4px 20px rgba(123,29,29,0.10);
    --radius: 14px;
  }

  html { scroll-behavior: smooth; }

  body {
    font-family: 'Nunito', sans-serif;
    background: var(--cream);
    color: var(--dark);
    min-height: 100vh;
  }

  /* ── Hero ── */
  .hero {
    background: linear-gradient(135deg, #3d0000 0%, #7b1d1d 50%, #4a1000 100%);
    color: #fff;
    text-align: center;
    padding: 60px 20px 50px;
    position: relative;
    overflow: hidden;
  }
  .hero::before {
    content: '';
    position: absolute; inset: 0;
    background: url("data:image/svg+xml,%3Csvg width='60' height='60' viewBox='0 0 60 60' xmlns='http://www.w3.org/2000/svg'%3E%3Cg fill='none' fill-rule='evenodd'%3E%3Cg fill='%23c8922a' fill-opacity='0.08'%3E%3Cpath d='M36 34v-4h-2v4h-4v2h4v4h2v-4h4v-2h-4zm0-30V0h-2v4h-4v2h4v4h2V6h4V4h-4zM6 34v-4H4v4H0v2h4v4h2v-4h4v-2H6zM6 4V0H4v4H0v2h4v4h2V6h4V4H6z'/%3E%3C/g%3E%3C/g%3E%3C/svg%3E");
    pointer-events: none;
  }
  .hero-logo {
    font-size: 72px;
    line-height: 1;
    margin-bottom: 8px;
    filter: drop-shadow(0 4px 8px rgba(0,0,0,0.3));
  }
  .hero h1 {
    font-family: 'Playfair Display', serif;
    font-size: clamp(2.4rem, 6vw, 4rem);
    font-weight: 700;
    letter-spacing: 2px;
    color: #fff;
    text-shadow: 0 2px 12px rgba(0,0,0,0.3);
  }
  .hero-sub {
    font-size: 1rem;
    color: var(--gold-light);
    letter-spacing: 4px;
    text-transform: uppercase;
    margin-top: 6px;
    font-weight: 300;
  }
  .hero-badges {
    display: flex;
    justify-content: center;
    gap: 16px;
    flex-wrap: wrap;
    margin-top: 28px;
  }
  .badge {
    background: rgba(200,146,42,0.18);
    border: 1px solid rgba(200,146,42,0.5);
    color: var(--gold-light);
    padding: 7px 18px;
    border-radius: 999px;
    font-size: .85rem;
    font-weight: 600;
    letter-spacing: 1px;
    backdrop-filter: blur(6px);
  }

  /* ── Sticky Nav ── */
  .sticky-nav {
    position: sticky;
    top: 0;
    z-index: 100;
    background: var(--maroon);
    display: flex;
    gap: 0;
    overflow-x: auto;
    scrollbar-width: none;
    box-shadow: 0 2px 12px rgba(0,0,0,0.25);
  }
  .sticky-nav::-webkit-scrollbar { display: none; }
  .nav-btn {
    flex: 0 0 auto;
    padding: 13px 20px;
    background: none;
    border: none;
    color: rgba(255,255,255,0.7);
    font-family: 'Nunito', sans-serif;
    font-size: .82rem;
    font-weight: 700;
    letter-spacing: 1px;
    text-transform: uppercase;
    cursor: pointer;
    transition: all .25s;
    white-space: nowrap;
    border-bottom: 3px solid transparent;
  }
  .nav-btn:hover, .nav-btn.active {
    color: var(--gold-light);
    border-bottom-color: var(--gold-light);
    background: rgba(255,255,255,0.06);
  }

  /* ── Main Layout ── */
  .main-wrap {
    max-width: 1100px;
    margin: 0 auto;
    padding: 40px 20px 80px;
  }

  /* ── Search ── */
  .search-bar {
    display: flex;
    align-items: center;
    background: #fff;
    border: 2px solid var(--gold);
    border-radius: 999px;
    padding: 10px 22px;
    margin-bottom: 40px;
    box-shadow: var(--shadow);
    gap: 10px;
  }
  .search-bar input {
    border: none;
    outline: none;
    flex: 1;
    font-family: 'Nunito', sans-serif;
    font-size: 1rem;
    color: var(--dark);
    background: transparent;
  }
  .search-icon { font-size: 1.3rem; }

  /* ── Section ── */
  .section { margin-bottom: 52px; animation: fadeUp .5s ease both; }
  @keyframes fadeUp { from { opacity:0; transform:translateY(24px); } to { opacity:1; transform:translateY(0); } }

  .section-header {
    display: flex;
    align-items: center;
    gap: 14px;
    margin-bottom: 20px;
    padding-bottom: 12px;
    border-bottom: 2px solid var(--gold-pale);
  }
  .section-icon {
    width: 48px; height: 48px;
    border-radius: 12px;
    display: flex; align-items: center; justify-content: center;
    font-size: 1.6rem;
    flex-shrink: 0;
  }
  .section-title {
    font-family: 'Playfair Display', serif;
    font-size: 1.7rem;
    font-weight: 700;
    color: var(--maroon);
  }
  .section-count {
    margin-left: auto;
    font-size: .8rem;
    font-weight: 700;
    color: var(--gold);
    background: var(--gold-pale);
    padding: 4px 12px;
    border-radius: 999px;
  }

  /* ── Grid ── */
  .items-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
    gap: 16px;
  }

  /* ── Item Card ── */
  .item-card {
    background: var(--card-bg);
    border: 1.5px solid var(--gold-pale);
    border-radius: var(--radius);
    padding: 18px 20px;
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
    gap: 12px;
    transition: transform .2s, box-shadow .2s, border-color .2s;
    cursor: pointer;
    position: relative;
    overflow: hidden;
  }
  .item-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 3px;
    background: var(--section-color, var(--gold));
    transform: scaleX(0);
    transform-origin: left;
    transition: transform .25s;
  }
  .item-card:hover {
    transform: translateY(-3px);
    box-shadow: 0 8px 28px rgba(123,29,29,0.14);
    border-color: var(--gold);
  }
  .item-card:hover::before { transform: scaleX(1); }
  .item-card.in-cart { border-color: var(--gold); background: #fffbf0; }

  .item-info { flex: 1; }
  .item-name {
    font-weight: 700;
    font-size: .97rem;
    color: var(--dark);
    line-height: 1.3;
    margin-bottom: 4px;
  }
  .item-qty {
    font-size: .78rem;
    color: #888;
    font-weight: 400;
  }

  .item-right { text-align: right; flex-shrink: 0; }
  .item-price {
    font-family: 'Playfair Display', serif;
    font-size: 1.15rem;
    font-weight: 700;
    color: var(--maroon);
  }
  .item-price span { font-size: .7rem; font-weight: 400; color: #999; display: block; }

  .add-btn {
    margin-top: 8px;
    width: 32px; height: 32px;
    border-radius: 50%;
    border: 2px solid var(--gold);
    background: none;
    color: var(--gold);
    font-size: 1.3rem;
    line-height: 1;
    cursor: pointer;
    transition: all .2s;
    display: flex; align-items: center; justify-content: center;
  }
  .add-btn:hover { background: var(--gold); color: #fff; }
  .qty-control {
    display: flex;
    align-items: center;
    gap: 6px;
    margin-top: 8px;
  }
  .qty-control button {
    width: 28px; height: 28px;
    border-radius: 50%;
    border: 1.5px solid var(--gold);
    background: none;
    color: var(--maroon);
    font-size: 1rem;
    cursor: pointer;
    transition: all .18s;
    display: flex; align-items: center; justify-content: center;
  }
  .qty-control button:hover { background: var(--gold); color: #fff; }
  .qty-num { font-weight: 700; font-size: .95rem; min-width: 20px; text-align: center; }

  /* ── Cart Drawer ── */
  .cart-fab {
    position: fixed;
    bottom: 28px; right: 28px;
    width: 64px; height: 64px;
    border-radius: 50%;
    background: linear-gradient(135deg, var(--maroon), #b71c1c);
    color: #fff;
    border: none;
    font-size: 1.6rem;
    cursor: pointer;
    box-shadow: 0 6px 24px rgba(123,29,29,0.4);
    transition: transform .2s, box-shadow .2s;
    z-index: 200;
    display: flex; align-items: center; justify-content: center;
  }
  .cart-fab:hover { transform: scale(1.08); box-shadow: 0 10px 32px rgba(123,29,29,0.5); }
  .cart-badge {
    position: absolute;
    top: -4px; right: -4px;
    background: var(--gold);
    color: #fff;
    width: 22px; height: 22px;
    border-radius: 50%;
    font-size: .72rem;
    font-weight: 700;
    display: flex; align-items: center; justify-content: center;
    border: 2px solid var(--cream);
  }

  .overlay {
    position: fixed; inset: 0;
    background: rgba(0,0,0,0.45);
    z-index: 300;
    opacity: 0; pointer-events: none;
    transition: opacity .3s;
  }
  .overlay.open { opacity: 1; pointer-events: all; }

  .cart-drawer {
    position: fixed;
    top: 0; right: 0; bottom: 0;
    width: min(420px, 100vw);
    background: var(--cream);
    z-index: 400;
    transform: translateX(100%);
    transition: transform .35s cubic-bezier(.4,0,.2,1);
    display: flex; flex-direction: column;
    box-shadow: -8px 0 40px rgba(0,0,0,0.2);
  }
  .cart-drawer.open { transform: translateX(0); }

  .cart-header {
    background: var(--maroon);
    color: #fff;
    padding: 20px 24px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    flex-shrink: 0;
  }
  .cart-header h2 {
    font-family: 'Playfair Display', serif;
    font-size: 1.4rem;
  }
  .close-btn {
    background: rgba(255,255,255,0.15);
    border: none;
    color: #fff;
    width: 36px; height: 36px;
    border-radius: 50%;
    font-size: 1.2rem;
    cursor: pointer;
    display: flex; align-items: center; justify-content: center;
    transition: background .2s;
  }
  .close-btn:hover { background: rgba(255,255,255,0.3); }

  .cart-body {
    flex: 1;
    overflow-y: auto;
    padding: 20px;
    display: flex;
    flex-direction: column;
    gap: 12px;
  }
  .cart-empty {
    text-align: center;
    padding: 60px 20px;
    color: #aaa;
    font-size: 1rem;
  }
  .cart-empty .big { font-size: 3rem; margin-bottom: 12px; }

  .cart-item {
    background: #fff;
    border: 1px solid var(--gold-pale);
    border-radius: 10px;
    padding: 14px 16px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    gap: 10px;
    animation: fadeUp .3s ease;
  }
  .cart-item-name { font-weight: 700; font-size: .9rem; }
  .cart-item-qty { font-size: .78rem; color: #999; }
  .cart-item-price { font-weight: 700; color: var(--maroon); font-size: .95rem; white-space: nowrap; }
  .cart-item-remove {
    background: none;
    border: none;
    color: #ccc;
    font-size: 1.1rem;
    cursor: pointer;
    transition: color .2s;
    padding: 0 4px;
  }
  .cart-item-remove:hover { color: #e74c3c; }

  .cart-footer {
    flex-shrink: 0;
    padding: 20px 24px;
    background: #fff;
    border-top: 1.5px solid var(--gold-pale);
  }
  .cart-total-row {
    display: flex;
    justify-content: space-between;
    font-size: 1.1rem;
    font-weight: 700;
    color: var(--dark);
    margin-bottom: 4px;
  }
  .cart-total-row .total-amount {
    font-family: 'Playfair Display', serif;
    font-size: 1.4rem;
    color: var(--maroon);
  }
  .cart-note {
    font-size: .75rem;
    color: #999;
    margin-bottom: 16px;
  }
  .order-btn {
    width: 100%;
    padding: 14px;
    background: linear-gradient(135deg, var(--maroon), #b71c1c);
    color: #fff;
    border: none;
    border-radius: 10px;
    font-family: 'Nunito', sans-serif;
    font-size: 1rem;
    font-weight: 700;
    letter-spacing: 1px;
    cursor: pointer;
    transition: opacity .2s, transform .2s;
  }
  .order-btn:hover { opacity: .9; transform: translateY(-1px); }
  .order-btn:disabled { background: #ccc; cursor: default; transform: none; }

  /* ── Info Bar ── */
  .info-bar {
    background: linear-gradient(90deg, var(--maroon), #b71c1c);
    color: #fff;
    display: flex;
    flex-wrap: wrap;
    justify-content: center;
    gap: 32px;
    padding: 22px 24px;
    text-align: center;
  }
  .info-item strong { display: block; font-size: 1rem; font-weight: 700; }
  .info-item span { font-size: .82rem; opacity: .8; }
  .contact-link {
    color: var(--gold-light);
    font-size: 1.3rem;
    font-weight: 700;
    font-family: 'Playfair Display', serif;
    text-decoration: none;
  }

  /* ── Toast ── */
  .toast {
    position: fixed;
    bottom: 100px; left: 50%;
    transform: translateX(-50%) translateY(20px);
    background: var(--dark);
    color: #fff;
    padding: 12px 24px;
    border-radius: 999px;
    font-size: .88rem;
    font-weight: 600;
    z-index: 500;
    pointer-events: none;
    opacity: 0;
    transition: all .3s;
    white-space: nowrap;
  }
  .toast.show { opacity: 1; transform: translateX(-50%) translateY(0); }

  /* ── Hidden ── */
  .hidden { display: none !important; }
</style>
</head>
<body>

<!-- Hero -->
<header class="hero">
  <div class="hero-logo">🍲</div>
  <h1>Home Kitchen</h1>
  <p class="hero-sub">Catering Service · Mrs. Mudassar Khan</p>
  <div class="hero-badges">
    <span class="badge">🏠 Home Cooked</span>
    <span class="badge">👥 Up to 40–50 Persons</span>
    <span class="badge">⏰ 3–4 Days Advance Notice</span>
    <span class="badge">💰 Min. Order 100 AED</span>
  </div>
</header>

<!-- Sticky Nav -->
<nav class="sticky-nav" id="stickyNav">
  {% for key, section in menu.items() %}
  <button class="nav-btn" onclick="scrollToSection('{{ key }}')" id="nav-{{ key }}">
    {{ section.icon }} {{ section.label }}
  </button>
  {% endfor %}
</nav>

<!-- Main -->
<main class="main-wrap">
  <!-- Search -->
  <div class="search-bar">
    <span class="search-icon">🔍</span>
    <input type="text" id="searchInput" placeholder="Search any dish…" oninput="filterItems(this.value)"/>
  </div>

  <!-- Sections -->
  {% for key, section in menu.items() %}
  <section class="section" id="sec-{{ key }}">
    <div class="section-header">
      <div class="section-icon" style="background:{{ section.color }}22;">{{ section.icon }}</div>
      <h2 class="section-title">{{ section.label }}</h2>
      <span class="section-count" id="count-{{ key }}">{{ section.dishes|length }} items</span>
    </div>
    <div class="items-grid">
      {% for item in section.dishes %}
      <div class="item-card"
           id="card-{{ key }}-{{ loop.index0 }}"
           style="--section-color:{{ section.color }}"
           data-name="{{ item.name|lower }}"
           data-qty="{{ item.qty|lower }}"
           data-section="{{ key }}">
        <div class="item-info">
          <div class="item-name">{{ item.name }}</div>
          {% if item.qty %}<div class="item-qty">{{ item.qty }}</div>{% endif %}
        </div>
        <div class="item-right">
          <div class="item-price">AED {{ item.price }}<span>per unit</span></div>
          <button class="add-btn"
                  id="addbtn-{{ key }}-{{ loop.index0 }}"
                  onclick="addToCart('{{ key }}', {{ loop.index0 }}, '{{ item.name }}', {{ item.price }}, '{{ item.qty }}')"
                  title="Add to order">＋</button>
          <div class="qty-control hidden" id="qtyctrl-{{ key }}-{{ loop.index0 }}">
            <button onclick="changeQty('{{ key }}', {{ loop.index0 }}, -1)">−</button>
            <span class="qty-num" id="qty-{{ key }}-{{ loop.index0 }}">1</span>
            <button onclick="changeQty('{{ key }}', {{ loop.index0 }}, 1)">＋</button>
          </div>
        </div>
      </div>
      {% endfor %}
    </div>
  </section>
  {% endfor %}
</main>

<!-- Info Bar -->
<footer class="info-bar">
  <div class="info-item">
    <strong>📞 Call / WhatsApp</strong>
    <a class="contact-link" href="tel:0567141845">056 714 1845</a>
  </div>
  <div class="info-item">
    <strong>👩‍🍳 Contact</strong>
    <span>Mrs. Mudassar Khan</span>
  </div>
  <div class="info-item">
    <strong>💰 Minimum Order</strong>
    <span>AED 100</span>
  </div>
  <div class="info-item">
    <strong>⏰ Advance Notice</strong>
    <span>3–4 Days</span>
  </div>
</footer>

<!-- Cart FAB -->
<button class="cart-fab" id="cartFab" onclick="toggleCart()" title="View Order">
  🛒
  <span class="cart-badge hidden" id="cartBadge">0</span>
</button>

<!-- Overlay -->
<div class="overlay" id="overlay" onclick="toggleCart()"></div>

<!-- Cart Drawer -->
<div class="cart-drawer" id="cartDrawer">
  <div class="cart-header">
    <h2>🛒 Your Order</h2>
    <button class="close-btn" onclick="toggleCart()">✕</button>
  </div>
  <div class="cart-body" id="cartBody">
    <div class="cart-empty">
      <div class="big">🍽️</div>
      Your order is empty.<br/>Browse the menu and add items!
    </div>
  </div>
  <div class="cart-footer">
    <div class="cart-total-row">
      <span>Total</span>
      <span class="total-amount" id="cartTotal">AED 0</span>
    </div>
    <p class="cart-note">Min. order AED 100 · 3-4 days advance notice required</p>
    <button class="order-btn" id="orderBtn" onclick="sendWhatsApp()" disabled>
      📱 Order via WhatsApp
    </button>
  </div>
</div>

<!-- Toast -->
<div class="toast" id="toast"></div>

<script>
  // ── State ──
  const cart = {};   // key: { name, price, qty, qtyLabel, section, idx }

  // ── Add to Cart ──
  function addToCart(section, idx, name, price, qtyLabel) {
    const id = section + '-' + idx;
    cart[id] = { name, price, qty: 1, qtyLabel, section, idx };
    document.getElementById('addbtn-' + id).classList.add('hidden');
    document.getElementById('qtyctrl-' + id).classList.remove('hidden');
    document.getElementById('card-' + id).classList.add('in-cart');
    updateCartUI();
    showToast('✓ ' + name + ' added');
  }

  function changeQty(section, idx, delta) {
    const id = section + '-' + idx;
    if (!cart[id]) return;
    cart[id].qty = Math.max(0, cart[id].qty + delta);
    if (cart[id].qty === 0) {
      delete cart[id];
      document.getElementById('addbtn-' + id).classList.remove('hidden');
      document.getElementById('qtyctrl-' + id).classList.add('hidden');
      document.getElementById('card-' + id).classList.remove('in-cart');
    } else {
      document.getElementById('qty-' + id).textContent = cart[id].qty;
    }
    updateCartUI();
  }

  function removeFromCart(id) {
    if (!cart[id]) return;
    const { section, idx } = cart[id];
    delete cart[id];
    const cardId = section + '-' + idx;
    document.getElementById('addbtn-' + cardId).classList.remove('hidden');
    document.getElementById('qtyctrl-' + cardId).classList.add('hidden');
    document.getElementById('card-' + cardId).classList.remove('in-cart');
    document.getElementById('qty-' + cardId).textContent = 1;
    updateCartUI();
  }

  function updateCartUI() {
    const keys = Object.keys(cart);
    const count = keys.reduce((s, k) => s + cart[k].qty, 0);
    const total = keys.reduce((s, k) => s + cart[k].price * cart[k].qty, 0);

    // Badge
    const badge = document.getElementById('cartBadge');
    if (count > 0) { badge.textContent = count; badge.classList.remove('hidden'); }
    else { badge.classList.add('hidden'); }

    // Total
    document.getElementById('cartTotal').textContent = 'AED ' + total;

    // Order btn
    document.getElementById('orderBtn').disabled = (total < 100);

    // Body
    const body = document.getElementById('cartBody');
    if (keys.length === 0) {
      body.innerHTML = '<div class="cart-empty"><div class="big">🍽️</div>Your order is empty.<br/>Browse the menu and add items!</div>';
      return;
    }
    body.innerHTML = keys.map(id => {
      const it = cart[id];
      return `<div class="cart-item">
        <div>
          <div class="cart-item-name">${it.name}</div>
          <div class="cart-item-qty">${it.qtyLabel || ''} × ${it.qty}</div>
        </div>
        <div style="display:flex;align-items:center;gap:10px;">
          <div class="cart-item-price">AED ${it.price * it.qty}</div>
          <button class="cart-item-remove" onclick="removeFromCart('${id}')" title="Remove">✕</button>
        </div>
      </div>`;
    }).join('');
  }

  // ── Cart Drawer ──
  function toggleCart() {
    document.getElementById('cartDrawer').classList.toggle('open');
    document.getElementById('overlay').classList.toggle('open');
  }

  // ── WhatsApp ──
  function sendWhatsApp() {
    const keys = Object.keys(cart);
    if (!keys.length) return;
    const lines = keys.map(id => {
      const it = cart[id];
      return `• ${it.name}${it.qtyLabel ? ' (' + it.qtyLabel + ')' : ''} × ${it.qty} = AED ${it.price * it.qty}`;
    });
    const total = keys.reduce((s, k) => s + cart[k].price * cart[k].qty, 0);
    const msg = `Hello Mrs. Mudassar Khan,\n\nI'd like to place a catering order:\n\n${lines.join('\n')}\n\n*Total: AED ${total}*\n\nPlease confirm availability. Thank you!`;
    window.open('https://wa.me/9710567141845?text=' + encodeURIComponent(msg), '_blank');
  }

  // ── Search / Filter ──
  function filterItems(query) {
    query = query.toLowerCase().trim();
    document.querySelectorAll('.section').forEach(sec => {
      let visible = 0;
      sec.querySelectorAll('.item-card').forEach(card => {
        const match = !query || card.dataset.name.includes(query) || card.dataset.qty.includes(query);
        card.style.display = match ? '' : 'none';
        if (match) visible++;
      });
      const key = sec.id.replace('sec-', '');
      const cnt = document.getElementById('count-' + key);
      if (cnt) cnt.textContent = visible + ' items';
      sec.style.display = (visible === 0 && query) ? 'none' : '';
    });
  }

  // ── Scroll & Nav highlight ──
  function scrollToSection(key) {
    document.getElementById('sec-' + key).scrollIntoView({ behavior: 'smooth', block: 'start' });
  }

  const observer = new IntersectionObserver(entries => {
    entries.forEach(e => {
      if (e.isIntersecting) {
        const key = e.target.id.replace('sec-', '');
        document.querySelectorAll('.nav-btn').forEach(b => b.classList.remove('active'));
        const nb = document.getElementById('nav-' + key);
        if (nb) { nb.classList.add('active'); nb.scrollIntoView({ inline: 'nearest', behavior: 'smooth' }); }
      }
    });
  }, { threshold: 0.25 });
  document.querySelectorAll('.section').forEach(s => observer.observe(s));

  // ── Toast ──
  function showToast(msg) {
    const t = document.getElementById('toast');
    t.textContent = msg;
    t.classList.add('show');
    setTimeout(() => t.classList.remove('show'), 1800);
  }
</script>
</body>
</html>
"""


@app.route("/")
def index():
    return render_template_string(HTML_TEMPLATE, menu=MENU)


@app.route("/api/menu")
def api_menu():
    return jsonify(MENU)


@app.route("/api/menu/<section>")
def api_section(section):
    if section not in MENU:
        return jsonify({"error": "Section not found"}), 404
    return jsonify(MENU[section])


if __name__ == "__main__":
    print("\n🍲  Home Kitchen Catering Website")
    print("   Running at: http://localhost:5000\n")
    app.run(debug=True, port=8080)
