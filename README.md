# Autonomous Job Matcher

An explainable, human-in-the-loop job application assistant. The current milestone focuses on reliable resume-to-job matching before adding external job search or LLM features.

## Architecture

```text
PDF resumes -> resume discovery/parser -> resume text
																			\
																			 -> combined matcher -> ranked recommendations -> SQLite
Job JSON --------------------------------/
```

- `src/resume/` discovers every PDF in `data/resumes/` and extracts its text.
- `src/jobs/` loads local job descriptions from `data/jobs/jobs.json`.
- `src/matching/` compares every resume with every job using four signals:
	- semantic token similarity
	- required-skill coverage
	- role-title relevance
	- missing-skill penalty
- `src/database/` stores recommendations in SQLite.
- `src/agent/` contains plain Python tool wrappers. LangChain can be added later around these stable functions.
- `frontend/` is intentionally kept until the core workflow is stable.

## Workflow

1. Add a PDF anywhere in `data/resumes/`.
2. Add job objects to `data/jobs/jobs.json`.
3. Run the recommendation pipeline:

	 ```powershell
	 .\venv\Scripts\python.exe -m src.main
	 ```

4. Review the ranked resume/job pairs and their score breakdown.
5. Approve or reject a recommendation in SQLite before any future submission step.
6. Add Gemini later for tailored cover letters, application answers, job analysis, and recommendations. It is not required for matching.
7. Add job searching after local resume selection is proven reliable.

## Job format

`data/jobs/jobs.json` accepts either a list or an object containing a `jobs` list:

```json
[
	{
		"id": "job-001",
		"title": "Python Backend Developer",
		"company": "Example Inc",
		"description": "Build APIs with Python, FastAPI, SQL, Docker, and AWS"
	}
]
```

## Development

```powershell
python -m pip install -r requirements.txt
python -m pytest -q
```

The SQLite database is created at `data/autonomus_job.sqlite3` when recommendations are generated. It is ignored by Git, as are `.env`, the virtual environment, and Python cache files.
