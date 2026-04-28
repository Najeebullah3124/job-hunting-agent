# Reflection

## What I Built

I built a file-driven CareerPrep Job-Hunting Agent in Python that reads data from three folders (`input_jobs`, `input_resumes`, and `input_kb`) and produces practical outputs in `outputs/` and `tracker/`.

The system generates:
- job analysis
- skill-gap report
- tailored resume suggestions
- cover letter draft
- interview question bank
- preparation plan
- reminder text

It also creates/maintains a tracker file (`tracker/applications.csv`) for application statuses and actions.

## How I Tested It

- Added sample text files in all required input folders.
- Ran `python app.py`.
- Confirmed output files were generated successfully.
- Verified tracker CSV and reminders file creation.
- Checked match score and missing skill logic manually with sample content.

## Challenges Faced

- Handling reminders with different statuses while keeping output simple.
- Keeping extraction easy for beginners without external NLP libraries.

## Improvements Made

- Added top-term extraction for better job analysis context.
- Added urgency labels (`today`, `tomorrow`, `this week`, `overdue`) for follow-up reminders.
- Added a preparation plan output for interview readiness.
- Added a cover letter draft to support job applications beyond resume tailoring.

## Future Improvements

- Support PDF/DOCX input parsing.
- Add menu-based selection of specific job and resume files.
- Add Streamlit dashboard for visual tracker analytics.
- Add cover letter and recruiter message generation.
- Integrate LLM API for more adaptive suggestions.
