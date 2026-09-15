from typing import Any, TypedDict


class AgentState(TypedDict, total=False):
    """
    State carried through the AI job application agent workflow.

    The state stores information about:
    - the current job
    - resume matching
    - match score
    - matched and missing skills
    - generated cover letter
    - recommendation status
    """

    # Job information
    job: dict[str, Any]
    job_id: str

    # Resume matching
    resume: str
    match_score: float
    semantic_similarity: float
    required_skill_match: float
    role_relevance: float
    missing_skill_penalty: float

    # Skills
    matched_skills: list[str]
    missing_skills: list[str]

    # AI-generated content
    cover_letter: str

    # Workflow status
    status: str

    # Error information, if something goes wrong
    error: str