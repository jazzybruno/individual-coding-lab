# Grade Evaluator and Organizer

Individual Coding Lab: Introduction to Python Programming and Databases, BSE Year 1 Trimester 2.

## Files

| File | Purpose |
|---|---|
| `grade-evaluator.py` | Validates the grades, calculates the GPA, decides PASSED/FAILED and lists resubmissions |
| `organizer.sh` | Archives `grades.csv` with a timestamp, creates a fresh one and logs the run |
| `grades.csv` | The course grades: `assignment,group,score,weight` |

## Grade evaluator

```bash
python3 grade-evaluator.py
```

Enter `grades.csv` when asked. The program:

1. **Validates the scores:** every score must be between 0 and 100.
2. **Validates the weights:** they must add up to exactly 100, with Formative = 60 and Summative = 40.
3. **Calculates the GPA:** Total Grade = sum of `score × weight / 100`, then `GPA = (Total Grade / 100) × 5.0`.
4. **Decides the status:** PASSED only if the student scores at least 50% in **both** Formative and Summative.
   A category's percentage is the points earned divided by its weight.
5. **Lists resubmissions:** the failed formative assignment(s) (score below 50) with the highest weight. Ties are all listed.

If anything is wrong, it prints a clear message and stops instead of crashing. That covers a missing or empty file, missing columns, empty rows (skipped), non-numeric scores or weights, an unknown group, scores outside 0–100, and wrong weight totals.

### Result for the provided `grades.csv`

| Check | Result |
|---|---|
| Formative | (85×20 + 40×20 + 45×20) / 60 = **56.67%** |
| Summative | (70×20 + 60×20) / 40 = **65.00%** |
| Total Grade | **60.00** |
| GPA | 60 / 100 × 5.0 = **3.00** |
| Status | **PASSED** (both categories ≥ 50%) |
| Resubmission | **Group Exercise** and **Functions and Debugging Lab** (both failed, both weight 20) |

## Organizer

```bash
chmod +x organizer.sh
./organizer.sh
```

1. Creates the `archive/` directory if it doesn't exist.
2. Moves `grades.csv` to `archive/grades_YYYYMMDD-HHMMSS.csv`.
3. Creates a new, empty `grades.csv`.
4. Appends the timestamp, original filename and archived filename to `organizer.log`, which keeps every run.

If `grades.csv` doesn't exist, it says so and stops without changing anything.
