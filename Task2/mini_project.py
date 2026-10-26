"""
Student Management System
-------------------------
A menu-driven console app to add, view, search, update and delete students,
calculate grades, and save data to a file.

Concepts demonstrated:
  - Variables & data types   : str, int, float, bool, list, dict, tuple, set
  - Input & output           : input(), print(), f-strings
  - Conditional statements   : if / elif / else
  - Loops                    : while (menu, validation), for (display, totals)
  - Functions                : one function per feature
  - Data structures          : dict of dicts (students), list, tuple, set
  - File handling            : save/load JSON, export text report
  - Exception handling       : try / except / else / finally
  - Library                  : json (storage) and datetime (timestamps)
"""

import json                      # json: converts Python data <-> text files
from datetime import datetime    # datetime: timestamps for the report

DATA_FILE = "students.json"      # file where student data is stored
REPORT_FILE = "report.txt"       # file for the exported report

# Tuple: fixed (min_percentage, grade) pairs, checked from highest to lowest
GRADE_SCALE = ((90, "A+"), (80, "A"), (70, "B"), (60, "C"), (50, "D"))


# Helpers
def read_int(prompt, minimum=None, maximum=None):
    """Keep asking until the user enters a valid integer in range."""
    while True:
        try:
            value = int(input(prompt))
        except ValueError:                       # text like "abc"
            print("  Invalid input. Please enter a whole number.")
            continue
        if minimum is not None and value < minimum:
            print(f"  Value must be at least {minimum}.")
        elif maximum is not None and value > maximum:
            print(f"  Value must be at most {maximum}.")
        else:
            return value


def read_text(prompt):
    """Keep asking until the user enters a non-empty string."""
    while True:
        text = input(prompt).strip()
        if text:
            return text
        print("  Input cannot be empty.")


def calculate_average(marks):
    """Return the average of a dict of marks (0 if there are none)."""
    if not marks:
        return 0.0
    return sum(marks.values()) / len(marks)


def get_grade(average):
    """Convert an average percentage into a letter grade."""
    for minimum, grade in GRADE_SCALE:
        if average >= minimum:
            return grade
    return "F"                                   # below every threshold


# File handling
def load_students():
    """Load students from the JSON file; return empty dict if unavailable."""
    try:
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        print("No saved data found. Starting with an empty list.")
    except json.JSONDecodeError:
        print("Data file is corrupted. Starting with an empty list.")
    return {}


def save_students(students):
    """Write all students to the JSON file."""
    try:
        with open(DATA_FILE, "w") as f:
            json.dump(students, f, indent=4)
        print("  Data saved.")
    except OSError as e:
        print(f"  Could not save data: {e}")


def export_report(students):
    """Write a readable text report of all students."""
    try:
        with open(REPORT_FILE, "w") as f:
            f.write("STUDENT REPORT\n")
            f.write(f"Generated: {datetime.now():%d %B %Y, %I:%M %p}\n")
            f.write("=" * 45 + "\n")
            for roll, s in students.items():
                avg = calculate_average(s["marks"])
                f.write(f"{roll:<6}{s['name']:<20}"
                        f"{avg:>6.1f}%  Grade {get_grade(avg)}\n")
        print(f"  Report exported to {REPORT_FILE}")
    except OSError as e:
        print(f"  Could not write report: {e}")


# --------------------------------------------------------------- Features
def add_student(students):
    """Add a new student with name, age and subject marks."""
    roll = read_text("Roll number: ")
    if roll in students:                         # dict membership check
        print("  A student with this roll number already exists.")
        return

    name = read_text("Name: ")
    age = read_int("Age: ", 3, 100)
    count = read_int("How many subjects? ", 1, 10)

    marks = {}                                   # dict: subject -> score
    for i in range(1, count + 1):
        subject = read_text(f"  Subject {i} name: ")
        marks[subject] = read_int(f"  Marks in {subject} (0-100): ", 0, 100)

    students[roll] = {"name": name, "age": age, "marks": marks}
    print(f"  Student '{name}' added.")


def view_students(students):
    """Display all students in a table."""
    if not students:
        print("  No students to show.")
        return
    print(f"\n{'Roll':<8}{'Name':<20}{'Age':<6}{'Average':<10}Grade")
    print("-" * 50)
    for roll, s in students.items():
        avg = calculate_average(s["marks"])
        print(f"{roll:<8}{s['name']:<20}{s['age']:<6}{avg:<10.1f}{get_grade(avg)}")


def search_student(students):
    """Find a student by roll number and show full details."""
    roll = read_text("Enter roll number to search: ")
    student = students.get(roll)                 # returns None if missing
    if student is None:
        print("  Student not found.")
        return
    print(f"\n  Name: {student['name']}   Age: {student['age']}")
    for subject, score in student["marks"].items():
        print(f"    {subject}: {score}")
    avg = calculate_average(student["marks"])
    print(f"  Average: {avg:.1f}%   Grade: {get_grade(avg)}")


def update_marks(students):
    """Change the marks of one subject for a student."""
    roll = read_text("Enter roll number: ")
    if roll not in students:
        print("  Student not found.")
        return
    marks = students[roll]["marks"]
    print("  Subjects:", ", ".join(marks))
    subject = read_text("Subject to update: ")
    if subject in marks:
        marks[subject] = read_int("New marks (0-100): ", 0, 100)
        print("  Marks updated.")
    else:
        print("  Subject not found for this student.")


def delete_student(students):
    """Remove a student after confirmation."""
    roll = read_text("Enter roll number to delete: ")
    if roll not in students:
        print("  Student not found.")
        return
    confirm = input(f"  Delete {students[roll]['name']}? (y/n): ").lower()
    if confirm == "y":
        del students[roll]
        print("  Student deleted.")
    else:
        print("  Deletion cancelled.")


def show_statistics(students):
    """Show class size, class average, topper and list of all subjects."""
    if not students:
        print("  No data available.")
        return

    averages = []                                # list of (average, name)
    all_subjects = set()                         # set: keeps only unique items
    for s in students.values():
        averages.append((calculate_average(s["marks"]), s["name"]))
        all_subjects.update(s["marks"].keys())

    class_avg = sum(a for a, _ in averages) / len(averages)
    top_avg, top_name = max(averages)            # tuple comparison: highest avg

    print(f"\n  Total students : {len(students)}")
    print(f"  Class average  : {class_avg:.1f}%")
    print(f"  Topper         : {top_name} ({top_avg:.1f}%)")
    print(f"  Subjects       : {', '.join(sorted(all_subjects))}")


# Menu
def show_menu():
    print("\n===== STUDENT MANAGEMENT SYSTEM =====")
    print("1. Add student")
    print("2. View all students")
    print("3. Search student")
    print("4. Update marks")
    print("5. Delete student")
    print("6. Show statistics")
    print("7. Export report")
    print("8. Save & exit")


def main():
    students = load_students()
    running = True                               # bool controlling the loop

    # Dictionary mapping menu choice -> function (cleaner than many elifs)
    actions = {
        1: add_student, 2: view_students, 3: search_student,
        4: update_marks, 5: delete_student, 6: show_statistics,
        7: export_report,
    }

    try:
        while running:
            show_menu()
            choice = read_int("Choose an option (1-8): ", 1, 8)

            if choice == 8:
                save_students(students)
                print("Goodbye!")
                running = False
            else:
                actions[choice](students)
    except KeyboardInterrupt:
        # Ctrl+C: save work before quitting so nothing is lost
        print("\nInterrupted. Saving data...")
        save_students(students)
    except EOFError:
        print("\nInput ended. Saving data...")
        save_students(students)


if __name__ == "__main__":
    main()