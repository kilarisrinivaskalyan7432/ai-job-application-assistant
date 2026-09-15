from dataclasses import asdict, dataclass
from pathlib import Path
import sys

# Project root
PROJECT_ROOT = Path(__file__).resolve().parents[2]

# Make src importable
sys.path.insert(0, str(PROJECT_ROOT))

from src.matching.semantic_matcher import calculate_semantic_similarity
from src.matching.skill_matcher import calculate_skill_match


@dataclass(frozen=True)
class MatchScore:
    total: float
    semantic_similarity: float
    required_skill_match: float
    role_relevance: float
    missing_skill_penalty: float
    matched_skills: tuple[str, ...]
    missing_skills: tuple[str, ...]

    def as_dict(self) -> dict[str, object]:
        return asdict(self)


def calculate_role_relevance(
    resume_text: str,
    job_description: str
) -> float:

    role_keywords = [
        "python",
        "developer",
        "software",
        "backend",
        "engineer",
        "data",
        "machine learning",
        "ai",
        "artificial intelligence",
        "api",
        "fastapi",
    ]

    resume_lower = resume_text.lower()
    job_lower = job_description.lower()

    job_role_keywords = [
        keyword
        for keyword in role_keywords
        if keyword in job_lower
    ]

    if not job_role_keywords:
        return 0.0

    matched_keywords = [
        keyword
        for keyword in job_role_keywords
        if keyword in resume_lower
    ]

    return len(matched_keywords) / len(job_role_keywords)


def score_resume_against_job(
    resume_text: str,
    job_description: str
) -> MatchScore:

    # 1. Semantic similarity
    semantic_score = calculate_semantic_similarity(
        resume_text,
        job_description
    )

    # 2. Skill matching
    skill_result = calculate_skill_match(
        resume_text,
        job_description
    )

    skill_score = skill_result["score"]

    matched_skills = skill_result["matched_skills"]
    missing_skills = skill_result["missing_skills"]

    # 3. Role relevance
    role_score = calculate_role_relevance(
        resume_text,
        job_description
    )

    # 4. Missing skill penalty
    total_required_skills = (
        len(matched_skills) + len(missing_skills)
    )

    if total_required_skills == 0:
        missing_penalty = 0.0
    else:
        missing_penalty = (
            len(missing_skills) / total_required_skills
        )

    # 5. Final score
    total_score = (
        0.40 * semantic_score
        + 0.35 * skill_score
        + 0.25 * role_score
        - 0.10 * missing_penalty
    )

    # Keep score between 0 and 1
    total_score = max(
        0.0,
        min(1.0, total_score)
    )

    return MatchScore(
        total=total_score,
        semantic_similarity=semantic_score,
        required_skill_match=skill_score,
        role_relevance=role_score,
        missing_skill_penalty=missing_penalty,
        matched_skills=tuple(sorted(matched_skills)),
        missing_skills=tuple(sorted(missing_skills)),
    )


if __name__ == "__main__":

    JD_FILE = PROJECT_ROOT / "data" / "jobs" / "test_jd.txt"

    if not JD_FILE.exists():
        raise FileNotFoundError(
            f"Job description not found: {JD_FILE}"
        )

    job_description = JD_FILE.read_text(
        encoding="utf-8"
    )

    test_resume = """
    Python Developer with experience in Python,
    Object-Oriented Programming, SQL, MySQL,
    REST APIs, JSON, Git, GitHub, Pandas,
    NumPy and FastAPI.
    """

    result = score_resume_against_job(
        test_resume,
        job_description
    )

    print("\n" + "=" * 70)
    print("RESUME - JOB MATCH SCORE")
    print("=" * 70)

    print(
        f"\nOverall Match Score: "
        f"{result.total * 100:.2f}%"
    )

    print(
        f"Semantic Similarity: "
        f"{result.semantic_similarity * 100:.2f}%"
    )

    print(
        f"Required Skill Match: "
        f"{result.required_skill_match * 100:.2f}%"
    )

    print(
        f"Role Relevance: "
        f"{result.role_relevance * 100:.2f}%"
    )

    print(
        f"Missing Skill Penalty: "
        f"{result.missing_skill_penalty * 100:.2f}%"
    )

    print("\nMatched Skills:")

    if result.matched_skills:
        for skill in result.matched_skills:
            print(f"  ✓ {skill}")
    else:
        print("  None")

    print("\nMissing Skills:")

    if result.missing_skills:
        for skill in result.missing_skills:
            print(f"  ✗ {skill}")
    else:
        print("  None")

    print("=" * 70)