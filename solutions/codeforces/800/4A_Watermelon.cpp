/*
Platform: Codeforces
Problem: Watermelon
Contest ID: 4
Index: A
Rating: 800
Tags: math, implementation
Solved Date: 2026-06-01
URL: https://codeforces.com/problemset/problem/4/A
*/

#include <bits/stdc++.h>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int w;
    cin >> w;

    cout << (w > 2 && w % 2 == 0 ? "YES" : "NO");
    return 0;
}

