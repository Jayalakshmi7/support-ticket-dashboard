const API_URL = "https://support-ticket-dashboard-1.onrender.com";
const form = document.getElementById("ticketForm");
const message = document.getElementById("message");

form.addEventListener("submit", async (event) => {

    event.preventDefault();

    message.className = "ticket-message";
    message.textContent = "Submitting your ticket...";

    const payload = {
        name: document.getElementById("name").value.trim(),
        email: document.getElementById("email").value.trim(),
        subject: document.getElementById("subject").value.trim(),
        description: document.getElementById("description").value.trim()
    };

    try {

        const response = await fetch(`${API_URL}/tickets`, {
            method: "POST",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify(payload)
        });

        const data = await response.json();

        if (response.ok) {

            message.className = "ticket-message success";

            message.innerHTML = `
                <strong>Ticket submitted successfully!</strong><br>
                Ticket ID: #${data.id}<br>
                Category: ${data.category}<br>
                Priority: ${data.priority}<br>
                Our support team will review your issue.
            `;

            form.reset();

        } else {

            message.className = "ticket-message error";

            message.textContent =
                data.error || "Unable to submit the ticket.";

        }

    } catch (error) {

        message.className = "ticket-message error";

        message.textContent =
            "Unable to connect to the support server. Please try again.";

        console.error("API Error:", error);
    }
});