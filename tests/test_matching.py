from src.matching.scorer import score_resume_against_job


def test_combined_score_rewards_required_skills_and_role_match():
	job = {"title": "Python Backend Developer", "description": "Python FastAPI SQL Docker AWS"}
	strong = score_resume_against_job("Python Backend Developer FastAPI SQL Docker AWS", job)
	weak = score_resume_against_job("Graphic Designer Photoshop Illustrator", job)

	assert strong.total > weak.total
	assert strong.required_skill_match == 1.0
	assert set(strong.missing_skills) == set()
