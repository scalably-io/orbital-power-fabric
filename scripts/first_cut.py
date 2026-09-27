#!/usr/bin/env python3
"""EXPLORATORY first cut (E004) — handoff-seeded values + labelled assumptions.

Not the verdict: the verdict uses merged, sourced values (docs/PREREGISTRATION.md).
B is deliberately a LOWER BOUND (PV mass only: no transmitter, structure or bus),
so if B loses here it loses everywhere at this tier.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from opf import lifecycle, orbit, power_chain, reflector
from opf.params import h as v  # E004 is handoff-seeded by design

L = 15                     # lifecycle years
ALT, MASK = 625e3, 30.0    # handoff reflector altitude; ASSUMPTION: 30 deg elevation mask
chain = power_chain.RFChain(v("pv_eff"), v("dc_dc_space"), v("dc_rf"), v("antenna"), v("atmosphere_rf"),
                            v("beam_capture"), v("rectenna"), v("dc_dc_ground"))

a = lifecycle.OrbitalCompute(kw_per_tonne=v("orbital_compute_kw_per_tonne"),
                             gpu_refresh_years=5, vehicle_life_years=5)  # ASSUMPTION pending R1 (10-K lives)
print(f"A orbital GPU (75 kW/t vendor-stated, 5 y service): {a.kg_per_kw():6.1f} kg/kW once, "
      f"{a.lifecycle_kg_per_kw(L):6.1f} kg/kW over {L} y")

print("\nB lower bound (PV only, 140 W/kg = top of handoff range, dawn-dusk sunlit=1, 15 y life, PUE 1.15):")
for n in (1, 10, 100, 1000):
    duty = orbit.fabric_visibility(ALT, MASK, n)
    b = lifecycle.PowerBeaming(chain, pv_w_per_kg=140, tx_w_per_kg=1e12, structure_fraction=0.0,
                               link_duty=duty, sunlit_fraction=1.0, vehicle_life_years=15, pue=v("pue"))
    print(f"  receivers={n:5d} duty={duty:6.3f}  {b.kg_per_kw():9.1f} kg/kW  lifecycle {b.lifecycle_kg_per_kw(L):9.1f}")

print("\nC mirror, overhead-only best case vs realistic geometry (ground PV at full-sun efficiency = optimistic):")
flat = reflector.optical_w_per_m2_mirror(v("solar_constant"), v("mirror_reflectivity"), 0.0, v("atm_clear_zenith"))
tilt = reflector.optical_w_per_m2_mirror(v("solar_constant"), v("mirror_reflectivity"), 45.0,
                                         reflector.transmission(v("atm_clear_zenith"), 45.0))
fp90 = reflector.footprint_area_m2(ALT, 90, v("sun_angle"))
for label, opt in (("flat, overhead (handoff)", flat), ("45 deg tilt, 45 deg elev airmass", tilt)):
    for kgm2 in (0.01, 0.05):   # ASSUMPTION sweep pending R1 (ACS3 areal density)
        c = lifecycle.MirrorFabric(opt, v("ground_pv_eff"), 1.0, orbit.fabric_visibility(ALT, MASK, 100),
                                   1.0, kgm2, 5, v("pue"))
        print(f"  {label:34s} {kgm2:5.2f} kg/m2  100 rx: {c.kg_per_kw():8.1f} kg/kW  lifecycle {c.lifecycle_kg_per_kw(L):8.1f}")

m = reflector.mirror_area_for_load(v("rack_kw") * v("pue") * 1000, flat, v("ground_pv_eff"), 1.0)
e = reflector.ground_irradiance_w_m2(m, flat, fp90)
print(f"\nC low-light check: handoff's {m:.0f} m2 mirror adds {e:.4f} W/m2 over {fp90/1e6:.1f} km2 "
      f"= {e/1000:.1e} of full sun")
for target in (10, 100):
    print(f"  mirror area to add {target} W/m2 over the overhead footprint: "
          f"{reflector.mirror_area_for_irradiance(target, flat, fp90)/1e6:.2f} km2")

print("\nB at GEO (continuous view, no receiver fabric needed) - aperture physics only:")
from opf import microwave
from opf.constants import GEO_ALTITUDE
import math
for f_ghz in (2.45, 5.8):
    lam = microwave.wavelength_m(f_ghz * 1e9)
    for d_tx in (500.0, 1000.0, 2000.0):
        tx = math.pi / 4 * d_tx**2
        rx = microwave.rx_area_for_efficiency(0.95, tx, lam, GEO_ALTITUDE)
        print(f"  {f_ghz:4.2f} GHz  tx {d_tx:6.0f} m  -> rectenna {rx/1e6:7.1f} km2 for 95% capture "
              f"(diameter {2*math.sqrt(rx/math.pi)/1000:5.1f} km)")
print(f"  GEO equinox eclipse: {orbit.eclipse_fraction(GEO_ALTITUDE, 0)*24*60:.0f} min/day max (cylindrical shadow)")
