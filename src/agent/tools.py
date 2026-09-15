from pathlib import Path
from typing import Any

from src.database.db import set_status
from src.main import build_recommendations
from src.jobs.job_manager import load_jobs
from src.resume.resume_manager import load_all_resumes
from src.resume.resume_selector import rank_resumes
from src.ai.cover_letter import generate_cover_letter


# ============================================================
# PREPARE RECOMMENDATIONS
# ============================================================

def prepare_recommendations(
    jobs_path: str | Path = "data/jobs/jobs.json",
    database_path: str | Path = "data/autonomus_job.sqlite3",
) -> list[dict[str, object]]:
    """
    Prepare job recommendations without submitting applications.

    The function:
    1. Loads available jobs.
    2. Matches each job with available resumes.
    3. Selects the best resume.
    4. Calculates the match score.
    5. Saves the recommendation to the database.

    No application is submitted automatically.
    """

    return build_recommendations(
        jobs_path=jobs_path,
        database_path=database_path,
    )


# ============================================================
# SEARCH JOBS
# ============================================================

def search_jobs(
    role: str | None = None,
    location: str | None = None,
    limit: int = 10,
) -> list[dict[str, Any]]:
    """
    Search available jobs by role and location.
    """

    jobs = load_jobs(
        Path("data/jobs/jobs.json")
    )

    results = []

    for job in jobs:

        title = str(
            job.get("title", "")
        )

        job_location = str(
            job.get("location", "")
        )

        # Role filter
        if role and role.lower() not in title.lower():
            continue

        # Location filter
        if (
            location
            and location.lower()
            not in job_location.lower()
        ):
            continue

        results.append(job)

        if len(results) >= limit:
            break

    return results


# ============================================================
# MATCH RESUME TO JOB
# ============================================================

def match_resume_to_job(
    job_description: str,
) -> dict[str, Any]:
    """
    Compare all available resumes against a job description
    and return the best matching resume.
    """

    if not job_description.strip():

        raise ValueError(
            "Job description cannot be empty."
        )

    results = rank_resumes(
        job_description
    )

    if not results:
        return {}

    best = results[0]

    score = best["score"]

    return {
        "resume": best["filename"],
        "match_score": score.total,
        "semantic_similarity": score.semantic_similarity,
        "required_skill_match": score.required_skill_match,
        "role_relevance": score.role_relevance,
        "missing_skill_penalty": score.missing_skill_penalty,
        "matched_skills": list(
            score.matched_skills
        ),
        "missing_skills": list(
            score.missing_skills
        ),
    }


# ============================================================
# GENERATE COVER LETTER
# ============================================================

def create_cover_letter(
    job_title: str,
    company: str,
    job_description: str,
    resume_filename: str,
    matched_skills: list[str],
    missing_skills: list[str],
) -> str:
    """
    Generate a tailored cover letter using the selected resume.
    """

    resumes = load_all_resumes()

    resume_text = resumes.get(
        resume_filename
    )

    if not resume_text:

        raise ValueError(
            f"Resume not found: {resume_filename}"
        )

    return generate_cover_letter(
        job_title=job_title,
        company=company,
        job_description=job_description,
        resume_text=resume_text,
        matched_skills=matched_skills,
        missing_skills=missing_skills,
    )


# ============================================================
# APPROVE RECOMMENDATION
# ============================================================

def approve_recommendation(
    recommendation_id: int,
    database_path: str | Path = "data/autonomus_job.sqlite3",
) -> None:
    """
    Record explicit human approval.

    Application submission remains a separate action.
    """

    set_status(
        recommendation_id,
        "approved",
        database_path
    )


# ============================================================
# TEST
# ============================================================

if __name__ == "__main__":

    print("\n" + "=" * 70)
    print("AGENT TOOLS TEST")
    print("=" * 70)

    # --------------------------------------------------------
    # Test 1: Search Jobs
    # --------------------------------------------------------

    print("\n1. SEARCH JOBS")
    print("-" * 70)

    jobs = search_jobs(
        role="Python",
        location="Hyderabad",
        limit=10
    )

    print(
        f"Jobs found: {len(jobs)}"
    )

    for job in jobs:

        print(
            f"- {job.get('title', 'Unknown')} "
            f"| {job.get('company', 'Unknown')} "
            f"| {job.get('location', 'Unknown')}"
        )

    # --------------------------------------------------------
    # Test 2: Match Resume
    # --------------------------------------------------------

    if jobs:

        job = jobs[0]

        job_description = str(
            job.get(
                "description",
                ""
            )
        )

        print("\n2. MATCH RESUME")
        print("-" * 70)

        match_result = match_resume_to_job(
            job_description
        )

        print(
            f"Best Resume: "
            f"{match_result.get('resume')}"
        )

        print(
            f"Match Score: "
            f"{match_result.get('match_score', 0) * 100:.2f}%"
        )

        print("\nMatched Skills:")

        for skill in match_result.get(
            "matched_skills",
            []
        ):

            print(
                f"  ✓ {skill}"
            )

        print("\nMissing Skills:")

        for skill in match_result.get(
            "missing_skills",
            []
        ):

            print(
                f"  ✗ {skill}"
            )

        # ----------------------------------------------------
        # Test 3: Generate Cover Letter
        # ----------------------------------------------------

        print("\n3. GENERATE COVER LETTER")
        print("-" * 70)

        cover_letter = create_cover_letter(
            job_title=str(
                job.get(
                    "title",
                    "Unknown Role"
                )
            ),
            company=str(
                job.get(
                    "company",
                    "Unknown Company"
                )
            ),
            job_description=job_description,
            resume_filename=match_result["resume"],
            matched_skills=match_result[
                "matched_skills"
            ],
            missing_skills=match_result[
                "missing_skills"
            ],
        )

        print("\nGenerated Cover Letter:")
        print("-" * 70)
        print(cover_letter)
        print("-" * 70)

    else:

        print(
            "\nNo jobs available for testing."
        )

    print("\n" + "=" * 70)