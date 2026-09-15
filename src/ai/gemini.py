import os
from pathlib import Path

from dotenv import load_dotenv
from google import genai


# ============================================================
# PROJECT ROOT
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parents[2]


# ============================================================
# LOAD ENVIRONMENT VARIABLES
# ============================================================

load_dotenv(PROJECT_ROOT / ".env")


# ============================================================
# GEMINI API KEY
# ============================================================

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")


if not GEMINI_API_KEY:
    raise ValueError(
        "GEMINI_API_KEY not found. "
        "Please add it to the .env file."
    )


# ============================================================
# GEMINI CLIENT
# ============================================================

client = genai.Client(
    api_key=GEMINI_API_KEY
)


# ============================================================
# GENERATE RESPONSE
# ============================================================

def generate_response(prompt: str) -> str:
    """
    Send a prompt to Gemini and return the generated response.
    """

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )

    return response.text


# ============================================================
# TEST
# ============================================================

if __name__ == "__main__":

    test_prompt = """
    Explain what a Python developer does
    in simple terms for a fresher.
    """

    result = generate_response(test_prompt)

    print("\n" + "=" * 70)
    print("GEMINI TEST")
    print("=" * 70)

    print("\nPrompt:")
    print(test_prompt)

    print("\nGemini Response:")
    print(result)

    print("\n" + "=" * 70)