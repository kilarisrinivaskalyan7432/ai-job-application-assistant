import sqlite3

from pathlib import Path

from .models import ApplicationRecommendation


ALLOWED_STATUSES = {
    "FOUND",
    "MATCHED",
    "SHORTLISTED",
    "DRAFTED",
    "PENDING_APPROVAL",
    "APPROVED",
    "REJECTED",
    "APPLIED",
}


def connect(
    database_path: str | Path = "data/autonomus_job.sqlite3"
) -> sqlite3.Connection:

    path = Path(database_path)

    path.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    connection = sqlite3.connect(path)

    connection.row_factory = sqlite3.Row

    connection.execute(
        """
        CREATE TABLE IF NOT EXISTS recommendations (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            resume_name TEXT NOT NULL,

            job_id TEXT NOT NULL,

            score REAL NOT NULL,

            status TEXT NOT NULL
                DEFAULT 'PENDING_APPROVAL',

            UNIQUE(resume_name, job_id)
        )
        """
    )

    connection.commit()

    return connection


def save_recommendation(
    recommendation: ApplicationRecommendation,
    database_path: str | Path = "data/autonomus_job.sqlite3",
) -> None:

    if recommendation.status not in ALLOWED_STATUSES:

        raise ValueError(
            f"Invalid status: "
            f"{recommendation.status}"
        )

    with connect(database_path) as connection:

        connection.execute(
            """
            INSERT INTO recommendations
                (
                    resume_name,
                    job_id,
                    score,
                    status
                )

            VALUES (?, ?, ?, ?)

            ON CONFLICT(resume_name, job_id)
            DO UPDATE SET
                score = excluded.score,
                status = excluded.status
            """,

            (
                recommendation.resume_name,
                recommendation.job_id,
                recommendation.score,
                recommendation.status,
            ),
        )

        connection.commit()


def set_status(
    recommendation_id: int,
    status: str,
    database_path: str | Path = "data/autonomus_job.sqlite3",
) -> None:

    if status not in ALLOWED_STATUSES:

        raise ValueError(
            f"Invalid status: {status}"
        )

    with connect(database_path) as connection:

        connection.execute(
            """
            UPDATE recommendations
            SET status = ?
            WHERE id = ?
            """,

            (
                status,
                recommendation_id,
            ),
        )

        connection.commit()


def get_recommendations(
    database_path: str | Path = "data/autonomus_job.sqlite3",
) -> list[dict]:

    with connect(database_path) as connection:

        rows = connection.execute(
            """
            SELECT
                id,
                resume_name,
                job_id,
                score,
                status
            FROM recommendations
            ORDER BY id DESC
            """
        ).fetchall()

    return [
        dict(row)
        for row in rows
    ]