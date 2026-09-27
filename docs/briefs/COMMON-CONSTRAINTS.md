<hard_constraints>
1. Read-only on the web: no messages, emails, form submissions, sign-ups, account creation, purchases or quote requests. Never contact anyone.
2. Write ONLY to your two output files, plus downloads into evidence/sources/<your prefix>/. Touch nothing else.
3. Do the work yourself. Do not use the Agent tool.
4. Today is 2026-09-27. Your training memory is stale. Never state a number from memory. Every number needs: URL + exact locator (page/section/table/figure) + a verbatim quote of 40 words or fewer. No quote → the claim does not go in.
5. If a source is inaccessible, record ACCESS-FAILED with the reason and try alternatives (preprint, author manuscript, agency PDF, archive.org). Never fill a gap with a guess.
6. Provenance class exact: MEASURED · VENDOR-STATED · FILING · STUDY-ASSUMED · DERIVED (formula in notes) · PROJECTED.
</hard_constraints>
Tools: WebSearch, WebFetch. PDFs: `curl -sL -o <path>.pdf <url>` then `/opt/homebrew/bin/pdftotext -layout <file> -`; search with /usr/bin/grep (plain grep is ugrep here).
CSV header exactly: claim_id,branch,claim,value,unit,status,source_url,locator,quote,source_date,retrieved,confidence,notes — write it with Python's csv module; retrieved = 2026-09-27.
