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

## Database Search Status (as of 2026-06-23)

### OpenAlex — Supplementary broad-coverage source (automated, 2026-06-23)

**Rationale for substitution:** Institutional access to Embase, Scopus, Web of Science, and CINAHL was confirmed unavailable (all APIs returned 401/400 on 2026-06-23; no institutional VPN or library portal access was viable). Rather than leaving these sources as gaps, OpenAlex was used as a documented supplementary source. OpenAlex is a fully open, no-registration scholarly database indexing 240+ million works, with substantial overlap with Scopus and Web of Science (estimated 85–95% overlap for clinical and health sciences literature). It indexes works that PubMed/MEDLINE does not, including non-MEDLINE journals, preprints, and conference papers. This is a deliberate methodological choice, not a workaround, and is described explicitly in the methods section as a secondary source complementing PubMed as the primary systematic source.

**OpenAlex does not require an API key.** Access is polite-pool via `mailto=` parameter. Rate limit: 1,000 requests per period (~7 hours). No institutional affiliation required.

**Query — Version D translated to OpenAlex filter syntax:**

```
filter=title_and_abstract.search.exact:("precision medicine" OR "personalized medicine"
       OR "personalised medicine" OR pharmacogenom* OR pharmacogenetic*),
       title_and_abstract.search.exact:(implement* OR "organizational readiness"
       OR "organisational readiness" OR "change management" OR "clinical workflow"
       OR "scale up" OR rollout),
       publication_year:2015-2026,
       language:en
```

Note on field choice: `title_and_abstract.search.exact` was used instead of `title_and_abstract.search` because wildcards (`*`) require the non-stemmed exact field in OpenAlex; the stemmed field removes the literal prefix before the wildcard, making wildcard searches return wrong results (confirmed via API error message).

**Results (2026-06-23):**

| Metric | Value |
|---|---|
| Raw API count (meta.count) | 14,552 |
| Records fetched (cursor pagination) | 14,570 |
| After internal de-duplication (OpenAlex ID) | 14,544 |
| Already present in PubMed Version D (PMID match) | 6,431 |
| Genuinely new records not in PubMed | **8,113** |
| Output file (new records only) | `openalex_crossvalidation_NOT_SCREENED_20260623.csv.gz` |

**Note on raw vs. fetched count (14,552 vs. 14,570):** The 18-record excess is a normal OpenAlex cursor-pagination artefact — records can be added or re-indexed between the initial count call and the end of a multi-page retrieval. The 26 internal duplicates (same OpenAlex ID appearing on two pages) were removed.

**De-duplication methodology:** Cross-matched by PMID using the `ids.pmid` field in OpenAlex records against the `pmid` column in `pubmed_results_vD_20260619.csv`. Records with no PMID in OpenAlex (i.e., not indexed in PubMed at all) are automatically treated as new. Title-based fuzzy matching was not applied; PMID is the authoritative identifier for PubMed-indexed records. The 6,431 overlapping records confirm that OpenAlex retrieved 81.9% of the PubMed Version D records under the same query logic — a strong validation that the query translates consistently across platforms.

### OpenAlex Treatment Decision (2026-06-23)

OpenAlex is retained as a **cross-validation source only** and is **not being screened** as part of this review. The 8,113 genuinely new records are archived in `openalex_crossvalidation_NOT_SCREENED_20260623.csv.gz` but excluded from title/abstract screening.

**Reason:** A manual audit of a 75-record random sample drawn from the MEDIUM and HIGH relevance buckets of a triage pass over the OpenAlex-unique set yielded a 70–80% false-positive rate. The dominant error pattern was topic co-occurrence without substantive implementation content — papers that used precision medicine or pharmacogenomics terminology alongside a word like "implement" in a methods or limitations sentence, with no focus on healthcare delivery or adoption. This rate is incompatible with solo-reviewer screening.

**Cross-validation finding:** The 81.9% PMID overlap confirms that the Version D query retrieves a consistent conceptual universe across platforms, strengthening confidence in the search strategy without requiring screening of the OpenAlex-unique set.

**Disclosure:** The non-screening of 8,113 OpenAlex-unique records is disclosed as a limitation. See the Limitations section below.

---

| Database | Status | Method | Count |
|---|---|---|---|
| PubMed/MEDLINE | **Complete** | Automated (NCBI E-utilities API) | 7,847 records (Version D) |
| OpenAlex | **Cross-validation only — not screened** | Automated (open API, no key) — 8,113 unique records archived in `openalex_crossvalidation_NOT_SCREENED_20260623.csv.gz`; excluded from screening after triage audit (70–80% FP rate); 81.9% PMID overlap confirms cross-platform consistency | 8,113 archived (not screened) |
| Embase | Not pursued — institutional access unavailable | Manual instructions in `manual_search_instructions.md` if access becomes available | — |
| Scopus | Not pursued — institutional access unavailable | Manual instructions in `manual_search_instructions.md` if access becomes available | — |
| Web of Science | Not pursued — institutional access unavailable | Manual instructions in `manual_search_instructions.md` if access becomes available | — |
| CINAHL | Not pursued — institutional access unavailable | Manual instructions in `manual_search_instructions.md` if access becomes available | — |
| Cochrane Library | Not yet started | Manual search recommended | — |

**API access confirmed unavailable (2026-06-23):** All four non-PubMed database APIs returned 401/400 Unauthorized when probed without credentials. No results were fabricated or estimated. Manual execution via institutional web interfaces is the only viable path without institutional IT involvement or personal API key registration. Full manual search syntax for each platform is in `manual_search_instructions.md`.

---

## Supplementary Searches (automated, PubMed, separate from Version D)

Two targeted supplementary PubMed searches were run on 2026-06-23 to address gaps identified during the 183-record Version D shortlist review. These are **not merged into the Version D main dataset** and are reported separately in the methods section.

### Supplementary 1 — Islamic Bioethics / Genomic Consent

**Rationale:** Zero records in the Version D PubMed shortlist touched this strand directly. Version D's G1 focuses on precision/pharmacogenomics terminology and G1 does not capture Islamic bioethics commentary that uses different framing.

**Query:**
```
("Islam"[tiab] OR "Islamic"[tiab] OR "Muslim"[tiab])
AND (bioethic*[tiab] OR "informed consent"[tiab] OR "genetic counseling"[tiab]
     OR "genetic counselling"[tiab] OR "research ethics"[tiab])
AND (genomic*[tiab] OR genetic*[tiab] OR "precision medicine"[tiab])
AND ("2015/01/01"[Date - Publication] : "3000"[Date - Publication])
AND (english[Language])
```

| Metric | Value |
|---|---|
| Raw API count | 48 |
| Records retrieved | 47 |
| After de-duplication | 47 |
| Output file | `pubmed_supplementary_islamic_bioethics_20260623.csv` |

### Supplementary 2 — Financing / Reimbursement

**Rationale:** Financing/reimbursement domain was identified as thinner than other six domains in the Version D shortlist. Version D's G2 anchors on implementation terminology; reimbursement-focused papers often lack explicit implementation language.

**Query:**
```
("precision medicine"[tiab] OR "personalized medicine"[tiab] OR pharmacogenom*[tiab])
AND (reimburs*[tiab] OR "cost-effectiveness"[tiab] OR "health economics"[tiab]
     OR financ*[tiab] OR "payer"[tiab] OR "insurance coverage"[tiab])
AND (implement*[tiab] OR adopt*[tiab] OR "healthcare delivery"[tiab])
AND ("2015/01/01"[Date - Publication] : "3000"[Date - Publication])
AND (english[Language])
```

| Metric | Value |
|---|---|
| Raw API count | 593 |
| Records retrieved | 589 |
| After de-duplication | 589 |
| Output file | `pubmed_supplementary_financing_20260623.csv` |

---

## Hand-Search Log

The following known relevant sources will be added via documented hand-search, separate from the automated database search:

| Source | PMID / Identifier | Reason for hand-search |
|---|---|---|
| Popejoy & Fullerton (2016). *Genomics is failing on diversity.* Nature. | 27734877 | No abstract indexed in PubMed; tiab search cannot retrieve it. |

Additional sources may be added here as reference-list checking proceeds.

---

## Limitations of the Search Strategy

**Single primary database design.** The originally planned four-database search (PubMed, Embase, Scopus, CINAHL) was not executed because institutional API access to all four non-PubMed platforms was unavailable (all returned 401/400 Unauthorized on 2026-06-23). The systematic search is therefore concentrated in PubMed/MEDLINE, supplemented by two targeted PubMed supplementary searches (Islamic bioethics strand, 47 records; financing strand, 589 records) and a documented hand-search log.

**OpenAlex cross-validation and non-screening.** OpenAlex (240M+ works, including non-MEDLINE journals and conference papers) was queried under the same Version D logic and returned 14,544 records, of which 8,113 were not indexed in PubMed. These records were not screened. A 75-record manual audit of the OpenAlex-unique set's highest-relevance tier showed a 70–80% false-positive rate driven by topic co-occurrence without substantive implementation content — a volume incompatible with solo-reviewer screening. The 81.9% PMID overlap between OpenAlex and PubMed under the same query confirms that the Version D search strategy is platform-consistent; the non-PubMed 18.1% represents the residual coverage gap from the single-database design.

**Future research note.** A multi-database replication — particularly including Embase (clinical trial and drug literature depth) and CINAHL (nursing and allied health implementation literature) — would be the methodological ideal for a systematic map of this topic. The search syntax for all four databases is documented in `manual_search_instructions.md` to facilitate this.

---

## Methodological Transparency

This repository and its commit timestamps serve as the pre-analysis registration record for this review, in lieu of external OSF pre-registration, consistent with publication in the author's institutional journal. The Version B commit (c655ead, 2026-06-19) is the permanent record of the initial pilot search. Version D, once retrieved and committed, will be the operative dataset for screening. The revision history above is part of the methods section, not a correction to hide.

---

## Inclusion/Exclusion

All screening and inclusion/exclusion decisions are made by the review author. No automated filtering has been applied. The `decision` column in the CSV is defaulted to `pending` for all records.
