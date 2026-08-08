# ==============================
# parser.py
# ==============================

def parse_file(file_path):
    """
    Reads a Job Description or Resume text file
    and extracts name, skills, experience,
    education, projects and certifications.
    """

    data = {
        "name": "",
        "skills": [],
        "experience": "",
        "education": "",
        "projects": [],
        "certifications": []
    }

    current_section = None

    with open(file_path, "r", encoding="utf-8") as file:

        for line in file:

            line = line.strip()

            if not line:
                continue

            # Remove bullets
            clean_line = line.lstrip("-•*").strip()

            lower_line = clean_line.lower()

            # ---------------- Name ----------------

            if lower_line.startswith("name:"):

                data["name"] = clean_line.split(":", 1)[1].strip()
                current_section = None
                continue

            # ---------------- Skills ----------------

            if lower_line.startswith("skills:"):

                current_section = "skills"

                value = clean_line.split(":", 1)[1].strip()

                if value:

                    # Handles:
                    # Skills: Python, Java, SQL

                    for skill in value.replace(";", ",").split(","):

                        skill = skill.strip()

                        if skill:
                            data["skills"].append(skill)

                continue

            # ---------------- Experience ----------------

            if lower_line.startswith("experience:"):

                current_section = "experience"

                value = clean_line.split(":", 1)[1].strip()

                if value:
                    data["experience"] = value

                continue

            # ---------------- Education ----------------

            if lower_line.startswith("education:"):

                current_section = "education"

                value = clean_line.split(":", 1)[1].strip()

                if value:
                    data["education"] = value

                continue

            # ---------------- Projects ----------------

            if lower_line.startswith("projects:"):

                current_section = "projects"

                value = clean_line.split(":", 1)[1].strip()

                if value:
                    data["projects"].append(value)

                continue

            # ---------------- Certifications ----------------

            if lower_line.startswith("certifications:"):

                current_section = "certifications"

                value = clean_line.split(":", 1)[1].strip()

                if value:
                    data["certifications"].append(value)

                continue

            # ---------------- Store Section Data ----------------

            if current_section == "skills":

                # Supports comma-separated skills
                parts = clean_line.replace(";", ",").split(",")

                for skill in parts:

                    skill = skill.strip()

                    if skill and skill.lower() not in [
                        x.lower() for x in data["skills"]
                    ]:

                        data["skills"].append(skill)

            elif current_section == "experience":

                data["experience"] = clean_line

            elif current_section == "education":

                data["education"] = clean_line

            elif current_section == "projects":

                data["projects"].append(clean_line)

            elif current_section == "certifications":

                data["certifications"].append(clean_line)

    return data