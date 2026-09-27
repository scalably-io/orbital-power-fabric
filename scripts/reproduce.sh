#!/usr/bin/env bash
# Rebuild every number, table and chart from the evidence ledger. Exit non-zero on any failure.
set -euo pipefail
cd "$(dirname "$0")/.."
python3 scripts/validate_evidence.py            # evidence schema + quotes present
python3 -m pytest -q                            # physics, handoff reproduction, provenance guard
python3 scripts/verdict.py > /dev/null          # docs/generated/verdict_v1.md
python3 scripts/open_problems.py > /dev/null    # docs/generated/open_problems.md
python3 scripts/build_charts.py                 # figures/*.svg
python3 scripts/efficiency_v2.py > /dev/null      # current photonic families (E028)
python3 scripts/chip_predictions.py > /dev/null
python3 scripts/efficiency_levers.py > /dev/null   # superseded record (E014/E015)
python3 scripts/synthesis_candidates.py > /dev/null  # superseded record (E018)
python3 paper/build_paper.py > /dev/null     # paper/paper.md from the evidence register (asserts)
echo "reproduce: OK"
