from __future__ import annotations

import json
import re
from datetime import date, datetime
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"
ASSETS_DIR = ROOT / "assets"
GRAPHS_DIR = ASSETS_DIR / "graphs"
SOLUTIONS_DIR = ROOT / "solutions"
CODEFORCES_DIR = SOLUTIONS_DIR / "codeforces"

PROFILE_FILE = DATA_DIR / "profile.json"
SOLVED_FILE = DATA_DIR / "solved.json"
STATS_FILE = DATA_DIR / "stats.json"
README_FILE = ROOT / "README.md"
README_TEMPLATE_FILE = ROOT / "templates" / "README_TEMPLATE.md"

CODEFORCES_PROBLEM_URL = "https://codeforces.com/problemset/problem/{contest}/{index}"


def ensure_project_dirs() -> None:
    """Create directories that generated files depend on."""
    for path in [
        DATA_DIR,
        GRAPHS_DIR,
        ASSETS_DIR / "badges",
        CODEFORCES_DIR / "800",
        CODEFORCES_DIR / "900",
        CODEFORCES_DIR / "1000",
        CODEFORCES_DIR / "1100",
        CODEFORCES_DIR / "1200",
        CODEFORCES_DIR / "unrated",
    ]:
        path.mkdir(parents=True, exist_ok=True)


def load_json(path: Path, default: Any) -> Any:
    if not path.exists():
        return default
    try:
        with path.open("r", encoding="utf-8") as file:
            return json.load(file)
    except json.JSONDecodeError as exc:
        raise SystemExit(f"Invalid JSON in {path}: {exc}") from exc


def save_json(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as file:
        json.dump(data, file, indent=2, ensure_ascii=False)
        file.write("\n")


def parse_iso_date(value: str | None) -> date | None:
    if not value:
        return None
    try:
        return datetime.strptime(value, "%Y-%m-%d").date()
    except ValueError:
        return None


def normalize_rating(rating: Any) -> int | None:
    if rating is None:
        return None
    if isinstance(rating, int):
        return rating
    text = str(rating).strip().lower()
    if not text or text in {"none", "null", "unrated", "-"}:
        return None
    try:
        return int(text)
    except ValueError:
        return None


def rating_label(rating: Any) -> str:
    value = normalize_rating(rating)
    return str(value) if value is not None else "unrated"


def rating_folder(rating: Any) -> str:
    return rating_label(rating)


def codeforces_problem_id(contest_id: int | str, index: str) -> str:
    return f"cf-{contest_id}{str(index).upper()}"


def codeforces_problem_url(contest_id: int | str, index: str) -> str:
    return CODEFORCES_PROBLEM_URL.format(contest=contest_id, index=str(index).upper())


def slugify_title(title: str) -> str:
    slug = re.sub(r"[^A-Za-z0-9]+", "_", title.strip()).strip("_")
    return slug or "Problem"


def language_extension(language: str) -> str:
    aliases = {
        "c++": "cpp",
        "cpp": "cpp",
        "cc": "cpp",
        "cxx": "cpp",
        "python": "py",
        "py": "py",
        "java": "java",
        "go": "go",
        "golang": "go",
        "rust": "rs",
        "rs": "rs",
        "javascript": "js",
        "js": "js",
        "typescript": "ts",
        "ts": "ts",
    }
    return aliases.get(language.strip().lower(), language.strip().lower() or "txt")


def relative_to_root(path: Path) -> str:
    return path.resolve().relative_to(ROOT).as_posix()


def sorted_solved(entries: list[dict[str, Any]]) -> list[dict[str, Any]]:
    def key(entry: dict[str, Any]) -> tuple[str, str, str]:
        return (
            str(entry.get("solvedDate", "")),
            str(entry.get("platform", "")),
            str(entry.get("id", "")),
        )

    return sorted(entries, key=key)


def unique_sorted_tags(tags: list[str] | str | None) -> list[str]:
    if tags is None:
        return []
    if isinstance(tags, str):
        parts = tags.split(",")
    else:
        parts = tags
    cleaned = {str(tag).strip().lower() for tag in parts if str(tag).strip()}
    return sorted(cleaned)

