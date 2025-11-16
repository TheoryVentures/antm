"""Convert question observation JSON blocks into leaderboard-ready CSV rows."""

from __future__ import annotations

import argparse
import csv
import json
import re
from pathlib import Path
from typing import Any, Iterable, Iterator, Sequence

JSON_BLOCK_PATTERN = re.compile(r"```json(.*?)```", re.DOTALL | re.IGNORECASE)
DEFAULT_SKIP_FIELDS = ("question", "difficulty")
DEFAULT_INPUT_FILES = [
    Path("scripts/training-questions.md"),
    Path("scripts/round-1-questions.md"),
    Path("scripts/round-2-questions.md"),
    Path("scripts/round-3-questions.md"),
]
EXPECTED_TOTAL_ROWS = 63  # Always generate rows 0-62


def parse_arguments() -> argparse.Namespace:
    """Build and parse CLI arguments."""
    parser = argparse.ArgumentParser(
        description=(
            "Convert question files with ```json observation blocks into the "
            "leaderboard submission CSV schema."
        ),
    )
    parser.add_argument(
        "inputs",
        nargs="*",
        type=Path,
        help="Markdown files that contain observation JSON blocks.",
    )
    parser.add_argument(
        "-o",
        "--output",
        type=Path,
        default=Path("scripts/submission.csv"),
        help="Destination CSV file (default: scripts/submission.csv).",
    )
    parser.add_argument(
        "--skip",
        nargs="*",
        default=list(DEFAULT_SKIP_FIELDS),
        help="Field names to ignore when building submission columns.",
    )
    parser.add_argument(
        "--start-index",
        type=int,
        default=0,
        help="Row index to start from (default: 0).",
    )
    parser.add_argument(
        "--max-cols",
        type=int,
        default=5,
        help="Number of answer columns to emit (default: 5).",
    )
    return parser.parse_args()


def read_observation_blocks(path: Path) -> Iterator[list[tuple[str, Any]]]:
    """Yield ordered key-value pairs for each observation JSON block."""
    text = path.read_text(encoding="utf-8")
    for match in JSON_BLOCK_PATTERN.finditer(text):
        block = match.group(1).strip()
        if not block:
            continue
        yield json.loads(block, object_pairs_hook=list)


def normalize_value(value: Any) -> str:
    """Convert arbitrary JSON values into CSV-friendly strings."""
    if value is None:
        return ""
    if isinstance(value, bool):
        return "TRUE" if value else "FALSE"
    if isinstance(value, (int, float)):
        # Preserve negatives and decimals without adding trailing zeros.
        return format(value, ".15g")
    if isinstance(value, str):
        return value
    if isinstance(value, list):
        return "|".join(normalize_value(item) for item in value)
    if isinstance(value, dict):
        return json.dumps(value, separators=(",", ":"))
    return str(value)


def pairs_to_columns(
    pairs: Sequence[tuple[str, Any]],
    skip_fields: Iterable[str],
    max_cols: int,
) -> list[str]:
    """Convert ordered key-value pairs into contiguous submission columns."""
    skip = set(skip_fields)
    values: list[str] = [
        normalize_value(value) for key, value in pairs if key not in skip
    ]

    if len(values) > max_cols:
        raise ValueError(
            f"Found {len(values)} values but max_cols is {max_cols}. "
            "Increase --max-cols or trim the observation."
        )

    values.extend([""] * (max_cols - len(values)))
    return values


def build_rows(
    inputs: Iterable[Path],
    skip_fields: Iterable[str],
    max_cols: int,
    start_index: int,
) -> list[list[str]]:
    """Assemble all submission rows from the provided markdown files."""
    rows: list[list[str]] = []
    row_index = start_index

    for path in inputs:
        if not path.exists():
            continue
        try:
            for pairs in read_observation_blocks(path):
                columns = pairs_to_columns(pairs, skip_fields, max_cols)
                rows.append([str(row_index), *columns])
                row_index += 1
        except (json.JSONDecodeError, ValueError, OSError):
            # Skip files with invalid JSON or other errors
            continue

    return rows


def write_csv(
    output_path: Path,
    rows: list[list[str]],
    max_cols: int,
    expected_rows: int,
) -> None:
    """Write rows to disk with the leaderboard header, padding to expected count."""
    header = ["row_index", *[f"col_{i}" for i in range(1, max_cols + 1)]]
    output_path.parent.mkdir(parents=True, exist_ok=True)

    # Build a dict of existing rows by index
    rows_dict = {int(row[0]): row for row in rows}

    # Generate all rows 0 to expected_rows-1, filling missing with blanks
    all_rows = []
    for i in range(expected_rows):
        if i in rows_dict:
            all_rows.append(rows_dict[i])
        else:
            # Missing row: index + empty columns
            all_rows.append([str(i)] + [""] * max_cols)

    with output_path.open("w", encoding="utf-8", newline="") as fp:
        writer = csv.writer(fp)
        writer.writerow(header)
        writer.writerows(all_rows)


def main() -> None:
    """CLI entrypoint."""
    args = parse_arguments()
    inputs = args.inputs or DEFAULT_INPUT_FILES
    inputs = [path if path.is_absolute() else Path.cwd() / path for path in inputs]
    output_path = (
        args.output if args.output.is_absolute() else Path.cwd() / args.output
    )
    rows = build_rows(
        inputs=inputs,
        skip_fields=args.skip,
        max_cols=args.max_cols,
        start_index=args.start_index,
    )
    write_csv(output_path, rows, args.max_cols, EXPECTED_TOTAL_ROWS)
    print(f"Wrote {EXPECTED_TOTAL_ROWS} rows to {output_path} ({len(rows)} populated)")


if __name__ == "__main__":
    main()

