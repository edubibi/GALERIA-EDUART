/**
 * SHOPPING CART LOGIC
 * Uses LocalStorage to persist items.
 */

const CART_KEY = 'tu_arte_cart';

// --- Core Functions ---

function getCart() {
    const json = localStorage.getItem(CART_KEY);
    return json ? JSON.parse(json) : [];
}

/**
 * Calculates discounts and promotions.
 * Promo: Buy 3, get 1 free (cheapest one is free).
 */
function calculateTotals() {
    const cart = getCart();
    let subtotal = 0;
    let discount = 0;

    // Parse prices
    const itemsWithPrice = cart.map(item => {
        let priceStr = item.price || '0';
        let clean = priceStr.replace('€', '').replace('.', '').replace(',', '.');
        let price = parseFloat(clean) || 0;
        return { ...item, numericPrice: price };
    });

    itemsWithPrice.sort((a, b) => b.numericPrice - a.numericPrice);

    // Apply 3+1 Promo
    const freeItemsCount = Math.floor(itemsWithPrice.length / 4);
    for (let i = 0; i < itemsWithPrice.length; i++) {
        subtotal += itemsWithPrice[i].numericPrice;
        // The last N cheapest items are free
        if (i >= itemsWithPrice.length - freeItemsCount) {
            discount += itemsWithPrice[i].numericPrice;
        }
    }

    return {
        subtotal: subtotal,
        discount: discount,
        total: subtotal - discount
    };
}

function addToCart(item) {
    const cart = getCart();
    const exists = cart.find(i => i.id === item.id);
    if (!exists) {
        cart.push(item);
        localStorage.setItem(CART_KEY, JSON.stringify(cart));
        updateCartCount();
        window.dispatchEvent(new Event('cartUpdated'));
        return true;
    }
    return false;
}

function removeFromCart(id) {
    let cart = getCart();
    cart = cart.filter(item => item.id !== id);
    localStorage.setItem(CART_KEY, JSON.stringify(cart));
    updateCartCount();
    window.dispatchEvent(new Event('cartUpdated'));
}

function clearCart() {
    localStorage.removeItem(CART_KEY);
    updateCartCount();
    window.dispatchEvent(new Event('cartUpdated'));
}

function updateCartCount() {
    const cart = getCart();
    const count = cart.length;
    const badges = document.querySelectorAll('.cart-badge');
    badges.forEach(el => {
        if (count > 0) {
            el.innerText = count;
            el.style.display = 'inline-block';
        } else {
            el.innerText = '';
            el.style.display = 'none';
        }
    });
}

// Init
document.addEventListener('DOMContentLoaded', () => {
    updateCartCount();
});
