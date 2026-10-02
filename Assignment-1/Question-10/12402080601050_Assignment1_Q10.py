'''
Problem Statement: Create a Tkinter GUI application to manage student assignment submissions. The application must support adding
a student, adding a submission, updating marks, filtering by pending/completed status, and exporting a CSV report. Data must persist
locally using JSON or CSV files. Input fields must be validated before saving.
'''

import tkinter as tk
from tkinter import ttk
import json
import csv
import os

file_name = "assignments.json"

if os.path.exists(file_name):

    with open(file_name, "r") as file:
        records = json.load(file)

else:
    records = []


def save_data():
    with open(file_name, "w") as file:
        json.dump(records, file, indent=4)


def add_record():

    enrollment = enrollment_entry.get()
    name = name_entry.get()
    assignment = assignment_entry.get()
    status = status_var.get()
    marks = marks_entry.get()
    remarks = remarks_entry.get()

    if enrollment == "" or name == "" or assignment == "":
        return

    if marks == "":
        marks_value = ""
    else:
        try:
            marks_value = float(marks)
        except ValueError:
            return

    record = {
        "enrollment": enrollment,
        "name": name,
        "assignment": assignment,
        "status": status,
        "marks": marks_value,
        "remarks": remarks
    }

    records.append(record)

    save_data()
    show_records()


def show_records():

    for item in tree.get_children():
        tree.delete(item)

    selected = filter_var.get()

    for record in records:

        if selected != "All" and record["status"] != selected:
            continue

        tree.insert(
            "",
            "end",
            values=(
                record["enrollment"],
                record["name"],
                record["assignment"],
                record["status"],
                record["marks"],
                record["remarks"]
            )
        )


def update_marks():

    selected = tree.selection()

    if not selected:
        return

    item = tree.item(selected[0])
    values = item["values"]

    enrollment = values[0]
    assignment = values[2]

    marks = marks_entry.get()

    try:
        marks = float(marks)
    except ValueError:
        return

    for record in records:

        if record["enrollment"] == enrollment and record["assignment"] == assignment:
            record["marks"] = marks
            record["status"] = "Completed"

    save_data()
    show_records()


def export_csv():

    with open("assignment_report.csv", "w", newline="") as file:

        writer = csv.writer(file)

        writer.writerow([
            "enrollment",
            "name",
            "assignment",
            "status",
            "marks",
            "remarks"
        ])

        for record in records:

            writer.writerow([
                record["enrollment"],
                record["name"],
                record["assignment"],
                record["status"],
                record["marks"],
                record["remarks"]
            ])


root = tk.Tk()

root.title("Assignment Tracker")
root.geometry("900x600")

tk.Label(root, text="Enrollment").pack()

enrollment_entry = tk.Entry(root)
enrollment_entry.pack()

tk.Label(root, text="Name").pack()

name_entry = tk.Entry(root)
name_entry.pack()

tk.Label(root, text="Assignment").pack()

assignment_entry = tk.Entry(root)
assignment_entry.pack()

tk.Label(root, text="Status").pack()

status_var = tk.StringVar(value="Pending")

status_menu = ttk.Combobox(
    root,
    textvariable=status_var,
    values=["Pending", "Completed"]
)

status_menu.pack()

tk.Label(root, text="Marks").pack()

marks_entry = tk.Entry(root)
marks_entry.pack()

tk.Label(root, text="Remarks").pack()

remarks_entry = tk.Entry(root)
remarks_entry.pack()

tk.Button(
    root,
    text="Add Submission",
    command=add_record
).pack()

tk.Button(
    root,
    text="Update Marks",
    command=update_marks
).pack()

filter_var = tk.StringVar(value="All")

filter_menu = ttk.Combobox(
    root,
    textvariable=filter_var,
    values=["All", "Pending", "Completed"]
)

filter_menu.pack()

filter_menu.bind("<<ComboboxSelected>>", lambda event: show_records())

tk.Button(
    root,
    text="Export CSV",
    command=export_csv
).pack()

columns = (
    "Enrollment",
    "Name",
    "Assignment",
    "Status",
    "Marks",
    "Remarks"
)

tree = ttk.Treeview(
    root,
    columns=columns,
    show="headings"
)

for column in columns:
    tree.heading(column, text=column)

tree.pack(fill="both", expand=True)

show_records()

root.mainloop()
