## Question Converter Script

- **What it is**: `questions_to_submission.py` scans markdown question files for ```json observation blocks, skips the `question`/`difficulty` fields, and emits submission ready rows into `scripts/submission.csv` (or a custom `--output`). It keeps the key order from each observation so answers line up with the expected CSV schema.
- **Why it helps**: lets you regenerate the submission file in one command instead of copying answers by hand. Works across rounds and enforces consistent formatting (fixed column count, sequential row indexes, normalized scalars/lists/dicts).

### Setup

To run the script, add your completed question markdown files to the `scripts/` directory (you don't need all of them—just whichever rounds you've completed):

1. **`round-1-questions.md`** - Round 1 questions with answers filled in the JSON blocks
2. **`round-2-questions.md`** - Round 2 questions with answers filled in the JSON blocks  
3. **`round-3-questions.md`** - Round 3 questions with answers filled in the JSON blocks

The script will automatically look for these files (plus `training-questions.md` which is already included). If any file is missing or has invalid JSON, the script will skip it and leave those rows blank in the output CSV. The CSV will always contain 63 rows (0-62) regardless of which files are present.

**By the end**, make sure you have all three round files with answers filled in so you can generate the final complete submission CSV.

### Expected Observation Format

Each question must include a fenced JSON block like the training example:

````markdown
```json
{
  "question": "Store #5's operations team noticed inventory shortages from one warehouse in November 2022. Despite overall revenue growth, investigate which warehouse experienced an inventory shortage that affected Store #5, and identify which product category was most impacted by this shortage. What was the revenue change in dollars for Store #5 in this specific warehouse-category combination from October to November 2022?",
  "warehouse_sk": 3,
  "category": "Jewelry",
  "revenue_impact": -32798.3
}
```
````

When the script runs, it drops `question`/`difficulty` and writes the remaining key values (in order) into `col_1`-`col_n` for that row of the CSV.

### Quick Start

```bash
cd scripts
python3 questions_to_submission.py
```

This will create `submission.csv` in your current directory. Add `--max-cols`, `--skip`, or `--start-index` if you need to customize column counts or offsets.

