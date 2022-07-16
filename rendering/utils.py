from __future__ import annotations


def approx(a: float, b: float, eps=1e-7):
    return abs(a - b) < eps
