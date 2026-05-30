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

function renderCartPage() {
    loadCart();
    const cartContainer = document.getElementById('cart-container');
    const cartSummaryContainer = document.getElementById('cart-summary');

    if (Object.keys(cart).length === 0) {
        cartContainer.innerHTML = `
            <div class="cart-empty-placeholder">
                <div class="big">🛒</div>
                <h2>Your Cart is Empty</h2>
                <p>Looks like you haven't added any items to your order yet.</p>
            </div>
        `;
        cartSummaryContainer.style.display = 'none';
        return;
    }

    cartSummaryContainer.style.display = 'block';
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
}

function renderSummary() {
    const cartSummaryContainer = document.getElementById('cart-summary');
    const subtotal = Object.values(cart).reduce((sum, item) => sum + (item.price * item.qty), 0);
    const deliveryFee = 0; // Or calculate based on logic
    const total = subtotal + deliveryFee;

    cartSummaryContainer.innerHTML = `
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
        <button class="order-btn" id="orderBtn" ${total < 100 ? 'disabled' : ''} onclick="submitOrder()">
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
        renderCartPage(); // Re-render the entire page to reflect changes
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

function submitOrder() {
    loadCart();
    if (Object.keys(cart).length === 0) {
        showToast("Your cart is empty!");
        return;
    }

    const total = Object.values(cart).reduce((s, i) => s + i.price * i.qty, 0);
    if (total < 100) {
        showToast("Minimum order is AED 100 for delivery.");
        return;
    }

    let message = "Salaam, I'd like to place an order:\n\n";
    let subtotal = 0;
    Object.values(cart).forEach(item => {
        message += `*${item.name}* (${item.qtyLabel})\n`;
        message += `↳ ${item.qty} x AED ${item.price} = AED ${item.qty * item.price}\n\n`;
        subtotal += item.qty * item.price;
    });
    message += `*Total: AED ${subtotal.toFixed(2)}*`;

    const whatsappUrl = `https://wa.me/971567141845?text=${encodeURIComponent(message)}`;
    window.open(whatsappUrl, '_blank');
}

function showToast(msg) {
    const t = document.getElementById('toast');
    t.textContent = msg;
    t.classList.add('show');
    setTimeout(() => t.classList.remove('show'), 2500);
}
