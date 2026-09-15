import json

from src.jobs.job_manager import load_jobs
from src.resume.resume_manager import discover_resumes
from src.resume.resume_selector import rank_resumes


def test_new_pdf_is_discovered_and_every_pair_is_ranked(tmp_path):
	resumes_dir = tmp_path / "resumes"
	resumes_dir.mkdir()
	(resumes_dir / "new_resume.pdf").write_bytes(b"placeholder")
	jobs_path = tmp_path / "jobs.json"
	jobs_path.write_text(json.dumps([{"id": "job-1", "title": "Python Developer"}, {"id": "job-2", "title": "Data Analyst"}]))

	resumes = discover_resumes(resumes_dir)
	jobs = load_jobs(jobs_path)
	rankings = rank_resumes(resumes, jobs, lambda _: "Python SQL")

	assert len(resumes) == 1
	assert len(rankings) == 2
