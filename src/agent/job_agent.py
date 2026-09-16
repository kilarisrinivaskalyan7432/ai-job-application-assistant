from pathlib import Path
import sys

# Project root
PROJECT_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(PROJECT_ROOT))

from src.agent.state import AgentState
from src.agent.tools import (
    search_jobs,
    match_resume_to_job,
    create_cover_letter,
)
from src.database.db import save_recommendation
from src.database.models import ApplicationRecommendation


# ---------------------------------------------------------
# AGENT CONFIGURATION
# ---------------------------------------------------------

MATCH_THRESHOLD = 0.60


# ---------------------------------------------------------
# STEP 1: SEARCH JOBS
# ---------------------------------------------------------

def search_jobs_step(
    role: str,
    location: str,
    limit: int = 10,
) -> list[dict]:
    """
    Search for jobs matching the requested role and location.
    """

    print("\n" + "=" * 70)
    print("STEP 1: SEARCHING JOBS")
    print("=" * 70)

    jobs = search_jobs(
        role=role,
        location=location,
        limit=limit,
    )

    print(f"\nJobs found: {len(jobs)}")

    for job in jobs:
        print(
            f"- {job.get('title', 'Unknown')} "
            f"| {job.get('company', 'Unknown')} "
            f"| {job.get('location', 'Unknown')}"
        )

    return jobs


# ---------------------------------------------------------
# STEP 2: MATCH RESUME
# ---------------------------------------------------------

def match_resume_step(
    state: AgentState,
) -> AgentState:
    """
    Find the best resume for the current job.
    """

    print("\n" + "=" * 70)
    print("STEP 2: MATCHING RESUME")
    print("=" * 70)

    job = state["job"]

    job_description = str(
        job.get("description", "")
    )

    if not job_description.strip():
        state["status"] = "SKIPPED"
        state["error"] = "Job description is empty."
        return state

    result = match_resume_to_job(
        job_description
    )

    if not result:
        state["status"] = "SKIPPED"
        state["error"] = "No resume found."
        return state

    state["resume"] = result["resume"]
    state["match_score"] = result["match_score"]
    state["semantic_similarity"] = result[
        "semantic_similarity"
    ]
    state["required_skill_match"] = result[
        "required_skill_match"
    ]
    state["role_relevance"] = result[
        "role_relevance"
    ]
    state["missing_skill_penalty"] = result[
        "missing_skill_penalty"
    ]

    state["matched_skills"] = result[
        "matched_skills"
    ]

    state["missing_skills"] = result[
        "missing_skills"
    ]

    state["status"] = "MATCHED"

    print(
        f"\nBest Resume: {state['resume']}"
    )

    print(
        f"Match Score: "
        f"{state['match_score'] * 100:.2f}%"
    )

    print("\nMatched Skills:")

    for skill in state["matched_skills"]:
        print(f"  ✓ {skill}")

    print("\nMissing Skills:")

    for skill in state["missing_skills"]:
        print(f"  ✗ {skill}")

    return state


# ---------------------------------------------------------
# STEP 3: DECIDE WHETHER TO SHORTLIST
# ---------------------------------------------------------

def evaluate_match_step(
    state: AgentState,
) -> AgentState:
    """
    Decide whether the job is strong enough
    to continue to application preparation.
    """

    print("\n" + "=" * 70)
    print("STEP 3: EVALUATING MATCH")
    print("=" * 70)

    score = state.get(
        "match_score",
        0.0
    )

    print(
        f"\nMatch Score: {score * 100:.2f}%"
    )

    print(
        f"Required Threshold: "
        f"{MATCH_THRESHOLD * 100:.2f}%"
    )

    if score >= MATCH_THRESHOLD:

        state["status"] = "SHORTLISTED"

        print(
            "\n✓ Job shortlisted."
        )

    else:

        state["status"] = "SKIPPED"

        print(
            "\n✗ Match score below threshold."
        )

    return state


# ---------------------------------------------------------
# STEP 4: GENERATE COVER LETTER
# ---------------------------------------------------------

def generate_cover_letter_step(
    state: AgentState,
) -> AgentState:
    """
    Generate a tailored cover letter
    using the selected resume and job.
    """

    print("\n" + "=" * 70)
    print("STEP 4: GENERATING COVER LETTER")
    print("=" * 70)

    if state.get("status") != "SHORTLISTED":
        print(
            "\nSkipping cover letter generation."
        )
        return state

    job = state["job"]

    job_title = str(
        job.get(
            "title",
            "Unknown Role"
        )
    )

    company = str(
        job.get(
            "company",
            "Unknown Company"
        )
    )

    job_description = str(
        job.get(
            "description",
            ""
        )
    )

    cover_letter = create_cover_letter(
        job_title=job_title,
        company=company,
        job_description=job_description,
        resume_filename=state["resume"],
        matched_skills=state[
            "matched_skills"
        ],
        missing_skills=state[
            "missing_skills"
        ],
    )

    state["cover_letter"] = cover_letter

    state["status"] = "DRAFTED"

    print(
        "\n✓ Cover letter generated."
    )

    return state


# ---------------------------------------------------------
# STEP 5: SAVE RECOMMENDATION
# ---------------------------------------------------------

def save_recommendation_step(
    state: AgentState,
    database_path: str | Path = (
        PROJECT_ROOT
        / "data"
        / "autonomus_job.sqlite3"
    ),
) -> AgentState:
    """
    Save the prepared application recommendation
    to the database.

    No application is submitted.
    """

    print("\n" + "=" * 70)
    print("STEP 5: SAVING RECOMMENDATION")
    print("=" * 70)

    if state.get("status") != "DRAFTED":
        print(
            "\nSkipping database save."
        )
        return state

    recommendation = ApplicationRecommendation(
        resume_name=state["resume"],
        job_id=state["job_id"],
        score=state["match_score"],
    )

    save_recommendation(
        recommendation,
        database_path,
    )

    state["status"] = "PENDING_APPROVAL"

    print(
        "\n✓ Recommendation saved."
    )

    print(
        "Status: PENDING_APPROVAL"
    )

    return state


# ---------------------------------------------------------
# PROCESS ONE JOB
# ---------------------------------------------------------

def process_job(
    job: dict,
    job_id: str,
    database_path: str | Path = (
        PROJECT_ROOT
        / "data"
        / "autonomus_job.sqlite3"
    ),
) -> AgentState:
    """
    Run the complete agent workflow for one job.
    """

    state: AgentState = {
        "job": job,
        "job_id": job_id,
        "status": "FOUND",
    }

    print("\n\n")
    print("#" * 70)
    print("PROCESSING JOB")
    print("#" * 70)

    print(
        f"\nTitle: "
        f"{job.get('title', 'Unknown')}"
    )

    print(
        f"Company: "
        f"{job.get('company', 'Unknown')}"
    )

    print(
        f"Location: "
        f"{job.get('location', 'Unknown')}"
    )

    # Step 2
    state = match_resume_step(state)

    # Stop if matching failed
    if state.get("status") == "SKIPPED":
        return state

    # Step 3
    state = evaluate_match_step(state)

    # Stop if score is too low
    if state.get("status") == "SKIPPED":
        return state

    # Step 4
    state = generate_cover_letter_step(state)

    # Step 5
    state = save_recommendation_step(
        state,
        database_path,
    )

    return state


# ---------------------------------------------------------
# RUN COMPLETE AGENT
# ---------------------------------------------------------

def run_agent(
    role: str = None,
    location: str = None,
    limit: int = 10,
    database_path: str | Path = (
        PROJECT_ROOT
        / "data"
        / "autonomus_job.sqlite3"
    ),
) -> list[AgentState]:
    """
    Run the complete job application preparation workflow.
    """

    print("\n")
    print("=" * 70)
    print("AUTONOMOUS AI JOB APPLICATION AGENT")
    print("=" * 70)

    print(
        f"\nRole: {role}"
    )

    print(
        f"Location: {location}"
    )

    # Step 1
    jobs = search_jobs_step(
        role=role,
        location=location,
        limit=limit,
    )

    if not jobs:
        print(
            "\nNo jobs found."
        )
        return []

    results = []

    for index, job in enumerate(
        jobs,
        start=1
    ):

        state = process_job(
            job=job,
            job_id=str(index),
            database_path=database_path,
        )

        results.append(state)

    return results


# ---------------------------------------------------------
# TEST
# ---------------------------------------------------------

if __name__ == "__main__":

    results = run_agent(
        role=None,
        location=None,
        limit=10,
    )

    print("\n")
    print("=" * 70)
    print("FINAL AGENT RESULTS")
    print("=" * 70)

    print(
        f"\nJobs processed: {len(results)}"
    )

    for index, state in enumerate(
        results,
        start=1
    ):

        job = state["job"]

        print("\n" + "-" * 70)

        print(
            f"{index}. "
            f"{job.get('title', 'Unknown')}"
        )

        print(
            f"Company: "
            f"{job.get('company', 'Unknown')}"
        )

        print(
            f"Resume: "
            f"{state.get('resume', 'None')}"
        )

        print(
            f"Match Score: "
            f"{state.get('match_score', 0) * 100:.2f}%"
        )

        print(
            f"Status: "
            f"{state.get('status', 'UNKNOWN')}"
        )

        if state.get("error"):
            print(
                f"Error: "
                f"{state['error']}"
            )

    print("\n" + "=" * 70)
    print("AGENT WORKFLOW COMPLETED")
    print("=" * 70)