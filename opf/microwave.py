"""Microwave/laser beam sizing.

Airy first-null (uniform circular aperture): diameter = 2.44 * lambda * L / D.
Collection efficiency between two apertures uses the Goubau parameter
tau = sqrt(A_t * A_r) / (lambda * L); for optimally tapered (near-Gaussian)
illumination the transmittable fraction is approximately 1 - exp(-tau^2).
"""
import math

from .constants import C


def wavelength_m(frequency_hz: float) -> float:
    return C / frequency_hz


def airy_first_null_diameter_m(wavelength: float, distance_m: float, aperture_m: float) -> float:
    return 2.44 * wavelength * distance_m / aperture_m


def goubau_tau(tx_area_m2: float, rx_area_m2: float, wavelength: float, distance_m: float) -> float:
    return math.sqrt(tx_area_m2 * rx_area_m2) / (wavelength * distance_m)


def collection_efficiency(tau: float) -> float:
    return 1.0 - math.exp(-tau**2)


def rx_area_for_efficiency(eta: float, tx_area_m2: float, wavelength: float, distance_m: float) -> float:
    """Receiver area needed for collection efficiency `eta` given the transmit aperture."""
    tau = math.sqrt(-math.log(1.0 - eta))
    return (tau * wavelength * distance_m) ** 2 / tx_area_m2
