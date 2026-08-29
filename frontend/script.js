const API_URL = "http://127.0.0.1:5000";

const form = document.getElementById("ticketForm");

form.addEventListener("submit", async (event) => {
    event.preventDefault();

    const payload = {
        name: document.getElementById("name").value,
        email: document.getElementById("email").value,
        subject: document.getElementById("subject").value,
        description: document.getElementById("description").value
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

        const message = document.getElementById("message");

        if (response.ok) {
            message.textContent =
                `Ticket submitted! Category: ${data.category}, Priority: ${data.priority}`;

            form.reset();
        } else {
            message.textContent = `Error: ${data.error}`;
        }

    } catch (error) {
        document.getElementById("message").textContent =
            "Unable to connect to the server.";
        console.error(error);
    }
});