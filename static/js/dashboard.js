/* Dashboard JavaScript */

document.addEventListener('DOMContentLoaded', function () {
    loadDashboardData();
});

async function loadDashboardData() {
    try {
        // Load user balance and stats from API
        console.log('Loading dashboard data...');
        console.log('Token available:', !!localStorage.getItem('token'));
        
        const meResponse = await fetchAPI('/users/me/');
        console.log('User data received:', meResponse);
        displayBalance(meResponse);

        // Load active investments
        try {
            const investmentsResponse = await fetchAPI('/investments/my-investments/active_investments/');
            console.log('Investments data:', investmentsResponse);
            displayActiveInvestments(investmentsResponse);
        } catch (invErr) {
            console.error('Error loading investments:', invErr);
            displayActiveInvestments([]);
        }

        // Load recent deposits
        try {
            const depositsResponse = await fetchAPI('/deposits/my_deposits/');
            console.log('Deposits data:', depositsResponse);
            displayRecentDeposits(depositsResponse);
        } catch (depErr) {
            console.error('Error loading deposits:', depErr);
            displayRecentDeposits([]);
        }
    } catch (error) {
        console.error('Error loading dashboard:', error);
        console.warn('If you see this, the API call failed. Make sure you are logged in and have a valid token.');
    }
}

function displayBalance(user) {
    // Update balance cards with data from API
    console.log('Displaying balance, user object:', user);
    const balanceEl = document.querySelector('[data-balance]');
    const investedEl = document.querySelector('[data-invested]');
    const earningsEl = document.querySelector('[data-earnings]');
    
    console.log('Balance element:', balanceEl);
    console.log('Invested element:', investedEl);
    console.log('Earnings element:', earningsEl);
    
    if (balanceEl && user.balance !== undefined) {
        const formattedBalance = '$' + parseFloat(user.balance).toFixed(2);
        console.log('Setting balance to:', formattedBalance);
        balanceEl.textContent = formattedBalance;
    } else {
        console.warn('Balance element not found or user.balance is undefined');
    }
    if (investedEl && user.total_invested !== undefined) {
        investedEl.textContent = '$' + parseFloat(user.total_invested).toFixed(2);
    }
    if (earningsEl && user.total_earnings !== undefined) {
        earningsEl.textContent = '$' + parseFloat(user.total_earnings).toFixed(2);
    }
}

function displayActiveInvestments(investments) {
    const container = document.getElementById('investments-list');
    
    if (!investments || investments.length === 0) {
        container.innerHTML = '<div class="card-body"><p class="text-muted">No active investments yet</p></div>';
        return;
    }

    let html = '<div class="list-group">';
    investments.forEach(inv => {
        html += `
            <div class="list-group-item">
                <div class="d-flex w-100 justify-content-between">
                    <h6 class="mb-1">${inv.plan_name}</h6>
                    <small>${formatDate(inv.start_date)}</small>
                </div>
                <p class="mb-1"><strong>Amount:</strong> ${formatCurrency(inv.amount)}</p>
                <p class="mb-1"><strong>ROI:</strong> ${inv.plan_roi}%</p>
                <small><strong>Expected Return:</strong> ${formatCurrency(inv.expected_return)}</small>
            </div>
        `;
    });
    html += '</div>';
    container.innerHTML = html;
}

function displayRecentDeposits(deposits) {
    const container = document.getElementById('deposits-list');
    
    if (!deposits || deposits.length === 0) {
        container.innerHTML = '<div class="card-body"><p class="text-muted">No deposits yet</p></div>';
        return;
    }

    let html = '<div class="list-group">';
    deposits.slice(0, 3).forEach(deposit => {
        const walletAddr = deposit.wallet_address ? `<div class="mt-1"><code style="word-break: break-all; font-size:0.8rem;">${deposit.wallet_address}</code></div>` : '';
        html += `
            <div class="list-group-item">
                <div class="d-flex w-100 justify-content-between align-items-center">
                    <div>
                        <h6 class="mb-1">${deposit.cryptocurrency}</h6>
                        <small>${formatDate(deposit.created_at)}</small>
                        ${walletAddr}
                    </div>
                    <div class="text-end">
                        <strong>${formatCurrency(deposit.amount)}</strong>
                        <br>
                        ${getStatusBadge(deposit.status)}
                    </div>
                </div>
            </div>
        `;
    });
    html += '</div>';
    container.innerHTML = html;
}
