# Evidence schema

`evidence/claims.csv` (merged) and every `evidence/research/R*-*.csv` use exactly:

`claim_id,branch,claim,value,unit,status,source_url,locator,quote,source_date,retrieved,confidence,notes`

| field | rule |
|---|---|
| claim_id | `R<n>-<nnn>` from researchers; `H-C0xx` = original handoff claim (unverified) |
| branch | A_orbital_gpu · B_rf_power · C_reflector · D_ground_photonic · E_orbital_photonic · F_photonic_fab · T_terrestrial · X_common |
| status | MEASURED · VENDOR-STATED · FILING · STUDY-ASSUMED · DERIVED · PROJECTED · ACCESS-FAILED |
| locator | page / section / table / figure / supplementary note — enough to find the quote in under a minute |
| quote | verbatim from the source, ≤40 words. Empty quote ⇒ the claim is not usable (except ACCESS-FAILED rows) |
| retrieved | date the researcher read it (ISO) |
| confidence | High / Medium / Low |

Merge rule: a row enters `claims.csv` only if `scripts/validate_evidence.py` passes it (schema, status enum, non-empty URL+locator+quote, DERIVED rows show the formula in notes). Model parameters cite claim_ids; a parameter with no claim_id must say `ASSUMPTION:<why>`.
