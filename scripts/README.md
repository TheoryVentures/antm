## Question Converter Script

- **What it is**: `questions_to_submission.py` scans markdown question files for ```json observation blocks, skips the `question`/`difficulty` fields, and emits submission ready rows into `scripts/submission.csv` (or a custom `--output`). It keeps the key order from each observation so answers line up with the expected CSV schema.
- **Why it helps**: lets you regenerate the submission file in one command instead of copying answers by hand. Works across rounds and enforces consistent formatting (fixed column count, sequential row indexes, normalized scalars/lists/dicts).

### Expected Observation Format

Each question must include a fenced JSON block like the training example:

```
```json
{
  "question": "January 2023 saw a spike in item returns in one state. What percentage of December revenue in the biggest returns category should be discounted due to those returns?",
  "state": "CA",
  "category": "Jewelry",
  "return_count": 2500,
  "return_value": 691182.47,
  "difficulty": 1
}
```
```

When the script runs, it drops `question`/`difficulty` and writes the remaining key values (in order) into `col_1`-`col_n` for that row of the CSV.

### Quick Start

```
cd /path/to/modeler-hackathon-starter
python3 scripts/questions_to_submission.py
```

Add `--max-cols`, `--skip`, or `--start-index` if you need to customize column counts or offsets.

