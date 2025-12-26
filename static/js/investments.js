/* Investments JavaScript */

document.addEventListener('DOMContentLoaded', function () {
    loadInvestmentPlans();
    loadUserInvestments();
    
    document.getElementById('subscribe-form').addEventListener('submit', submitSubscription);
    document.getElementById('investment-amount').addEventListener('input', calculateReturn);
});

async function loadInvestmentPlans() {
    try {
        const plans = await fetchAPI('/investments/plans/');
        displayInvestmentPlans(plans);
    } catch (error) {
        console.error('Error loading plans:', error);
    }
}

function displayInvestmentPlans(plans) {
    const grid = document.getElementById('plans-grid');
    
    if (!plans || plans.length === 0) {
        grid.innerHTML = '<div class="col-md-12 text-center"><p class="text-muted">No investment plans available</p></div>';
        return;
    }

    let html = '';
    plans.forEach(plan => {
        html += `
            <div class="col-md-6 col-lg-4 mb-4">
                <div class="card h-100 border-0 shadow-sm">
                    <div class="card-header bg-primary text-white">
                        <h5 class="mb-0">${plan.name}</h5>
                    </div>
                    <div class="card-body">
                        <p class="card-text text-muted">${plan.description}</p>
                        <hr>
                        <div class="mb-3">
                            <p class="mb-1"><strong>ROI:</strong> <span class="badge bg-success">${plan.roi_percentage}%</span></p>
                            <p class="mb-1"><strong>Duration:</strong> ${plan.duration_days} days</p>
                            <p><strong>Min. Investment:</strong> ${formatCurrency(plan.minimum_investment)}</p>
                            ${plan.maximum_investment ? `<p><strong>Max. Investment:</strong> ${formatCurrency(plan.maximum_investment)}</p>` : ''}
                        </div>
                    </div>
                    <div class="card-footer bg-light">
                        <button class="btn btn-primary w-100" onclick="openSubscribeModal(${plan.id}, '${plan.name}', ${plan.roi_percentage}, ${plan.minimum_investment})">
                            <i class="bi bi-star"></i> Invest Now
                        </button>
                    </div>
                </div>
            </div>
        `;
    });
    grid.innerHTML = html;
}

async function loadUserInvestments() {
    try {
        const investments = await fetchAPI('/investments/my-investments/');
        displayUserInvestments(investments);
    } catch (error) {
        console.error('Error loading investments:', error);
    }
}

function displayUserInvestments(investments) {
    const tbody = document.getElementById('investments-table');
    
    if (!investments || investments.length === 0) {
        tbody.innerHTML = '<tr><td colspan="7" class="text-center text-muted">No investments yet</td></tr>';
        return;
    }

    let html = '';
    investments.forEach(inv => {
        html += `
            <tr>
                <td>${inv.plan_name}</td>
                <td>${formatCurrency(inv.amount)}</td>
                <td>${inv.plan_roi}%</td>
                <td>${formatDate(inv.start_date)}</td>
                <td>${formatDate(inv.end_date)}</td>
                <td>${formatCurrency(inv.expected_return)}</td>
                <td>${getStatusBadge(inv.status)}</td>
            </tr>
        `;
    });
    tbody.innerHTML = html;
}

function openSubscribeModal(planId, planName, roi, minAmount) {
    document.getElementById('plan-id').value = planId;
    document.getElementById('min-amount-text').textContent = `Minimum: ${formatCurrency(minAmount)}`;
    document.getElementById('investment-amount').min = minAmount;
    document.getElementById('investment-amount').value = minAmount;
    document.getElementById('subscribe-form').dataset.roi = roi;
    
    calculateReturn();
    
    new bootstrap.Modal(document.getElementById('subscribeModal')).show();
}

function calculateReturn() {
    const amount = parseFloat(document.getElementById('investment-amount').value) || 0;
    const roi = parseFloat(document.getElementById('subscribe-form').dataset.roi || 0);
    const expectedReturn = (amount * roi) / 100;
    
    document.getElementById('estimated-return').textContent = formatCurrency(expectedReturn);
}

async function submitSubscription(e) {
    e.preventDefault();
    
    const planId = document.getElementById('plan-id').value;
    const amount = parseFloat(document.getElementById('investment-amount').value);
    
    try {
        const response = await fetchAPI('/investments/my-investments/subscribe/', {
            method: 'POST',
            body: JSON.stringify({
                plan: planId,
                amount: amount,
            }),
        });

        showAlert('Investment created successfully!', 'success');
        bootstrap.Modal.getInstance(document.getElementById('subscribeModal')).hide();
        loadUserInvestments();
    } catch (error) {
        console.error('Error creating investment:', error);
        showAlert('Failed to create investment. Please try again.', 'danger');
    }
}
