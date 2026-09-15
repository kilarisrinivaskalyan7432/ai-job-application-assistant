from pathlib import Path
import sys

from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity


# --------------------------------------------------
# Project paths
# --------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parents[2]

JD_FILE = PROJECT_ROOT / "data" / "jobs" / "test_jd.txt"


# --------------------------------------------------
# Import resume manager
# --------------------------------------------------

sys.path.insert(0, str(PROJECT_ROOT))

from src.resume.resume_manager import load_all_resumes


# --------------------------------------------------
# Load embedding model
# --------------------------------------------------

model = SentenceTransformer("all-MiniLM-L6-v2")


# --------------------------------------------------
# Semantic similarity
# --------------------------------------------------

def calculate_semantic_similarity(resume_text, job_description):

    resume_embedding = model.encode([resume_text])
    jd_embedding = model.encode([job_description])

    similarity = cosine_similarity(
        resume_embedding,
        jd_embedding
    )[0][0]

    return float(similarity)


# --------------------------------------------------
# Load Job Description
# --------------------------------------------------

def load_job_description():

    if not JD_FILE.exists():
        raise FileNotFoundError(
            f"Job description not found: {JD_FILE}"
        )

    return JD_FILE.read_text(encoding="utf-8")


# --------------------------------------------------
# Rank resumes
# --------------------------------------------------

def rank_resumes():

    job_description = load_job_description()

    resumes = load_all_resumes()

    results = []

    for filename, resume_text in resumes.items():

        score = calculate_semantic_similarity(
            resume_text,
            job_description
        )

        results.append((filename, score))

    results.sort(
        key=lambda x: x[1],
        reverse=True
    )

    return results


# --------------------------------------------------
# Main
# --------------------------------------------------

if __name__ == "__main__":

    results = rank_resumes()

    print("\n" + "=" * 70)
    print("RESUME RANKING FOR JOB DESCRIPTION")
    print("=" * 70)

    for rank, (filename, score) in enumerate(results, start=1):

        print(
            f"{rank}. {filename}"
            f" -> {score * 100:.2f}%"
        )

    print("=" * 70)