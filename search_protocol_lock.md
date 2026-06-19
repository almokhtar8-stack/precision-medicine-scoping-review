# Search Protocol Lock — Precision Medicine Implementation in Healthcare Systems
## Scoping Review (MHA Program)

**Current protocol version:** Version D (proposed, pending author approval before retrieval)
**Original lock date:** 2026-06-19
**Last revised:** 2026-06-19

---

## Version History

### Version B — Initial pilot (committed 2026-06-19, commit c655ead)

**Structure:** `(G1) AND (G2 OR G3)`, English, 2015-present

G1 covered precision medicine/genomics concepts. G2 covered implementation/adoption terms. G3 covered governance/policy/infrastructure terms. G1, G2, and G3 all used broad OR logic internally.

**PubMed result:** 117,943 raw hits.

**Finding:** Unworkable. G2 and G3 each contained individually very common words (`barrier*`, `facilitat*`, `policy`, `leadership`, `workforce`, `financ*`, `ethic*`); OR logic across both groups meant that almost any genomics paper touching one of these words was captured. Count was approximately 100× the total cross-source estimate from the original proposal. Full dataset retrieved and committed as an honest record of the pilot (commit c655ead, `pubmed_results_20260619.csv.gz`, 117,592 records). Not used for screening.

---

### Version C — First revision (count-only, not retrieved, 2026-06-19)

**Change from B:** Dropped G3 entirely. Tightened G2 by removing the single-word broadeners (`barrier*`, `facilitat*`, `enabler*`, `readiness`, `uptake`, `adopt*`, `integrat*`, `service delivery`, `healthcare delivery`). Added a narrow EQUITY_RESCUE clause to catch equity/ethics commentary papers lacking an explicit implementation verb (target: Popejoy & Fullerton 2016, PMID 27734877).

**PubMed result:** 82,361 raw hits.

**Finding:** Still unworkable (82,361 >> 8,000 ceiling for solo-reviewer scoping review). Additionally, the EQUITY_RESCUE clause failed to catch its own target paper: Popejoy & Fullerton (2016) has **no abstract indexed in PubMed** — it is a Nature Comment with only the title *"Genomics is failing on diversity"* as searchable text. None of the EQUITY_RESCUE's `[tiab]` terms appear in that four-word title. Patching the clause with standalone `diversity[tiab]` would have increased the count to 111,006 (worse than Version B), confirming the clause was not viable. No retrieval performed.

**Popejoy handling decision (2026-06-19):** Popejoy & Fullerton (2016, PMID 27734877) will be added via a documented hand-search step rather than automated query. This is consistent with standard scoping review methodology (Levac et al., 2010) and the protocol's pre-specified hand-search of reference lists. Any other known key sources lacking indexed abstracts will be handled the same way and logged separately.

---

### Version D — Proposed (count-only, awaiting author approval, 2026-06-19)

**Change from C:** Removed EQUITY_RESCUE clause entirely. Further tightened G1 by removing `genomic*[tiab]` (the single biggest noise source — matched any paper using the word "genomic" anywhere), removing all MeSH terms (`"Genomics"[Mesh]`, `"Precision Medicine"[Mesh]`, `"Pharmacogenetics"[Mesh]` — the Genomics MeSH is especially broad), and removing `"genomic medicine"[tiab]` (adds 337 unique papers net, which largely represent basic-science genomics literature rather than implementation studies; recoverable through hand-search). Removed `"precision health"[tiab]` and `"precision oncology"[tiab]` from G1 (combined isolation cost: ~1,000 records; significant overlap with "precision medicine" in practice). Retained all pharmacogenomics terms (`pharmacogenom*`, `pharmacogenetic*`) since these target specific implementation-relevant literature not captured by precision medicine terminology alone.

In G2: removed `adopt*`, `integrat*`, `"healthcare delivery"`, `"health care delivery"`, `"service delivery"` (all contributed substantially to noise). Retained `implement*` as the primary implementation anchor, plus the multi-word phrases that are specific to implementation science: `"organizational readiness"`, `"organisational readiness"`, `"change management"`, `"clinical workflow"`, `"scale up"`, `rollout`.

**Final Version D query:**

```
G1 = ("precision medicine"[tiab] OR "personalized medicine"[tiab]
      OR "personalised medicine"[tiab] OR pharmacogenom*[tiab]
      OR pharmacogenetic*[tiab])

G2 = (implement*[tiab] OR "organizational readiness"[tiab]
      OR "organisational readiness"[tiab] OR "change management"[tiab]
      OR "clinical workflow"[tiab] OR "scale up"[tiab] OR rollout[tiab])

FULL QUERY:
(G1) AND (G2)
AND ("2015/01/01"[Date - Publication] : "3000"[Date - Publication])
AND (english[Language])
```

**PubMed count-only result:** 7,895 raw hits.

**Status:** Within the 2,000–8,000 target range for a solo-reviewer scoping review (PubMed contribution only). **Awaiting author approval before full retrieval.**

---

## Term-removal decision log (2026-06-19)

Full count table from systematic testing, for methods transparency:

| What changed | Count |
|---|---|
| Version B (G1 full + G2 OR G3) | 117,943 |
| Version C (G1 full + G2 tight + EQUITY_RESCUE) | 82,361 |
| Version C, no EQUITY_RESCUE | 81,685 |
| Remove `genomic*[tiab]` from G1 | 50,751 |
| Remove `adopt*` and `integrat*` from G2 | 23,856 |
| Both above together | 16,498 |
| G1 without `genomic*` + G2 phrases-only | 16,442 |
| G1 without `genomic*` and `"Genomics"[Mesh]` + G2 phrases | 10,166 |
| G1 tiab-only (no MeSH) + G2 phrases | 9,031 |
| G1 tiab-only + G2 core (no `"healthcare delivery"` variants) | 8,884 |
| G1 tiab-only + G2 narrowest (no `"change mgmt"`, no `"scale up"`) | 8,829 |
| G1 without `"genomic medicine"` + G2 core | **7,895** ← Version D |
| G1 core only (3 PM terms) + G2 core | 6,426 |
| G1 core + `"implementation"[tiab]` only | 5,661 |

Each step represents a documentable methodological narrowing with a clear rationale. No arbitrary cuts.

---

## Planned Sources (not yet searched)

1. PubMed/MEDLINE (Version B pilot complete; Version D pending)
2. Embase
3. CINAHL
4. Web of Science
5. Cochrane Library

---

## Hand-Search Log

The following known relevant sources will be added via documented hand-search, separate from the automated database search:

| Source | PMID / Identifier | Reason for hand-search |
|---|---|---|
| Popejoy & Fullerton (2016). *Genomics is failing on diversity.* Nature. | 27734877 | No abstract indexed in PubMed; tiab search cannot retrieve it. |

Additional sources may be added here as reference-list checking proceeds.

---

## Methodological Transparency

This repository and its commit timestamps serve as the pre-analysis registration record for this review, in lieu of external OSF pre-registration, consistent with publication in the author's institutional journal. The Version B commit (c655ead, 2026-06-19) is the permanent record of the initial pilot search. Version D, once retrieved and committed, will be the operative dataset for screening. The revision history above is part of the methods section, not a correction to hide.

---

## Inclusion/Exclusion

All screening and inclusion/exclusion decisions are made by the review author. No automated filtering has been applied. The `decision` column in the CSV is defaulted to `pending` for all records.
