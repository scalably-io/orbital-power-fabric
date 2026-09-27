"""Radiator floor: q = eps * sigma * (T^4 - T_sink^4) per radiating side."""
from .constants import SIGMA


def radiative_flux_w_m2(emissivity: float, temp_k: float, sink_k: float = 0.0) -> float:
    return emissivity * SIGMA * (temp_k**4 - sink_k**4)


def radiator_area_m2(heat_w: float, emissivity: float, temp_k: float,
                     sink_k: float = 0.0, sides: int = 1) -> float:
    """Ideal radiator area. A hard floor, not a design: view factors, gradients
    and structure only make the real radiator larger."""
    return heat_w / (sides * radiative_flux_w_m2(emissivity, temp_k, sink_k))
