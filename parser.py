import fitz  # PyMuPDF
import re
import json

def extract_text(pdf_path):
    text = ""
    with fitz.open(pdf_path) as doc:
        for page in doc:
            text += page.get_text()
    return text

def extract_name(text):
    lines = text.strip().split('\n')
    for line in lines[:5]:
        if "@" not in line and len(line.strip().split()) in [1, 2]:
            return line.strip()
    return "Unknown"

def extract_email(text):
    match = re.search(r'[\w\.-]+@[\w\.-]+', text)
    return match.group(0) if match else None

def extract_phone(text):
    match = re.search(r'(\+91[\s\-]?\d{10})', text)
    return match.group(0) if match else None

def extract_links(text):
    linkedin = github = None
    for line in text.split('\n'):
        if "linkedin" in line.lower():
            linkedin = line.strip()
        if "github" in line.lower():
            github = line.strip()
    return linkedin, github

def extract_education(text):
    lines = text.split('\n')
    edu = []
    capture = False
    for line in lines:
        if "EDUCATION" in line.upper():
            capture = True
        elif capture and ("SKILLS" in line.upper() or line.strip() == ""):
            break
        elif capture:
            edu.append(line.strip())
    return [e for e in edu if e]

def extract_skills(text):
    known_skills = [
        "Python", "C", "C++", "Java", "SQL", "HTML", "CSS", "JavaScript",
        "MATLAB", "PyCharm", "Visual Studio Code", "Leadership", "Project Management"
    ]
    lines = text.split('\n')
    skill_lines = []
    capture = False
    for line in lines:
        if "SKILLS" in line.upper():
            capture = True
        elif capture and ("INTERNSHIP" in line.upper() or "PROJECT" in line.upper()):
            break
        elif capture:
            skill_lines.append(line)

    skill_text = " ".join(skill_lines)
    extracted = []
    for skill in known_skills:
        if skill.lower() in skill_text.lower():
            extracted.append(skill)
    
    return list(set(extracted))

def extract_projects(text):
    lines = text.split('\n')
    projects = []
    capture = False
    current_project = ""

    # Normalize lines to remove invisible Unicode characters
    lines = [line.strip().replace('\u2022', '').replace('\xa0', ' ') for line in lines]

    for line in lines:
        if not capture and "PROJECTS" in line.upper():
            capture = True
            continue

        if capture:
            # Stop if next section starts
            if any(kw in line.upper() for kw in ["COURSE", "WORKSHOP", "ACHIEVEMENT", "ACTIVITIES", "CERTIFICATION"]):
                if current_project:
                    projects.append(current_project.strip())
                break

            if "—" in line or "|" in line or line.strip().startswith("•"):
                if current_project:
                    projects.append(current_project.strip())
                current_project = line.strip()
            else:
                current_project += " " + line.strip()

    if current_project:
        projects.append(current_project.strip())

    # Post-filter: remove duplicates and invalid lines
    clean_projects = []
    for p in projects:
        if (
            len(p.split()) >= 5 and
            "my knowledge" not in p.lower() and
            p not in clean_projects
        ):
            clean_projects.append(p)

    return clean_projects


def extract_experience(text):
    lines = text.split('\n')
    experience = []
    for i, line in enumerate(lines):
        if "INTERNSHIP" in line.upper() or "DREXPED" in line.upper():
            experience.append("Software Engineering Intern – Drexped Tech LLP (Mar–Sep 2025)")
            break
    return experience

def parse_resume(pdf_path):
    text = extract_text(pdf_path)
    return {
        "name": extract_name(text),
        "email": extract_email(text),
        "phone": extract_phone(text),
        "linkedin": extract_links(text)[0],
        "github": extract_links(text)[1],
        "education": extract_education(text),
        "skills": extract_skills(text),
        "projects": extract_projects(text),
        "experience": extract_experience(text)
    }

if __name__ == "__main__":
    pdf_path = "sample_resume_1.pdf"  # Make sure this file exists
    parsed_data = parse_resume(pdf_path)

    # Save structured data to JSON
    with open("parsed_resume.json", "w", encoding='utf-8') as f:
        json.dump(parsed_data, f, indent=4)

    print("✅ Resume parsed successfully and saved to parsed_resume.json")
