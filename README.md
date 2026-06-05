# CP & DSA Streak Tracker

![Total Solved](https://img.shields.io/badge/Total%20Solved-34-2563eb?style=for-the-badge)
![Current Streak](https://img.shields.io/badge/Current%20Streak-5%20days-16a34a?style=for-the-badge)
![Longest Streak](https://img.shields.io/badge/Longest%20Streak-8%20days-f59e0b?style=for-the-badge)
![Codeforces Rating](https://img.shields.io/badge/Codeforces%20Rating-734-dc2626?style=for-the-badge)
![Last Updated](https://img.shields.io/badge/Last%20Updated-2026--06--05-4b5563?style=for-the-badge)

A clean dashboard to track my competitive programming, DSA practice, Codeforces progress, topic-wise growth, rating-wise progress, and daily consistency.

> Generated from `templates/README_TEMPLATE.md`. Edit the template, then run `python scripts/generate_readme.py`.

## About

I am **Abhijeet Ranjan**, practicing competitive programming and DSA with a Codeforces-first workflow. My current goal is: **Become strong in CP, DSA, DevOps and Open Source**.

## My Coding Profiles

| Platform | Handle | Link |
| --- | --- | --- |
| GitHub | Abhi190702 | [Profile](https://github.com/Abhi190702) |
| Codeforces | ZAck19_0 | [Profile](https://codeforces.com/profile/ZAck19_0) |

## Progress Dashboard

| Metric | Value |
| --- | --- |
| Total solved | 34 |
| Current streak | 5 day(s) |
| Longest streak | 8 day(s) |
| Platforms tracked | 1 |
| Codeforces handle | ZAck19_0 |
| Codeforces rating | 734 |
| Last updated | 2026-06-05T06:33:45Z |

## Current Streak

Current streak: **5 day(s)**. Longest streak so far: **8 day(s)**.

## Total Problems Solved

Total logged problems: **34**. Latest active month: **2026-06** with **5** solved problem(s).

## Topic-wise Distribution

![Topic-wise distribution](assets/graphs/topic_distribution.svg)

| Topic | Solved |
| --- | --- |
| greedy | 21 |
| math | 19 |
| implementation | 18 |
| number theory | 7 |
| brute force | 6 |
| sortings | 4 |
| strings | 4 |
| games | 2 |
| binary search | 1 |
| constructive algorithms | 1 |
| dp | 1 |

## Rating-wise Distribution

![Rating-wise distribution](assets/graphs/rating_distribution.svg)

| Rating | Solved |
| --- | --- |
| 800 | 27 |
| 900 | 3 |
| 1000 | 1 |
| 1100 | 2 |
| 1200 | 1 |

## Platform Distribution

![Platform distribution](assets/graphs/platform_distribution.svg)

| Platform | Solved |
| --- | --- |
| Codeforces | 34 |

## Daily Activity Graph

![Daily activity graph](assets/graphs/daily_activity.svg)

## Streak Calendar

![Streak calendar](assets/graphs/streak_calendar.svg)

## Latest Solved Problems

| Date | Platform | Problem | Rating | Topics | Solution |
| --- | --- | --- | --- | --- | --- |
| 2026-06-05 | Codeforces | [Domino piling](https://codeforces.com/problemset/problem/50/A) | 800 | math, greedy | [cpp](solutions/codeforces/800/50A_Domino_piling.cpp) |
| 2026-06-04 | Codeforces | [Next Round](https://codeforces.com/problemset/problem/158/A) | 800 | implementation | [cpp](solutions/codeforces/800/158A_Next_Round.cpp) |
| 2026-06-03 | Codeforces | [Team](https://codeforces.com/problemset/problem/231/A) | 800 | implementation | [cpp](solutions/codeforces/800/231A_Team.cpp) |
| 2026-06-02 | Codeforces | [Way Too Long Words](https://codeforces.com/problemset/problem/71/A) | 800 | strings, implementation | [cpp](solutions/codeforces/800/71A_Way_Too_Long_Words.cpp) |
| 2026-06-01 | Codeforces | [Watermelon](https://codeforces.com/problemset/problem/4/A) | 800 | math, implementation | [cpp](solutions/codeforces/800/4A_Watermelon.cpp) |
| 2025-12-26 | Codeforces | [Stock Arbitraging](https://codeforces.com/problemset/problem/1150/A) | 800 | greedy, implementation | Imported |
| 2025-12-23 | Codeforces | [Blackslex and Password](https://codeforces.com/problemset/problem/2179/A) | 800 | math, strings | Imported |
| 2025-12-23 | Codeforces | [Blackslex and Showering](https://codeforces.com/problemset/problem/2179/B) | 800 | dp, greedy, implementation | Imported |
| 2025-12-23 | Codeforces | [Blackslex and Number Theory](https://codeforces.com/problemset/problem/2179/C) | 1100 | implementation, math, number theory, sortings | Imported |
| 2025-12-22 | Codeforces | [Neko Finds Grapes](https://codeforces.com/problemset/problem/1152/A) | 800 | greedy, implementation, math | Imported |

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

The data model already stores `platform`, `tags`, `rating`, `solutionPath`, and `solvedDate`, so new platforms can reuse the same dashboard. For LeetCode or AtCoder, add a platform folder under `solutions/`, create a fetcher only if the API is reliable, and keep manual JSON entry as the fallback path.

## License

This project is licensed under the MIT License. See [LICENSE](LICENSE).

