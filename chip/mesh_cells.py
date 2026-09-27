"""Clements-mesh building blocks composed from MIT-licensed cspdk (CORNERSTONE si220) cells.

Every optical/electrical primitive here is an unmodified cspdk cell
(mmi2x2, straight_heater_metal, straight, bend_s). Only their arrangement is
ours. Licenses: cspdk MIT (c) 2024 gdsfactory; this file CERN-OHL-P-2.0
(see chip/LICENSE-CERN-OHL-P-2.0.txt).

Design choices (see chip/DESIGN.md):
- HEATER_LEN = the cspdk default 320 um (unmodified); four columns fit the
  5.5 x 4.9 mm die with 172 um fan-in/out on each side.
- Heaters of MZIs on the lowest mode pair sit on the BOTTOM arm with contacts
  facing south; all others on the TOP arm facing north. Metal therefore never
  crosses more than one waveguide.
"""
import gdsfactory as gf
from cspdk.si220.cband import PDK

PDK.activate()

PITCH = 80.0          # centre-to-centre spacing of mesh modes (um)
HEATER_LEN = 320.0    # cspdk default heater length (um)
SBEND_DX = 60.0       # S-bend length for a PITCH/2 - 1 um lateral move


def _sbend(dy: float) -> gf.Component:
    return gf.get_component("bend_s", size=(SBEND_DX, dy), cross_section="strip")


@gf.cell
def arm_pair(heater_top: bool = True) -> gf.Component:
    """Two parallel waveguides at PITCH: one heater arm, one length-matched straight.

    Ports o1 bottom-in, o2 top-in, o3 top-out, o4 bottom-out; e_l / e_r heater contacts.
    """
    c = gf.Component()
    h = c << gf.get_component("straight_heater_metal", length=HEATER_LEN)
    s = c << gf.get_component("straight", length=HEATER_LEN, cross_section="strip")
    if heater_top:
        h.dmove((0, PITCH / 2))
        s.dmove((0, -PITCH / 2))
        top, bot = h, s
    else:
        h.dmirror_y()                     # contacts face south
        h.dmove((0, -PITCH / 2))
        s.dmove((0, PITCH / 2))
        top, bot = s, h
    c.add_port("o1", port=bot.ports["o1"])
    c.add_port("o2", port=top.ports["o1"])
    c.add_port("o3", port=top.ports["o2"])
    c.add_port("o4", port=bot.ports["o2"])
    c.add_port("e_l", port=h.ports["l_e2"])
    c.add_port("e_r", port=h.ports["r_e2"])
    return c


@gf.cell
def mzi_unit(heater_top: bool = True) -> gf.Component:
    """Balanced MZI at mode pitch PITCH: [phi heater] -> MMI -> [theta heater] -> MMI.

    Optical ports: o1 bottom-in, o2 top-in, o3 top-out, o4 bottom-out.
    Electrical: phi_l/phi_r (external phase), th_l/th_r (internal phase).
    """
    c = gf.Component()
    ext = c << arm_pair(heater_top)
    mmi_a = c << gf.get_component("mmi2x2")
    arms = c << arm_pair(heater_top)
    mmi_b = c << gf.get_component("mmi2x2")

    dy = PITCH / 2 - 1.0  # MMI ports sit at +-1 um
    top_in = c << _sbend(-dy)
    bot_in = c << _sbend(dy)
    top_in.connect("o1", ext.ports["o3"])
    bot_in.connect("o1", ext.ports["o4"])
    mmi_a.connect("o2", top_in.ports["o2"])
    top_a = c << _sbend(dy)
    bot_a = c << _sbend(-dy)
    top_a.connect("o1", mmi_a.ports["o3"])
    bot_a.connect("o1", mmi_a.ports["o4"])
    arms.connect("o2", top_a.ports["o2"])
    top_b = c << _sbend(-dy)
    bot_b = c << _sbend(dy)
    top_b.connect("o1", arms.ports["o3"])
    bot_b.connect("o1", arms.ports["o4"])
    mmi_b.connect("o2", top_b.ports["o2"])
    top_o = c << _sbend(dy)
    bot_o = c << _sbend(-dy)
    top_o.connect("o1", mmi_b.ports["o3"])
    bot_o.connect("o1", mmi_b.ports["o4"])

    c.add_port("o1", port=ext.ports["o1"])
    c.add_port("o2", port=ext.ports["o2"])
    c.add_port("o3", port=top_o.ports["o2"])
    c.add_port("o4", port=bot_o.ports["o2"])
    c.add_port("phi_l", port=ext.ports["e_l"])
    c.add_port("phi_r", port=ext.ports["e_r"])
    c.add_port("th_l", port=arms.ports["e_l"])
    c.add_port("th_r", port=arms.ports["e_r"])
    return c


@gf.cell
def clements_mesh(n: int = 4) -> gf.Component:
    """N x N Clements mesh: N columns, MZIs on pairs (m, m+1), m = c%2, c%2+2, ...

    Idle modes in a column get a length-matched straight. Mode k sits at y = k*PITCH.
    Ports: in0..in{n-1} (west), out0..out{n-1} (east),
    electrical c{col}m{m}_{phi|th}_{l|r} per MZI.
    """
    c = gf.Component()
    unit_len = mzi_unit(True).ports["o3"].center[0] - mzi_unit(True).ports["o2"].center[0]
    ends = {}
    for col in range(n):
        x0 = col * unit_len
        busy = set()
        for m in range(col % 2, n - 1, 2):
            top = m != 0                      # lowest pair: heaters south
            u = c << mzi_unit(top)
            u.dmove((x0 - u.ports["o1"].center[0], m * PITCH - u.ports["o1"].center[1]))
            busy |= {m, m + 1}
            if col == 0:
                c.add_port(f"in{m}", port=u.ports["o1"])
                c.add_port(f"in{m + 1}", port=u.ports["o2"])
            ends[m], ends[m + 1] = u.ports["o4"], u.ports["o3"]
            for p in ("phi_l", "phi_r", "th_l", "th_r"):
                c.add_port(f"c{col}m{m}_{p}", port=u.ports[p])
        for k in set(range(n)) - busy:
            s = c << gf.get_component("straight", length=unit_len, cross_section="strip")
            s.dmove((x0, k * PITCH))
            if col == 0:
                c.add_port(f"in{k}", port=s.ports["o1"])
            ends[k] = s.ports["o2"]
    for k in range(n):
        c.add_port(f"out{k}", port=ends[k])
    return c
