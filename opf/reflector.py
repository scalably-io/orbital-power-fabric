"""Branch C: passive orbital mirror -> ground PV.

The Sun is an extended source (~0.53 deg), so a flat mirror cannot make a spot
smaller than slant_range * sun_angle (plus the mirror's own size). This module
adds the three effects the handoff's first model left out:
  1. mirror tilt: the mirror normal bisects Sun and target, so it intercepts
     A*cos(incidence) of sunlight;
  2. off-nadir geometry: slant range grows and the beam hits the ground
     obliquely, stretching the footprint by 1/sin(elevation);
  3. airmass: clear-sky transmission falls with 1/sin(elevation).
Irradiance on the ground is reported so the low-light regime of PV is visible.
"""
import math

from . import orbit


def spot_diameter_m(slant_m: float, sun_angle_deg: float, mirror_diameter_m: float = 0.0) -> float:
    """Beam diameter perpendicular to the beam at distance `slant_m`."""
    return mirror_diameter_m + 2.0 * slant_m * math.tan(math.radians(sun_angle_deg) / 2.0)


def footprint_area_m2(altitude_m: float, elevation_deg: float, sun_angle_deg: float,
                      mirror_diameter_m: float = 0.0) -> float:
    """Ground footprint (ellipse) of the solar image seen at `elevation_deg`."""
    d = orbit.slant_range(altitude_m, elevation_deg)
    minor = spot_diameter_m(d, sun_angle_deg, mirror_diameter_m)
    major = minor / math.sin(math.radians(elevation_deg))
    return math.pi / 4.0 * minor * major


def incidence_deg(sun_target_angle_deg: float) -> float:
    """Incidence on the mirror when Sun and target are `sun_target_angle_deg` apart as seen from it."""
    return sun_target_angle_deg / 2.0


def transmission(zenith_transmission: float, elevation_deg: float, airmass: bool = True) -> float:
    if not airmass:
        return zenith_transmission
    return zenith_transmission ** (1.0 / math.sin(math.radians(elevation_deg)))


def optical_w_per_m2_mirror(solar_w_m2: float, reflectivity: float, incidence: float,
                            atm_transmission: float) -> float:
    """Sunlight power reaching the ground per m² of mirror."""
    return solar_w_m2 * reflectivity * math.cos(math.radians(incidence)) * atm_transmission


def ground_irradiance_w_m2(mirror_area_m2: float, optical_per_m2: float, footprint_m2: float) -> float:
    """Mean added irradiance inside the footprint (uniform-disk approximation)."""
    return mirror_area_m2 * optical_per_m2 / footprint_m2


def capture_fraction(receiver_m2: float, footprint_m2: float) -> float:
    """First-order share of the footprint's energy landing on the receiver."""
    return min(1.0, receiver_m2 / footprint_m2)


def mirror_area_for_load(load_w: float, optical_per_m2: float, ground_pv_eff: float,
                         capture: float) -> float:
    """Mirror area needed so the receiver's PV output equals `load_w`."""
    return load_w / (optical_per_m2 * ground_pv_eff * capture)


def mirror_area_for_irradiance(target_w_m2: float, optical_per_m2: float, footprint_m2: float) -> float:
    """Mirror area needed to raise the whole footprint by `target_w_m2`."""
    return target_w_m2 * footprint_m2 / optical_per_m2
