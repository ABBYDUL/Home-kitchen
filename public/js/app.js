document.addEventListener('DOMContentLoaded', () => {
    const menuContainer = document.getElementById('menu-container');
    const stickyNav = document.getElementById('stickyNav');

    if (!menuContainer || !stickyNav) {
        console.error('Required elements not found in the DOM');
        return;
    }

    // Render navigation buttons
    for (const [key, section] of Object.entries(MENU)) {
        stickyNav.innerHTML += `
            <button class="nav-btn" onclick="scrollToSection('${key}')" id="nav-${key}">
                ${section.icon} ${section.label}
            </button>
        `;
    }

    // Render menu sections and items
    for (const [key, section] of Object.entries(MENU)) {
        const sectionDiv = document.createElement('section');
        sectionDiv.className = 'section';
        sectionDiv.id = `sec-${key}`;

        const dishesHtml = section.dishes.map((item, index) => `
            <div class="item-card"
                 id="card-${key}-${index}"
                 style="--section-color:${section.color}"
                 data-name="${item.name.toLowerCase()}"
                 data-qty="${item.qty.toLowerCase()}"
                 data-section="${key}">
                <div class="item-info">
                    <div class="item-name">${item.name}</div>
                    ${item.qty ? `<div class="item-qty">${item.qty}</div>` : ''}
                </div>
                <div class="item-right">
                    <div class="item-price">AED ${item.price}<span>per unit</span></div>
                    <button class="add-btn"
                            id="addbtn-${key}-${index}"
                            onclick="addToCart('${key}', ${index}, '${item.name}', ${item.price}, '${item.qty}')"
                            title="Add to order">＋</button>
                    <div class="qty-control hidden" id="qtyctrl-${key}-${index}">
                        <button onclick="changeQty('${key}', ${index}, -1)">−</button>
                        <span class="qty-num" id="qty-${key}-${index}">1</span>
                        <button onclick="changeQty('${key}', ${index}, 1)">＋</button>
                    </div>
                </div>
            </div>
        `).join('');

        sectionDiv.innerHTML = `
            <div class="section-header">
                <div class="section-icon" style="background:${section.color}22;">${section.icon}</div>
                 <h2 class="section-title">${section.label}</h2>
                <span class="section-count" id="count-${key}">${section.dishes.length} items</span>
                <button class="collapse-btn" id="collapse-btn-${key}">
                    <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="6 9 12 15 18 9"></polyline></svg>
                </button>
            </div>
            <div class="items-grid" id="grid-${key}">
                ${dishesHtml}
            </div>
        `;
        sectionDiv.querySelector('.section-header').addEventListener('click', () => toggleSection(key));
        menuContainer.appendChild(sectionDiv);
    }
    
    loadCart();
    // Initially, open the first section if it exists
    const firstKey = Object.keys(MENU)[0];
    if (firstKey) {
        // A slight delay ensures the initial animation is visible
        setTimeout(() => toggleSection(firstKey, false), 50);
    }
});

function toggleSection(key, shouldScroll = false) {
    const grid = document.getElementById(`grid-${key}`);
    const section = document.getElementById(`sec-${key}`);
    if (!grid || !section) return;

    const isOpen = section.classList.contains('open');

    // Close all other open sections
    document.querySelectorAll('.section.open').forEach(openSection => {
        if (openSection.id !== `sec-${key}`) {
            openSection.classList.remove('open');
            const otherKey = openSection.id.split('-')[1];
            document.getElementById(`grid-${otherKey}`).style.maxHeight = '0px';
        }
    });

    // Deactivate all nav buttons
    document.querySelectorAll('.nav-btn').forEach(b => b.classList.remove('active'));

    // Toggle the clicked section
    if (isOpen) {
        section.classList.remove('open');
        grid.style.maxHeight = '0px';
        // When a section is closed by clicking, no nav button should be active
    } else {
        section.classList.add('open');
        grid.style.maxHeight = grid.scrollHeight + 'px';
        const navBtn = document.getElementById(`nav-${key}`);
        if (navBtn) navBtn.classList.add('active');
        if (shouldScroll) {
             section.scrollIntoView({ behavior: 'smooth', block: 'start' });
        }
    }
}

let cart = {};
const CART_STORAGE_KEY = 'homeKitchenCart';

function saveCart() {
    localStorage.setItem(CART_STORAGE_KEY, JSON.stringify(cart));
}

function loadCart() {
    const savedCart = localStorage.getItem(CART_STORAGE_KEY);
    if (savedCart) {
        cart = JSON.parse(savedCart);
        Object.keys(cart).forEach(id => {
            const item = cart[id];
            const card = document.getElementById('card-' + id);
            if (card) {
                card.classList.add('in-cart');
                document.getElementById('addbtn-' + id).classList.add('hidden');
                const qtyCtrl = document.getElementById('qtyctrl-' + id);
                qtyCtrl.classList.remove('hidden');
                qtyCtrl.querySelector('.qty-num').textContent = item.qty;
            }
        });
        updateCartUI();
    }
}

function addToCart(section, idx, name, price, qtyLabel) {
    const id = `${section}-${idx}`;
    cart[id] = { name, price, qty: 1, qtyLabel, section, idx };
    document.getElementById(`addbtn-${id}`).classList.add('hidden');
    document.getElementById(`qtyctrl-${id}`).classList.remove('hidden');
    document.getElementById(`card-${id}`).classList.add('in-cart');
    updateCartUI();
    saveCart();
    showToast(`✓ ${name} added`);
}

function changeQty(section, idx, delta) {
    const id = `${section}-${idx}`;
    if (!cart[id]) return;
    cart[id].qty = Math.max(0, cart[id].qty + delta);
    if (cart[id].qty === 0) {
        delete cart[id];
        document.getElementById(`addbtn-${id}`).classList.remove('hidden');
        document.getElementById(`qtyctrl-${id}`).classList.add('hidden');
        document.getElementById(`card-${id}`).classList.remove('in-cart');
    } else {
        document.getElementById(`qty-${id}`).textContent = cart[id].qty;
    }
    updateCartUI();
    saveCart();
}

function removeFromCart(id) {
    if (!cart[id]) return;
    const { section, idx } = cart[id];
    delete cart[id];
    const cardId = `${section}-${idx}`;
    document.getElementById(`addbtn-${cardId}`).classList.remove('hidden');
    document.getElementById(`qtyctrl-${cardId}`).classList.add('hidden');
    document.getElementById(`card-${cardId}`).classList.remove('in-cart');
    document.getElementById(`qty-${cardId}`).textContent = 1;
    updateCartUI();
    saveCart();
}

function updateCartUI() {
    const keys = Object.keys(cart);
    const count = keys.reduce((s, k) => s + cart[k].qty, 0);
    const total = keys.reduce((s, k) => s + cart[k].price * cart[k].qty, 0);

    const badge = document.getElementById('cartBadge');
    if (badge) {
        if (count > 0) {
            badge.textContent = count;
            badge.classList.remove('hidden');
        } else {
            badge.classList.add('hidden');
        }
    }

    const cartTotal = document.getElementById('cartTotal');
    if (cartTotal) {
        cartTotal.textContent = `AED ${total}`;
    }

    const orderBtn = document.getElementById('orderBtn');
    if (orderBtn) {
        orderBtn.disabled = total < 100;
    }

    const body = document.getElementById('cartBody');
    if (body) {
        if (keys.length === 0) {
            body.innerHTML = '<div class="cart-empty"><div class="big">🍽️</div>Your order is empty.<br/>Browse the menu and add items!</div>';
            return;
        }
        body.innerHTML = keys.map(id => {
            const it = cart[id];
            return `
                <div class="cart-item">
                    <div>
                        <div class="cart-item-name">${it.name}</div>
                        <div class="cart-item-qty">${it.qtyLabel || ''} × ${it.qty}</div>
                    </div>
                    <div style="display:flex;align-items:center;gap:10px;">
                        <div class="cart-item-price">AED ${it.price * it.qty}</div>
                        <button class="cart-item-remove" onclick="removeFromCart('${id}')" title="Remove">✕</button>
                    </div>
                </div>
            `;
        }).join('');
    }
}

function toggleCart() {
    document.getElementById('cartDrawer').classList.toggle('open');
    document.getElementById('overlay').classList.toggle('open');
}

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
        const cnt = document.getElementById(`count-${key}`);
        if (cnt) cnt.textContent = `${visible} items`;
        sec.style.display = (visible === 0 && query) ? 'none' : '';
    });
}

function scrollToSection(key) {
    toggleSection(key, true);
}

function showToast(msg) {
    const t = document.getElementById('toast');
    t.textContent = msg;
    t.classList.add('show');
    setTimeout(() => t.classList.remove('show'), 2500);
}
