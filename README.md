# CareerPrep Job-Hunting Agent

A beginner-friendly, file-driven Python agent for career preparation.

It reads:
- job posters from `input_jobs/`
- resume text from `input_resumes/`
- interview/course notes from `input_kb/`

Then it generates:
- job analysis
- skill-gap report
- tailored resume suggestions
- cover letter draft
- interview questions
- preparation plan
- application reminders

It also maintains an application tracker in `tracker/applications.csv`.

## Repository Structure

```text
job-hunting-agent/
|-- README.md
|-- app.py
|-- requirements.txt
|-- reflection.md
|-- input_jobs/
|-- input_resumes/
|-- input_kb/
|-- outputs/
|-- tracker/
|-- samples/
```

## Setup and Run

1. Ensure Python 3.9+ is installed.
2. (Optional) Create a virtual environment.
3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Add at least one `.txt` file in each of:
   - `input_jobs/`
   - `input_resumes/`
   - `input_kb/`

5. Run:

```bash
python app.py
```

## Generated Output Files

After running, the agent creates:
- `outputs/job_analysis_report.txt`
- `outputs/skill_gap_report.txt`
- `outputs/tailored_resume_suggestions.txt`
- `outputs/cover_letter_draft.txt`
- `outputs/interview_questions.txt`
- `outputs/preparation_plan.txt`
- `outputs/final_agent_report.txt`
- `tracker/applications.csv`
- `tracker/reminders.txt`

## GAME Framework Mapping

- **Goal**: Help students organize and improve job application readiness.
- **Actions**: Read files, extract keywords, compare skills, generate reports, track applications, generate reminders.
- **Memory**: Current analyzed text, extracted skills, generated output files, tracker history.
- **Environment**: Local folders and text files inside this repository.

## Features Implemented (Rubric)

- Folder-based file reading (jobs/resumes/KB)
- Job keyword extraction and analysis report
- Resume keyword extraction
- Skill-gap analysis and match score
- Tailored resume suggestions
- Cover letter draft generation
- Interview questions from job + KB content
- Application tracker CSV creation/update
- Reminder generation based on status/date

## Unique Feature Added

Urgency-aware reminders with labels like:
- `today`
- `tomorrow`
- `this week`
- `overdue by X day(s)`

This improves practical follow-up behavior for real job workflows.

## Notes

- This baseline version uses `.txt` files.
- You can extend it with PDF/DOCX parsing, menu interface, Streamlit dashboard, or LLM API integration.
