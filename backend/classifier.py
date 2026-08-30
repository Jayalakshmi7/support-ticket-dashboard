CATEGORY_KEYWORDS = {
    "Billing": [
        "invoice",
        "refund",
        "charge",
        "charged",
        "payment",
        "subscription",
        "billing",
        "money",
        "transaction",
        "duplicate payment"
    ],

    "Shipping": [
        "delivery",
        "package",
        "tracking",
        "shipment",
        "courier",
        "shipping",
        "parcel",
        "delayed",
        "late delivery",
        "order not arrived"
    ],

    "Technical": [
        "error",
        "bug",
        "crash",
        "login",
        "not working",
        "broken",
        "website",
        "password",
        "server",
        "page",
        "application",
        "app"
    ],
}


PRIORITY_KEYWORDS = {
    "High": [
        "urgent",
        "asap",
        "immediately",
        "critical",
        "emergency",
        "down",
        "cannot access",
        "not working",
        "blocked"
    ],

    "Medium": [
        "soon",
        "issue",
        "problem",
        "delayed",
        "unable"
    ],
}


def classify_ticket(subject, description):
    text = f"{subject} {description}".lower()

    # -------------------------
    # Category classification
    # -------------------------
    category_scores = {}

    for category, keywords in CATEGORY_KEYWORDS.items():
        score = 0

        for keyword in keywords:
            if keyword in text:
                score += 1

        category_scores[category] = score

    # Select category with highest score
    category = max(
        category_scores,
        key=category_scores.get
    )

    # If no category keyword matched
    if category_scores[category] == 0:
        category = "Technical"

    # -------------------------
    # Priority classification
    # -------------------------
    priority = "Low"

    for level in ["High", "Medium"]:
        if any(keyword in text for keyword in PRIORITY_KEYWORDS[level]):
            priority = level
            break

    return category, priority