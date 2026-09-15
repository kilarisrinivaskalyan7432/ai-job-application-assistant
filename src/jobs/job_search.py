from pathlib import Path
import json


# Project root
PROJECT_ROOT = Path(__file__).resolve().parents[2]

# Jobs data file
JOBS_FILE = PROJECT_ROOT / "data" / "jobs" / "jobs.json"


def load_jobs():
    """
    Load jobs from the local jobs.json file.
    """

    if not JOBS_FILE.exists():
        raise FileNotFoundError(
            f"Jobs file not found: {JOBS_FILE}"
        )

    with open(JOBS_FILE, "r", encoding="utf-8") as file:
        jobs = json.load(file)

    return jobs


def search_jobs(
    role=None,
    location=None,
    limit=10
):
    """
    Search jobs based on role and location.
    """

    jobs = load_jobs()

    results = []

    for job in jobs:

        title = str(job.get("title", ""))
        job_location = str(job.get("location", ""))

        # Role filter
        if role:
            if role.lower() not in title.lower():
                continue

        # Location filter
        if location:
            if location.lower() not in job_location.lower():
                continue

        results.append(job)

        if len(results) >= limit:
            break

    return results


if __name__ == "__main__":

    jobs = search_jobs(
        role="Python",
        location="Hyderabad",
        limit=10
    )

    print("\n" + "=" * 70)
    print("JOB SEARCH RESULTS")
    print("=" * 70)

    if not jobs:
        print("\nNo jobs found.")

    else:
        for index, job in enumerate(jobs, start=1):

            print(f"\n{index}. {job.get('title', 'Unknown Role')}")

            print(
                f"   Company: "
                f"{job.get('company', 'Unknown')}"
            )

            print(
                f"   Location: "
                f"{job.get('location', 'Unknown')}"
            )

            print(
                f"   URL: "
                f"{job.get('url', 'Not available')}"
            )

    print("\n" + "=" * 70)