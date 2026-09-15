from pathlib import Path
import sys

# Project root
PROJECT_ROOT = Path(__file__).resolve().parents[2]

# Make src importable
sys.path.insert(0, str(PROJECT_ROOT))

from src.resume.resume_manager import load_all_resumes
from src.jobs.jd_parser import load_job_description
from src.matching.scorer import score_resume_against_job


def rank_resumes(job_description):
    """
    Score and rank all available resumes
    against the given job description.
    """

    resumes = load_all_resumes()

    results = []

    for filename, resume_text in resumes.items():

        score = score_resume_against_job(
            resume_text,
            job_description
        )

        results.append({
            "filename": filename,
            "score": score
        })

    # Highest score first
    results.sort(
        key=lambda item: item["score"].total,
        reverse=True
    )

    return results


if __name__ == "__main__":

    JD_FILE = PROJECT_ROOT / "data" / "jobs" / "test_jd.txt"

    job_description = load_job_description(JD_FILE)

    results = rank_resumes(job_description)

    print("\n" + "=" * 80)
    print("RESUME RANKING")
    print("=" * 80)

    for rank, result in enumerate(results, start=1):

        filename = result["filename"]
        score = result["score"]

        print(
            f"\n{rank}. {filename}"
        )

        print(
            f"   Overall Match: "
            f"{score.total * 100:.2f}%"
        )

        print(
            f"   Semantic: "
            f"{score.semantic_similarity * 100:.2f}%"
        )

        print(
            f"   Skills: "
            f"{score.required_skill_match * 100:.2f}%"
        )

        print(
            f"   Role Relevance: "
            f"{score.role_relevance * 100:.2f}%"
        )

        print(
            f"   Missing Skills: "
            f"{score.missing_skill_penalty * 100:.2f}%"
        )

    print("\n" + "=" * 80)

    if results:
        best_resume = results[0]

        print(
            "\nBEST RESUME:"
        )

        print(
            best_resume["filename"]
        )

        print(
            f"Match Score: "
            f"{best_resume['score'].total * 100:.2f}%"
        )

    print("=" * 80)