# Search Protocol Lock — Precision Medicine Implementation in Healthcare Systems
## Scoping Review (MHA Program)

**Protocol version:** Version B (locked)
**Lock date:** 2026-06-19
**Database searched:** PubMed/MEDLINE (via NCBI E-utilities API)
**Search executed:** 2026-06-19 (UTC timestamp in run log)

---

## Search Structure

`(Group 1) AND (Group 2 OR Group 3)`

All filters applied: English language; publication date 2015-01-01 to present.

---

## Group 1 — Precision Medicine Concepts

```
("precision medicine"[tiab] OR "personalized medicine"[tiab] OR
"personalised medicine"[tiab] OR "genomic medicine"[tiab] OR
genomic*[tiab] OR pharmacogenom*[tiab] OR pharmacogenetic*[tiab] OR
"precision health"[tiab] OR "precision oncology"[tiab] OR
"Precision Medicine"[Mesh] OR "Pharmacogenetics"[Mesh] OR "Genomics"[Mesh])
```

## Group 2 — Implementation & Adoption

```
(implement*[tiab] OR adopt*[tiab] OR integrat*[tiab] OR
"organizational readiness"[tiab] OR "organisational readiness"[tiab] OR
readiness[tiab] OR "change management"[tiab] OR "healthcare delivery"[tiab] OR
"health care delivery"[tiab] OR "service delivery"[tiab] OR
"clinical workflow"[tiab] OR uptake[tiab] OR rollout[tiab] OR
"scale up"[tiab] OR barrier*[tiab] OR facilitat*[tiab] OR enabler*[tiab])
```

## Group 3 — Governance, Policy & Infrastructure

```
(governance[tiab] OR policy[tiab] OR policies[tiab] OR leadership[tiab] OR
workforce[tiab] OR "human resources"[tiab] OR "digital infrastructure"[tiab] OR
interoperab*[tiab] OR "decision support"[tiab] OR financ*[tiab] OR
reimburs*[tiab] OR "cost-effectiveness"[tiab] OR equity[tiab] OR
ethic*[tiab] OR sustainab*[tiab])
```

---

## Results — PubMed (this source)

| Metric | Value |
|---|---|
| Raw API hit count | 117,943 |
| PMIDs collected (date-chunked esearch) | 117,942 |
| Records retrieved via efetch | 117,592 |
| After de-duplication by PMID | 117,592 |
| Duplicates removed | 0 |
| Output file | `pubmed_results_20260619.csv` (185 MB); also `pubmed_results_20260619.csv.gz` (69 MB) |

**Note on retrieval method:** PubMed's esearch endpoint caps at 9,999 records per call. Full retrieval was achieved by splitting the 2015–2026 date range into annual (and where necessary monthly) windows, collecting all PMIDs via repeated esearch calls, then fetching full records via HTTP POST to efetch using direct PMID lists (no history-server WebEnv, which has a separate 10,000-record cap). Machine-readable audit trail: `pubmed_run_log_20260619.json`.

**Note on count vs. proposal estimate:** The proposal estimated 800–1,200 records across all five sources combined. PubMed alone returned 117,943 records, approximately 100× the total estimate. This reflects the broad-sensitivity design of Version B. The discrepancy should be addressed in the methods/limitations section.

---

## Other Planned Sources (not yet searched)

1. Embase
2. CINAHL
3. Web of Science
4. Cochrane Library

---

## Methodological Transparency

This repository and its initial commit timestamp serve as the pre-analysis registration record for this review, in lieu of external OSF pre-registration, consistent with publication in the author's institutional journal. The commit hash and date are the authoritative record of when the search was locked and executed.

---

## Inclusion/Exclusion

All screening and inclusion/exclusion decisions are made by the review author. No automated filtering has been applied. The `decision` column in the CSV is defaulted to `pending` for all records.
