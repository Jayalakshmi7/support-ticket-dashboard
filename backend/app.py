from flask import Flask, request, jsonify
from flask_cors import CORS
import mysql.connector

from db import get_db
from classifier import classify_ticket


app = Flask(__name__)
CORS(app)


# --------------------------------------------------
# Home
# --------------------------------------------------

@app.route("/")
def home():
    return jsonify({
        "message": "Support Ticket API is running"
    })


# --------------------------------------------------
# Health Check
# --------------------------------------------------

@app.route("/health")
def health():
    try:
        db = get_db()
        db.close()

        return jsonify({
            "status": "ok",
            "database": "connected"
        })

    except Exception:
        return jsonify({
            "status": "error",
            "database": "unavailable"
        }), 503


# --------------------------------------------------
# Create Ticket
# --------------------------------------------------

@app.route("/tickets", methods=["POST"])
def create_ticket():

    data = request.get_json(silent=True)

    if not data:
        return jsonify({
            "error": "Request body must contain valid JSON"
        }), 400

    required = [
        "name",
        "email",
        "subject",
        "description"
    ]

    missing = [
        field
        for field in required
        if not isinstance(data.get(field), str)
        or not data.get(field).strip()
    ]

    if missing:
        return jsonify({
            "error": f"Missing fields: {', '.join(missing)}"
        }), 400

    name = data["name"].strip()
    email = data["email"].strip()
    subject = data["subject"].strip()
    description = data["description"].strip()

    # Length validation
    if len(name) > 100:
        return jsonify({
            "error": "Name must be 100 characters or less"
        }), 400

    if len(email) > 150:
        return jsonify({
            "error": "Email must be 150 characters or less"
        }), 400

    if len(subject) > 200:
        return jsonify({
            "error": "Subject must be 200 characters or less"
        }), 400

    if len(description) > 5000:
        return jsonify({
            "error": "Description must be 5000 characters or less"
        }), 400

    # Automatic classification
    category, priority = classify_ticket(
        subject,
        description
    )

    db = None
    cursor = None

    try:

        db = get_db()
        cursor = db.cursor()

        cursor.execute(
            """
            INSERT INTO tickets
            (
                name,
                email,
                subject,
                description,
                category,
                priority,
                status
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            """,
            (
                name,
                email,
                subject,
                description,
                category,
                priority,
                "Open"
            )
        )

        db.commit()

        ticket_id = cursor.lastrowid

        return jsonify({
            "id": ticket_id,
            "category": category,
            "priority": priority,
            "status": "Open"
        }), 201

    except mysql.connector.Error:

        if db:
            db.rollback()

        return jsonify({
            "error": "Database error while creating ticket"
        }), 500

    finally:

        if cursor:
            cursor.close()

        if db:
            db.close()


# --------------------------------------------------
# Ticket Statistics
# --------------------------------------------------

@app.route("/tickets/stats", methods=["GET"])
def get_ticket_stats():

    db = None
    cursor = None

    try:

        db = get_db()
        cursor = db.cursor(dictionary=True)

        # Category statistics
        cursor.execute(
            """
            SELECT
                category,
                COUNT(*) AS count
            FROM tickets
            GROUP BY category
            """
        )

        category_rows = cursor.fetchall()

        # Priority statistics
        cursor.execute(
            """
            SELECT
                priority,
                COUNT(*) AS count
            FROM tickets
            GROUP BY priority
            """
        )

        priority_rows = cursor.fetchall()

        # Status statistics
        cursor.execute(
            """
            SELECT
                status,
                COUNT(*) AS count
            FROM tickets
            GROUP BY status
            """
        )

        status_rows = cursor.fetchall()

        # Total tickets
        cursor.execute(
            """
            SELECT COUNT(*) AS total
            FROM tickets
            """
        )

        total = cursor.fetchone()["total"]

        # Default values
        category = {
            "Billing": 0,
            "Shipping": 0,
            "Technical": 0
        }

        priority = {
            "High": 0,
            "Medium": 0,
            "Low": 0
        }

        status = {
            "Open": 0,
            "In Progress": 0,
            "Resolved": 0
        }

        # Fill category counts
        for row in category_rows:

            if row["category"] in category:
                category[row["category"]] = row["count"]

        # Fill priority counts
        for row in priority_rows:

            if row["priority"] in priority:
                priority[row["priority"]] = row["count"]

        # Fill status counts
        for row in status_rows:

            if row["status"] in status:
                status[row["status"]] = row["count"]

        return jsonify({
            "category": category,
            "priority": priority,
            "status": status,
            "total": total
        })

    except mysql.connector.Error:

        return jsonify({
            "error": "Database error while retrieving statistics"
        }), 500

    finally:

        if cursor:
            cursor.close()

        if db:
            db.close()


# --------------------------------------------------
# Get Tickets
# Supports:
# category
# priority
# status
# search
# --------------------------------------------------

@app.route("/tickets", methods=["GET"])
def get_tickets():

    category = request.args.get("category")
    priority = request.args.get("priority")
    status = request.args.get("status")
    search = request.args.get("search")

    allowed_categories = [
        "Technical",
        "Billing",
        "Shipping"
    ]

    allowed_priorities = [
        "High",
        "Medium",
        "Low"
    ]

    allowed_statuses = [
        "Open",
        "In Progress",
        "Resolved"
    ]

    # Validate category
    if category and category not in allowed_categories:

        return jsonify({
            "error": "Invalid category"
        }), 400

    # Validate priority
    if priority and priority not in allowed_priorities:

        return jsonify({
            "error": "Invalid priority"
        }), 400

    # Validate status
    if status and status not in allowed_statuses:

        return jsonify({
            "error": "Invalid status"
        }), 400

    # Base query
    query = """
        SELECT *
        FROM tickets
        WHERE 1=1
    """

    params = []

    # Category filter
    if category:

        query += " AND category = %s"
        params.append(category)

    # Priority filter
    if priority:

        query += " AND priority = %s"
        params.append(priority)

    # Status filter
    if status:

        query += " AND status = %s"
        params.append(status)

    # Search
    if search:

        query += """
            AND (
                name LIKE %s
                OR email LIKE %s
                OR subject LIKE %s
                OR description LIKE %s
                OR category LIKE %s
            )
        """

        search_value = f"%{search}%"

        params.extend([
            search_value,
            search_value,
            search_value,
            search_value,
            search_value
        ])

    # Newest tickets first
    query += " ORDER BY created_at DESC"

    db = None
    cursor = None

    try:

        db = get_db()
        cursor = db.cursor(dictionary=True)

        cursor.execute(query, params)

        tickets = cursor.fetchall()

        return jsonify(tickets)

    except mysql.connector.Error:

        return jsonify({
            "error": "Database error while retrieving tickets"
        }), 500

    finally:

        if cursor:
            cursor.close()

        if db:
            db.close()


# --------------------------------------------------
# Update Ticket Status
# --------------------------------------------------

@app.route("/tickets/<int:ticket_id>", methods=["PATCH"])
def update_status(ticket_id):

    data = request.get_json(silent=True)

    if not data:

        return jsonify({
            "error": "Request body must contain valid JSON"
        }), 400

    new_status = data.get("status")

    allowed_statuses = [
        "Open",
        "In Progress",
        "Resolved"
    ]

    if new_status not in allowed_statuses:

        return jsonify({
            "error": "Invalid status"
        }), 400

    db = None
    cursor = None

    try:

        db = get_db()
        cursor = db.cursor()

        cursor.execute(
            """
            UPDATE tickets
            SET status = %s
            WHERE id = %s
            """,
            (new_status, ticket_id)
        )

        # Ticket does not exist
        if cursor.rowcount == 0:

            return jsonify({
                "error": "Ticket not found"
            }), 404

        db.commit()

        return jsonify({
            "id": ticket_id,
            "status": new_status
        })

    except mysql.connector.Error:

        if db:
            db.rollback()

        return jsonify({
            "error": "Database error while updating ticket"
        }), 500

    finally:

        if cursor:
            cursor.close()

        if db:
            db.close()


# --------------------------------------------------
# Run Application
# --------------------------------------------------

if __name__ == "__main__":

    app.run(
        host="127.0.0.1",
        port=5000,
        debug=True
    )