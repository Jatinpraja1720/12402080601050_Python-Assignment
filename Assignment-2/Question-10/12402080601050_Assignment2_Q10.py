
import csv
import os
import math
import html

input_file = input("Enter CSV file path: ")
output_folder = input("Enter output folder path: ")
os.makedirs(output_folder, exist_ok=True)

# Read CSV
with open(input_file, "r", newline="") as f:
    reader = csv.DictReader(f)
    data = list(reader)
    columns = reader.fieldnames

subjects = columns[2:]

# Clean missing and invalid marks
for subject in subjects:
    valid = []
    for row in data:
        try:
            mark = float(row[subject])
            if math.isfinite(mark) and 0 <= mark <= 100:
                valid.append(mark)
            else:
                row[subject] = ""
        except (ValueError, TypeError):
            row[subject] = ""

    average = round(sum(valid) / len(valid)) if valid else 0

    for row in data:
        if row[subject] == "":
            row[subject] = str(average)

# Save cleaned CSV
with open(os.path.join(output_folder, "cleaned_marks.csv"),
          "w", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=columns)
    writer.writeheader()
    writer.writerows(data)

# Calculate statistics
summary = {}
for subject in subjects:
    marks = [float(row[subject]) for row in data]
    summary[subject] = {
        "Average": sum(marks) / len(marks) if marks else 0,
        "Minimum": min(marks) if marks else 0,
        "Maximum": max(marks) if marks else 0
    }

with open(os.path.join(output_folder, "summary.csv"),
          "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["Subject", "Average", "Minimum", "Maximum"])
    for subject, stats in summary.items():
        writer.writerow([
            subject, round(stats["Average"], 2),
            stats["Minimum"], stats["Maximum"]
        ])

# Calculate student averages
for row in data:
    row["average"] = sum(float(row[s]) for s in subjects) / len(subjects)

# Create SVG chart without external libraries
def create_chart(filename, title, labels, values, max_value):
    width, height = 700, 400
    left, bottom = 170, 320
    chart_width, chart_height = 450, 250
    bar_height = min(28, chart_height / max(len(labels), 1) - 4)

    svg = [
        f'<svg xmlns="http://www.w3.org/2000/svg" '
        f'width="{width}" height="{height}">',
        '<rect width="100%" height="100%" fill="white"/>',
        f'<text x="350" y="30" font-size="20" '
        f'text-anchor="middle">{html.escape(title)}</text>'
    ]

    for i, (label, value) in enumerate(zip(labels, values)):
        y = 60 + i * (chart_height / max(len(labels), 1))
        bar_width = max(0, value / max_value * chart_width) if max_value else 0

        svg.append(
            f'<text x="{left-10}" y="{y+bar_height}" '
            f'text-anchor="end" font-size="12">'
            f'{html.escape(str(label))}</text>'
        )
        svg.append(
            f'<rect x="{left}" y="{y}" width="{bar_width}" '
            f'height="{bar_height}" fill="steelblue"/>'
        )
        svg.append(
            f'<text x="{left+bar_width+5}" y="{y+bar_height}" '
            f'font-size="12">{value:.1f}</text>'
        )

    svg.append("</svg>")

    with open(os.path.join(output_folder, filename), "w") as f:
        f.write("\n".join(svg))


# 1. Grade distribution
grades = {"A": 0, "B": 0, "C": 0, "D": 0, "F": 0}

for row in data:
    for subject in subjects:
        mark = float(row[subject])
        if mark >= 90:
            grades["A"] += 1
        elif mark >= 80:
            grades["B"] += 1
        elif mark >= 70:
            grades["C"] += 1
        elif mark >= 60:
            grades["D"] += 1
        else:
            grades["F"] += 1

create_chart("grade_distribution.svg", "Grade Distribution",
             list(grades.keys()), list(grades.values()),
             max(max(grades.values()), 1))

# 2. Subject averages
create_chart("subject_average.svg", "Subject-wise Average",
             list(summary.keys()),
             [s["Average"] for s in summary.values()], 100)

# 3. Top 10 performers
top = sorted(data, key=lambda r: r["average"], reverse=True)[:10]
create_chart("top_performers.svg", "Top 10 Performers",
             [r["name"] for r in top],
             [r["average"] for r in top], 100)

print("Analysis completed!")
print("Files saved in:", output_folder)
print("Created cleaned_marks.csv, summary.csv")
print("Created grade_distribution.svg, subject_average.svg")
print("Created top_performers.svg")
