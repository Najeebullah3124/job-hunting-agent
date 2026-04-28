import csv
import os
from collections import Counter
from datetime import date, datetime

JOB_DIR = "input_jobs"
RESUME_DIR = "input_resumes"
KB_DIR = "input_kb"
OUTPUT_DIR = "outputs"
TRACKER_DIR = "tracker"

TRACKER_FILE = os.path.join(TRACKER_DIR, "applications.csv")
REMINDERS_FILE = os.path.join(TRACKER_DIR, "reminders.txt")

KEYWORDS = [
    "python",
    "machine learning",
    "data preprocessing",
    "github",
    "git",
    "api",
    "prompt engineering",
    "sql",
    "communication",
    "problem solving",
    "oop",
    "database",
    "jupyter",
    "pandas",
    "numpy",
    "deep learning",
    "html",
    "css",
    "flask",
    "streamlit",
    "resume",
    "interview",
]

TRACKER_COLUMNS = [
    "application_id",
    "company",
    "role",
    "source",
    "status",
    "applied_date",
    "interview_date",
    "follow_up_date",
    "next_action",
    "notes",
]


def ensure_folders():
    for folder in [JOB_DIR, RESUME_DIR, KB_DIR, OUTPUT_DIR, TRACKER_DIR]:
        os.makedirs(folder, exist_ok=True)


def read_text_files(folder):
    combined_text = ""
    files = []
    for filename in sorted(os.listdir(folder)):
        if filename.lower().endswith(".txt"):
            path = os.path.join(folder, filename)
            with open(path, "r", encoding="utf-8") as file:
                content = file.read().strip()
            combined_text += f"\n\n--- FILE: {filename} ---\n{content}\n"
            files.append(filename)
    return combined_text.strip(), files


def save_text(path, content):
    with open(path, "w", encoding="utf-8") as file:
        file.write(content)


def extract_keywords(text):
    text_lower = text.lower()
    return sorted({keyword for keyword in KEYWORDS if keyword in text_lower})


def extract_top_terms(text, min_len=4, top_n=12):
    stop_words = {
        "the",
        "and",
        "with",
        "for",
        "you",
        "your",
        "from",
        "that",
        "this",
        "have",
        "will",
        "are",
        "our",
        "job",
        "role",
        "team",
        "work",
    }
    tokens = []
    current = []
    for char in text.lower():
        if char.isalnum() or char == "_":
            current.append(char)
        else:
            if current:
                token = "".join(current)
                if len(token) >= min_len and token not in stop_words:
                    tokens.append(token)
                current = []
    if current:
        token = "".join(current)
        if len(token) >= min_len and token not in stop_words:
            tokens.append(token)
    counts = Counter(tokens)
    return counts.most_common(top_n)


def compare_skills(job_skills, resume_skills):
    matched = sorted([skill for skill in job_skills if skill in resume_skills])
    missing = sorted([skill for skill in job_skills if skill not in resume_skills])
    score = 0.0 if not job_skills else round((len(matched) / len(job_skills)) * 100, 2)
    return matched, missing, score


def generate_job_analysis(job_files, job_skills, top_terms):
    report = ["Job Analysis Report", "===================", ""]
    report.append(f"Job files analyzed: {len(job_files)}")
    for job_file in job_files:
        report.append(f"- {job_file}")
    report.append("")
    report.append("Skills/keywords found in job posters:")
    if job_skills:
        for skill in job_skills:
            report.append(f"- {skill}")
    else:
        report.append("- No tracked keywords found. Add more detailed JDs or extend KEYWORDS.")
    report.append("")
    report.append("Frequently appearing terms from posters:")
    if top_terms:
        for term, count in top_terms:
            report.append(f"- {term}: {count}")
    else:
        report.append("- No terms extracted.")
    return "\n".join(report)


def generate_skill_gap_report(job_skills, resume_skills, matched, missing, score):
    report = ["Skill Gap Report", "================", ""]
    report.append(f"Job skills found: {len(job_skills)}")
    report.append(f"Resume skills found: {len(resume_skills)}")
    report.append(f"Match Score: {score}%")
    report.append("")
    report.append("Matched Skills:")
    if matched:
        for skill in matched:
            report.append(f"- {skill}")
    else:
        report.append("- No direct matches found yet.")
    report.append("")
    report.append("Missing Skills:")
    if missing:
        for skill in missing:
            report.append(f"- {skill}")
    else:
        report.append("- No gaps identified from tracked keywords.")
    return "\n".join(report)


def generate_resume_suggestions(job_skills, missing):
    output = ["Tailored Resume Suggestions", "===========================", ""]
    output.append("Suggested improvements according to selected job needs:")
    for skill in job_skills:
        output.append(f"- Add a measurable bullet proving your work in {skill}.")
    output.append("")
    output.append("Suggested resume bullets:")
    output.append("- Built Python-based projects and documented implementation decisions clearly.")
    output.append("- Used Git and GitHub to manage versions, pull requests, and issue tracking.")
    output.append("- Converted class assignments into practical problem-solving deliverables.")
    output.append("")
    output.append("Project-to-JD mapping idea:")
    output.append("- For each required skill, map one project, one tool used, and one quantifiable result.")
    if missing:
        output.append("")
        output.append("Skills to improve before applying/interview:")
        for skill in missing:
            output.append(f"- {skill}")
    return "\n".join(output)


def generate_interview_questions(job_skills, kb_text):
    questions = ["Interview Questions", "===================", ""]
    questions.append("Technical questions based on job posters:")
    if job_skills:
        for skill in job_skills:
            questions.append(f"- Explain your understanding of {skill}.")
            questions.append(f"- Share one project example where you used {skill}.")
    else:
        questions.append("- Explain a technical project you are most proud of.")
    questions.append("")
    questions.append("HR and behavioral questions:")
    questions.append("- Tell me about yourself in 90 seconds.")
    questions.append("- Why are you interested in this role and company?")
    questions.append("- Describe a challenge and how you solved it.")
    questions.append("- What are your strengths and current improvement areas?")
    questions.append("- Why should we select you for this position?")
    questions.append("")
    questions.append("Questions inspired by KB/slides:")
    kb_lines = [line.strip("- ").strip() for line in kb_text.splitlines() if line.strip()]
    for line in kb_lines[:10]:
        questions.append(f"- How would you explain this point in an interview: {line}?")
    if not kb_lines:
        questions.append("- Add slide notes in input_kb/ to generate KB-specific questions.")
    return "\n".join(questions)


def load_or_create_tracker():
    rows = []
    if os.path.exists(TRACKER_FILE):
        with open(TRACKER_FILE, "r", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            for row in reader:
                rows.append({column: row.get(column, "") for column in TRACKER_COLUMNS})
    else:
        rows.append(
            {
                "application_id": "APP-001",
                "company": "Sample Company",
                "role": "AI Intern",
                "source": "Job Poster",
                "status": "Not Applied",
                "applied_date": "",
                "interview_date": "",
                "follow_up_date": "",
                "next_action": "Tailor resume and apply",
                "notes": "Sample row",
            }
        )
    with open(TRACKER_FILE, "w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=TRACKER_COLUMNS)
        writer.writeheader()
        writer.writerows(rows)
    return rows


def parse_iso_date(date_text):
    if not date_text:
        return None
    try:
        return datetime.strptime(date_text, "%Y-%m-%d").date()
    except ValueError:
        return None


def urgency_label(target_date):
    if target_date is None:
        return "no date"
    days = (target_date - date.today()).days
    if days < 0:
        return f"overdue by {-days} day(s)"
    if days == 0:
        return "today"
    if days == 1:
        return "tomorrow"
    if days <= 7:
        return "this week"
    return f"in {days} days"


def generate_reminders(rows):
    reminders = ["Application Reminders", "=====================", ""]
    for row in rows:
        app_id = row.get("application_id", "").strip()
        company = row.get("company", "").strip() or "Unknown Company"
        role = row.get("role", "").strip() or "Unknown Role"
        status = row.get("status", "").strip().lower()
        interview_date = row.get("interview_date", "").strip()
        follow_up_date = row.get("follow_up_date", "").strip()
        next_action = row.get("next_action", "").strip() or "Review JD and prepare."

        if status == "interview scheduled":
            label = urgency_label(parse_iso_date(interview_date))
            reminders.append(
                f"- {app_id}: Interview scheduled for {role} at {company} on {interview_date or 'N/A'} ({label}). Next action: {next_action}"
            )
        elif status == "not applied":
            reminders.append(
                f"- {app_id}: Not applied yet for {role} at {company}. Tailor resume, submit application, then update tracker."
            )
        elif status == "applied":
            label = urgency_label(parse_iso_date(follow_up_date))
            reminders.append(
                f"- {app_id}: Application submitted to {company}. Follow up on {follow_up_date or 'N/A'} ({label}) if no response is received."
            )
        elif status == "shortlisted":
            reminders.append(
                f"- {app_id}: You are shortlisted at {company}. Prepare role-specific questions and revise your projects."
            )
        elif status == "offered":
            reminders.append(f"- {app_id}: Offer received from {company}. Review compensation and deadline details.")

    if len(reminders) == 3:
        reminders.append("- No application records found in tracker/applications.csv.")
    return "\n".join(reminders)


def run_agent():
    ensure_folders()

    job_text, job_files = read_text_files(JOB_DIR)
    resume_text, resume_files = read_text_files(RESUME_DIR)
    kb_text, kb_files = read_text_files(KB_DIR)

    if not job_files or not resume_files or not kb_files:
        print("Please add at least one .txt file in input_jobs/, input_resumes/, and input_kb/.")
        print(f"Found job files: {len(job_files)}, resume files: {len(resume_files)}, kb files: {len(kb_files)}")
        return

    job_skills = extract_keywords(job_text)
    resume_skills = extract_keywords(resume_text)
    matched, missing, score = compare_skills(job_skills, resume_skills)

    job_report = generate_job_analysis(job_files, job_skills, extract_top_terms(job_text))
    gap_report = generate_skill_gap_report(job_skills, resume_skills, matched, missing, score)
    resume_suggestions = generate_resume_suggestions(job_skills, missing)
    interview_questions = generate_interview_questions(job_skills, kb_text)

    tracker_rows = load_or_create_tracker()
    reminders = generate_reminders(tracker_rows)

    preparation_plan = "\n".join(
        [
            "Preparation Plan",
            "================",
            "",
            "1) Review missing skills and select one mini-project per missing area.",
            "2) Practice STAR format answers for at least 3 project stories.",
            "3) Rehearse 10 technical + 5 HR questions from interview_questions.txt.",
            "4) Update tracker status after each application/interview event.",
            "5) Do a follow-up check every 3-5 days for active applications.",
        ]
    )

    final_report = "\n".join(
        [
            "CareerPrep Job-Hunting Agent Report",
            "===================================",
            f"Generated on: {datetime.now().isoformat(timespec='seconds')}",
            "",
            f"Job files read: {len(job_files)}",
            f"Resume files read: {len(resume_files)}",
            f"KB files read: {len(kb_files)}",
            f"Match score: {score}%",
            "",
            job_report,
            "",
            gap_report,
            "",
            resume_suggestions,
            "",
            interview_questions,
            "",
            reminders,
            "",
            preparation_plan,
        ]
    )

    save_text(os.path.join(OUTPUT_DIR, "job_analysis_report.txt"), job_report)
    save_text(os.path.join(OUTPUT_DIR, "skill_gap_report.txt"), gap_report)
    save_text(os.path.join(OUTPUT_DIR, "tailored_resume_suggestions.txt"), resume_suggestions)
    save_text(os.path.join(OUTPUT_DIR, "interview_questions.txt"), interview_questions)
    save_text(os.path.join(OUTPUT_DIR, "preparation_plan.txt"), preparation_plan)
    save_text(os.path.join(OUTPUT_DIR, "final_agent_report.txt"), final_report)
    save_text(REMINDERS_FILE, reminders)

    print("Agent completed successfully.")
    print(f"Job files read: {len(job_files)}")
    print(f"Resume files read: {len(resume_files)}")
    print(f"KB files read: {len(kb_files)}")
    print(f"Match score: {score}%")
    print("Outputs saved in outputs/ and tracker/ folders.")


if __name__ == "__main__":
    run_agent()
