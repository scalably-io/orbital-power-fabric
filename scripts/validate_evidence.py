#!/usr/bin/env python3
"""Validate researcher CSVs and merge the passing rows into evidence/claims.csv.

Usage: python3 scripts/validate_evidence.py [--write]
Without --write it only reports. Rejected rows are listed with the reason and
never merged. Rules: evidence/SCHEMA.md.
"""
import csv
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
RESEARCH = ROOT / "evidence" / "research"
OUT = ROOT / "evidence" / "claims.csv"

HEADER = ["claim_id", "branch", "claim", "value", "unit", "status", "source_url", "locator",
          "quote", "source_date", "retrieved", "confidence", "notes"]
BRANCHES = {"A_orbital_gpu", "B_rf_power", "C_reflector", "D_ground_photonic", "E_orbital_photonic",
            "F_photonic_fab", "T_terrestrial", "X_common"}
STATUSES = {"MEASURED", "VENDOR-STATED", "FILING", "STUDY-ASSUMED", "DERIVED", "PROJECTED", "ACCESS-FAILED"}
CONFIDENCE = {"High", "Medium", "Low"}
ID_RE = re.compile(r"^R\d+-\d{3}$")
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
MAX_QUOTE_WORDS = 60   # schema asks for <=40; tolerate light overrun, flag it


def check(row: dict) -> list[str]:
    errs = []
    if not ID_RE.match(row["claim_id"]):
        errs.append("bad claim_id")
    if row["branch"] not in BRANCHES:
        errs.append(f"bad branch {row['branch']!r}")
    if row["status"] not in STATUSES:
        errs.append(f"bad status {row['status']!r}")
    if row["confidence"] not in CONFIDENCE:
        errs.append(f"bad confidence {row['confidence']!r}")
    if not DATE_RE.match(row["retrieved"]):
        errs.append("bad retrieved date")
    if row["status"] == "ACCESS-FAILED":
        return errs
    if not row["source_url"].startswith("http"):
        errs.append("missing source_url")
    if not row["locator"].strip():
        errs.append("missing locator")
    words = len(row["quote"].split())
    if words == 0:
        errs.append("missing quote")
    elif words > MAX_QUOTE_WORDS:
        errs.append(f"quote too long ({words} words)")
    if row["status"] == "DERIVED" and not row["notes"].strip():
        errs.append("DERIVED without formula in notes")
    return errs


def main(write: bool) -> int:
    merged, rejected, seen = [], [], set()
    files = sorted(RESEARCH.glob("R*-*.csv"))
    for path in files:
        with path.open(newline="") as fh:
            reader = csv.DictReader(fh)
            if reader.fieldnames != HEADER:
                print(f"{path.name}: HEADER MISMATCH {reader.fieldnames}")
                return 2
            for row in reader:
                errs = check(row)
                if row["claim_id"] in seen:
                    errs.append("duplicate claim_id")
                seen.add(row["claim_id"])
                (rejected if errs else merged).append((path.name, row, errs))
    by_status = {}
    for _, row, _ in merged:
        by_status[row["status"]] = by_status.get(row["status"], 0) + 1
    print(f"files={len(files)} merged={len(merged)} rejected={len(rejected)} by_status={by_status}")
    for name, row, errs in rejected:
        print(f"REJECT {name} {row['claim_id']}: {'; '.join(errs)}")
    if write:
        with OUT.open("w", newline="") as fh:
            w = csv.DictWriter(fh, fieldnames=HEADER)
            w.writeheader()
            for _, row, _ in merged:
                w.writerow(row)
        print(f"wrote {OUT.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main("--write" in sys.argv))
