"""Render a GDS (or a window of it) to PNG with KLayout's own layout view.

Usage: python chip/render.py in.gds out.png [x1 y1 x2 y2]   (um; default = full extent)
"""
import sys

import klayout.db as db
import klayout.lay as lay


def render(gds: str, png: str, box: tuple[float, float, float, float] | None = None,
           width: int = 1800, height: int = 900) -> None:
    view = lay.LayoutView()
    view.load_layout(gds, True)
    view.max_hier()
    view.set_config("background-color", "#000000")
    view.set_config("grid-visible", "false")
    if box:
        view.zoom_box(db.DBox(*box))
    else:
        view.zoom_fit()
    view.save_image(png, width, height)


if __name__ == "__main__":
    args = sys.argv[1:]
    render(args[0], args[1], tuple(map(float, args[2:6])) if len(args) >= 6 else None)
