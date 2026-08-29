from flask import Flask, request, jsonify
from flask_cors import CORS

from db import get_db
from classifier import classify_ticket


app = Flask(__name__)

CORS(app)


@app.route("/")
def home():
    return "Support Ticket API is running"


@app.route("/tickets", methods=["POST"])
def create_ticket():
    data = request.json

    required = ["name", "email", "subject", "description"]
    missing = [field for field in required if not data.get(field)]

    if missing:
        return jsonify({
            "error": f"Missing fields: {', '.join(missing)}"
        }), 400

    category, priority = classify_ticket(
        data["subject"],
        data["description"]
    )

    db = get_db()
    cursor = db.cursor()

    cursor.execute(
        """
        INSERT INTO tickets
        (name, email, subject, description, category, priority, status)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        """,
        (
            data["name"],
            data["email"],
            data["subject"],
            data["description"],
            category,
            priority,
            "Open"
        )
    )

    db.commit()

    ticket_id = cursor.lastrowid

    cursor.close()
    db.close()

    return jsonify({
        "id": ticket_id,
        "category": category,
        "priority": priority
    }), 201
@app.route("/tickets", methods=["GET"])
def get_tickets():
    category = request.args.get("category")
    priority = request.args.get("priority")
    status = request.args.get("status")

    query = "SELECT * FROM tickets WHERE 1=1"
    params = []

    if category:
        query += " AND category = %s"
        params.append(category)

    if priority:
        query += " AND priority = %s"
        params.append(priority)

    if status:
        query += " AND status = %s"
        params.append(status)

    query += " ORDER BY created_at DESC"

    db = get_db()
    cursor = db.cursor(dictionary=True)

    cursor.execute(query, params)

    tickets = cursor.fetchall()

    cursor.close()
    db.close()

    return jsonify(tickets)
@app.route("/tickets/<int:ticket_id>", methods=["PATCH"])
def update_status(ticket_id):
    new_status = request.json.get("status")

    if new_status not in ["Open", "In Progress", "Resolved"]:
        return jsonify({"error": "Invalid status"}), 400

    db = get_db()
    cursor = db.cursor()

    cursor.execute(
        "UPDATE tickets SET status = %s WHERE id = %s",
        (new_status, ticket_id)
    )

    db.commit()

    cursor.close()
    db.close()

    return jsonify({
        "id": ticket_id,
        "status": new_status
    })


if __name__ == "__main__":
    app.run(debug=True, port=5000)