````markdown
# AI Job Application Assistant

An AI-powered, human-in-the-loop job application assistant that analyzes job descriptions against multiple resumes, selects the best-fit resume, generates tailored cover letters, and tracks application recommendations.

> **Project Status:** In Development

## Features

- Search and load job descriptions from local job data
- Load and analyze multiple PDF resumes
- Compare resumes against job descriptions
- Calculate resume--JD match scores
- Identify matched and missing technical skills
- Select the best-fit resume for each job
- Generate resume-grounded cover letters using Google Gemini
- Store job recommendations and match scores in SQLite
- Track application workflow status
- Human approval before any application submission
- Streamlit dashboard for reviewing recommendations

## Architecture

```text
                    +------------------+
                    |   Job Sources    |
                    |  JSON / Search   |
                    +--------+---------+
                             |
                             v
                    +------------------+
                    |   Job Analysis   |
                    | JD Parsing/Search|
                    +--------+---------+
                             |
                             v
+----------------+   +------------------+
| PDF Resumes    |-->| Resume Matching  |
| Multiple       |   | Semantic + Skill |
+----------------+   +--------+---------+
                             |
                             v
                    +------------------+
                    | Best Resume      |
                    | Selection        |
                    +--------+---------+
                             |
                             v
                    +------------------+
                    | Google Gemini    |
                    | Cover Letter     |
                    +--------+---------+
                             |
                             v
                    +------------------+
                    | SQLite Database  |
                    | Recommendations  |
                    | Status Tracking  |
                    +--------+---------+
                             |
                             v
                    +------------------+
                    | Human Approval   |
                    +------------------+
````

## Project Workflow

1. Load available job descriptions.
2. Load all PDF resumes from `data/resumes/`.
3. Extract and clean resume text.
4. Compare each resume with the job description.
5. Calculate semantic similarity and skill-based matching scores.
6. Identify matched and missing skills.
7. Select the highest-scoring resume.
8. Generate a tailored cover letter using Google Gemini.
9. Save the recommendation and match score to SQLite.
10. Move the recommendation through the application workflow with human approval.

The system does **not** automatically submit job applications.

## Matching System

The resume matching system evaluates multiple signals:

* **Semantic similarity** - Measures similarity between resume and job-description content.
* **Required skill match** - Compares technical skills found in the resume and job description.
* **Role relevance** - Checks how well the resume aligns with the target role.
* **Missing skill penalty** - Accounts for required skills that are not present in the selected resume.

The final score combines these signals into an overall resume--JD match score.

## AI Integration

Google Gemini is used for:

* Tailored cover-letter generation
* Job-specific application content
* Resume-grounded recommendations

The generated content is designed to use information supported by the selected resume and job description rather than inventing candidate experience.

## Human-in-the-Loop Workflow

The project is designed around human approval rather than unrestricted automatic application submission.

```text
FOUND
  |
  v
MATCHED
  |
  v
SHORTLISTED
  |
  v
DRAFTED
  |
  v
PENDING_APPROVAL
  |
  +----> REJECTED
  |
  v
APPROVED
  |
  v
APPLIED
```

The approval step keeps the candidate in control of the final application decision.

## Project Structure

```text
ai-job-application-assistant/
│
├── data/
│   ├── jobs/
│   │   ├── jobs.json
│   │   └── test_jd.txt
│   │
│   └── resumes/
│       └── *.pdf
│
├── frontend/
│   └── streamlit_app.py
│
├── src/
│   ├── agent/
│   │   ├── job_agent.py
│   │   ├── state.py
│   │   └── tools.py
│   │
│   ├── ai/
│   │   ├── cover_letter.py
│   │   ├── gemini.py
│   │   └── prompts.py
│   │
│   ├── api/
│   │   └── routes.py
│   │
│   ├── database/
│   │   ├── db.py
│   │   └── models.py
│   │
│   ├── jobs/
│   │   ├── jd_parser.py
│   │   ├── job_manager.py
│   │   └── job_search.py
│   │
│   ├── matching/
│   │   ├── scorer.py
│   │   ├── semantic_matcher.py
│   │   └── skill_matcher.py
│   │
│   └── resume/
│       ├── main.py
│       ├── resume_manager.py
│       ├── resume_parser.py
│       └── resume_selector.py
│
├── tests/
│   ├── test_job_search.py
│   ├── test_matching.py
│   └── t
```

