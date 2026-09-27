"""Single-parameter break-even: where does a comparison flip sign?"""
from typing import Callable


def flip_value(diff: Callable[[float], float], lo: float, hi: float,
               tol: float = 1e-9, max_iter: int = 200) -> float | None:
    """Value x in [lo, hi] where diff(x) changes sign (bisection).

    `diff` is usually metric_option(x) - metric_rival(x). Returns None when
    there is no sign change in the interval — i.e. no flip in the swept range,
    which is itself a result worth publishing.
    """
    f_lo, f_hi = diff(lo), diff(hi)
    if f_lo == 0:
        return lo
    if f_hi == 0:
        return hi
    if (f_lo > 0) == (f_hi > 0):
        return None
    for _ in range(max_iter):
        mid = (lo + hi) / 2.0
        f_mid = diff(mid)
        if abs(hi - lo) < tol * max(1.0, abs(mid)):
            return mid
        if (f_mid > 0) == (f_lo > 0):
            lo, f_lo = mid, f_mid
        else:
            hi = mid
    return (lo + hi) / 2.0
