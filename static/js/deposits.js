/* Deposits JavaScript */

document.addEventListener('DOMContentLoaded', function () {
    loadWallets();
    loadDeposits();
    
    // Form handling
    document.getElementById('deposit-form').addEventListener('submit', submitDeposit);
    document.getElementById('proof_type').addEventListener('change', handleProofTypeChange);
    // Show wallet when user selects a cryptocurrency
    const cryptoSelect = document.getElementById('cryptocurrency');
    if (cryptoSelect) {
        cryptoSelect.addEventListener('change', function () {
            updateSelectedWallet(this.value);
        });
    }
});

async function loadWallets() {
    try {
        const resp = await fetchAPI('/deposits/wallets/');
        // store wallets for later lookup
        window.__WALLETS = resp && resp.results ? resp.results : resp || [];
        // don't auto-show all wallets; show placeholder until user selects
        showWalletPlaceholder();
    } catch (error) {
        console.error('Error loading wallets:', error);
    }
}

function displayWallets(wallets) {
    // displayWallets removed — wallets are now shown inline under the select via updateSelectedWallet()
}

function showWalletPlaceholder() {
    const container = document.getElementById('selected-wallet');
    const addr = document.getElementById('selected-wallet-address');
    const copyBtn = document.getElementById('copy-selected-wallet');
    if (!container || !addr) return;
    addr.textContent = 'Choose a payment method to reveal the receiving address.';
    if (copyBtn) copyBtn.style.display = 'none';
}

function updateSelectedWallet(crypto) {
    const addr = document.getElementById('selected-wallet-address');
    const copyBtn = document.getElementById('copy-selected-wallet');
    const wallets = window.__WALLETS || [];
    if (!addr) return;
    if (!crypto) {
        showWalletPlaceholder();
        return;
    }
    const wallet = wallets.find(w => w.cryptocurrency === crypto);
    if (!wallet) {
        addr.textContent = 'No active wallet for the selected cryptocurrency.';
        if (copyBtn) copyBtn.style.display = 'none';
        return;
    }
    addr.innerHTML = `<code style="word-break: break-all; font-size:0.95rem;">${wallet.wallet_address}</code>`;
    if (copyBtn) {
        copyBtn.style.display = '';
        copyBtn.onclick = function () { copyToClipboard(wallet.wallet_address); };
    }
}

async function loadDeposits() {
    try {
        const deposits = await fetchAPI('/deposits/my_deposits/');
        displayDeposits(deposits);
    } catch (error) {
        console.error('Error loading deposits:', error);
    }
}

function displayDeposits(deposits) {
    const tbody = document.getElementById('deposits-table');
    
    if (!deposits || deposits.length === 0) {
        tbody.innerHTML = '<tr><td colspan="5" class="text-center text-muted">No deposits yet</td></tr>';
        return;
    }

    let html = '';
    deposits.forEach(deposit => {
        html += `
            <tr>
                <td>${formatDate(deposit.created_at)}</td>
                <td>
                    ${deposit.cryptocurrency}
                    ${deposit.wallet_address ? `<div class="mt-1"><code style="word-break: break-all; font-size:0.8rem;">${deposit.wallet_address}</code></div>` : ''}
                </td>
                <td>${formatCurrency(deposit.amount)}</td>
                <td>${getStatusBadge(deposit.status)}</td>
                <td>
                    <button class="btn btn-sm btn-outline-primary" onclick="viewDepositDetails(${deposit.id})">
                        <i class="bi bi-eye"></i> View
                    </button>
                </td>
            </tr>
        `;
    });
    tbody.innerHTML = html;
}

async function submitDeposit(e) {
    e.preventDefault();
    
    const formData = new FormData(document.getElementById('deposit-form'));
    
    try {
        const response = await fetchAPI('/deposits/', {
            method: 'POST',
            body: formData,
            headers: {},
        });

        showAlert('Deposit submitted successfully. Awaiting admin approval.', 'success');
        document.getElementById('deposit-form').reset();
        loadDeposits();
    } catch (error) {
        console.error('Error submitting deposit:', error);
    }
}

function handleProofTypeChange(e) {
    const proofType = e.target.value;
    const contentGroup = document.getElementById('proof-content-group');
    const imageGroup = document.getElementById('proof-image-group');

    if (proofType === 'screenshot') {
        contentGroup.style.display = 'none';
        imageGroup.style.display = 'block';
    } else {
        contentGroup.style.display = 'block';
        imageGroup.style.display = 'none';
    }
}

function copyToClipboard(text) {
    navigator.clipboard.writeText(text).then(() => {
        showAlert('Wallet address copied to clipboard!', 'success');
    });
}

function viewDepositDetails(id) {
    // Implementation for viewing deposit details
    console.log('View deposit:', id);
}
