/*
Platform: Codeforces
Problem: Next Round
Contest ID: 158
Index: A
Rating: 800
Tags: implementation
Solved Date: 2026-06-04
URL: https://codeforces.com/problemset/problem/158/A
*/

#include <bits/stdc++.h>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n, k;
    cin >> n >> k;

    vector<int> scores(n);
    for (int &score : scores) {
        cin >> score;
    }

    int advanced = 0;
    for (int score : scores) {
        if (score > 0 && score >= scores[k - 1]) {
            advanced++;
        }
    }

    cout << advanced;
    return 0;
}

