# CP & DSA Streak Tracker

{{BADGES}}

A clean dashboard to track my competitive programming, DSA practice, Codeforces progress, topic-wise growth, rating-wise progress, and daily consistency.

> Generated from `templates/README_TEMPLATE.md`. Edit the template, then run `python scripts/generate_readme.py`.

## About

{{ABOUT}}

## My Coding Profiles

{{PROFILE_LINKS}}

## Progress Dashboard

{{DASHBOARD_TABLE}}

## Current Streak

{{STREAK_SUMMARY}}

## Total Problems Solved

{{TOTAL_SOLVED_SECTION}}

## Topic-wise Distribution

![Topic-wise distribution](assets/graphs/topic_distribution.svg)

{{TOPIC_TABLE}}

## Rating-wise Distribution

![Rating-wise distribution](assets/graphs/rating_distribution.svg)

{{RATING_TABLE}}

## Platform Distribution

![Platform distribution](assets/graphs/platform_distribution.svg)

{{PLATFORM_TABLE}}

## Daily Activity Graph

![Daily activity graph](assets/graphs/daily_activity.svg)

## Streak Calendar

![Streak calendar](assets/graphs/streak_calendar.svg)

## Latest Solved Problems

{{LATEST_TABLE}}

## Folder Structure

```text
cp-dsa-streak-tracker/
├── data/
│   ├── profile.json
│   ├── solved.json
│   └── stats.json
├── solutions/
│   └── codeforces/
│       ├── 800/
│       ├── 900/
│       ├── 1000/
│       ├── 1100/
│       ├── 1200/
│       └── unrated/
├── scripts/
│   ├── add_problem.py
│   ├── common.py
│   ├── fetch_codeforces.py
│   ├── generate_readme.py
│   ├── generate_stats.py
│   └── validate_solution.py
├── assets/
│   ├── graphs/
│   └── badges/
├── templates/
│   └── README_TEMPLATE.md
└── .github/
    └── workflows/
        ├── update-readme.yml
        └── validate.yml
```

## How I Add a New Problem

Step 1: create a solution file in the matching rating folder.

```bash
solutions/codeforces/<rating>/<contestId><index>_<Problem_Name>.cpp
```

Step 2: add a metadata block at the top.

```cpp
/*
Platform: Codeforces
Problem: Watermelon
Contest ID: 4
Index: A
Rating: 800
Tags: math, implementation
Solved Date: 2026-06-05
URL: https://codeforces.com/problemset/problem/4/A
*/
```

Step 3: regenerate the dashboard.

```bash
python scripts/validate_solution.py
python scripts/generate_stats.py
python scripts/generate_readme.py
```

Step 4: commit and push.

```bash
git add .
git commit -m "solve: add Codeforces 4A Watermelon"
git push
```

CLI shortcut:

```bash
python scripts/add_problem.py --platform Codeforces --contest 4 --index A --title "Watermelon" --rating 800 --tags "math,implementation" --language cpp --date 2026-06-05
```

## Roadmap

- Codeforces support
- LeetCode support
- AtCoder support
- CodeChef support
- GitHub Action auto-update
- Better SVG contribution calendar
- Personal CP analytics dashboard
- Public website version

## Extending Beyond Codeforces

{{EXTENSION_NOTES}}

## License

This project is licensed under the MIT License. See [LICENSE](LICENSE).

