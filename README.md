# Orbital Power Fabric

**Should space power AI by sending energy down, or by hosting the GPUs? An open, falsifiable model. The answer: not yet, either way.**

White paper: *Move the energy, not the data centre? A falsifiable model of orbital energy for AI, and exactly what must change before space wins*, by Pavle Lazić (ScalablyAI), report SR-2026-003: `paper/paper.md` (web: https://scalably.io/research/orbital-power-fabric).

## Built with AI, on purpose

This work was built by one founder directing AI agents (Anthropic's Claude) that searched primary sources, wrote a quote-per-claim evidence ledger, built and tested the model, and wrote the paper from that ledger. Fresh-context AI reviewers (Anthropic's Claude Opus and OpenAI's Codex) then attacked the model and the paper; their reviews reversed several of our own conclusions, and every reversal is recorded (`docs/NEGATIVE-FINDINGS.md`, `EXPERIMENTS.md`). No human domain expert has reviewed it yet. That is what this repository is for: find where it breaks.

## Reproduce everything

```
python3 -m pip install -e ".[test]"
./scripts/reproduce.sh      # validates the ledger, runs the tests, regenerates the verdict, tables, figures and the paper
```

Every number in the paper's prose is a placeholder filled by `paper/build_paper.py` from the model or the ledger; the build fails on a typed number, an unknown claim or derivation, or a hype word.

## Where things are

| Path | What |
|---|---|
| `evidence/claims.csv` | The ledger: every claim with source URL, locator, verbatim quote (≤ 40 words), status and date. Built from `evidence/research/R*.csv` by `scripts/validate_evidence.py`. Downloaded sources are not redistributed (copyright); every row is re-fetchable from its URL. |
| `opf/` | The model (orbits, beams, mirrors, lifecycle mass, photonic energy). `opf/params.py`: parameters with claim IDs; `opf/scenarios.py`: the verdict scenarios. |
| `docs/DERIVATIONS.md` | Every formula, derived, with the test that pins it. |
| `docs/PREREGISTRATION.md` | The metric and verdict rules, fixed before any break-even was computed. |
| `docs/generated/` | Verdict and open problems, generated. Never edit by hand. |
| `docs/NEGATIVE-FINDINGS.md` | The dead ends and our own errors, with numbers. |
| `docs/briefs/` | The exact briefs given to the AI research agents. |
| `EXPERIMENTS.md` | The run log, including every review round. |
| `chip/` | OPF-MZI4, an open 4×4 photonic test-chip layout, and a build guide for any lab that wants to fabricate it. |

## Challenge a number

Open an issue with the claim ID, a better source, its locator and a verbatim quote. Change an assumption in `opf/scenarios.py` and rerun `python3 scripts/verdict.py` to see where the verdict flips; `docs/generated/open_problems.md` lists the twelve quantities that decide it.

## Notes

- The working history of this project is private; this repository is a curated export. The preregistration was committed before the first break-even in that history; the original research brief we audited (a ChatGPT-built handoff) is not included; its numbers are reproduced in `opf/params.py` (`HANDOFF`) and `tests/test_handoff_baseline.py`.
- `chip/` needs `pip install -e ".[chip]"` (cspdk, which pins gdsfactory).

## Licences

Code: Apache-2.0 (`LICENSE`). Text, data and figures: CC BY 4.0 (`LICENSE-CC-BY-4.0.txt`). Chip design files: CERN-OHL-P-2.0 (`chip/LICENSE-CERN-OHL-P-2.0.txt`).

## Cite

See `CITATION.cff`. https://github.com/scalably-io/orbital-power-fabric
