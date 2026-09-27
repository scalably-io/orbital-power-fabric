import pytest

from opf import limits


def test_shot_noise_floor_values():
    assert limits.shot_noise_photons(5) == 1024
    assert limits.shot_noise_photons(8) == 65536
    # 8-bit at 1550 nm: 65,536 x 0.1282 aJ = 8.40 fJ per detection
    assert limits.shot_noise_detection_j(8) == pytest.approx(8.40e-15, rel=2e-3)


def test_capacitive_detection():
    # 1 fF swung by 1 V needs 1e-15 / 1.602e-19 = 6,242 photons -> 0.80 fJ at 1550 nm
    assert limits.capacitive_detection_j(1e-15, 1.0) == pytest.approx(0.800e-15, rel=2e-3)


def test_stack_reproduces_r3_105_components():
    s = limits.Stack(n=128, detect_j=limits.R3_PRACTICAL_DETECT_J, loss_db=20, wallplug=1.0,
                     dac_j=0.5e-12, tia_j=2.4e-12, adc_j=2.19e-12,
                     sram_j_per_mac=2 * 8 * 0.3e-12 / 128, fetch_j_per_mac=8 * 11.68e-12 / 64)
    t = s.per_mac()
    assert t["laser"] == pytest.approx(78.1e-15, rel=1e-2)
    assert t["dac"] == pytest.approx(3.9e-15, rel=1e-2)
    assert t["adc"] == pytest.approx(17.1e-15, rel=1e-2)
    assert t["tia"] == pytest.approx(18.75e-15, rel=1e-2)
    assert t["sram"] == pytest.approx(37.5e-15, rel=1e-2)
    assert t["memory"] == pytest.approx(1460e-15, rel=1e-3)


def test_time_integration_divides_readout_only():
    base = limits.Stack(n=64, detect_j=1e-15, loss_db=0, wallplug=1, adc_j=1e-12, tia_j=1e-12, dac_j=1e-12)
    integ = limits.Stack(n=64, detect_j=1e-15, loss_db=0, wallplug=1, adc_j=1e-12, tia_j=1e-12, dac_j=1e-12,
                         t_integrate=8)
    a, b = base.per_mac(), integ.per_mac()
    assert b["adc"] == pytest.approx(a["adc"] / 8) and b["tia"] == pytest.approx(a["tia"] / 8)
    # the precision target is on the integrated sum: photons per read are spread over T cycles too
    assert b["laser"] == pytest.approx(a["laser"] / 8)
    assert b["dac"] == a["dac"]


def test_sunlight_per_mode_brightness_bound():
    # Sun ~5772 K at 1550 nm: h nu = 0.80 eV, kT = 0.497 eV -> n ~ 0.25 photons per mode
    n = limits.thermal_occupancy(5772, 1550e-9)
    assert 0.24 < n < 0.26
    # one spatial mode, both polarisations, 1 THz optical bandwidth -> ~64 nW
    p = limits.thermal_mode_power_w(5772, 1550e-9, 1e12)
    assert 5e-8 < p < 8e-8


def test_time_integration_without_streamed_weights_is_flagged():
    # R8-129: integrating T cycles sums a length-(k*T) dot product -> weights must change every cycle
    bad = limits.Stack(n=64, detect_j=1e-15, loss_db=0, wallplug=1, t_integrate=8)
    ok = limits.Stack(n=64, detect_j=1e-15, loss_db=0, wallplug=1, t_integrate=8, weight_j=1.56e-12, weight_reuse=64)
    assert bad.issues() and not ok.issues()
    assert ok.per_mac()["weights"] == pytest.approx(1.56e-12 / 64)


def test_spatial_fan_in_amortises_like_time_integration():
    square = limits.Stack(n=128, detect_j=1e-15, loss_db=0, wallplug=1, adc_j=1e-12, t_integrate=1)
    wide = limits.Stack(n=128, k=4096, detect_j=1e-15, loss_db=0, wallplug=1, adc_j=1e-12, t_integrate=1)
    assert wide.per_mac()["adc"] == pytest.approx(square.per_mac()["adc"] * 128 / 4096)
    assert not wide.issues()


def test_laser_cannot_amortise_beyond_outputs_without_wdm():
    # D13 correction 3 (E028, Opus review): power conservation in a passive coherent k->n network
    wide = limits.Stack(n=128, k=4096, detect_j=1e-15, loss_db=0, wallplug=1)
    square = limits.Stack(n=128, detect_j=1e-15, loss_db=0, wallplug=1)
    wdm = limits.Stack(n=128, k=4096, detect_j=1e-15, loss_db=0, wallplug=1, wdm=True)
    assert wide.per_mac()["laser"] == pytest.approx(square.per_mac()["laser"])      # /n, not /k
    assert wdm.per_mac()["laser"] == pytest.approx(1e-15 / 4096)                     # k wavelengths


def test_dist_precision_photons_by_monte_carlo():
    # D21 (E032): at p = 9*4^b/256 photons per unit, the shot noise of a balanced read-out equals one LSB of
    # b bits spanning +/-4 sigma_y — checked by Poisson simulation, not by re-evaluating the formula
    import numpy as np
    rng = np.random.default_rng(21)
    k, bits, trials = 256, 5, 4000
    p = 2 * limits.dist_photons_per_mac(bits)            # photons per unit w*x on the active arm
    w = rng.uniform(-1, 1, (trials, k))
    x = rng.uniform(0, 1, (trials, k))
    y = (w * x).sum(axis=1)
    n_pos = rng.poisson(p * np.clip(w, 0, None) * x).sum(axis=1)
    n_neg = rng.poisson(p * np.clip(-w, 0, None) * x).sum(axis=1)
    noise = (n_pos - n_neg) / p - y
    lsb = 8 * np.sqrt(k / 9) / 2**bits
    assert np.std(noise) / lsb == pytest.approx(1.0, rel=0.05)
    assert limits.dist_photons_per_mac(5) == pytest.approx(18.0)
