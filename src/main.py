from pathlib import Path
import sys


# ============================================================
# PROJECT ROOT
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parents[1]

sys.path.insert(0, str(PROJECT_ROOT))


# ============================================================
# IMPORTS
# ============================================================

from src.database.db import save_recommendation
from src.database.models import ApplicationRecommendation
from src.jobs.job_manager import load_jobs, get_job_description
from src.resume.resume_selector import rank_resumes


# ============================================================
# BUILD RECOMMENDATIONS
# ============================================================

def build_recommendations(
    jobs_path: str | Path = PROJECT_ROOT / "data" / "jobs" / "jobs.json",
    database_path: str | Path = PROJECT_ROOT / "data" / "autonomus_job.sqlite3",
) -> list[dict[str, object]]:
    """
    Load jobs, find the best matching resume for each job,
    and save the recommendations to the database.

    No job application is submitted automatically.
    """

    # --------------------------------------------------------
    # Load jobs
    # --------------------------------------------------------

    jobs = load_jobs(jobs_path)

    print(f"\nJobs loaded: {len(jobs)}")

    recommendations = []

    # --------------------------------------------------------
    # Process every job
    # --------------------------------------------------------

    for index, job in enumerate(jobs, start=1):

        print("\n" + "-" * 80)
        print(f"PROCESSING JOB {index}")
        print("-" * 80)

        title = str(
            job.get("title", "Unknown Role")
        )

        company = str(
            job.get("company", "Unknown Company")
        )

        location = str(
            job.get("location", "Unknown Location")
        )

        print(f"Title: {title}")
        print(f"Company: {company}")
        print(f"Location: {location}")

        # ----------------------------------------------------
        # Get job description
        # ----------------------------------------------------

        job_description = get_job_description(job)

        if not job_description.strip():

            print(
                "Skipping: Job description is empty."
            )

            continue

        # ----------------------------------------------------
        # Find best resume
        # ----------------------------------------------------

        print("\nFinding best resume...")

        rankings = rank_resumes(
            job_description
        )

        print(
            f"Resumes ranked: {len(rankings)}"
        )

        if not rankings:

            print(
                "Skipping: No resumes found."
            )

            continue

        # ----------------------------------------------------
        # Get best resume
        # ----------------------------------------------------

        best_resume = rankings[0]

        resume_filename = best_resume["filename"]

        score = best_resume["score"]

        print(
            f"\nBest Resume: {resume_filename}"
        )

        print(
            f"Match Score: "
            f"{score.total * 100:.2f}%"
        )

        print(
            f"Semantic Similarity: "
            f"{score.semantic_similarity * 100:.2f}%"
        )

        print(
            f"Required Skill Match: "
            f"{score.required_skill_match * 100:.2f}%"
        )

        print(
            f"Role Relevance: "
            f"{score.role_relevance * 100:.2f}%"
        )

        print(
            f"Missing Skill Penalty: "
            f"{score.missing_skill_penalty * 100:.2f}%"
        )

        # ----------------------------------------------------
        # Job ID
        # ----------------------------------------------------
        # Your current jobs.json does not contain an ID.
        # Therefore, we use the job's position in jobs.json.

        job_id = str(index)

        print(
            f"Job ID: {job_id}"
        )

        # ----------------------------------------------------
        # Display matched skills
        # ----------------------------------------------------

        print("\nMatched Skills:")

        if score.matched_skills:

            for skill in score.matched_skills:

                print(
                    f"  ✓ {skill}"
                )

        else:

            print("  None")

        # ----------------------------------------------------
        # Display missing skills
        # ----------------------------------------------------

        print("\nMissing Skills:")

        if score.missing_skills:

            for skill in score.missing_skills:

                print(
                    f"  ✗ {skill}"
                )

        else:

            print("  None")

        # ----------------------------------------------------
        # Create database recommendation
        # ----------------------------------------------------

        recommendation = ApplicationRecommendation(
            resume_name=resume_filename,
            job_id=job_id,
            score=score.total,
        )

        print(
            "\nSaving recommendation to database..."
        )

        save_recommendation(
            recommendation,
            database_path,
        )

        print(
            "Recommendation saved."
        )

        # ----------------------------------------------------
        # Store recommendation in memory
        # ----------------------------------------------------

        recommendations.append(
            {
                "job": job,
                "job_id": job_id,
                "resume": resume_filename,
                "score": score,
                "matched_skills": list(
                    score.matched_skills
                ),
                "missing_skills": list(
                    score.missing_skills
                ),
            }
        )

    return recommendations


# ============================================================
# MAIN PROGRAM
# ============================================================

if __name__ == "__main__":

    print("\n" + "=" * 80)
    print("AUTONOMOUS AI JOB APPLICATION AGENT")
    print("=" * 80)

    try:

        # ----------------------------------------------------
        # Build recommendations
        # ----------------------------------------------------

        recommendations = build_recommendations()

        # ----------------------------------------------------
        # Final results
        # ----------------------------------------------------

        print("\n" + "=" * 80)
        print("FINAL RESULTS")
        print("=" * 80)

        print(
            f"\nTotal recommendations: "
            f"{len(recommendations)}"
        )

        # ----------------------------------------------------
        # Print every recommendation
        # ----------------------------------------------------

        for index, recommendation in enumerate(
            recommendations,
            start=1
        ):

            job = recommendation["job"]

            score = recommendation["score"]

            print("\n" + "-" * 80)

            print(
                f"{index}. "
                f"{job.get('title', 'Unknown Role')}"
            )

            print(
                f"   Company: "
                f"{job.get('company', 'Unknown Company')}"
            )

            print(
                f"   Location: "
                f"{job.get('location', 'Unknown Location')}"
            )

            print(
                f"   Job ID: "
                f"{recommendation['job_id']}"
            )

            print(
                f"   Best Resume: "
                f"{recommendation['resume']}"
            )

            print(
                f"   Match Score: "
                f"{score.total * 100:.2f}%"
            )

            print(
                "\n   Matched Skills:"
            )

            if recommendation["matched_skills"]:

                for skill in recommendation[
                    "matched_skills"
                ]:

                    print(
                        f"      ✓ {skill}"
                    )

            else:

                print(
                    "      None"
                )

            print(
                "\n   Missing Skills:"
            )

            if recommendation["missing_skills"]:

                for skill in recommendation[
                    "missing_skills"
                ]:

                    print(
                        f"      ✗ {skill}"
                    )

            else:

                print(
                    "      None"
                )

        # ----------------------------------------------------
        # Completed
        # ----------------------------------------------------

        print("\n" + "=" * 80)
        print("PROCESS COMPLETED")
        print("=" * 80)

    except Exception as error:

        print("\n" + "=" * 80)
        print("ERROR")
        print("=" * 80)

        print(
            f"\n{type(error).__name__}: {error}"
        )

        print("\n" + "=" * 80)