# report.py

def generate_report(results):

    # Sort candidates by score (Highest to Lowest)
    results.sort(key=lambda x: x["score"], reverse=True)

    report = ""

    report += "=" * 70 + "\n"
    report += "          RESUME SCREENING REPORT\n"
    report += "=" * 70 + "\n\n"

    rank = 1

    for result in results:

        report += f"Rank               : {rank}\n"
        report += f"Candidate Name     : {result['candidate']}\n"
        report += f"Match Score        : {result['score']}%\n"
        report += f"Recommendation     : {result['recommendation']}\n\n"

        report += "Matched Skills\n"

        if len(result["matched_skills"]) == 0:
            report += "None\n"
        else:
            for skill in result["matched_skills"]:
                report += "  ✓ " + skill + "\n"

        report += "\nMissing Skills\n"

        if len(result["missing_skills"]) == 0:
            report += "None\n"
        else:
            for skill in result["missing_skills"]:
                report += "  ✗ " + skill + "\n"

        report += "\n"
        report += "-" * 70
        report += "\n\n"

        rank += 1

    return report


def save_report(report):

    file = open("output/report.txt", "w", encoding="utf-8")

    file.write(report)

    file.close()