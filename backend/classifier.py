CATEGORY_KEYWORDS = {
    "Billing": ["invoice", "refund", "charge", "payment", "subscription", "billing"],
    "Shipping": ["delivery", "package", "tracking", "shipment", "courier", "shipping"],
    "Technical": ["error", "bug", "crash", "login", "not working", "broken"],
}

PRIORITY_KEYWORDS = {
    "High": ["urgent", "asap", "immediately", "critical", "down", "not working"],
    "Medium": ["soon", "issue", "problem"],
}


def classify_ticket(subject, description):
    text = f"{subject} {description}".lower()

    category = "Technical"

    for cat, keywords in CATEGORY_KEYWORDS.items():
        if any(kw in text for kw in keywords):
            category = cat
            break

    priority = "Low"

    for pri, keywords in PRIORITY_KEYWORDS.items():
        if any(kw in text for kw in keywords):
            priority = pri
            break

    return category, priority