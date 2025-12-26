/**
 * Referrals Page JavaScript
 */

document.addEventListener('DOMContentLoaded', function() {
    loadReferralStats();
    loadReferrals();
    loadCommissions();
});

/**
 * Get CSRF token from cookie
 */
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

/**
 * Get authentication headers
 */
function getAuthHeaders() {
    const token = localStorage.getItem('token');
    const headers = {
        'Content-Type': 'application/json',
        'X-CSRFToken': getCookie('csrftoken')
    };
    
    if (token) {
        headers['Authorization'] = `Token ${token}`;
    }
    
    return headers;
}

/**
 * Load referral statistics
 */
async function loadReferralStats() {
    try {
        const response = await fetch('/api/referrals/stats/', {
            headers: getAuthHeaders(),
            credentials: 'include'  // Include cookies for session auth
        });
        
        if (response.ok) {
            const data = await response.json();
            
            document.getElementById('referralCode').textContent = data.referral_code || 'N/A';
            document.getElementById('totalReferrals').textContent = data.total_referrals || 0;
            document.getElementById('pendingCommissions').textContent = `$${parseFloat(data.pending_commissions || 0).toFixed(2)}`;
            document.getElementById('totalEarned').textContent = `$${parseFloat(data.paid_commissions || 0).toFixed(2)}`;
            document.getElementById('commissionRate').textContent = data.commission_percentage || 0;
            
            // Set referral link
            const referralLink = `${window.location.origin}/register/?ref=${data.referral_code}`;
            document.getElementById('referralLink').value = referralLink;
        }
    } catch (error) {
        console.error('Error loading referral stats:', error);
    }
}

/**
 * Load referrals list
 */
async function loadReferrals() {
    try {
        const response = await fetch('/api/referrals/my_referrals/', {
            headers: getAuthHeaders(),
            credentials: 'include'
        });
        
        const tableBody = document.getElementById('referralsTable');
        
        if (response.ok) {
            const data = await response.json();
            
            if (data.length === 0) {
                tableBody.innerHTML = `
                    <tr>
                        <td colspan="4" class="px-6 py-8 text-center text-gray-400">
                            <div class="flex flex-col items-center">
                                <svg class="w-16 h-16 text-gray-700 mb-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z"></path>
                                </svg>
                                <p class="font-semibold mb-1">No referrals yet</p>
                                <p class="text-sm">Share your referral link to get started!</p>
                            </div>
                        </td>
                    </tr>
                `;
                return;
            }
            
            tableBody.innerHTML = data.map(referral => `
                <tr class="hover:bg-gray-800 transition">
                    <td class="px-6 py-4 whitespace-nowrap text-sm font-medium text-white">${referral.referred.username}</td>
                    <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-300">${referral.referred.email}</td>
                    <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-300">${new Date(referral.created_at).toLocaleDateString()}</td>
                    <td class="px-6 py-4 whitespace-nowrap">
                        <span class="px-3 py-1 inline-flex text-xs leading-5 font-semibold rounded-full bg-green-900 text-green-200">
                            Active
                        </span>
                    </td>
                </tr>
            `).join('');
        } else {
            tableBody.innerHTML = '<tr><td colspan="4" class="px-6 py-8 text-center text-red-400">Error loading referrals</td></tr>';
        }
    } catch (error) {
        console.error('Error loading referrals:', error);
        document.getElementById('referralsTable').innerHTML = '<tr><td colspan="4" class="px-6 py-8 text-center text-red-400">Error loading referrals</td></tr>';
    }
}

/**
 * Load commissions history
 */
async function loadCommissions() {
    try {
        const token = localStorage.getItem('token');
        const response = await fetch('/api/commissions/', {
            heresponse = await fetch('/api/commissions/', {
            headers: getAuthHeaders(),
            credentials: 'include'
        const tableBody = document.getElementById('commissionsTable');
        
        if (response.ok) {
            const data = await response.json();
            
            if (data.length === 0) {
                tableBody.innerHTML = `
                    <tr>
                        <td colspan="6" class="px-6 py-8 text-center text-gray-400">
                            <div class="flex flex-col items-center">
                                <svg class="w-16 h-16 text-gray-700 mb-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path>
                                </svg>
                                <p class="font-semibold mb-1">No commissions yet</p>
                                <p class="text-sm">Commissions appear when your referrals make deposits</p>
                            </div>
                        </td>
                    </tr>
                `;
                return;
            }
            
            tableBody.innerHTML = data.map(commission => {
                const statusColors = {
                    'paid': 'bg-green-900 text-green-200',
                    'pending': 'bg-yellow-900 text-yellow-200',
                    'cancelled': 'bg-red-900 text-red-200'
                };
                const statusClass = statusColors[commission.status] || 'bg-gray-900 text-gray-200';
                const paidDate = commission.paid_at ? 
                    new Date(commission.paid_at).toLocaleDateString() : '-';
                
                return `
                    <tr class="hover:bg-gray-800 transition">
                        <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-300">${new Date(commission.created_at).toLocaleDateString()}</td>
                        <td class="px-6 py-4 whitespace-nowrap text-sm font-medium text-white">${commission.referred_name}</td>
                        <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-300">$${parseFloat(commission.deposit_amount).toFixed(2)}</td>
                        <td class="px-6 py-4 whitespace-nowrap text-sm font-bold text-green-400">$${parseFloat(commission.amount).toFixed(2)}</td>
                        <td class="px-6 py-4 whitespace-nowrap">
                            <span class="px-3 py-1 inline-flex text-xs leading-5 font-semibold rounded-full ${statusClass}">
                                ${commission.status}
                            </span>
                        </td>
                        <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-300">${paidDate}</td>
                    </tr>
                `;
            }).join('');
        } else {
            tableBody.innerHTML = '<tr><td colspan="6" class="px-6 py-8 text-center text-red-400">Error loading commissions</td></tr>';
        }
    } catch (error) {
        console.error('Error loading commissions:', error);
        document.getElementById('commissionsTable').innerHTML = '<tr><td colspan="6" class="px-6 py-8 text-center text-red-400">Error loading commissions</td></tr>';
    }
}

/**
 * Copy referral code to clipboard
 */
function copyReferralCode() {
    const code = document.getElementById('referralCode').textContent;
    navigator.clipboard.writeText(code).then(() => {
        alert('Referral code copied to clipboard!');
    }).catch(err => {
        console.error('Error copying code:', err);
    });
}

/**
 * Copy referral link to clipboard
 */
function copyReferralLink() {
    const link = document.getElementById('referralLink');
    link.select();
    navigator.clipboard.writeText(link.value).then(() => {
        alert('Referral link copied to clipboard!');
    }).catch(err => {
        console.error('Error copying link:', err);
    });
}

/**
 * Share referral link
 */
function shareReferralLink() {
    const link = document.getElementById('referralLink').value;
    const text = 'Join me on this amazing investment platform!';
    
    if (navigator.share) {
        navigator.share({
            title: 'Join Investment Platform',
            text: text,
            url: link
        }).catch(err => console.log('Error sharing:', err));
    } else {
        // Fallback - copy to clipboard
        copyReferralLink();
    }
}
