# Contributing

This repository is designed for daily competitive programming practice. Keep each solution small, traceable, and easy to scan later.

## Add a Codeforces Solution

1. Create the solution file under the rating folder:

```bash
solutions/codeforces/<rating>/<contestId><index>_<Problem_Name>.cpp
```

2. Add the metadata block at the top:

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

3. Run the local checks:

```bash
python scripts/validate_solution.py
python scripts/generate_stats.py
python scripts/generate_readme.py
```

4. Commit the update:

```bash
git add .
git commit -m "solve: add Codeforces 4A Watermelon"
git push
```

## Use the CLI Helper

```bash
python scripts/add_problem.py --platform Codeforces --contest 4 --index A --title "Watermelon" --rating 800 --tags "math,implementation" --language cpp --date 2026-06-05
```

The helper creates the solution file, writes a metadata template, and adds the entry to `data/solved.json` without duplicating existing problems.

## Metadata Rules

Every solution file must include:

- `Platform`
- `Problem`
- `Contest ID`
- `Index`
- `Rating`
- `Tags`
- `Solved Date`
- `URL`

The validation workflow fails if required metadata is missing.

## Extending to Other Platforms

Add one platform at a time:

- Create a new folder under `solutions/`.
- Add a fetcher script only if the platform has a stable public API.
- Reuse the same `data/solved.json` schema.
- Update `scripts/add_problem.py` and `scripts/generate_stats.py` only when the schema needs a new field.
- Keep manual entry working even when platform APIs are unavailable.

