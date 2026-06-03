import csv
from statistics import mean, median, pstdev
from pathlib import Path

DATA_FILE = Path(__file__).resolve().parents[1] / "data" / "grades.csv"
REPORT_FILE = Path(__file__).resolve().parents[1] / "student_grade_report.txt"
COURSES = ["programming", "data_structure", "algorithm", "database", "statistics"]


def letter_grade(score: float) -> str:
    if score >= 90:
        return "A+"
    if score >= 85:
        return "A"
    if score >= 80:
        return "B+"
    if score >= 75:
        return "B"
    if score >= 70:
        return "C+"
    if score >= 65:
        return "C"
    return "D"


def load_students():
    with DATA_FILE.open(newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    for row in rows:
        scores = [float(row[c]) for c in COURSES]
        row["average"] = round(mean(scores), 2)
        row["grade"] = letter_grade(row["average"])
    return rows


def course_statistics(rows):
    stats = {}
    for course in COURSES:
        values = [float(row[course]) for row in rows]
        stats[course] = {
            "mean": round(mean(values), 2),
            "median": round(median(values), 2),
            "min": min(values),
            "max": max(values),
            "std_dev": round(pstdev(values), 2),
        }
    return stats


def build_report(rows):
    rows = sorted(rows, key=lambda r: r["average"], reverse=True)
    lines = ["STUDENT GRADE ANALYTICS REPORT", "=" * 35, ""]
    lines.append("Ranking")
    lines.append("-------")
    for rank, row in enumerate(rows, start=1):
        lines.append(f"{rank}. {row['name']} ({row['student_id']}) - Average: {row['average']} - Grade: {row['grade']}")

    lines.append("\nCourse Statistics")
    lines.append("-----------------")
    for course, stat in course_statistics(rows).items():
        lines.append(
            f"{course}: mean={stat['mean']}, median={stat['median']}, "
            f"min={stat['min']}, max={stat['max']}, std={stat['std_dev']}"
        )
    return "\n".join(lines)


if __name__ == "__main__":
    students = load_students()
    report = build_report(students)
    print(report)
    REPORT_FILE.write_text(report, encoding="utf-8")
    print(f"\nReport saved to: {REPORT_FILE}")
