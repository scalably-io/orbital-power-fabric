#!/usr/bin/env python3
"""Connectivity check (LVS-lite) for OPF-MZI4: shorts and opens on the metal layers.

Rules, from the design intent:
  1. The PAD (routing) layer must split into exactly 2 x n_heaters islands — one per
     heater contact — and every island must hold exactly one 90x90 um pad.
  2. Every HEATER-layer island (one heater resistor) must touch exactly two PAD islands.
Run: .venv/bin/python chip/check_nets.py chip/gds/opf_mzi4_v0.1.gds 14
"""
import sys

import klayout.db as db
from cspdk.si220.cband import LAYER


def main(gds: str, n_heaters: int) -> int:
    ly = db.Layout()
    ly.read(gds)
    top = ly.top_cell()
    li = {name: ly.layer(*getattr(LAYER, name)) for name in ("PAD", "HEATER")}
    metal = db.Region(top.begin_shapes_rec(li["PAD"])).merged()
    heater = db.Region(top.begin_shapes_rec(li["HEATER"])).merged()

    islands = list(metal.each())
    # a pad is a >= 89x89 um box drawn on the PAD layer
    pad_boxes = db.Region([p.bbox() for p in db.Region(top.begin_shapes_rec(li["PAD"])).each()
                           if p.bbox().width() >= 89_000 and p.bbox().height() >= 89_000
                           and p.is_box()]).merged()

    errors = []
    if len(islands) != 2 * n_heaters:
        errors.append(f"PAD islands = {len(islands)}, expected {2 * n_heaters}")
    for i, isl in enumerate(islands):
        n_pad = pad_boxes.interacting(db.Region(isl)).count()
        if n_pad != 1:
            errors.append(f"island {i} at {isl.bbox().center()} holds {n_pad} pads")
    heaters = list(heater.each())
    if len(heaters) < n_heaters:
        errors.append(f"HEATER islands = {len(heaters)}, expected >= {n_heaters}")
    for i, h in enumerate(heaters):
        touching = metal.interacting(db.Region(h)).count()
        if touching != 2:
            errors.append(f"heater {i} at {h.bbox().center()} touches {touching} metal islands")

    print(f"PAD islands {len(islands)} (expected {2 * n_heaters}); pads {pad_boxes.count()}; "
          f"HEATER islands {len(heaters)}")
    for e in errors:
        print("FAIL", e)
    print("PASS" if not errors else f"{len(errors)} errors")
    return 0 if not errors else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1], int(sys.argv[2])))
