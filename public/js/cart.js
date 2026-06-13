// js/cart.js

document.addEventListener('DOMContentLoaded', () => {
    renderCartPage();
});

const CART_STORAGE_KEY = 'homeKitchenCart';
let cart = {};

function loadCart() {
    const savedCart = localStorage.getItem(CART_STORAGE_KEY);
    if (savedCart) {
        cart = JSON.parse(savedCart);
    }
}

function saveCart() {
    localStorage.setItem(CART_STORAGE_KEY, JSON.stringify(cart));
}

function isDeliveryFormValid() {
    const form = document.getElementById('deliveryForm');
    if (!form) return false;
    return (
        form.address1.value.trim() !== '' &&
        form.building.value.trim() !== '' &&
        form.apt.value.trim()      !== '' &&
        form.emirate.value.trim()  !== ''
    );
}

function updateOrderBtn() {
    const btn = document.getElementById('orderBtn');
    if (!btn) return;
    const total = Object.values(cart).reduce((s, i) => s + i.price * i.qty, 0);
    btn.disabled = total < 100 || !isDeliveryFormValid();
    renderMessagePreview();
}

function attachFormListeners() {
    const form = document.getElementById('deliveryForm');
    if (!form) return;
    const allFields = ['address1', 'address2', 'building', 'floor', 'apt', 'emirate', 'comment'];
    allFields.forEach(name => {
        form[name].addEventListener('input', updateOrderBtn);
        form[name].addEventListener('change', updateOrderBtn);
    });
}

function buildOrderMessage() {
    const form = document.getElementById('deliveryForm');
    const address1 = form ? form.address1.value.trim() : '';
    const address2 = form ? form.address2.value.trim() : '';
    const building = form ? form.building.value.trim() : '';
    const floor    = form ? form.floor.value.trim()    : '';
    const apt      = form ? form.apt.value.trim()      : '';
    const emirate  = form ? form.emirate.value.trim()  : '';
    const comment  = form ? form.comment.value.trim()  : '';

    let message = "Salaam, I'd like to place an order:\n\n";
    let subtotal = 0;

    Object.values(cart).forEach(item => {
        message += `*${item.name}* (${item.qtyLabel})\n`;
        message += `↳ ${item.qty} x AED ${item.price} = AED ${item.qty * item.price}\n\n`;
        subtotal += item.qty * item.price;
    });

    message += `*Total: AED ${subtotal.toFixed(2)}*\n\n`;
    message += "Delivery Details:\n";
    if (address1) message += `${address1}\n`;
    if (address2) message += `${address2}\n`;
    if (building) {
        message += `${building}`;
        if (floor) message += `, Floor ${floor}`;
        if (apt)   message += `, Apt/House ${apt}`;
        message += '\n';
    }
    if (emirate) message += `${emirate}\n`;
    if (comment) message += `\nComment: ${comment}\n`;

    return message;
}

function renderMessagePreview() {
    const preview = document.getElementById('message-preview');
    if (!preview) return;

    const raw = buildOrderMessage();
    const formatted = raw
        .replace(/\*(.*?)\*/g, '<strong>$1</strong>')
        .replace(/\n/g, '<br>');

    preview.innerHTML = formatted;
}

function renderCartPage() {
    loadCart();
    const cartContainer      = document.getElementById('cart-container');
    const cartSummaryEl      = document.getElementById('cart-summary');
    const deliverySection    = document.getElementById('delivery-section');
    const previewSection     = document.getElementById('preview-section');

    if (Object.keys(cart).length === 0) {
        cartContainer.innerHTML = `
            <div class="cart-empty-placeholder">
                <div class="big">🛒</div>
                <h2>Your Cart is Empty</h2>
                <p>Looks like you haven't added any items to your order yet.</p>
            </div>
        `;
        cartSummaryEl.style.display   = 'none';
        deliverySection.style.display = 'none';
        previewSection.style.display  = 'none';
        return;
    }

    deliverySection.style.display = 'block';
    previewSection.style.display  = 'block';
    cartSummaryEl.style.display   = 'block';

    let itemsHtml = '';
    for (const id in cart) {
        const item = cart[id];
        itemsHtml += `
            <div class="cart-item-card" id="card-${id}">
                <div class="cart-item-info">
                    <div class="cart-item-name">${item.name}</div>
                    <div class="cart-item-details">${item.qtyLabel}</div>
                </div>
                <div class="qty-control">
                    <button onclick="changeQty('${id}', -1)">−</button>
                    <span class="qty-num">${item.qty}</span>
                    <button onclick="changeQty('${id}', 1)">＋</button>
                </div>
                <div class="cart-item-price">AED ${item.price * item.qty}</div>
                <button class="remove-item-btn" onclick="removeFromCart('${id}')" title="Remove">×</button>
            </div>
        `;
    }
    cartContainer.innerHTML = itemsHtml;

    renderSummary();
    attachFormListeners();
    renderMessagePreview();
}

function renderSummary() {
    const cartSummaryEl = document.getElementById('cart-summary');
    const subtotal = Object.values(cart).reduce((sum, item) => sum + (item.price * item.qty), 0);
    const deliveryFee = 0;
    const total = subtotal + deliveryFee;
    const belowMin  = total < 100;
    const formValid = isDeliveryFormValid();

    cartSummaryEl.innerHTML = `
        <div class="summary-row">
            <span>Subtotal</span>
            <span>AED ${subtotal.toFixed(2)}</span>
        </div>
        <div class="summary-row">
            <span>Delivery Fee</span>
            <span>${deliveryFee > 0 ? `AED ${deliveryFee.toFixed(2)}` : 'FREE'}</span>
        </div>
        <div class="summary-row total">
            <span>Total</span>
            <span class="total-amount">AED ${total.toFixed(2)}</span>
        </div>
        <div class="summary-note">Minimum order for delivery is AED 100</div>
        <button class="order-btn" id="orderBtn" ${belowMin || !formValid ? 'disabled' : ''} onclick="submitOrder()">
            Place WhatsApp Order
        </button>
    `;
}

function changeQty(id, delta) {
    if (!cart[id]) return;
    cart[id].qty += delta;
    if (cart[id].qty <= 0) {
        removeFromCart(id);
    } else {
        saveCart();
        renderCartPage();
    }
}

function removeFromCart(id) {
    if (!cart[id]) return;
    const itemName = cart[id].name;
    delete cart[id];
    saveCart();

    const cardElement = document.getElementById(`card-${id}`);
    if (cardElement) {
        cardElement.style.transition = 'opacity 0.3s ease, transform 0.3s ease';
        cardElement.style.opacity = '0';
        cardElement.style.transform = 'translateX(-20px)';
        setTimeout(() => {
            renderCartPage();
            showToast(`✓ ${itemName} removed`);
        }, 300);
    } else {
        renderCartPage();
    }
}

function getDeliveryDetails() {
    const form = document.getElementById('deliveryForm');
    if (!form) return null;
    const address1 = form.address1.value.trim();
    const address2 = form.address2.value.trim();
    const building = form.building.value.trim();
    const floor    = form.floor.value.trim();
    const apt      = form.apt.value.trim();
    const emirate  = form.emirate.value.trim();
    const comment  = form.comment.value.trim();

    if (!address1 || !building || !apt || !emirate) {
        showToast('Please fill in all required delivery fields.');
        return null;
    }
    return { address1, address2, building, floor, apt, emirate, comment };
}

function submitOrder() {
    loadCart();
    if (Object.keys(cart).length === 0) {
        showToast('Your cart is empty!');
        return;
    }

    const total = Object.values(cart).reduce((s, i) => s + i.price * i.qty, 0);
    if (total < 100) {
        showToast('Minimum order is AED 100 for delivery.');
        return;
    }

    const delivery = getDeliveryDetails();
    if (!delivery) return;

    const whatsappUrl = `https://wa.me/971567141845?text=${encodeURIComponent(buildOrderMessage())}`;
    window.open(whatsappUrl, '_blank');
}

function showToast(msg) {
    const t = document.getElementById('toast');
    t.textContent = msg;
    t.classList.add('show');
    setTimeout(() => t.classList.remove('show'), 2500);
}