"""Clements-layout MZI mesh: forward model, programming, heater power.

Physical MZI (as laid out on chip): external phase phi on the top input arm,
50:50 coupler, internal phase theta on the top arm, 50:50 coupler:
    T(theta, phi) = B(r) @ diag(e^{i theta}, 1) @ B(r) @ diag(e^{i phi}, 1)
    B(r) = [[sqrt(r), i sqrt(1-r)], [i sqrt(1-r), sqrt(r)]]   (r = 0.5 ideal)
Clements rectangular arrangement: N columns; column c holds MZIs on mode
pairs (m, m+1) for m = c % 2, c % 2 + 2, ... -> N(N-1)/2 MZIs.
An output phase screen (N phases) completes an arbitrary unitary.

Programming uses least squares on the phases (exact for an ideal mesh, and the
same code fits a mesh with measured imperfections, which is what the test chip
calibration will need). Thermo-optic heater power is linear in phase:
P = (phase mod 2 pi) / pi * P_pi.
"""
import numpy as np
from scipy.optimize import least_squares


def coupler(r: float = 0.5) -> np.ndarray:
    t, k = np.sqrt(r), 1j * np.sqrt(1.0 - r)
    return np.array([[t, k], [k, t]])


def mzi(theta: float, phi: float, r1: float = 0.5, r2: float = 0.5, bottom: bool = False) -> np.ndarray:
    """bottom=True: both heaters on the lower arm (as laid out for the m = 0 pair on the chip)."""
    ph = (lambda a: np.diag([1.0, np.exp(1j * a)])) if bottom else (lambda a: np.diag([np.exp(1j * a), 1.0]))
    return coupler(r2) @ ph(theta) @ coupler(r1) @ ph(phi)


def layout(n: int) -> list[tuple[int, int]]:
    """(column, top mode) for every MZI, in light-propagation order."""
    return [(c, m) for c in range(n) for m in range(c % 2, n - 1, 2)]


def n_phases(n: int) -> int:
    return 2 * len(layout(n)) + n


def unitary(n: int, phases: np.ndarray, splits: np.ndarray | None = None,
            loss_db_per_mzi: float = 0.0, chip_layout: bool = False) -> np.ndarray:
    """Transfer matrix of the mesh. phases = [theta, phi] per MZI, then N output phases.

    splits: optional (n_mzi, 2) coupler ratios (fabrication imbalance).
    chip_layout: heaters of m = 0 MZIs sit on the bottom arm (chip/mesh_cells.py).
    """
    cells = layout(n)
    u = np.eye(n, dtype=complex)
    amp = 10 ** (-loss_db_per_mzi / 20.0)
    for k, (_, m) in enumerate(cells):
        theta, phi = phases[2 * k], phases[2 * k + 1]
        r1, r2 = (0.5, 0.5) if splits is None else splits[k]
        t = np.eye(n, dtype=complex)
        t[m:m + 2, m:m + 2] = amp * mzi(theta, phi, r1, r2, bottom=chip_layout and m == 0)
        u = t @ u
    out = phases[2 * len(cells):]
    return np.diag(np.exp(1j * out)) @ u


def random_unitary(n: int, rng: np.random.Generator) -> np.ndarray:
    """Haar-random unitary (QR of a complex Ginibre matrix with phase fix)."""
    z = (rng.standard_normal((n, n)) + 1j * rng.standard_normal((n, n))) / np.sqrt(2)
    q, r = np.linalg.qr(z)
    return q * (np.diag(r) / np.abs(np.diag(r)))


def fidelity(u: np.ndarray, v: np.ndarray) -> float:
    """|Tr(U^dagger V)| / N — 1.0 means identical up to a global phase."""
    return float(abs(np.trace(u.conj().T @ v)) / u.shape[0])


def power_fidelity(u: np.ndarray, v: np.ndarray) -> float:
    """What a power-only (intensity) measurement can check: mean over input ports of the classical
    fidelity sum_i sqrt(|u_ij|^2 |v_ij|^2). 1.0 for equal |U|^2 even when phases differ, so it cannot
    certify `fidelity` (complex); that needs a phase-sensitive measurement (E028)."""
    pu, pv = np.abs(u) ** 2, np.abs(v) ** 2
    pu, pv = pu / pu.sum(axis=0), pv / pv.sum(axis=0)
    return float(np.mean(np.sqrt(pu * pv).sum(axis=0)))


def program(target: np.ndarray, rng: np.random.Generator, restarts: int = 20,
            splits: np.ndarray | None = None, chip_layout: bool = False) -> tuple[np.ndarray, float]:
    """Phases that realise `target` on the (possibly imperfect) mesh. Returns (phases, fidelity)."""
    n = target.shape[0]

    def resid(p):
        d = unitary(n, p, splits, chip_layout=chip_layout) - target
        return np.concatenate([d.real.ravel(), d.imag.ravel()])

    best, best_f = None, -1.0
    for _ in range(restarts):
        p0 = rng.uniform(0, 2 * np.pi, n_phases(n))
        sol = least_squares(resid, p0, xtol=1e-12, ftol=1e-12, gtol=1e-12)
        f = fidelity(unitary(n, sol.x, splits, chip_layout=chip_layout), target)
        if f > best_f:
            best, best_f = sol.x, f
        if best_f > 1 - 1e-10:
            break
    return np.mod(best, 2 * np.pi), best_f


def heater_power_w(phases: np.ndarray, p_pi_w: float, n: int, include_output: bool = True) -> float:
    """Static thermo-optic power to hold `phases` (each wrapped to [0, 2 pi))."""
    p = np.mod(phases, 2 * np.pi)
    if not include_output:
        p = p[: 2 * len(layout(n))]
    return float(np.sum(p / np.pi) * p_pi_w)
