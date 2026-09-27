"""Energy per MAC for an N x N photonic matrix-vector engine, term by term, down to the physics floor.

Per cycle an N x N crossbar does N^2 MACs, encodes N inputs (DAC + modulator)
and reads N outputs (detector + TIA + ADC). Each output detection must carry
enough photons for the target precision; the laser supplies that through the
chip loss at its wall-plug efficiency. Levers modelled:
  T  (time integration): the detector/integrator accumulates T cycles before one
     TIA/ADC read, so read-out energy is shared by N*T MACs; the precision target
     applies to the integrated sum, so the photons needed per read are ALSO spread
     over T cycles (laser / T) — DERIVATIONS D13 (corrected 2026-09-27, E015);
  direct O-E-O: a detector drives the next layer's modulator, removing the DAC;
  non-volatile weights: no hold power;
  weight reuse (batch / prefill): memory fetch divided across reused tokens.
Shot-noise floor: resolving b bits needs sigma <= full-scale / 2^b, i.e.
N_photons >= 4^b / QE (Poisson, ideal detector). Physics only — every
other term's value must come from evidence/claims.csv.
"""
from dataclasses import dataclass

from .constants import C, H

E_CHARGE = 1.602176634e-19  # C (exact)
K_B = 1.380649e-23          # J/K (exact)


def photon_energy_j(wavelength_m: float) -> float:
    return H * C / wavelength_m


def shot_noise_photons(bits: int, qe: float = 1.0) -> float:
    return 4.0**bits / qe


def shot_noise_detection_j(bits: int, wavelength_m: float = 1550e-9, qe: float = 1.0) -> float:
    return shot_noise_photons(bits, qe) * photon_energy_j(wavelength_m)


def capacitive_detection_j(capacitance_f: float, swing_v: float, wavelength_m: float = 1550e-9,
                           qe: float = 1.0) -> float:
    """Optical energy to swing a detector node of capacitance C by V directly (no amplifier)."""
    return capacitance_f * swing_v / (E_CHARGE * qe) * photon_energy_j(wavelength_m)


def dist_photons_per_mac(bits: int) -> float:
    """Photons that must reach the weight elements per MAC for `bits` of precision over the OUTPUT
    DISTRIBUTION (D21): inputs x ~ U[0,1], weights w ~ U[-1,1] as transmissions on the +/- arm of a
    balanced detector pair, shot noise <= 1 LSB of b bits spanning +/-4 sigma_y. Independent of fan-in."""
    return 9.0 * 4.0**bits / 512.0


@dataclass(frozen=True)
class Stack:
    n: int                        # fan-out: outputs sharing each input encoding (matrix rows)
    detect_j: float               # optical energy needed per output detection at the detector
    loss_db: float                # optical loss laser -> detector
    wallplug: float               # laser electrical -> optical
    dac_j: float = 0.0            # per input sample
    mod_j: float = 0.0            # per input sample
    tia_j: float = 0.0            # per output read
    adc_j: float = 0.0            # per output read
    t_integrate: int = 1          # cycles accumulated per read
    hold_j_per_mac: float = 0.0   # weight hold (thermo-optic) per MAC
    sram_j_per_mac: float = 0.0
    fetch_j_per_mac: float = 0.0  # weight fetch from memory per MAC
    k: int | None = None          # fan-in: MACs summed onto one detector per cycle (default = n, square crossbar)
    weight_j: float = 0.0         # energy to encode one streamed weight symbol (DAC + modulator), D19
    weight_reuse: float = 1.0     # input vectors sharing each streamed weight symbol (batch / broadcast)
    wdm: bool = False             # inputs on k distinct wavelengths, summed incoherently per detector (D13 corr. 3)

    def issues(self) -> list[str]:
        """Physical inconsistencies (R8-129): time integration sums a length-(k*T) dot product, so the
        weights must change every cycle -> streamed weights must be paid for."""
        out = []
        if self.t_integrate > 1 and self.weight_j == 0.0:
            out.append("t_integrate > 1 needs a new weight every cycle: set weight_j (streamed weights)")
        return out

    def per_mac(self) -> dict:
        n, t = self.n, self.t_integrate
        k = self.k if self.k is not None else n
        # D13 correction 3 (E028): a passive single-wavelength k->n network delivers on average <= n/k of its
        # input power to the n outputs, so the laser amortises over min(n, k); only k distinct wavelengths
        # (WDM, incoherent sum on one detector) let it amortise over the full fan-in k.
        k_laser = k if self.wdm else min(n, k)
        terms = {
            "laser": self.detect_j * 10 ** (self.loss_db / 10) / self.wallplug / (k_laser * t),
            "dac": self.dac_j / n,
            "modulator": self.mod_j / n,
            "weights": self.weight_j / self.weight_reuse,
            "tia": self.tia_j / (k * t),
            "adc": self.adc_j / (k * t),
            "weight_hold": self.hold_j_per_mac,
            "sram": self.sram_j_per_mac,
            "memory": self.fetch_j_per_mac,
        }
        terms["total"] = sum(terms.values())
        return terms


# R3-037 practical rule: laser = 10^(2 + 0.1 * loss_dB) / N fJ per MAC (NEP-limited Ge detector,
# 10 GS/s, 5-bit). In Stack terms that is detect_j = 100 fJ per output read with wallplug = 1
# (the rule's own normalisation; DERIVED). It reproduces R3-105's 78 fJ/MAC at N = 128, 20 dB.
R3_PRACTICAL_DETECT_J = 1e-13


def thermal_occupancy(temp_k: float, wavelength_m: float) -> float:
    """Mean photon number per mode of blackbody radiation (Bose-Einstein), DERIVATIONS D18."""
    import math
    return 1.0 / math.expm1(photon_energy_j(wavelength_m) / (K_B * temp_k))


def thermal_mode_power_w(temp_k: float, wavelength_m: float, bandwidth_hz: float,
                         polarizations: int = 2) -> float:
    """Power a single spatial mode can collect from a blackbody that fills its field of view (D18).

    Brightness (etendue) conservation: no passive optics can put more than n*h*nu*dnu per
    polarization into one spatial mode, whatever the collecting area.
    """
    return polarizations * thermal_occupancy(temp_k, wavelength_m) * photon_energy_j(wavelength_m) * bandwidth_hz
