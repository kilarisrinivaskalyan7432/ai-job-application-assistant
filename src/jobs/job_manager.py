import json
from pathlib import Path
from typing import Any
import sys


# ============================================================
# PROJECT ROOT
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parents[2]

# Make src importable
sys.path.insert(0, str(PROJECT_ROOT))


# ============================================================
# LOAD JOBS
# ============================================================

def load_jobs(
    jobs_path: str | Path = "data/jobs/jobs.json"
) -> list[dict[str, Any]]:
    """
    Load job descriptions from a JSON array
    or a JSON object containing a 'jobs' list.
    """

    path = Path(jobs_path)

    if not path.exists():
        return []

    content = path.read_text(encoding="utf-8").strip()

    if not content:
        return []

    payload = json.loads(content)

    if isinstance(payload, list):
        jobs = payload

    elif (
        isinstance(payload, dict)
        and isinstance(payload.get("jobs"), list)
    ):
        jobs = payload["jobs"]

    else:
        raise ValueError(
            "jobs.json must contain a list "
            "or an object with a 'jobs' list"
        )

    return [
        job
        for job in jobs
        if isinstance(job, dict)
    ]


# ============================================================
# GET JOB DESCRIPTION
# ============================================================

def get_job_description(
    job: dict[str, Any]
) -> str:
    """
    Extract the job description text from a job dictionary.
    """

    description = job.get("description")

    if description is None:
        description = job.get("job_description")

    if description is None:
        description = job.get("jd")

    if description is None:
        return ""

    return str(description)


# ============================================================
# FIND BEST RESUME
# ============================================================

def find_best_resume_for_job(
    job: dict[str, Any]
):
    """
    Compare all available resumes against a job
    and return the best matching resume.
    """

    from src.resume.resume_selector import rank_resumes

    job_description = get_job_description(job)

    if not job_description.strip():
        raise ValueError(
            "Job does not contain a description."
        )

    results = rank_resumes(job_description)

    if not results:
        return None

    return results[0]


# ============================================================
# PROCESS A JOB
# ============================================================

def process_job(
    job: dict[str, Any]
) -> dict[str, Any]:
    """
    Process one job and determine the best resume
    for that job.
    """

    best_resume = find_best_resume_for_job(job)

    if best_resume is None:
        return {
            "job": job,
            "best_resume": None
        }

    score = best_resume["score"]

    return {
        "job": job,
        "best_resume": best_resume["filename"],
        "match_score": score.total,
        "semantic_similarity": score.semantic_similarity,
        "required_skill_match": score.required_skill_match,
        "role_relevance": score.role_relevance,
        "missing_skill_penalty": score.missing_skill_penalty,
        "matched_skills": list(score.matched_skills),
        "missing_skills": list(score.missing_skills)
    }


# ============================================================
# GENERATE APPLICATION FOR A JOB
# ============================================================

def generate_application_for_job(
    job: dict[str, Any]
) -> dict[str, Any]:
    """
    Find the best resume for a job and generate
    a tailored cover letter using Gemini.
    """

    # Import cover-letter generator
    from src.ai.cover_letter import generate_cover_letter

    # --------------------------------------------------------
    # Find best resume
    # --------------------------------------------------------

    best_resume = find_best_resume_for_job(job)

    if best_resume is None:
        raise ValueError(
            "No suitable resume found for this job."
        )

    # --------------------------------------------------------
    # Get best resume filename and score
    # --------------------------------------------------------

    best_resume_filename = best_resume["filename"]
    score = best_resume["score"]

    # --------------------------------------------------------
    # Load all resumes
    # --------------------------------------------------------

    from src.resume.resume_manager import load_all_resumes

    resumes = load_all_resumes()

    resume_text = resumes.get(best_resume_filename)

    if not resume_text:
        raise ValueError(
            f"Resume text not found: {best_resume_filename}"
        )

    # --------------------------------------------------------
    # Get job information
    # --------------------------------------------------------

    job_title = str(
        job.get("title", "Unknown Role")
    )

    company = str(
        job.get("company", "Unknown Company")
    )

    job_description = get_job_description(job)

    if not job_description.strip():
        raise ValueError(
            "Job description is empty."
        )

    # --------------------------------------------------------
    # Generate tailored cover letter
    # --------------------------------------------------------

    cover_letter = generate_cover_letter(
        job_title=job_title,
        company=company,
        job_description=job_description,
        resume_text=resume_text,
        matched_skills=list(score.matched_skills),
        missing_skills=list(score.missing_skills)
    )

    # --------------------------------------------------------
    # Return complete application information
    # --------------------------------------------------------

    return {
        "job": job,
        "best_resume": best_resume_filename,

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

        "cover_letter": cover_letter
    }


# ============================================================
# TEST
# ============================================================

if __name__ == "__main__":

    JOBS_FILE = (
        PROJECT_ROOT
        / "data"
        / "jobs"
        / "jobs.json"
    )

    # --------------------------------------------------------
    # Load jobs
    # --------------------------------------------------------

    jobs = load_jobs(JOBS_FILE)

    print("\n" + "=" * 80)
    print("JOB APPLICATION AGENT TEST")
    print("=" * 80)

    print(
        f"\nTotal jobs loaded: {len(jobs)}"
    )

    if not jobs:

        print("\nNo jobs found.")

    else:

        # ----------------------------------------------------
        # Test the first job only
        # ----------------------------------------------------

        job = jobs[0]

        print("\n" + "-" * 80)

        print(
            f"JOB: "
            f"{job.get('title', 'Unknown Role')}"
        )

        print(
            f"Company: "
            f"{job.get('company', 'Unknown')}"
        )

        print(
            f"Location: "
            f"{job.get('location', 'Unknown')}"
        )

        print("-" * 80)

        try:

            # ------------------------------------------------
            # Generate application
            # ------------------------------------------------

            result = generate_application_for_job(
                job
            )

            # ------------------------------------------------
            # Display best resume
            # ------------------------------------------------

            print("\nBEST RESUME:")

            print(
                result["best_resume"]
            )

            # ------------------------------------------------
            # Display scores
            # ------------------------------------------------

            print(
                f"\nOVERALL MATCH: "
                f"{result['match_score'] * 100:.2f}%"
            )

            print(
                f"Semantic Similarity: "
                f"{result['semantic_similarity'] * 100:.2f}%"
            )

            print(
                f"Required Skill Match: "
                f"{result['required_skill_match'] * 100:.2f}%"
            )

            print(
                f"Role Relevance: "
                f"{result['role_relevance'] * 100:.2f}%"
            )

            print(
                f"Missing Skill Penalty: "
                f"{result['missing_skill_penalty'] * 100:.2f}%"
            )

            # ------------------------------------------------
            # Display matched skills
            # ------------------------------------------------

            print("\nMATCHED SKILLS:")

            if result["matched_skills"]:

                for skill in result["matched_skills"]:
                    print(f"  ✓ {skill}")

            else:

                print("  None")

            # ------------------------------------------------
            # Display missing skills
            # ------------------------------------------------

            print("\nMISSING SKILLS:")

            if result["missing_skills"]:

                for skill in result["missing_skills"]:
                    print(f"  ✗ {skill}")

            else:

                print("  None")

            # ------------------------------------------------
            # Display generated cover letter
            # ------------------------------------------------

            print("\n" + "=" * 80)
            print("GENERATED COVER LETTER")
            print("=" * 80)

            print(
                result["cover_letter"]
            )

            print("\n" + "=" * 80)

        except Exception as error:

            print("\nERROR:")
            print(error)

    print("\n" + "=" * 80)