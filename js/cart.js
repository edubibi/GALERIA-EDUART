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

function addToCart(item) {
    const cart = getCart();
    // Prevent duplicates? Or allow multiple? For art, usually 1 unless prints.
    // Let's allow duplicates but maybe warn user? For now simple list.
    const exists = cart.find(i => i.id === item.id);
    if (!exists) {
        cart.push(item);
        localStorage.setItem(CART_KEY, JSON.stringify(cart));
        updateCartCount();
        return true; // Added
    }
    return false; // Already there
}

function removeFromCart(id) {
    let cart = getCart();
    cart = cart.filter(item => item.id !== id);
    localStorage.setItem(CART_KEY, JSON.stringify(cart));
    updateCartCount();
    // Dispatch event for UI updates
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
    // User requested badge style (just number)
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
