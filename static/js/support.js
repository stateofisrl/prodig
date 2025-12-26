/* Support JavaScript */

document.addEventListener('DOMContentLoaded', function () {
    loadSupportTickets();
    
    document.getElementById('ticket-form').addEventListener('submit', submitSupportTicket);
});

async function loadSupportTickets() {
    try {
        const tickets = await fetchAPI('/support/tickets/my_tickets/');
        displaySupportTickets(tickets);
        displayTicketsSummary(tickets);
    } catch (error) {
        console.error('Error loading tickets:', error);
    }
}

function displayTicketsSummary(tickets) {
    const container = document.getElementById('tickets-summary');
    
    const openCount = tickets.filter(t => t.status === 'open').length;
    const inProgressCount = tickets.filter(t => t.status === 'in_progress').length;
    const resolvedCount = tickets.filter(t => t.status === 'resolved').length;

    let html = `
        <div class="row">
            <div class="col-md-6 mb-2">
                <p class="mb-1"><strong>Open:</strong> <span class="badge bg-danger">${openCount}</span></p>
            </div>
            <div class="col-md-6 mb-2">
                <p class="mb-1"><strong>In Progress:</strong> <span class="badge bg-warning">${inProgressCount}</span></p>
            </div>
            <div class="col-md-6">
                <p class="mb-1"><strong>Resolved:</strong> <span class="badge bg-success">${resolvedCount}</span></p>
            </div>
            <div class="col-md-6">
                <p class="mb-1"><strong>Total:</strong> <span class="badge bg-info">${tickets.length}</span></p>
            </div>
        </div>
    `;
    container.innerHTML = html;
}

function displaySupportTickets(tickets) {
    const container = document.getElementById('tickets-list');
    
    if (!tickets || tickets.length === 0) {
        container.innerHTML = '<p class="text-muted">You have no support tickets yet.</p>';
        return;
    }

    let html = '<div class="row">';
    tickets.forEach(ticket => {
        html += `
            <div class="col-md-12 mb-3">
                <div class="card">
                    <div class="card-body">
                        <div class="d-flex justify-content-between align-items-start">
                            <div>
                                <h6 class="card-title">#${ticket.id} - ${ticket.subject}</h6>
                                <p class="card-text text-muted small mb-2">${formatDateTime(ticket.created_at)}</p>
                                <p class="card-text">${ticket.message.substring(0, 100)}...</p>
                            </div>
                            <div class="text-end">
                                ${getStatusBadge(ticket.status)}
                                <br>
                                <span class="badge ${getPriorityColor(ticket.priority)}">${ticket.priority}</span>
                            </div>
                        </div>
                        <button class="btn btn-sm btn-outline-primary mt-2" onclick="viewTicketDetail(${ticket.id}, '${ticket.subject}')">
                            <i class="bi bi-arrow-right"></i> View & Reply
                        </button>
                    </div>
                </div>
            </div>
        `;
    });
    html += '</div>';
    container.innerHTML = html;
}

async function submitSupportTicket(e) {
    e.preventDefault();
    
    const formData = new FormData(document.getElementById('ticket-form'));
    const data = {
        subject: formData.get('subject'),
        message: formData.get('message'),
        priority: formData.get('priority'),
    };
    
    try {
        const response = await fetchAPI('/support/tickets/', {
            method: 'POST',
            body: JSON.stringify(data),
        });

        showAlert('Support ticket created successfully!', 'success');
        document.getElementById('ticket-form').reset();
        loadSupportTickets();
    } catch (error) {
        console.error('Error creating ticket:', error);
    }
}

async function viewTicketDetail(ticketId, subject) {
    try {
        const ticket = await fetchAPI(`/support/tickets/${ticketId}/`);
        displayTicketDetail(ticket);
        
        document.getElementById('ticket-title').textContent = `#${ticket.id} - ${subject}`;
        new bootstrap.Modal(document.getElementById('ticketModal')).show();
    } catch (error) {
        console.error('Error loading ticket:', error);
    }
}

function displayTicketDetail(ticket) {
    const detailContainer = document.getElementById('ticket-details');
    const repliesContainer = document.getElementById('ticket-replies');
    
    // Display ticket details
    let detailHtml = `
        <p><strong>Status:</strong> ${getStatusBadge(ticket.status)}</p>
        <p><strong>Priority:</strong> <span class="badge ${getPriorityColor(ticket.priority)}">${ticket.priority}</span></p>
        <p><strong>Created:</strong> ${formatDateTime(ticket.created_at)}</p>
        <p><strong>Message:</strong></p>
        <p>${ticket.message}</p>
    `;
    detailContainer.innerHTML = detailHtml;
    
    // Display replies
    let repliesHtml = '<h6 class="mb-3">Conversation:</h6>';
    if (ticket.replies && ticket.replies.length > 0) {
        repliesHtml += '<div class="list-group">';
        ticket.replies.forEach(reply => {
            repliesHtml += `
                <div class="list-group-item">
                    <div class="d-flex w-100 justify-content-between">
                        <h6 class="mb-1">${reply.sender_name} ${reply.is_from_admin ? '<span class="badge bg-danger">Admin</span>' : ''}</h6>
                        <small>${formatDateTime(reply.created_at)}</small>
                    </div>
                    <p class="mb-0">${reply.message}</p>
                </div>
            `;
        });
        repliesHtml += '</div>';
    } else {
        repliesHtml += '<p class="text-muted">No replies yet</p>';
    }
    repliesContainer.innerHTML = repliesHtml;
    
    // Store ticket ID for reply submission
    document.getElementById('reply-form').dataset.ticketId = ticket.id;
}

document.addEventListener('DOMContentLoaded', function () {
    const replyForm = document.getElementById('reply-form');
    if (replyForm) {
        replyForm.addEventListener('submit', submitTicketReply);
    }
});

async function submitTicketReply(e) {
    e.preventDefault();
    
    const ticketId = e.target.dataset.ticketId;
    const message = document.getElementById('reply-message').value;
    
    try {
        const response = await fetchAPI(`/support/tickets/${ticketId}/add_reply/`, {
            method: 'POST',
            body: JSON.stringify({ message }),
        });

        showAlert('Reply sent successfully!', 'success');
        document.getElementById('reply-message').value = '';
        
        // Refresh ticket details
        viewTicketDetail(ticketId, document.getElementById('ticket-title').textContent);
    } catch (error) {
        console.error('Error sending reply:', error);
    }
}

function getPriorityColor(priority) {
    const colors = {
        low: 'bg-info',
        medium: 'bg-warning',
        high: 'bg-orange',
        urgent: 'bg-danger',
    };
    return colors[priority] || 'bg-secondary';
}
