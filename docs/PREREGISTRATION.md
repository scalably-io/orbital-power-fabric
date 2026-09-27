# Preregistration — written 2026-09-27, BEFORE any break-even result was computed

Frozen once committed. Changes go below as dated amendments with the reason; the original text stays.

## Unit of comparison
One kilowatt of AI accelerator load (IT power, GB300 NVL72-class) running continuously (time-averaged) for a lifecycle of L = 10 / 15 / 20 years.
- A (orbital GPU): the accelerator is in orbit.
- B (orbital PV → microwave → ground), C (orbital mirror → ground PV): the accelerator is on Earth; required delivered electricity = IT kW × PUE, time-averaged at the site/fabric.
- T (terrestrial baseline, added by us — missing from the handoff): the same Earth load on grid / ground PV + battery. Every orbital-energy option must be compared with T, not only with A.

## Primary metric (decides the verdict)
Lifecycle LAUNCHED MASS per continuous kW of AI load (kg / kW), including every replacement over L:
- A relaunches its compute payload at min(GPU refresh cadence, vehicle lifetime);
- B and C relaunch their orbital energy hardware at the vehicle lifetime; GPUs refresh on the ground at zero launch mass.
Duty factors are explicit: eclipse, receiver visibility (fraction of orbit time a receiver is in view above minimum elevation), weather, and transmit-chain losses.

## Secondary metrics (reported, do not decide)
Launch cost per kW-year · orbital area per kW · ground area per kW · radiator area/mass (A, E) · full-system joules per useful operation (D, E) · $/MWh versus T.

## Value-selection rule (fixed now)
- Tier `current`: median of MEASURED / qualified / buyable values; vendor-stated values allowed only where no measurement exists, labelled as such.
- Tier `next`: best demonstrated lab/flight value.
- Tier `speculative`: PROJECTED values.
Tiers never mix inside one scenario.

## Verdict rules (from handoff §K, made quantitative)
- V1 Reject B for a tier if its lifecycle launched mass per continuous kW exceeds A's at the tier's sourced refresh cadence.
- V2 Same test for C.
- V3 Orbital energy is not competitive with T for a tier if B's and C's launch cost alone per delivered MWh exceeds the sourced terrestrial PV + storage cost per MWh.
- V4 Photonic compute (D/E) is not supported for a tier unless best-sourced FULL-SYSTEM joules per useful operation (same precision) is below the electronic GB300-class value.
- For every comparison, publish the single-parameter break-even value (all others at tier baseline) and a Monte Carlo over the sourced ranges. Publish whichever answer comes out.
