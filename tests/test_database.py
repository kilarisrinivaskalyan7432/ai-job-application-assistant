from src.database.db import connect, save_recommendation, set_status
from src.database.models import ApplicationRecommendation


def test_recommendation_requires_explicit_status_transition(tmp_path):
    database_path = tmp_path / "test.sqlite3"
    save_recommendation(ApplicationRecommendation("resume.pdf", "job-1", 0.8), database_path)

    with connect(database_path) as connection:
        row = connection.execute("SELECT id, status FROM recommendations").fetchone()
        assert row["status"] == "recommended"
        recommendation_id = row["id"]

    set_status(recommendation_id, "approved", database_path)

    with connect(database_path) as connection:
        assert connection.execute("SELECT status FROM recommendations").fetchone()["status"] == "approved"