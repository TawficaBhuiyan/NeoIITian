def get_local_context():
    """Load any custom text or docs for chatbot context (optional)."""
    try:
        with open("data/sample_context.txt", "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        return "No extra context available."
