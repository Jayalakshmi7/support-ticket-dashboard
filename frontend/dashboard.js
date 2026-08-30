const API_URL = "https://support-ticket-dashboard-1.onrender.com";

// ========================================
// LOAD STATISTICS
// ========================================

async function loadStats() {

    try {

        const response = await fetch(`${API_URL}/tickets/stats`);

        if (!response.ok) {
            throw new Error("Failed to load statistics");
        }

        const data = await response.json();


        // Total
        document.getElementById("totalTickets").textContent =
            data.total;


        // Status
        document.getElementById("openTickets").textContent =
            data.status.Open;

        document.getElementById("progressTickets").textContent =
            data.status["In Progress"];

        document.getElementById("resolvedTickets").textContent =
            data.status.Resolved;


        // Category
        document.getElementById("technicalCount").textContent =
            data.category.Technical;

        document.getElementById("billingCount").textContent =
            data.category.Billing;

        document.getElementById("shippingCount").textContent =
            data.category.Shipping;


        // Priority
        document.getElementById("highCount").textContent =
            data.priority.High;

        document.getElementById("mediumCount").textContent =
            data.priority.Medium;

        document.getElementById("lowCount").textContent =
            data.priority.Low;


        // Category progress bars

        const total = data.total || 1;

        document.getElementById("technicalBar").style.width =
            `${(data.category.Technical / total) * 100}%`;

        document.getElementById("billingBar").style.width =
            `${(data.category.Billing / total) * 100}%`;

        document.getElementById("shippingBar").style.width =
            `${(data.category.Shipping / total) * 100}%`;


    } catch (error) {

        console.error("Stats error:", error);

    }
}



// ========================================
// LOAD TICKETS
// ========================================

async function loadTickets() {

    const category =
        document.getElementById("filterCategory").value;

    const priority =
        document.getElementById("filterPriority").value;

    const status =
        document.getElementById("filterStatus").value;

    const search =
        document.getElementById("searchInput").value.trim();


    const params = new URLSearchParams();


    if (category) {
        params.append("category", category);
    }

    if (priority) {
        params.append("priority", priority);
    }

    if (status) {
        params.append("status", status);
    }

    if (search) {
        params.append("search", search);
    }


    try {

        const response =
            await fetch(`${API_URL}/tickets?${params.toString()}`);


        if (!response.ok) {
            throw new Error("Failed to load tickets");
        }


        const tickets = await response.json();


        renderTickets(tickets);


    } catch (error) {

        console.error("Ticket loading error:", error);

        document.getElementById("ticketTable").innerHTML = `
            <tr>
                <td colspan="7" class="error-message">
                    Unable to load tickets.
                </td>
            </tr>
        `;

    }

}



// ========================================
// RENDER TICKETS
// ========================================

function renderTickets(tickets) {

    const tbody =
        document.getElementById("ticketTable");


    tbody.innerHTML = "";


    if (tickets.length === 0) {

        tbody.innerHTML = `
            <tr>
                <td colspan="7" class="empty-state">
                    <div class="empty-icon">⌕</div>
                    <strong>No tickets found</strong>
                    <span>Try changing your search or filters.</span>
                </td>
            </tr>
        `;

        return;
    }


    tickets.forEach(ticket => {

        const row =
            document.createElement("tr");


        const initials =
            ticket.name
                ? ticket.name.charAt(0).toUpperCase()
                : "?";


        const categoryClass =
            `category-${ticket.category.toLowerCase()}`;


        const priorityClass =
            `priority-${ticket.priority.toLowerCase()}`;


        row.innerHTML = `

            <td>
                <span class="ticket-id">
                    #${ticket.id}
                </span>
            </td>


            <td>

                <div class="customer-cell">

                    <div class="customer-avatar">
                        ${initials}
                    </div>

                    <div class="customer-info">

                        <strong>
                            ${escapeHTML(ticket.name)}
                        </strong>

                        <span>
                            ${escapeHTML(ticket.email)}
                        </span>

                    </div>

                </div>

            </td>


            <td>

                <div class="subject-cell">

                    <strong>
                        ${escapeHTML(ticket.subject)}
                    </strong>

                    <span>
                        ${formatDate(ticket.created_at)}
                    </span>

                </div>

            </td>


            <td>

                <span class="badge ${categoryClass}">
                    ${escapeHTML(ticket.category)}
                </span>

            </td>


            <td>

                <span class="badge ${priorityClass}">

                    <span class="badge-dot"></span>

                    ${escapeHTML(ticket.priority)}

                </span>

            </td>


            <td>

                <select
                    class="status-select"
                    onchange="updateStatus(${ticket.id}, this.value)"
                >

                    <option
                        value="Open"
                        ${ticket.status === "Open" ? "selected" : ""}
                    >
                        Open
                    </option>

                    <option
                        value="In Progress"
                        ${ticket.status === "In Progress" ? "selected" : ""}
                    >
                        In Progress
                    </option>

                    <option
                        value="Resolved"
                        ${ticket.status === "Resolved" ? "selected" : ""}
                    >
                        Resolved
                    </option>

                </select>

            </td>


            <td>

                <button
                    class="view-button"
                    onclick='openTicketModal(${JSON.stringify(ticket)})'
                >
                    View
                </button>

            </td>

        `;


        tbody.appendChild(row);

    });

}



// ========================================
// UPDATE STATUS
// ========================================

async function updateStatus(id, newStatus) {

    try {

        const response =
            await fetch(`${API_URL}/tickets/${id}`, {

                method: "PATCH",

                headers: {
                    "Content-Type": "application/json"
                },

                body: JSON.stringify({
                    status: newStatus
                })

            });


        const data = await response.json();


        if (!response.ok) {

            alert(data.error || "Failed to update ticket");

            return;
        }


        // Refresh tickets
        await loadTickets();

        // Refresh statistics
        await loadStats();


    } catch (error) {

        console.error("Status update error:", error);

        alert("Unable to update ticket status.");

    }

}



// ========================================
// OPEN TICKET MODAL
// ========================================

function openTicketModal(ticket) {

    document.getElementById("modalSubject").textContent =
        ticket.subject;

    document.getElementById("modalName").textContent =
        ticket.name;

    document.getElementById("modalEmail").textContent =
        ticket.email;

    document.getElementById("modalCategory").textContent =
        ticket.category;

    document.getElementById("modalPriority").textContent =
        ticket.priority;

    document.getElementById("modalStatus").textContent =
        ticket.status;

    document.getElementById("modalDate").textContent =
        formatDate(ticket.created_at);

    document.getElementById("modalDescription").textContent =
        ticket.description;


    document.getElementById("ticketModal")
        .classList.add("show");

}



// ========================================
// CLOSE TICKET MODAL
// ========================================

function closeTicketModal() {

    document.getElementById("ticketModal")
        .classList.remove("show");

}



// ========================================
// CLOSE MODAL WHEN CLICKING OUTSIDE
// ========================================

document.getElementById("ticketModal")
    .addEventListener("click", function(event) {

        if (event.target === this) {
            closeTicketModal();
        }

    });



// ========================================
// ESCAPE KEY CLOSES MODAL
// ========================================

document.addEventListener("keydown", function(event) {

    if (event.key === "Escape") {
        closeTicketModal();
    }

});



// ========================================
// SEARCH + FILTER EVENTS
// ========================================

document
    .getElementById("searchInput")
    .addEventListener("input", loadTickets);


[
    "filterCategory",
    "filterPriority",
    "filterStatus"
].forEach(id => {

    document
        .getElementById(id)
        .addEventListener("change", loadTickets);

});



// ========================================
// DATE FORMATTER
// ========================================

function formatDate(dateString) {

    if (!dateString) {
        return "-";
    }

    const date = new Date(dateString);

    return date.toLocaleString();

}



// ========================================
// HTML ESCAPE
// ========================================

function escapeHTML(value) {

    if (value === null || value === undefined) {
        return "";
    }

    return String(value)
        .replace(/&/g, "&amp;")
        .replace(/</g, "&lt;")
        .replace(/>/g, "&gt;")
        .replace(/"/g, "&quot;")
        .replace(/'/g, "&#039;");

}



// ========================================
// INITIAL LOAD
// ========================================

loadStats();
loadTickets();