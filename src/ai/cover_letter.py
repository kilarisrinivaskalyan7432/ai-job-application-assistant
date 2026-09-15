from pathlib import Path
import sys


# ============================================================
# PROJECT ROOT
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parents[2]

sys.path.insert(0, str(PROJECT_ROOT))


# ============================================================
# IMPORT AI FUNCTIONS
# ============================================================

from src.ai.gemini import generate_response
from src.ai.prompts import build_cover_letter_prompt


# ============================================================
# GENERATE COVER LETTER
# ============================================================

def generate_cover_letter(
    job_title: str,
    company: str,
    job_description: str,
    resume_text: str,
    matched_skills: list[str],
    missing_skills: list[str]
) -> str:
    """
    Generate a tailored cover letter using Gemini.
    """

    # Build the prompt
    prompt = build_cover_letter_prompt(
        job_title=job_title,
        company=company,
        job_description=job_description,
        resume_text=resume_text,
        matched_skills=matched_skills,
        missing_skills=missing_skills
    )

    # Send prompt to Gemini
    cover_letter = generate_response(prompt)

    return cover_letter.strip()


# ============================================================
# TEST
# ============================================================

if __name__ == "__main__":

    test_job_title = "Python Developer"

    test_company = "Test Company"

    test_job_description = """
    We are looking for an entry-level Python Developer.

    Requirements:
    - Python
    - SQL
    - REST APIs
    - Git
    - Pandas
    - FastAPI
    """

    test_resume = """
    Srinivas Kalyan Kilari

    Electronics and Communication Engineering graduate.

    Skills:
    Python, SQL, FastAPI, REST API, Pandas, NumPy,
    LangChain, Google Gemini API, Git, GitHub.

    Projects:
    Smart Resume-JD Matcher
    Intelligent Document Search and Question Answering System
    Diabetes Prediction System
    """

    test_matched_skills = [
        "Python",
        "SQL",
        "REST API",
        "Git",
        "Pandas"
    ]

    test_missing_skills = [
        "FastAPI"
    ]

    print("\n" + "=" * 70)
    print("COVER LETTER GENERATION TEST")
    print("=" * 70)

    try:

        cover_letter = generate_cover_letter(
            job_title=test_job_title,
            company=test_company,
            job_description=test_job_description,
            resume_text=test_resume,
            matched_skills=test_matched_skills,
            missing_skills=test_missing_skills
        )

        print("\nGENERATED COVER LETTER:")
        print("-" * 70)
        print(cover_letter)
        print("-" * 70)

    except Exception as error:

        print("\nERROR:")
        print(error)

    print("\n" + "=" * 70)