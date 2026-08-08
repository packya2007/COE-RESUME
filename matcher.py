

def normalize_text(text):

    return (
        str(text)
        .strip()
        .lower()
        .replace("-", " ")
        .replace("_", " ")
    )


def normalize_list(items):

    normalized = []

    for item in items:

        item = normalize_text(item)

        if item and item not in normalized:

            normalized.append(item)

    return normalized


def compare_skills(jd_skills, resume_skills):

    jd = normalize_list(jd_skills)
    resume = normalize_list(resume_skills)

    matched = []
    missing = []

    for jd_skill in jd:

        found = False

        for resume_skill in resume:

            # Exact or partial matching

            if (
                jd_skill == resume_skill
                or jd_skill in resume_skill
                or resume_skill in jd_skill
            ):

                found = True
                break

        if found:

            matched.append(jd_skill.title())

        else:

            missing.append(jd_skill.title())

    return matched, missing


def calculate_score(jd, resume):

    # ---------------- Skills ----------------

    matched_skills, missing_skills = compare_skills(
        jd["skills"],
        resume["skills"]
    )

    skill_score = 0

    if len(jd["skills"]) > 0:

        skill_score = (
            len(matched_skills)
            / len(jd["skills"])
        ) * 50

    # ---------------- Experience ----------------

    experience_score = 0

    try:

        jd_exp = int(
            ''.join(
                c for c in str(jd["experience"])
                if c.isdigit()
            )
        )

        resume_exp = int(
            ''.join(
                c for c in str(resume["experience"])
                if c.isdigit()
            )
        )

        if resume_exp >= jd_exp:

            experience_score = 20

        elif resume_exp > 0:

            experience_score = (
                resume_exp / jd_exp
            ) * 20

    except:

        pass

    # ---------------- Education ----------------

    education_score = 0

    jd_education = normalize_text(
        jd["education"]
    )

    resume_education = normalize_text(
        resume["education"]
    )

    if jd_education and resume_education:

        if (
            jd_education == resume_education
            or jd_education in resume_education
            or resume_education in jd_education
        ):

            education_score = 15

    # ---------------- Projects ----------------

    project_score = 0

    jd_projects = normalize_list(
        jd["projects"]
    )

    resume_projects = normalize_list(
        resume["projects"]
    )

    if len(jd_projects) > 0:

        matched_projects = 0

        for project in jd_projects:

            for resume_project in resume_projects:

                if (
                    project in resume_project
                    or resume_project in project
                ):

                    matched_projects += 1
                    break

        project_score = (
            matched_projects
            / len(jd_projects)
        ) * 10

    # ---------------- Certifications ----------------

    certification_score = 0

    jd_certifications = normalize_list(
        jd["certifications"]
    )

    resume_certifications = normalize_list(
        resume["certifications"]
    )

    if len(jd_certifications) > 0:

        matched_certifications = 0

        for cert in jd_certifications:

            for resume_cert in resume_certifications:

                if (
                    cert in resume_cert
                    or resume_cert in cert
                ):

                    matched_certifications += 1
                    break

        certification_score = (
            matched_certifications
            / len(jd_certifications)
        ) * 5

    # ---------------- Total Score ----------------

    score = (
        skill_score
        + experience_score
        + education_score
        + project_score
        + certification_score
    )

    score = round(score, 2)

    # ---------------- Recommendation ----------------

    if score >= 85:

        recommendation = "Highly Recommended"

    elif score >= 70:

        recommendation = "Recommended"

    elif score >= 50:

        recommendation = "Consider"

    else:

        recommendation = "Rejected"

    # ---------------- Result ----------------

    return {

        "candidate":
        resume["name"]
        if resume["name"]
        else "Unknown Candidate",

        "score": score,

        "matched_skills":
        matched_skills,

        "missing_skills":
        missing_skills,

        "recommendation":
        recommendation
    }