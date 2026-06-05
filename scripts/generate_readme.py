from __future__ import annotations

from html import escape
from typing import Any
from urllib.parse import quote

from common import (
    PROFILE_FILE,
    README_FILE,
    README_TEMPLATE_FILE,
    SOLVED_FILE,
    STATS_FILE,
    ensure_project_dirs,
    load_json,
    rating_label,
)


def shield(label: str, value: str | int, color: str) -> str:
    safe_label = quote(str(label).replace("-", "--"))
    safe_value = quote(str(value).replace("-", "--"))
    return f"![{label}](https://img.shields.io/badge/{safe_label}-{safe_value}-{color}?style=for-the-badge)"


def format_link(label: str, url: str | None) -> str:
    if not url:
        return escape(label)
    return f"[{escape(label)}]({url})"


def markdown_table(headers: list[str], rows: list[list[str]]) -> str:
    if not rows:
        return "No data yet."
    header = "| " + " | ".join(headers) + " |"
    separator = "| " + " | ".join(["---"] * len(headers)) + " |"
    body = ["| " + " | ".join(row) + " |" for row in rows]
    return "\n".join([header, separator, *body])


def build_badges(profile: dict[str, Any], stats: dict[str, Any]) -> str:
    cf_rating = profile.get("codeforcesRating") or "unrated"
    last_updated = str(stats.get("lastUpdated") or "not generated")[:10]
    badges = [
        shield("Total Solved", stats.get("totalSolved", 0), "2563eb"),
        shield("Current Streak", f"{stats.get('currentStreak', 0)} days", "16a34a"),
        shield("Longest Streak", f"{stats.get('longestStreak', 0)} days", "f59e0b"),
        shield("Codeforces Rating", cf_rating, "dc2626"),
        shield("Last Updated", last_updated, "4b5563"),
    ]
    return "\n".join(badges)


def build_about(profile: dict[str, Any]) -> str:
    name = profile.get("name") or "Abhijeet Ranjan"
    goal = profile.get("goal") or "Build strong problem-solving consistency."
    return (
        f"I am **{escape(name)}**, practicing competitive programming and DSA with a Codeforces-first workflow. "
        f"My current goal is: **{escape(goal)}**."
    )


def build_profile_links(profile: dict[str, Any]) -> str:
    rows: list[list[str]] = []
    github = profile.get("github")
    codeforces = profile.get("codeforces")
    leetcode = profile.get("leetcode")
    atcoder = profile.get("atcoder")
    codechef = profile.get("codechef")

    if github:
        rows.append(["GitHub", escape(github), format_link("Profile", f"https://github.com/{github}")])
    if codeforces:
        rows.append(["Codeforces", escape(codeforces), format_link("Profile", f"https://codeforces.com/profile/{codeforces}")])
    if leetcode:
        rows.append(["LeetCode", escape(leetcode), format_link("Profile", f"https://leetcode.com/{leetcode}")])
    if atcoder:
        rows.append(["AtCoder", escape(atcoder), format_link("Profile", f"https://atcoder.jp/users/{atcoder}")])
    if codechef:
        rows.append(["CodeChef", escape(codechef), format_link("Profile", f"https://www.codechef.com/users/{codechef}")])

    return markdown_table(["Platform", "Handle", "Link"], rows)


def build_dashboard_table(profile: dict[str, Any], stats: dict[str, Any]) -> str:
    rows = [
        ["Total solved", str(stats.get("totalSolved", 0))],
        ["Current streak", f"{stats.get('currentStreak', 0)} day(s)"],
        ["Longest streak", f"{stats.get('longestStreak', 0)} day(s)"],
        ["Platforms tracked", str(len(stats.get("platformStats", {})))],
        ["Codeforces handle", escape(profile.get("codeforces") or "not set")],
        ["Codeforces rating", escape(str(profile.get("codeforcesRating") or "unrated"))],
        ["Last updated", escape(str(stats.get("lastUpdated") or "not generated"))],
    ]
    return markdown_table(["Metric", "Value"], rows)


def build_streak_summary(stats: dict[str, Any]) -> str:
    current = stats.get("currentStreak", 0)
    longest = stats.get("longestStreak", 0)
    if current:
        return f"Current streak: **{current} day(s)**. Longest streak so far: **{longest} day(s)**."
    return f"No active streak today. Longest streak so far: **{longest} day(s)**."


def build_total_solved_section(stats: dict[str, Any]) -> str:
    total = stats.get("totalSolved", 0)
    monthly_stats = stats.get("monthlyStats", {})
    latest_month = next(reversed(monthly_stats), "none") if monthly_stats else "none"
    latest_month_count = monthly_stats.get(latest_month, 0) if latest_month != "none" else 0
    return f"Total logged problems: **{total}**. Latest active month: **{latest_month}** with **{latest_month_count}** solved problem(s)."


def build_counter_table(title: str, data: dict[str, int]) -> str:
    rows = [[escape(str(key)), str(value)] for key, value in data.items()]
    return markdown_table([title, "Solved"], rows)


def build_latest_table(solved: list[dict[str, Any]]) -> str:
    latest = sorted(solved, key=lambda entry: str(entry.get("solvedDate", "")), reverse=True)[:10]
    rows: list[list[str]] = []

    for entry in latest:
        title = str(entry.get("title") or entry.get("id") or "Problem")
        problem = format_link(title, entry.get("url"))
        topics = ", ".join(entry.get("tags") or []) or "-"
        solution_path = entry.get("solutionPath") or ""
        solution = format_link(entry.get("language") or "solution", solution_path) if solution_path else "Imported"
        rows.append(
            [
                escape(str(entry.get("solvedDate") or "-")),
                escape(str(entry.get("platform") or "-")),
                problem,
                escape(rating_label(entry.get("rating"))),
                escape(topics),
                solution,
            ]
        )

    return markdown_table(["Date", "Platform", "Problem", "Rating", "Topics", "Solution"], rows)


def build_platform_table(stats: dict[str, Any]) -> str:
    return build_counter_table("Platform", stats.get("platformStats", {}))


def build_extension_notes() -> str:
    return (
        "The data model already stores `platform`, `tags`, `rating`, `solutionPath`, and `solvedDate`, so new platforms can reuse the same dashboard. "
        "For LeetCode or AtCoder, add a platform folder under `solutions/`, create a fetcher only if the API is reliable, and keep manual JSON entry as the fallback path."
    )


def render_readme(profile: dict[str, Any], solved: list[dict[str, Any]], stats: dict[str, Any]) -> str:
    template = README_TEMPLATE_FILE.read_text(encoding="utf-8")
    replacements = {
        "{{BADGES}}": build_badges(profile, stats),
        "{{ABOUT}}": build_about(profile),
        "{{PROFILE_LINKS}}": build_profile_links(profile),
        "{{DASHBOARD_TABLE}}": build_dashboard_table(profile, stats),
        "{{STREAK_SUMMARY}}": build_streak_summary(stats),
        "{{TOTAL_SOLVED_SECTION}}": build_total_solved_section(stats),
        "{{TOPIC_TABLE}}": build_counter_table("Topic", stats.get("topicStats", {})),
        "{{RATING_TABLE}}": build_counter_table("Rating", stats.get("ratingStats", {})),
        "{{PLATFORM_TABLE}}": build_platform_table(stats),
        "{{LATEST_TABLE}}": build_latest_table(solved),
        "{{EXTENSION_NOTES}}": build_extension_notes(),
    }
    output = template
    for placeholder, value in replacements.items():
        output = output.replace(placeholder, value)
    return output


def main() -> int:
    ensure_project_dirs()
    profile = load_json(PROFILE_FILE, {})
    solved = load_json(SOLVED_FILE, [])
    stats = load_json(STATS_FILE, {})

    if not isinstance(profile, dict):
        raise SystemExit("data/profile.json must contain an object.")
    if not isinstance(solved, list):
        raise SystemExit("data/solved.json must contain a list.")
    if not isinstance(stats, dict):
        raise SystemExit("data/stats.json must contain an object.")
    if not README_TEMPLATE_FILE.exists():
        raise SystemExit("templates/README_TEMPLATE.md is missing.")

    README_FILE.write_text(render_readme(profile, solved, stats), encoding="utf-8")
    print(f"Generated {README_FILE.name}.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

