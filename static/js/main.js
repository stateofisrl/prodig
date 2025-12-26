/* Main JavaScript */

const API_BASE_URL = '/api';
const TOKEN = localStorage.getItem('token');

// Fetch wrapper
async function fetchAPI(endpoint, options = {}) {
    // When sending FormData, do not set Content-Type header
    const isFormData = options.body instanceof FormData;
    const headers = {
        'X-CSRFToken': getCookie('csrftoken'),
        ...options.headers,
    };
    if (!isFormData) headers['Content-Type'] = 'application/json';

    if (TOKEN) {
        headers['Authorization'] = `Token ${TOKEN}`;
    }

    try {
        const response = await fetch(`${API_BASE_URL}${endpoint}`, {
            ...options,
            headers,
            credentials: 'same-origin',
        });

        if (!response.ok) {
            if (response.status === 401) {
                window.location.href = '/login/';
            }
            const errorText = await response.text();
            console.error('API Error Response:', errorText);
            throw new Error(`HTTP ${response.status}: ${errorText}`);
        }

        return await response.json();
    } catch (error) {
        console.error('API Error:', error);
        showAlert('An error occurred. Please try again.', 'danger');
        throw error;
    }
}

// Logout handler - update nav link if present
document.addEventListener('DOMContentLoaded', function(){
    const logoutLink = document.getElementById('logout-link');
    if (logoutLink) {
        logoutLink.addEventListener('click', function(e){
            e.preventDefault();
            // Clear any leftover token used by API clients
            try { localStorage.removeItem('token'); } catch (_) {}
            // Use server-side session logout to avoid session mix-ups
            window.location.href = '/logout/';
        });
    }
});

// CSRF Token
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === name + '=') {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

// Show Alert
function showAlert(message, type = 'info') {
    const alertsContainer = document.querySelector('.alerts-container') || createAlertsContainer();
    const alertId = `alert-${Date.now()}`;
    
    const alertHTML = `
        <div class="alert alert-${type} alert-dismissible fade show" role="alert" id="${alertId}">
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        </div>
    `;
    
    alertsContainer.insertAdjacentHTML('beforeend', alertHTML);
    
    setTimeout(() => {
        const alert = document.getElementById(alertId);
        if (alert) {
            alert.remove();
        }
    }, 5000);
}

function createAlertsContainer() {
    const container = document.createElement('div');
    container.className = 'alerts-container container mt-3';
    document.querySelector('main').insertAdjacentElement('afterbegin', container);
    return container;
}

// Format currency
function formatCurrency(amount) {
    return new Intl.NumberFormat('en-US', {
        style: 'currency',
        currency: 'USD',
    }).format(amount);
}

// Format date
function formatDate(dateString) {
    return new Date(dateString).toLocaleDateString('en-US', {
        year: 'numeric',
        month: 'short',
        day: 'numeric',
    });
}

// Format datetime
function formatDateTime(dateString) {
    return new Date(dateString).toLocaleString('en-US', {
        year: 'numeric',
        month: 'short',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit',
    });
}

// Get status badge
function getStatusBadge(status) {
    const badges = {
        pending: '<span class="badge badge-pending">Pending</span>',
        approved: '<span class="badge badge-approved">Approved</span>',
        rejected: '<span class="badge badge-rejected">Rejected</span>',
        active: '<span class="badge badge-active">Active</span>',
        completed: '<span class="badge badge-completed">Completed</span>',
        processing: '<span class="badge bg-info">Processing</span>',
        closed: '<span class="badge bg-secondary">Closed</span>',
        in_progress: '<span class="badge bg-warning">In Progress</span>',
    };
    return badges[status] || `<span class="badge bg-secondary">${status}</span>`;
}
