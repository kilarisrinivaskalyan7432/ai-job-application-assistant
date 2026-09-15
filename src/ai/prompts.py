def build_cover_letter_prompt(
    job_title: str,
    company: str,
    job_description: str,
    resume_text: str,
    matched_skills: list[str],
    missing_skills: list[str]
) -> str:
    """
    Build a prompt for generating a tailored cover letter.
    """

    matched_skills_text = ", ".join(matched_skills)

    missing_skills_text = ", ".join(missing_skills)

    prompt = f"""
You are an AI assistant helping a job seeker prepare
a professional job application.

JOB INFORMATION
---------------

Job Title:
{job_title}

Company:
{company}

Job Description:
{job_description}


RESUME
------

{resume_text}


MATCHING INFORMATION
--------------------

Matched Skills:
{matched_skills_text}

Missing Skills:
{missing_skills_text}


TASK
----

Write a professional and concise cover letter for this job.

Requirements:

1. Use only information that is supported by the resume.
2. Do not invent experience, projects, companies, achievements,
   education, certifications, or skills.
3. Highlight the skills from the resume that are relevant to
   the job description.
4. Do not claim that the candidate has a missing skill.
5. Keep the tone professional and suitable for an entry-level
   candidate.
6. Keep the cover letter concise.
7. Do not use exaggerated claims.
8. Do not include placeholders such as [Name], [Company],
   or [Experience].
9. Do not mention that AI was used to write the letter.

Return only the cover letter.
"""

    return prompt