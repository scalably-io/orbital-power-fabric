import numpy as np
import pytest

from opf import mesh


def test_layout_counts_match_clements():
    for n in (2, 4, 8):
        assert len(mesh.layout(n)) == n * (n - 1) // 2
    assert mesh.layout(4) == [(0, 0), (0, 2), (1, 1), (2, 0), (2, 2), (3, 1)]


def test_mzi_is_unitary_and_switches():
    for th, ph in [(0.3, 1.1), (np.pi, 0.0), (0.0, 2.0)]:
        t = mesh.mzi(th, ph)
        assert np.allclose(t.conj().T @ t, np.eye(2))
    # theta = pi -> bar state, theta = 0 -> cross state (ideal couplers)
    assert abs(mesh.mzi(np.pi, 0)[0, 0]) == pytest.approx(1.0)
    assert abs(mesh.mzi(0.0, 0)[1, 0]) == pytest.approx(1.0)


def test_mesh_programs_random_unitaries():
    rng = np.random.default_rng(7)
    for n in (4,):
        for _ in range(3):
            u = mesh.random_unitary(n, rng)
            phases, f = mesh.program(u, rng)
            assert f > 1 - 1e-8
            assert np.allclose(mesh.unitary(n, phases), u, atol=1e-5)


def test_loss_scales_power():
    rng = np.random.default_rng(1)
    p = rng.uniform(0, 2 * np.pi, mesh.n_phases(4))
    u = mesh.unitary(4, p, loss_db_per_mzi=0.5)
    col_power = np.sum(abs(u) ** 2, axis=0)
    assert np.all(col_power < 1.0) and np.all(col_power > 10 ** (-0.5 * 4 / 10) - 1e-9)


def test_heater_power_linear_in_phase():
    assert mesh.heater_power_w(np.array([np.pi, 2 * np.pi, np.pi / 2]), 0.02, 1, True) == pytest.approx(
        0.02 * (1 + 0 + 0.5))


def test_chip_layout_bottom_heaters_still_universal():
    rng = np.random.default_rng(11)
    u = mesh.random_unitary(4, rng)
    phases, f = mesh.program(u, rng, chip_layout=True)
    assert f > 1 - 1e-8
    assert not np.allclose(mesh.unitary(4, phases, chip_layout=True), mesh.unitary(4, phases))


def test_power_only_measurement_cannot_certify_complex_fidelity():
    # Codex review (E028): two unitaries with identical |U|^2 but different phases
    import numpy as np
    from opf import mesh
    rng = np.random.default_rng(7)
    u = mesh.random_unitary(4, rng)
    d = np.diag(np.exp(1j * rng.uniform(0, 2 * np.pi, 4)))
    v = d @ u @ np.diag(np.exp(1j * rng.uniform(0, 2 * np.pi, 4)))   # same |U|^2, different matrix
    assert np.allclose(np.abs(u) ** 2, np.abs(v) ** 2)
    assert mesh.power_fidelity(u, v) == 1.0 or abs(mesh.power_fidelity(u, v) - 1.0) < 1e-12
    assert mesh.fidelity(u, v) < 0.99
    assert abs(mesh.power_fidelity(u, u) - 1.0) < 1e-12
