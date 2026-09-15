from dataclasses import dataclass


@dataclass(frozen=True)
class ApplicationRecommendation:

    resume_name: str

    job_id: str

    score: float

    status: str = "PENDING_APPROVAL"