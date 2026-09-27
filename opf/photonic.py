"""Photonic compute energy accounting (branches D/E).

Optical-core energy per MAC is NOT system energy. For an N x N matrix-vector
multiply per cycle: N inputs are encoded (DAC + modulator), N outputs are read
(photodetector + ADC), N^2 MACs happen optically, and weights must be loaded
and held. Per-MAC system energy therefore amortises the O(N) terms over N.
"""
from dataclasses import dataclass

from .constants import C, H


def photon_energy_j(wavelength_m: float) -> float:
    return H * C / wavelength_m


def photons_per_mac(energy_per_mac_j: float, wavelength_m: float) -> float:
    return energy_per_mac_j / photon_energy_j(wavelength_m)


def heat_w(energy_per_op_j: float, ops_per_s: float) -> float:
    return energy_per_op_j * ops_per_s


@dataclass(frozen=True)
class MVMEnergy:
    """Per-cycle energy terms for one N x N optical matrix-vector multiply (joules)."""
    n: int
    optical_per_mac_at_detector: float   # optical energy needed at the detectors, per MAC
    laser_wall_plug_eff: float           # electrical -> optical
    dac_per_input: float
    modulator_per_input: float
    detector_per_output: float
    adc_per_output: float
    weight_hold_per_cycle: float = 0.0   # thermo-optic hold power x cycle time, total
    memory_per_cycle: float = 0.0        # activations/weights moved per cycle, total
    control_per_cycle: float = 0.0       # calibration, feedback, clocking, total

    def per_mac(self) -> dict:
        macs = self.n * self.n
        terms = {
            "laser": self.optical_per_mac_at_detector / self.laser_wall_plug_eff,
            "dac": self.dac_per_input * self.n / macs,
            "modulator": self.modulator_per_input * self.n / macs,
            "detector": self.detector_per_output * self.n / macs,
            "adc": self.adc_per_output * self.n / macs,
            "weight_hold": self.weight_hold_per_cycle / macs,
            "memory": self.memory_per_cycle / macs,
            "control": self.control_per_cycle / macs,
        }
        terms["total"] = sum(terms.values())
        return terms
