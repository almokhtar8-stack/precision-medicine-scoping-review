# Manual Search Instructions — Remaining Databases
## Precision Medicine Implementation in Healthcare Systems (Scoping Review)

**Prepared:** 2026-06-23  
**Based on:** Version D query (PubMed count: 7,895; retrieved: 7,847)  
**Applies to:** Embase, Scopus, Web of Science, CINAHL

All queries below are direct translations of Version D's G1 AND G2 logic into each platform's native syntax. Apply the same filters throughout: **English language, publication date 2015–present**.

---

## API Status Summary

| Database | Provider | API Access | Status |
|---|---|---|---|
| Embase | Elsevier | `api.elsevier.com` | **401 Unauthorized** — institutional API key required, no free tier |
| Scopus | Elsevier | `api.elsevier.com` | **401 Unauthorized** — API key required; free registration at dev.elsevier.com gives limited metadata access; full records need institutional subscription |
| Web of Science | Clarivate | `api.clarivate.com/apis/wos-starter` | **401 Unauthorized** — API key required; **free Starter API available** (1,000 records/week) at developer.clarivate.com — viable if WoS count < 1,000 |
| CINAHL (EBSCOhost) | EBSCO | `eds-api.ebscohost.com` | **400/401** — institutional EDS credentials required, no free tier |

**Recommended path:**  
1. Register for Clarivate's free WoS Starter API at developer.clarivate.com — if the WoS count falls under 1,000 records, provide the API key and the full retrieval can be run programmatically in this session, same pipeline as PubMed.  
2. For Scopus: register at dev.elsevier.com for a free API key; if running from Midocean's institutional network or VPN, it may inherit subscription access for full records.  
3. Embase and CINAHL: manual execution via the web interfaces below is the most reliable path without institutional IT involvement.

---

## 1. Embase (embase.com — requires institutional login)

**Platform:** embase.com → Advanced Search → Expert Search

Copy and paste the following into the Expert Search box as a single query:

```
('precision medicine':ti,ab OR 'personalized medicine':ti,ab OR
'personalised medicine':ti,ab OR pharmacogenom*:ti,ab OR
pharmacogenetic*:ti,ab)
AND
(implement*:ti,ab OR 'organizational readiness':ti,ab OR
'organisational readiness':ti,ab OR 'change management':ti,ab OR
'clinical workflow':ti,ab OR 'scale up':ti,ab OR rollout:ti,ab)
AND [english]/lim
AND [2015-2026]/py
```

**After running:**
1. Note the total hit count.
2. Export all results: Results → Export → CSV → select fields: Title, Authors, Source, Abstract, Year, DOI, Embase Accession Number.
3. Save file as `embase_vD_YYYYMMDD.csv` and send/upload to this session for de-duplication and commit.

**Note on Emtree MeSH equivalents:** Embase has its own controlled vocabulary (Emtree). The query above uses title/abstract (`ti,ab`) terms only, consistent with PubMed Version D which dropped MeSH after the pilot. If your institution's Embase librarian suggests adding Emtree terms for 'precision medicine' (`exp precision medicine/`) or 'pharmacogenomics' (`exp pharmacogenomics/`), that is a legitimate enhancement — document any addition in the protocol.

---

## 2. Scopus (scopus.com — requires institutional login)

**Platform:** scopus.com → Search → Advanced Search

Paste the following into the Advanced Search query box:

```
( TITLE-ABS-KEY ( "precision medicine"  OR  "personalized medicine"  OR
"personalised medicine"  OR  pharmacogenom*  OR  pharmacogenetic* ) )
AND
( TITLE-ABS-KEY ( implement*  OR  "organizational readiness"  OR
"organisational readiness"  OR  "change management"  OR
"clinical workflow"  OR  "scale up"  OR  rollout ) )
```

Then apply **Document filters** (sidebar):
- Date range: **2015 – Present**
- Language: **English**
- Document type: (leave all checked — Scopus mixes article types; filter during screening)

**After running:**
1. Note the total hit count.
2. Export: Export → CSV → select Abstract & keywords, Author info, Title, Year, Source title, DOI.
3. Save as `scopus_vD_YYYYMMDD.csv`.

**Scopus API alternative:** If you obtain a free API key from dev.elsevier.com (personal account, no institutional subscription needed for metadata), provide the key and the retrieval can be run programmatically. The free tier returns 25 results per call with pagination; for counts under ~5,000 this is feasible but slow. For counts above that, the web export is faster.

---

## 3. Web of Science (webofscience.com — requires institutional login)

**Platform:** webofscience.com → Advanced Search

Paste into the Advanced Search query box:

```
TS=("precision medicine" OR "personalized medicine" OR "personalised medicine" OR pharmacogenom* OR pharmacogenetic*)
AND
TS=(implement* OR "organizational readiness" OR "organisational readiness" OR "change management" OR "clinical workflow" OR "scale up" OR rollout)
```

Then apply filters (right-hand panel):
- Publication Years: **2015 – 2026**
- Languages: **English**
- Web of Science Core Collection databases (default): All — leave as-is

**TS= note:** TS = Topic field in WoS, which searches Title + Abstract + Author Keywords + Keywords Plus. This is slightly broader than PubMed `[tiab]` because it includes Keywords Plus (algorithmically generated). Acceptable for a scoping review; note in methods if the librarian flags it.

**After running:**
1. Note the total hit count.
2. Export (up to 500 per export batch, repeat if needed): Export → Tab-delimited → Full Record.
3. Combine batches and save as `wos_vD_YYYYMMDD.csv`.

**WoS Starter API alternative:** Register for a free API key at developer.clarivate.com (no institutional affiliation required, limit: 1,000 records/week). If your WoS hit count is under 1,000, provide the key and the full retrieval can be run programmatically in this session. If the count exceeds 1,000, institutional API access is needed or the manual export above suffices.

---

## 4. CINAHL (EBSCOhost — requires institutional login via Midocean library portal)

**Platform:** EBSCOhost → CINAHL Complete → Advanced Search → Search in: Abstract (or use the field tag method below)

**Option A — Guided interface (recommended for first-time use):**

Use three separate search rows in the EBSCOhost Advanced Search form:

| Row | Search Term | Field |
|---|---|---|
| 1 | `"precision medicine" OR "personalized medicine" OR "personalised medicine" OR pharmacogenom* OR pharmacogenetic*` | TX All Text |
| 2 | `implement* OR "organizational readiness" OR "organisational readiness" OR "change management" OR "clinical workflow" OR "scale up" OR rollout` | TX All Text |
| 3 | (connect with AND) | |

Apply limiters: **Language: English**, **Published Date: 2015-01-01 to 2026-12-31**

**Option B — Expert / command-line search (paste as one block):**

```
TX ("precision medicine" OR "personalized medicine" OR "personalised medicine" OR pharmacogenom* OR pharmacogenetic*)
AND TX (implement* OR "organizational readiness" OR "organisational readiness" OR "change management" OR "clinical workflow" OR "scale up" OR rollout)
```

Limiters: Published 2015–2026, Language = English

**TX vs. TI/AB note:** CINAHL's TX field searches title, abstract, subject headings, and keywords — slightly broader than `[tiab]`. To match PubMed `[tiab]` exactly, replace TX with `(TI X OR AB X)` for every term. This is more precise but the query becomes very long. TX is the standard CINAHL practice and is citable as such.

**After running:**
1. Note the total hit count.
2. Export: Share → E-mail → choose CSV format. For large result sets (>500), use the Folder/export-all function. Save as `cinahl_vD_YYYYMMDD.csv`.

---

## Recording Results

Once you have CSV exports from any of these databases, paste them into this Claude Code session with the instruction: "de-duplicate and commit Embase/Scopus/WoS/CINAHL results." The pipeline will:
1. De-duplicate within each source by identifier (DOI preferred over title-matching for non-PubMed sources).
2. Cross-de-duplicate against PubMed Version D by DOI and title.
3. Save each source as a separate labeled file (not merged into Version D).
4. Commit all new files as a continuation of the existing commit history.
