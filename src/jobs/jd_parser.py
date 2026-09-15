from pathlib import Path


def load_job_description(file_path):
    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(f"Job description not found: {file_path}")

    return path.read_text(encoding="utf-8")


if __name__ == "__main__":
    jd = load_job_description("data/jobs/test_jd.txt")

    print("=" * 60)
    print("JOB DESCRIPTION")
    print("=" * 60)
    print(jd)