#!/usr/bin/env python3
"""OPF-MZI4 v0.1 — 4x4 Clements MZI mesh test chip for CORNERSTONE 220 nm SOI passive + heaters.

Die 5.5 x 4.9 mm (MPW #50 small block). Built only from unmodified cspdk cells
(MIT) arranged by chip/mesh_cells.py. Output: chip/gds/opf_mzi4_v0.1.gds + PNG.

Floorplan (um, origin lower-left):
  west edge  : grating-coupler array, 127 um pitch — 2 loopback + 4 mesh inputs
  east edge  : grating-coupler array, 127 um pitch — 4 mesh outputs + 2 loopback
  centre     : 4x4 Clements mesh (12 heaters), modes at 80 um pitch
  north edge : 16 pads (8 top-arm heaters x 2 contacts)
  south edge : 8 mesh pads (4 bottom-arm heaters x 2) + 4 pads for the calibration MZI
  lower band : standalone calibration MZI with its own grating couplers
Run: .venv/bin/python chip/opf_mzi4.py
"""
import sys
from pathlib import Path

import gdsfactory as gf

sys.path.insert(0, str(Path(__file__).resolve().parent))
from mesh_cells import PITCH, clements_mesh, mzi_unit  # noqa: E402

DIE = (5500.0, 4900.0)
EDGE = 100.0             # keep-out from die edge (um)
GC_PITCH = 127.0         # standard fibre-array pitch
PAD_PITCH = 150.0
PAD = 90.0
MESH_Y = 2330.0          # y of mode 0
CAL_Y = 1200.0           # y of the calibration MZI bottom mode
VERSION = "OPF-MZI4 v0.1 2026-09-27 CERN-OHL-P-2.0"


def gc_array(c, x_port, ys, facing_east):
    """Place rectangular GCs so their waveguide port o1 sits at (x_port, y), facing into the die."""
    ports = []
    for y in ys:
        g = c << gf.get_component("grating_coupler_rectangular")
        if facing_east:
            g.drotate(180)
        g.dmove((x_port - g.ports["o1"].center[0], y - g.ports["o1"].center[1]))
        ports.append(g.ports["o1"])
    return ports


def loopback(c, p1, p2):
    gf.routing.route_single(c, p1, p2, cross_section="strip")


def pad_xs(contact_xs, x_min, x_max):
    """Pad centres as close as possible above/below each contact, at least PAD_PITCH apart."""
    xs = []
    for x in sorted(contact_xs):
        xs.append(max(x, x_min, xs[-1] + PAD_PITCH if xs else x_min))
    overflow = xs[-1] - x_max
    if overflow > 0:                       # slide the whole row left, keeping order and pitch
        xs = [x - overflow for x in xs]
        for i in range(len(xs) - 2, -1, -1):
            xs[i] = min(xs[i], xs[i + 1] - PAD_PITCH)
    return xs


def pad_row(c, xs, y, facing):
    """Pads centred at (x, y); returns the port that faces the mesh ('e4' south / 'e2' north)."""
    out = []
    for x in xs:
        p = c << gf.get_component("pad", size=(PAD, PAD))
        p.dmove((x, y))
        out.append(p.ports["e4" if facing == "south" else "e2"])
    return out


@gf.cell
def opf_mzi4() -> gf.Component:
    c = gf.Component()
    floor = c << gf.get_component("rectangle", size=DIE, layer="FLOORPLAN")
    floor.dmove((0, 0))

    mesh = c << clements_mesh(4)
    gc_len = gf.get_component("grating_coupler_rectangular").ports["o2"].center[0]
    x_west = EDGE + gc_len + 20.0
    x_east = DIE[0] - EDGE - gc_len - 20.0
    mesh_w = mesh.ports["out0"].center[0] - mesh.ports["in0"].center[0]
    x_mesh = (x_west + x_east - mesh_w) / 2.0
    mesh.dmove((x_mesh - mesh.ports["in0"].center[0], MESH_Y - mesh.ports["in0"].center[1]))

    # --- optical I/O -------------------------------------------------------
    yc = MESH_Y + 1.5 * PITCH
    in_ys = [yc + (j - 1.5) * GC_PITCH for j in range(4)]
    lb_west = [yc - 3.5 * GC_PITCH, yc - 2.5 * GC_PITCH]
    lb_east = [yc + 2.5 * GC_PITCH, yc + 3.5 * GC_PITCH]
    w_in = gc_array(c, x_west, in_ys, facing_east=True)
    w_lb = gc_array(c, x_west, lb_west, facing_east=True)
    e_out = gc_array(c, x_east, in_ys, facing_east=False)
    e_lb = gc_array(c, x_east, lb_east, facing_east=False)
    for k in range(4):
        gf.routing.route_single(c, w_in[k], mesh.ports[f"in{k}"], cross_section="strip")
        gf.routing.route_single(c, mesh.ports[f"out{k}"], e_out[k], cross_section="strip")
    loopback(c, w_lb[0], w_lb[1])
    loopback(c, e_lb[0], e_lb[1])

    # --- calibration MZI (heaters on bottom arm, contacts south) ------------
    cal = c << mzi_unit(False)
    cal_x = x_mesh + mesh_w / 4.0        # under column 1: no south-facing mesh heaters there
    cal.dmove((cal_x - cal.ports["o1"].center[0], CAL_Y - cal.ports["o1"].center[1]))
    cal_in = gc_array(c, x_west, [CAL_Y + PITCH], facing_east=True)[0]
    cal_out = gc_array(c, x_east, [CAL_Y + PITCH], facing_east=False)[0]
    gf.routing.route_single(c, cal_in, cal.ports["o2"], cross_section="strip")
    gf.routing.route_single(c, cal.ports["o3"], cal_out, cross_section="strip")

    # --- electrical ---------------------------------------------------------
    north = sorted([p for p in mesh.ports if p.port_type == "electrical" and p.orientation == 90],
                   key=lambda p: p.center[0])
    south = sorted([p for p in mesh.ports if p.port_type == "electrical" and p.orientation == 270],
                   key=lambda p: p.center[0])
    cal_e = sorted([cal.ports[n] for n in ("phi_l", "phi_r", "th_l", "th_r")], key=lambda p: p.center[0])

    y_north = DIE[1] - EDGE - PAD / 2
    y_south = EDGE + PAD / 2
    x_lo, x_hi = EDGE + PAD, DIE[0] - EDGE - PAD
    xs_n = pad_xs([p.center[0] for p in north], x_lo, x_hi)
    pads_n = pad_row(c, xs_n, y_north, "south")
    gf.routing.route_bundle(c, north, pads_n, cross_section="metal_routing", bend="wire_corner",
                            port_type="electrical", allow_width_mismatch=True, separation=20.0, sort_ports=True)
    xs_s = pad_xs([p.center[0] for p in south + cal_e], x_lo, x_hi)
    pads_s = pad_row(c, xs_s, y_south, "north")
    gf.routing.route_bundle(c, south + cal_e, pads_s, cross_section="metal_routing", bend="wire_corner",
                            port_type="electrical", allow_width_mismatch=True, separation=20.0, sort_ports=True)

    label = c << gf.get_component("text_rectangular", text=VERSION, size=8.0, layer="WG")
    label.dmove((EDGE + 20, EDGE + 180))
    return c


def main() -> None:
    out = Path(__file__).resolve().parent / "gds"
    out.mkdir(exist_ok=True)
    chip = opf_mzi4()
    gds = out / "opf_mzi4_v0.1.gds"
    chip.write_gds(gds)
    bb = chip.dbbox()
    print(f"wrote {gds.name}: {bb.width():.1f} x {bb.height():.1f} um, "
          f"{len(chip.get_polygons())} layers with polygons")


if __name__ == "__main__":
    main()
