from __future__ import annotations

import argparse
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import requests

from common import (
    CODEFORCES_DIR,
    PROFILE_FILE,
    SOLVED_FILE,
    codeforces_problem_id,
    codeforces_problem_url,
    ensure_project_dirs,
    load_json,
    relative_to_root,
    save_json,
    sorted_solved,
    unique_sorted_tags,
)

API_BASE = "https://codeforces.com/api"


def api_get(endpoint: str, params: dict[str, Any]) -> Any:
    response = requests.get(f"{API_BASE}/{endpoint}", params=params, timeout=25)
    response.raise_for_status()
    payload = response.json()
    if payload.get("status") != "OK":
        comment = payload.get("comment", "unknown API error")
        raise RuntimeError(comment)
    return payload.get("result")


def fetch_user(handle: str) -> dict[str, Any] | None:
    result = api_get("user.info", {"handles": handle})
    if not result:
        return None
    return result[0]


def fetch_submissions(handle: str, count: int) -> list[dict[str, Any]]:
    return api_get("user.status", {"handle": handle, "from": 1, "count": count})


def update_profile(profile: dict[str, Any], user: dict[str, Any] | None) -> dict[str, Any]:
    if not user:
        return profile

    profile["codeforcesRating"] = user.get("rating", "")
    profile["codeforcesMaxRating"] = user.get("maxRating", "")
    profile["codeforcesRank"] = user.get("rank", "")
    profile["codeforcesMaxRank"] = user.get("maxRank", "")
    profile["codeforcesContribution"] = user.get("contribution", "")
    profile["codeforcesFriendOfCount"] = user.get("friendOfCount", "")
    profile["codeforcesLastFetched"] = datetime.now(timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z")
    return profile


def find_local_solution(contest_id: int, index: str) -> str:
    if not CODEFORCES_DIR.exists():
        return ""

    prefix = f"{contest_id}{index}".lower()
    for path in CODEFORCES_DIR.rglob("*"):
        if not path.is_file():
            continue
        if path.name.lower().startswith(prefix):
            return relative_to_root(path)
    return ""


def submission_to_entry(submission: dict[str, Any]) -> dict[str, Any] | None:
    if submission.get("verdict") != "OK":
        return None

    problem = submission.get("problem") or {}
    contest_id = problem.get("contestId")
    index = problem.get("index")
    title = problem.get("name")
    if contest_id is None or not index or not title:
        return None

    solved_at = datetime.fromtimestamp(submission.get("creationTimeSeconds", 0), tz=timezone.utc).date().isoformat()
    problem_id = codeforces_problem_id(contest_id, index)

    return {
        "id": problem_id,
        "platform": "Codeforces",
        "contestId": contest_id,
        "index": str(index).upper(),
        "title": title,
        "url": codeforces_problem_url(contest_id, index),
        "rating": problem.get("rating"),
        "tags": unique_sorted_tags(problem.get("tags") or []),
        "language": "",
        "solutionPath": find_local_solution(contest_id, str(index).upper()),
        "solvedDate": solved_at,
        "notes": "Imported from Codeforces API.",
    }


def merge_submissions(existing: list[dict[str, Any]], submissions: list[dict[str, Any]]) -> tuple[list[dict[str, Any]], int]:
    by_id: dict[str, dict[str, Any]] = {str(entry.get("id")): entry for entry in existing if entry.get("id")}
    imported = 0

    for submission in reversed(submissions):
        entry = submission_to_entry(submission)
        if entry is None:
            continue

        current = by_id.get(entry["id"])
        if current:
            if not current.get("solutionPath") and entry.get("solutionPath"):
                current["solutionPath"] = entry["solutionPath"]
            if current.get("rating") in {"", None} and entry.get("rating") is not None:
                current["rating"] = entry["rating"]
            if not current.get("tags") and entry.get("tags"):
                current["tags"] = entry["tags"]
            continue

        by_id[entry["id"]] = entry
        imported += 1

    return sorted_solved(list(by_id.values())), imported


def main() -> int:
    parser = argparse.ArgumentParser(description="Import accepted Codeforces submissions into data/solved.json.")
    parser.add_argument("--handle", help="Override the Codeforces handle from data/profile.json.")
    parser.add_argument("--count", type=int, default=10000, help="Maximum submissions to scan.")
    parser.add_argument("--strict", action="store_true", help="Exit non-zero if the Codeforces API is unavailable.")
    args = parser.parse_args()

    ensure_project_dirs()
    profile = load_json(PROFILE_FILE, {})
    solved = load_json(SOLVED_FILE, [])

    if not isinstance(profile, dict):
        raise SystemExit("data/profile.json must contain an object.")
    if not isinstance(solved, list):
        raise SystemExit("data/solved.json must contain a list.")

    handle = args.handle or profile.get("codeforces")
    if not handle:
        print("No Codeforces handle configured. Skipping fetch.")
        return 0

    try:
        user = fetch_user(handle)
        submissions = fetch_submissions(handle, args.count)
    except Exception as exc:
        print(f"Codeforces API fetch failed: {exc}")
        print("Keeping existing local JSON data. Manual workflow still works.")
        return 1 if args.strict else 0

    profile = update_profile(profile, user)
    merged, imported = merge_submissions(solved, submissions)
    save_json(PROFILE_FILE, profile)
    save_json(SOLVED_FILE, merged)

    print(f"Fetched Codeforces data for {handle}.")
    print(f"Imported {imported} new accepted problem(s). Total tracked: {len(merged)}.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

