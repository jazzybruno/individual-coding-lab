import csv
import sys
import os

REQUIRED_COLUMNS = ['assignment', 'group', 'score', 'weight']
GROUP_WEIGHTS = {'Formative': 60, 'Summative': 40}


def load_csv_data():
    """
    Prompts the user for a filename, checks if it exists,
    and extracts all fields into a list of dictionaries.
    """
    filename = input("Enter the name of the CSV file to process (e.g., grades.csv): ").strip()

    if not os.path.exists(filename):
        print(f"Error: The file '{filename}' was not found.")
        sys.exit(1)

    if os.path.getsize(filename) == 0:
        print(f"Error: The file '{filename}' is empty.")
        sys.exit(1)

    assignments = []
    errors = []

    try:
        with open(filename, mode='r', encoding='utf-8') as file:
            reader = csv.DictReader(file)

            missing = [c for c in REQUIRED_COLUMNS if c not in (reader.fieldnames or [])]
            if missing:
                print(f"Error: Missing column(s): {', '.join(missing)}")
                sys.exit(1)

            # line 1 is the header, so data starts on line 2
            for line, row in enumerate(reader, start=2):
                if not any((value or '').strip() for value in row.values()):
                    continue

                name = (row['assignment'] or '').strip()
                group = (row['group'] or '').strip().capitalize()

                if not name:
                    errors.append(f"Line {line}: the assignment name is missing.")
                    continue
                if group not in GROUP_WEIGHTS:
                    errors.append(f"Line {line} ({name}): group must be Formative or Summative, got '{row['group']}'.")
                    continue
                try:
                    score = float(row['score'])
                    weight = float(row['weight'])
                except (TypeError, ValueError):
                    errors.append(f"Line {line} ({name}): score and weight must be numbers, "
                                  f"got '{row['score']}' and '{row['weight']}'.")
                    continue

                assignments.append({
                    'assignment': name,
                    'group': group,
                    'score': score,
                    'weight': weight
                })
    except (OSError, UnicodeDecodeError, csv.Error) as e:
        print(f"An error occurred while reading the file: {e}")
        sys.exit(1)

    if errors:
        print("Error: Some rows could not be read:")
        for error in errors:
            print(f"  - {error}")
        sys.exit(1)

    if not assignments:
        print(f"Error: The file '{filename}' has no assignments.")
        sys.exit(1)

    return assignments


def validate(data):
    errors = []

    for a in data:
        if not 0 <= a['score'] <= 100:
            errors.append(f"{a['assignment']}: score {a['score']:g} is outside 0-100.")
        if a['weight'] <= 0:
            errors.append(f"{a['assignment']}: weight {a['weight']:g} must be greater than 0.")

    total_weight = round(sum(a['weight'] for a in data), 2)
    if total_weight != 100:
        errors.append(f"Total weight is {total_weight:g}, it must be exactly 100.")

    for group, expected in GROUP_WEIGHTS.items():
        group_weight = round(sum(a['weight'] for a in data if a['group'] == group), 2)
        if group_weight != expected:
            errors.append(f"{group} weight is {group_weight:g}, it must be exactly {expected}.")

    return errors


def evaluate_grades(data):
    print("\n--- Processing Grades ---")

    errors = validate(data)
    if errors:
        print("Validation failed:")
        for error in errors:
            print(f"  - {error}")
        sys.exit(1)
    print("All scores are between 0 and 100, and the weights are valid (Formative 60, Summative 40).")

    # each assignment adds score x weight / 100 to the final grade
    total_grade = sum(a['score'] * a['weight'] / 100 for a in data)
    gpa = (total_grade / 100) * 5.0

    # a category's percentage is the points earned out of its weight
    category = {}
    for group, weight in GROUP_WEIGHTS.items():
        earned = sum(a['score'] * a['weight'] / 100 for a in data if a['group'] == group)
        category[group] = earned / weight * 100

    passed = all(percent >= 50 for percent in category.values())

    failed_formative = [a for a in data if a['group'] == 'Formative' and a['score'] < 50]
    resubmit = []
    if failed_formative:
        highest = max(a['weight'] for a in failed_formative)
        resubmit = [a for a in failed_formative if a['weight'] == highest]

    print("\n--- Transcript ---")
    print(f"{'Assignment':<38}{'Group':<12}{'Score':>7}{'Weight':>8}")
    for a in data:
        print(f"{a['assignment']:<38}{a['group']:<12}{a['score']:>7g}{a['weight']:>8g}")

    print(f"\nFormative: {category['Formative']:.2f}%  (needs 50%)")
    print(f"Summative: {category['Summative']:.2f}%  (needs 50%)")
    print(f"Total Grade: {total_grade:.2f} / 100")
    print(f"GPA: {gpa:.2f} / 5.0")
    print(f"\nFinal Status: {'PASSED' if passed else 'FAILED'}")

    if resubmit:
        print("Eligible for resubmission:")
        for a in resubmit:
            print(f"  - {a['assignment']} (score {a['score']:g}, weight {a['weight']:g})")
    else:
        print("No formative assignment to resubmit.")


if __name__ == "__main__":
    # 1. Load the data
    course_data = load_csv_data()

    # 2. Process the features
    evaluate_grades(course_data)
