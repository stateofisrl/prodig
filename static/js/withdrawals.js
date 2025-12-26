/* Withdrawals JavaScript */

document.addEventListener('DOMContentLoaded', function () {
    loadUserBalance();
    loadWithdrawals();
    
    // Form handling
    document.getElementById('withdrawal-form').addEventListener('submit', submitWithdrawal);
});

async function loadUserBalance() {
    try {
        const user = await fetchAPI('/api/users/me/');
        const balance = parseFloat(user.balance).toFixed(2);
        document.getElementById('available-balance').textContent = '$' + balance;
    } catch (error) {
        console.error('Error loading balance:', error);
    }
}

async function loadWithdrawals() {
    try {
        const withdrawals = await fetchAPI('/api/withdrawals/my_withdrawals/');
        displayWithdrawals(withdrawals);
    } catch (error) {
        console.error('Error loading withdrawals:', error);
    }
}

function displayWithdrawals(withdrawals) {
    const tbody = document.getElementById('withdrawals-table');
    
    if (!withdrawals || withdrawals.length === 0) {
        tbody.innerHTML = '<tr><td colspan="5" class="text-center text-muted">No withdrawals yet</td></tr>';
        return;
    }

    let html = '';
    withdrawals.forEach(withdrawal => {
        html += `
            <tr>
                <td>${formatDate(withdrawal.created_at)}</td>
                <td>$${parseFloat(withdrawal.amount).toFixed(2)}</td>
                <td><code>${withdrawal.cryptocurrency}</code></td>
                <td class="font-monospace text-truncate" style="max-width: 150px;">${withdrawal.wallet_address}</td>
                <td>${getStatusBadge(withdrawal.status)}</td>
            </tr>
        `;
    });
    tbody.innerHTML = html;
}

async function submitWithdrawal(e) {
    e.preventDefault();
    
    const amount = document.getElementById('amount').value;
    const cryptocurrency = document.getElementById('cryptocurrency').value;
    const wallet_address = document.getElementById('wallet_address').value;
    
    if (!cryptocurrency) {
        alert('Please select a cryptocurrency');
        return;
    }
    
    try {
        const response = await fetchAPI('/api/withdrawals/request_withdrawal/', {
            method: 'POST',
            body: JSON.stringify({
                amount,
                cryptocurrency,
                wallet_address
            })
        });

        showAlert('Withdrawal request submitted successfully!', 'success');
        document.getElementById('withdrawal-form').reset();
        loadUserBalance();
        loadWithdrawals();
    } catch (error) {
        console.error('Error submitting withdrawal:', error);
    }
}
