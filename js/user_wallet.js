/**
 * VIRTUAL WALLET LOGIC ("La Caja")
 * Manages user credits and virtual balance.
 */

const WALLET_KEY = 'tu_arte_wallet';

function getWalletBalance() {
    const data = localStorage.getItem(WALLET_KEY);
    return data ? parseFloat(data) : 0.0;
}

function addWalletCredit(amount) {
    let balance = getWalletBalance();
    balance += parseFloat(amount);
    localStorage.setItem(WALLET_KEY, balance.toFixed(2));
    window.dispatchEvent(new Event('walletUpdated'));
}

function deductWalletCredit(amount) {
    let balance = getWalletBalance();
    if (balance >= amount) {
        balance -= amount;
        localStorage.setItem(WALLET_KEY, balance.toFixed(2));
        window.dispatchEvent(new Event('walletUpdated'));
        return true;
    }
    return false;
}

// Event listener for UI updates
window.addEventListener('walletUpdated', () => {
    const balanceElements = document.querySelectorAll('.wallet-balance');
    const currentBalance = getWalletBalance();
    balanceElements.forEach(el => {
        el.innerText = currentBalance.toFixed(2) + '€';
    });
});
