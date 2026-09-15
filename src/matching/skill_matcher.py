from pathlib import Path
import re


# --------------------------------------------------
# Project paths
# --------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parents[2]

SKILLS_FILE = PROJECT_ROOT / "data" / "skills_list.txt"
JD_FILE = PROJECT_ROOT / "data" / "jobs" / "test_jd.txt"


# --------------------------------------------------
# Load skills
# --------------------------------------------------

def load_skills():

    if not SKILLS_FILE.exists():
        raise FileNotFoundError(
            f"Skills file not found: {SKILLS_FILE}"
        )

    skills = []

    with open(SKILLS_FILE, "r", encoding="utf-8") as file:

        for line in file:

            skill = line.strip()

            if skill:
                skills.append(skill)

    return skills


# --------------------------------------------------
# Normalize text
# --------------------------------------------------

def normalize_text(text):

    text = text.lower()

    text = re.sub(r"[^a-z0-9+#.\s]", " ", text)

    text = re.sub(r"\s+", " ", text)

    return text


# --------------------------------------------------
# Extract skills from text
# --------------------------------------------------

def extract_skills(text, skills):

    normalized_text = normalize_text(text)

    matched_skills = []

    for skill in skills:

        normalized_skill = normalize_text(skill)

        if normalized_skill in normalized_text:

            matched_skills.append(skill)

    return matched_skills


# --------------------------------------------------
# Calculate skill match
# --------------------------------------------------

def calculate_skill_match(resume_text, job_description):

    skills = load_skills()

    required_skills = extract_skills(
        job_description,
        skills
    )

    resume_skills = extract_skills(
        resume_text,
        skills
    )

    matched_skills = [
        skill
        for skill in required_skills
        if skill in resume_skills
    ]

    missing_skills = [
        skill
        for skill in required_skills
        if skill not in resume_skills
    ]

    if len(required_skills) == 0:
        skill_score = 0.0

    else:
        skill_score = (
            len(matched_skills) /
            len(required_skills)
        )

    return {
        "required_skills": required_skills,
        "matched_skills": matched_skills,
        "missing_skills": missing_skills,
        "score": skill_score
    }


# --------------------------------------------------
# Test
# --------------------------------------------------

if __name__ == "__main__":

    job_description = JD_FILE.read_text(
        encoding="utf-8"
    )

    test_resume = """
    Python Developer with experience in Python,
    Object-Oriented Programming, SQL, MySQL,
    REST APIs, JSON, Git, GitHub, Pandas,
    NumPy and FastAPI.
    """

    result = calculate_skill_match(
        test_resume,
        job_description
    )

    print("\n" + "=" * 60)
    print("SKILL MATCHING TEST")
    print("=" * 60)

    print("\nRequired Skills:")
    for skill in result["required_skills"]:
        print(f"- {skill}")

    print("\nMatched Skills:")
    for skill in result["matched_skills"]:
        print(f"- {skill}")

    print("\nMissing Skills:")
    for skill in result["missing_skills"]:
        print(f"- {skill}")

    print(
        f"\nSkill Match Score: "
        f"{result['score'] * 100:.2f}%"
    )

    print("=" * 60)