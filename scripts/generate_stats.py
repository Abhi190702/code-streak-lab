from __future__ import annotations

import argparse
from collections import Counter
from datetime import date, datetime, timedelta, timezone
from typing import Any

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

from common import GRAPHS_DIR, SOLVED_FILE, STATS_FILE, ensure_project_dirs, load_json, parse_iso_date, rating_label, save_json

PALETTE = ["#2563eb", "#16a34a", "#f59e0b", "#dc2626", "#7c3aed", "#0891b2", "#db2777", "#4b5563"]
TEXT = "#111827"
MUTED = "#6b7280"
GRID = "#e5e7eb"


def calculate_current_streak(solved_dates: set[date], today: date) -> int:
    if not solved_dates:
        return 0

    if today in solved_dates:
        cursor = today
    elif today - timedelta(days=1) in solved_dates:
        cursor = today - timedelta(days=1)
    else:
        return 0

    streak = 0
    while cursor in solved_dates:
        streak += 1
        cursor -= timedelta(days=1)
    return streak


def calculate_longest_streak(solved_dates: set[date]) -> int:
    longest = 0
    current = 0
    previous: date | None = None

    for solved_date in sorted(solved_dates):
        if previous is None or solved_date == previous + timedelta(days=1):
            current += 1
        else:
            current = 1
        longest = max(longest, current)
        previous = solved_date

    return longest


def build_stats(solved: list[dict[str, Any]], today: date) -> dict[str, Any]:
    platform_counter: Counter[str] = Counter()
    topic_counter: Counter[str] = Counter()
    rating_counter: Counter[str] = Counter()
    weekly_counter: Counter[str] = Counter()
    monthly_counter: Counter[str] = Counter()
    daily_counter: Counter[str] = Counter()
    solved_dates: set[date] = set()

    for entry in solved:
        platform_counter[str(entry.get("platform") or "Unknown")] += 1
        rating_counter[rating_label(entry.get("rating"))] += 1

        for tag in entry.get("tags") or []:
            clean_tag = str(tag).strip().lower()
            if clean_tag:
                topic_counter[clean_tag] += 1

        solved_date = parse_iso_date(entry.get("solvedDate"))
        if solved_date is None:
            continue

        solved_dates.add(solved_date)
        daily_counter[solved_date.isoformat()] += 1
        iso_year, iso_week, _ = solved_date.isocalendar()
        weekly_counter[f"{iso_year}-W{iso_week:02d}"] += 1
        monthly_counter[solved_date.strftime("%Y-%m")] += 1

    rating_items = sorted(rating_counter.items(), key=lambda item: (999999 if item[0] == "unrated" else int(item[0])))
    topic_items = sorted(topic_counter.items(), key=lambda item: (-item[1], item[0]))
    platform_items = sorted(platform_counter.items(), key=lambda item: (-item[1], item[0]))

    return {
        "totalSolved": len(solved),
        "currentStreak": calculate_current_streak(solved_dates, today),
        "longestStreak": calculate_longest_streak(solved_dates),
        "platformStats": dict(platform_items),
        "topicStats": dict(topic_items),
        "ratingStats": dict(rating_items),
        "weeklyStats": dict(sorted(weekly_counter.items())),
        "monthlyStats": dict(sorted(monthly_counter.items())),
        "dailyStats": dict(sorted(daily_counter.items())),
        "lastUpdated": datetime.now(timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z"),
    }


def configure_axes(ax: plt.Axes, title: str) -> None:
    ax.set_title(title, fontsize=15, fontweight="bold", color=TEXT, pad=16)
    ax.tick_params(colors=MUTED, labelsize=10)
    for spine in ["top", "right"]:
        ax.spines[spine].set_visible(False)
    ax.spines["left"].set_color(GRID)
    ax.spines["bottom"].set_color(GRID)
    ax.grid(axis="y", color=GRID, linewidth=0.8, alpha=0.8)
    ax.set_axisbelow(True)


def save_figure(fig: plt.Figure, path_name: str) -> None:
    path = GRAPHS_DIR / path_name
    fig.tight_layout()
    fig.savefig(path, format="svg", bbox_inches="tight")
    plt.close(fig)


def draw_empty_chart(path_name: str, title: str) -> None:
    fig, ax = plt.subplots(figsize=(8, 3.2))
    fig.patch.set_facecolor("white")
    ax.set_facecolor("white")
    ax.text(0.5, 0.5, "No data yet", ha="center", va="center", fontsize=14, color=MUTED)
    ax.set_title(title, fontsize=15, fontweight="bold", color=TEXT, pad=16)
    ax.axis("off")
    save_figure(fig, path_name)


def draw_bar_chart(data: dict[str, int], path_name: str, title: str, *, horizontal: bool = False) -> None:
    if not data:
        draw_empty_chart(path_name, title)
        return

    labels = list(data.keys())
    values = list(data.values())
    colors = [PALETTE[index % len(PALETTE)] for index in range(len(labels))]
    height = max(3.2, min(8.0, 2.4 + len(labels) * 0.38))
    fig, ax = plt.subplots(figsize=(8.6, height))
    fig.patch.set_facecolor("white")
    ax.set_facecolor("white")

    if horizontal:
        ax.barh(labels, values, color=colors, height=0.58)
        ax.invert_yaxis()
        ax.set_xlabel("Solved", color=MUTED)
        for index, value in enumerate(values):
            ax.text(value + 0.05, index, str(value), va="center", color=TEXT, fontsize=10)
    else:
        ax.bar(labels, values, color=colors, width=0.62)
        ax.set_ylabel("Solved", color=MUTED)
        for index, value in enumerate(values):
            ax.text(index, value + 0.05, str(value), ha="center", va="bottom", color=TEXT, fontsize=10)

    configure_axes(ax, title)
    save_figure(fig, path_name)


def draw_daily_activity(daily_stats: dict[str, int], today: date) -> None:
    days = [today - timedelta(days=offset) for offset in range(29, -1, -1)]
    labels = [day.strftime("%b %d") for day in days]
    values = [daily_stats.get(day.isoformat(), 0) for day in days]

    fig, ax = plt.subplots(figsize=(10, 3.8))
    fig.patch.set_facecolor("white")
    ax.set_facecolor("white")
    ax.plot(range(len(days)), values, color="#2563eb", linewidth=2.4, marker="o", markersize=4)
    ax.fill_between(range(len(days)), values, color="#bfdbfe", alpha=0.45)
    ax.set_xticks(range(0, len(days), 5))
    ax.set_xticklabels([labels[index] for index in range(0, len(days), 5)], rotation=0)
    ax.set_ylabel("Solved", color=MUTED)
    ax.set_ylim(bottom=0)
    configure_axes(ax, "Daily Activity: Last 30 Days")
    save_figure(fig, "daily_activity.svg")


def streak_color(count: int) -> str:
    if count <= 0:
        return "#eef2f7"
    if count == 1:
        return "#93c5fd"
    if count == 2:
        return "#3b82f6"
    return "#1d4ed8"


def draw_streak_calendar(daily_stats: dict[str, int], today: date) -> None:
    start = today - timedelta(days=83)
    start -= timedelta(days=start.weekday())
    total_days = (today - start).days + 1
    weeks = total_days // 7 + 1

    fig, ax = plt.subplots(figsize=(max(9, weeks * 0.38), 2.8))
    fig.patch.set_facecolor("white")
    ax.set_facecolor("white")

    for offset in range(total_days):
        current = start + timedelta(days=offset)
        week = offset // 7
        weekday = current.weekday()
        count = daily_stats.get(current.isoformat(), 0)
        ax.add_patch(
            Rectangle(
                (week, 6 - weekday),
                0.82,
                0.82,
                facecolor=streak_color(count),
                edgecolor="white",
                linewidth=1,
            )
        )

    month_positions: dict[str, int] = {}
    for offset in range(total_days):
        current = start + timedelta(days=offset)
        label = current.strftime("%b")
        month_positions.setdefault(label, offset // 7)

    for label, x_position in month_positions.items():
        ax.text(x_position, 7.25, label, fontsize=9, color=MUTED, ha="left")

    for label, y_position in {"Mon": 6, "Wed": 4, "Fri": 2}.items():
        ax.text(-1.15, y_position + 0.15, label, fontsize=9, color=MUTED, ha="right")

    ax.set_xlim(-1.4, weeks + 0.2)
    ax.set_ylim(-0.2, 7.7)
    ax.set_title("Streak Calendar: Last 12 Weeks", fontsize=15, fontweight="bold", color=TEXT, pad=18)
    ax.axis("off")
    save_figure(fig, "streak_calendar.svg")


def generate_graphs(stats: dict[str, Any], today: date) -> None:
    draw_bar_chart(stats["topicStats"], "topic_distribution.svg", "Topic-wise Distribution", horizontal=True)
    draw_bar_chart(stats["ratingStats"], "rating_distribution.svg", "Rating-wise Distribution")
    draw_bar_chart(stats["platformStats"], "platform_distribution.svg", "Platform Distribution")
    draw_daily_activity(stats["dailyStats"], today)
    draw_streak_calendar(stats["dailyStats"], today)


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate JSON stats and SVG graphs from data/solved.json.")
    parser.add_argument("--today", help="Override today's date in YYYY-MM-DD format for streak testing.")
    args = parser.parse_args()

    ensure_project_dirs()
    today = parse_iso_date(args.today) if args.today else date.today()
    if today is None:
        raise SystemExit("--today must be in YYYY-MM-DD format.")

    solved = load_json(SOLVED_FILE, [])
    if not isinstance(solved, list):
        raise SystemExit("data/solved.json must contain a list of solved problem entries.")

    stats = build_stats(solved, today)
    save_json(STATS_FILE, stats)
    generate_graphs(stats, today)

    print(f"Generated stats for {stats['totalSolved']} solved problem(s).")
    print(f"Current streak: {stats['currentStreak']} day(s). Longest streak: {stats['longestStreak']} day(s).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

