from __future__ import annotations

import argparse
import re
from pathlib import Path
from typing import Any

from common import (
    CODEFORCES_DIR,
    SOLVED_FILE,
    codeforces_problem_id,
    codeforces_problem_url,
    load_json,
    normalize_rating,
    parse_iso_date,
    relative_to_root,
    save_json,
    sorted_solved,
    unique_sorted_tags,
)

SUPPORTED_EXTENSIONS = {".cpp", ".cc", ".cxx", ".py", ".java", ".go", ".rs", ".js", ".ts"}
REQUIRED_FIELDS = ["Platform", "Problem", "Contest ID", "Index", "Rating", "Tags", "Solved Date", "URL"]
KEY_PATTERN = re.compile(r"^\s*([A-Za-z][A-Za-z ]+):\s*(.*?)\s*$")


def canonical_key(key: str) -> str:
    return re.sub(r"[^a-z0-9]+", "", key.lower())


def parse_metadata(path: Path) -> dict[str, str]:
    metadata: dict[str, str] = {}
    lines = path.read_text(encoding="utf-8", errors="replace").splitlines()[:90]

    for line in lines:
        match = KEY_PATTERN.match(line.strip("/*# \t"))
        if not match:
            continue
        key, value = match.groups()
        normalized = canonical_key(key)
        metadata[normalized] = value.strip()

    return metadata


def get_value(metadata: dict[str, str], key: str) -> str:
    return metadata.get(canonical_key(key), "")


def validation_errors(path: Path, metadata: dict[str, str]) -> list[str]:
    errors = []
    for field in REQUIRED_FIELDS:
        if not get_value(metadata, field):
            errors.append(f"missing {field}")

    contest_id = get_value(metadata, "Contest ID")
    if contest_id and not contest_id.isdigit():
        errors.append("Contest ID must be a number")

    rating = get_value(metadata, "Rating")
    if rating and normalize_rating(rating) is None and rating.strip().lower() != "unrated":
        errors.append("Rating must be a number or unrated")

    solved_date = get_value(metadata, "Solved Date")
    if solved_date and parse_iso_date(solved_date) is None:
        errors.append("Solved Date must use YYYY-MM-DD")

    url = get_value(metadata, "URL")
    if url and not url.startswith(("http://", "https://")):
        errors.append("URL must start with http:// or https://")

    if not path.name.strip():
        errors.append("file name is empty")

    return errors


def solution_files() -> list[Path]:
    if not CODEFORCES_DIR.exists():
        return []
    return sorted(path for path in CODEFORCES_DIR.rglob("*") if path.suffix.lower() in SUPPORTED_EXTENSIONS)


def metadata_to_entry(path: Path, metadata: dict[str, str]) -> dict[str, Any]:
    platform = get_value(metadata, "Platform")
    contest_id = int(get_value(metadata, "Contest ID"))
    index = get_value(metadata, "Index").upper()
    rating = normalize_rating(get_value(metadata, "Rating"))
    title = get_value(metadata, "Problem")
    url = get_value(metadata, "URL") or codeforces_problem_url(contest_id, index)
    language = path.suffix.lstrip(".")

    if platform.lower() == "codeforces":
        problem_id = codeforces_problem_id(contest_id, index)
    else:
        problem_id = f"{platform.lower()}-{contest_id}{index}"

    return {
        "id": problem_id,
        "platform": platform,
        "contestId": contest_id,
        "index": index,
        "title": title,
        "url": url,
        "rating": rating,
        "tags": unique_sorted_tags(get_value(metadata, "Tags")),
        "language": language,
        "solutionPath": relative_to_root(path),
        "solvedDate": get_value(metadata, "Solved Date"),
        "notes": get_value(metadata, "Notes"),
    }


def sync_solved_json(valid_metadata: list[tuple[Path, dict[str, str]]]) -> None:
    solved = load_json(SOLVED_FILE, [])
    if not isinstance(solved, list):
        raise SystemExit("data/solved.json must contain a list.")

    by_id: dict[str, dict[str, Any]] = {str(entry.get("id")): entry for entry in solved if entry.get("id")}

    for path, metadata in valid_metadata:
        entry = metadata_to_entry(path, metadata)
        existing = by_id.get(entry["id"], {})
        merged = {**existing, **entry}
        if existing.get("notes") and not entry.get("notes"):
            merged["notes"] = existing["notes"]
        by_id[entry["id"]] = merged

    save_json(SOLVED_FILE, sorted_solved(list(by_id.values())))


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate solution metadata blocks.")
    parser.add_argument("--sync", action="store_true", help="Sync valid solution metadata into data/solved.json.")
    args = parser.parse_args()

    files = solution_files()
    if not files:
        print("No solution files found under solutions/codeforces.")
        return 0

    failures: list[tuple[Path, list[str]]] = []
    valid_metadata: list[tuple[Path, dict[str, str]]] = []

    for path in files:
        metadata = parse_metadata(path)
        errors = validation_errors(path, metadata)
        if errors:
            failures.append((path, errors))
        else:
            valid_metadata.append((path, metadata))

    if failures:
        print("Metadata validation failed:")
        for path, errors in failures:
            print(f"- {relative_to_root(path)}")
            for error in errors:
                print(f"  - {error}")
        return 1

    if args.sync:
        sync_solved_json(valid_metadata)
        print(f"Synced {len(valid_metadata)} solution file(s) into data/solved.json.")

    print(f"Validated {len(valid_metadata)} solution file(s).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

