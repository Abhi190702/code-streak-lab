from __future__ import annotations

import argparse
from pathlib import Path
from typing import Any

from common import (
    CODEFORCES_DIR,
    SOLVED_FILE,
    codeforces_problem_id,
    codeforces_problem_url,
    ensure_project_dirs,
    language_extension,
    load_json,
    normalize_rating,
    parse_iso_date,
    rating_folder,
    relative_to_root,
    save_json,
    slugify_title,
    sorted_solved,
    unique_sorted_tags,
)


def cpp_template(metadata: str) -> str:
    return f"""{metadata}

#include <bits/stdc++.h>
using namespace std;

int main() {{
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    // Write your solution here.
    return 0;
}}
"""


def plain_template(metadata: str) -> str:
    return f"""{metadata}

// Write your solution here.
"""


def python_template(metadata: str) -> str:
    return f"""{metadata}

# Write your solution here.
"""


def metadata_lines(args: argparse.Namespace, url: str) -> list[str]:
    return [
        f"Platform: {args.platform}",
        f"Problem: {args.title}",
        f"Contest ID: {args.contest}",
        f"Index: {args.index.upper()}",
        f"Rating: {args.rating}",
        f"Tags: {args.tags}",
        f"Solved Date: {args.date}",
        f"URL: {url}",
    ]


def metadata_block(args: argparse.Namespace, url: str, extension: str) -> str:
    body = "\n".join(metadata_lines(args, url))
    if extension == ".py":
        return f'"""\n{body}\n"""'
    return f"/*\n{body}\n*/"


def build_solution_path(args: argparse.Namespace) -> Path:
    extension = language_extension(args.language)
    folder = CODEFORCES_DIR / rating_folder(args.rating)
    filename = f"{args.contest}{args.index.upper()}_{slugify_title(args.title)}.{extension}"
    return folder / filename


def write_solution_file(path: Path, args: argparse.Namespace, url: str) -> None:
    if path.exists():
        print(f"Solution file already exists: {relative_to_root(path)}")
        return

    path.parent.mkdir(parents=True, exist_ok=True)
    extension = path.suffix.lower()
    metadata = metadata_block(args, url, extension)
    if extension in {".cpp", ".cc", ".cxx"}:
        content = cpp_template(metadata)
    elif extension == ".py":
        content = python_template(metadata)
    else:
        content = plain_template(metadata)
    path.write_text(content, encoding="utf-8")
    print(f"Created {relative_to_root(path)}")


def upsert_solved_entry(args: argparse.Namespace, path: Path, url: str) -> None:
    solved = load_json(SOLVED_FILE, [])
    if not isinstance(solved, list):
        raise SystemExit("data/solved.json must contain a list.")

    problem_id = codeforces_problem_id(args.contest, args.index)
    by_id: dict[str, dict[str, Any]] = {str(entry.get("id")): entry for entry in solved if entry.get("id")}
    if problem_id in by_id:
        print(f"{problem_id} already exists in data/solved.json. No duplicate added.")
        return

    by_id[problem_id] = {
        "id": problem_id,
        "platform": args.platform,
        "contestId": args.contest,
        "index": args.index.upper(),
        "title": args.title,
        "url": url,
        "rating": normalize_rating(args.rating),
        "tags": unique_sorted_tags(args.tags),
        "language": language_extension(args.language),
        "solutionPath": relative_to_root(path),
        "solvedDate": args.date,
        "notes": args.notes,
    }
    save_json(SOLVED_FILE, sorted_solved(list(by_id.values())))
    print(f"Added {problem_id} to data/solved.json")


def main() -> int:
    parser = argparse.ArgumentParser(description="Create a solution file and solved.json entry.")
    parser.add_argument("--platform", default="Codeforces", help="Currently only Codeforces is supported.")
    parser.add_argument("--contest", type=int, required=True, help="Codeforces contest ID.")
    parser.add_argument("--index", required=True, help="Problem index, for example A or B.")
    parser.add_argument("--title", required=True, help="Problem title.")
    parser.add_argument("--rating", default="unrated", help="Problem rating or unrated.")
    parser.add_argument("--tags", default="", help="Comma-separated topic tags.")
    parser.add_argument("--language", default="cpp", help="Solution language, for example cpp or py.")
    parser.add_argument("--date", required=True, help="Solved date in YYYY-MM-DD format.")
    parser.add_argument("--url", help="Problem URL. Defaults to the Codeforces problem URL.")
    parser.add_argument("--notes", default="", help="Optional notes for data/solved.json.")
    args = parser.parse_args()

    if args.platform.lower() != "codeforces":
        raise SystemExit("Only Codeforces is supported right now. Add other platforms by extending this script.")
    if parse_iso_date(args.date) is None:
        raise SystemExit("--date must use YYYY-MM-DD format.")
    if normalize_rating(args.rating) is None and str(args.rating).strip().lower() != "unrated":
        raise SystemExit("--rating must be a number or unrated.")

    ensure_project_dirs()
    url = args.url or codeforces_problem_url(args.contest, args.index)
    path = build_solution_path(args)
    write_solution_file(path, args, url)
    upsert_solved_entry(args, path, url)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
