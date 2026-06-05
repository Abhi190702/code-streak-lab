/*
Platform: Codeforces
Problem: Team
Contest ID: 231
Index: A
Rating: 800
Tags: implementation
Solved Date: 2026-06-03
URL: https://codeforces.com/problemset/problem/231/A
*/

#include <bits/stdc++.h>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n;
    cin >> n;

    int solved = 0;
    while (n--) {
        int petya, vasya, tonya;
        cin >> petya >> vasya >> tonya;
        solved += (petya + vasya + tonya >= 2);
    }

    cout << solved;
    return 0;
}

