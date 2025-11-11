import google.generativeai as genai
from .config import GEMINI_API_KEY, LLM_PROVIDER

def get_llm():
    """Return a function that calls Gemini API directly."""
    if LLM_PROVIDER.lower() == "gemini":
        if not GEMINI_API_KEY:
            return "❌ GEMINI_API_KEY missing in .env"

        try:
            # Configure API
            genai.configure(api_key=GEMINI_API_KEY)

            # Use a working Gemini Pro model
            model = genai.GenerativeModel("models/gemini-2.5-pro")

            # Return a callable
            def call_gemini(prompt: str):
                response = model.generate_content(prompt)
                return response.text

            return call_gemini

        except Exception as e:
            return f"⚠️ Gemini API Error: {str(e)}"

    return "⚠️ Only Gemini is supported in this setup."
