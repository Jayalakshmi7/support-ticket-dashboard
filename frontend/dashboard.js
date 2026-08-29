const API_URL = "http://127.0.0.1:5000";


async function loadTickets() {

    const category =
        document.getElementById("filterCategory").value;

    const priority =
        document.getElementById("filterPriority").value;

    const status =
        document.getElementById("filterStatus").value;


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


    const response =
        await fetch(`${API_URL}/tickets?${params}`);

    const tickets = await response.json();


    const tbody =
        document.getElementById("ticketTable");

    tbody.innerHTML = "";


    tickets.forEach(ticket => {

        const row = document.createElement("tr");

        row.innerHTML = `
            <td>${ticket.subject}</td>
            <td>${ticket.category}</td>
            <td>${ticket.priority}</td>
            <td>${ticket.status}</td>

            <td>
                <select
                    onchange="updateStatus(${ticket.id}, this.value)"
                >
                    <option ${ticket.status === "Open" ? "selected" : ""}>
                        Open
                    </option>

                    <option ${ticket.status === "In Progress" ? "selected" : ""}>
                        In Progress
                    </option>

                    <option ${ticket.status === "Resolved" ? "selected" : ""}>
                        Resolved
                    </option>
                </select>
            </td>
        `;

        tbody.appendChild(row);
    });
}


async function updateStatus(id, newStatus) {

    await fetch(`${API_URL}/tickets/${id}`, {
        method: "PATCH",

        headers: {
            "Content-Type": "application/json"
        },

        body: JSON.stringify({
            status: newStatus
        })
    });

    loadTickets();
}


["filterCategory", "filterPriority", "filterStatus"]
    .forEach(id => {

        document
            .getElementById(id)
            .addEventListener("change", loadTickets);

    });


loadTickets();