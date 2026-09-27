"""Circular-orbit geometry: slant range, visibility, pass duration, eclipse.

First-order, spherical Earth, no Earth rotation in pass timing. Good enough to
bound duty factors; replace with propagated ground tracks for site-specific work.
"""
import math

from .constants import MU_EARTH, R_EARTH


def slant_range(altitude_m: float, elevation_deg: float) -> float:
    """Distance from a ground site to a satellite seen at `elevation_deg`."""
    e = math.radians(elevation_deg)
    r = R_EARTH + altitude_m
    return math.sqrt(r**2 - (R_EARTH * math.cos(e)) ** 2) - R_EARTH * math.sin(e)


def central_angle(altitude_m: float, min_elevation_deg: float) -> float:
    """Earth central angle (rad) of the visibility circle above `min_elevation_deg`."""
    e = math.radians(min_elevation_deg)
    return math.acos(R_EARTH * math.cos(e) / (R_EARTH + altitude_m)) - e


def visible_fraction(altitude_m: float, min_elevation_deg: float) -> float:
    """Fraction of Earth's surface that sees the satellite above the elevation mask.

    Equals the long-run fraction of time one randomly placed site sees one
    satellite whose ground track covers the globe uniformly.
    """
    lam = central_angle(altitude_m, min_elevation_deg)
    return (1.0 - math.cos(lam)) / 2.0


def fabric_visibility(altitude_m: float, min_elevation_deg: float, n_receivers: int,
                      placement: str = "random") -> float:
    """Fraction of time at least one of N receivers is in view (DERIVATIONS D03).

    placement="random":   receivers placed independently at random -> 1 - (1 - f)^N
    placement="disjoint": receivers spaced so visibility caps never overlap -> min(1, N f)
    (the best case for a fabric; real sites sit on land at particular latitudes).
    """
    f = visible_fraction(altitude_m, min_elevation_deg)
    if placement == "disjoint":
        return min(1.0, n_receivers * f)
    if placement != "random":
        raise ValueError(placement)
    return 1.0 - (1.0 - f) ** n_receivers


def period_s(altitude_m: float) -> float:
    a = R_EARTH + altitude_m
    return 2.0 * math.pi * math.sqrt(a**3 / MU_EARTH)


def max_pass_duration_s(altitude_m: float, min_elevation_deg: float) -> float:
    """Duration of an overhead pass above the elevation mask (Earth rotation ignored)."""
    lam = central_angle(altitude_m, min_elevation_deg)
    return period_s(altitude_m) * (2.0 * lam) / (2.0 * math.pi)


def eclipse_fraction(altitude_m: float, beta_deg: float) -> float:
    """Fraction of a circular orbit spent in Earth's (cylindrical) shadow.

    beta = angle between the orbit plane and the Sun vector. Standard result:
    f = (1/pi) * acos( sqrt(h^2 + 2 R h) / ((R + h) cos beta) ) for |beta| < beta*.
    """
    r = R_EARTH + altitude_m
    beta = math.radians(abs(beta_deg))
    beta_star = math.asin(R_EARTH / r)
    if beta >= beta_star:
        return 0.0
    arg = math.sqrt(altitude_m**2 + 2.0 * R_EARTH * altitude_m) / (r * math.cos(beta))
    return math.acos(min(1.0, arg)) / math.pi


def terminator_site_fraction(altitude_m: float, min_elevation_deg: float) -> float:
    """Share of the day an equatorial site is inside the visibility cap of a dawn-dusk (terminator-following)
    orbit, DERIVATIONS D22: the site rotates through the band of half-width lambda around the terminator twice a day."""
    return 4.0 * central_angle(altitude_m, min_elevation_deg) / (2.0 * math.pi)

