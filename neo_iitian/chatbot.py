import os
from .llm_connector import get_llm

def load_context():
    """Load chatbot context from dataset/sample_context.txt."""
    context_path = os.path.join(os.path.dirname(__file__), "..", "dataset", "sample_context.txt")
    if os.path.exists(context_path):
        with open(context_path, "r", encoding="utf-8") as f:
            content = f.read().strip()
            if content:
                return content
    # Default fallback context
    return "You are NeoIITian, an AI assistant built for IIT students. Be helpful, polite, and concise."

def get_response(user_input: str):
    """Generate a response using the configured LLM and contextual knowledge."""
    llm = get_llm()

    # Handle initialization or config errors
    if isinstance(llm, str):
        return llm  # It's an error message

    # Load context dynamically
    context = load_context()

    # Create a prompt using the dataset context
    prompt = f"""{context}

User: {user_input}
NeoIITian:"""

    try:
        response = llm(prompt)
        # Some Gemini models return dict-like responses
        if isinstance(response, dict) and "text" in response:
            return response["text"]
        return str(response)
    except Exception as e:
        return f"⚠️ LLM Error: {str(e)}"
