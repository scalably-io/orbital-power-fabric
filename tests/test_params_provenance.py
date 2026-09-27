"""Every VERIFIED parameter cites a claim that exists in evidence/claims.csv, or says ASSUMPTION:<why>."""
import csv
from pathlib import Path

from opf.params import HANDOFF, VERIFIED

ROOT = Path(__file__).resolve().parent.parent


def claim_ids() -> set[str]:
    with (ROOT / "evidence/claims.csv").open(newline="") as fh:
        return {r["claim_id"] for r in csv.DictReader(fh)}


def test_verified_params_cite_existing_claims_or_assumptions():
    ids = claim_ids()
    bad = {k: p.source for k, p in VERIFIED.items()
           if not (p.source.startswith("ASSUMPTION:") and len(p.source) > len("ASSUMPTION:"))
           and p.source not in ids}
    assert not bad, f"unsourced VERIFIED params: {bad}"


def test_handoff_set_is_marked_as_handoff():
    assert all(p.source.startswith("H-") for p in HANDOFF.values())
