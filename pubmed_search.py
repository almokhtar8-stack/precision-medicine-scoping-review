"""
PubMed/MEDLINE search for scoping review:
"Precision Medicine Implementation in Healthcare Systems"

Version B search structure: (Group 1) AND (Group 2 OR Group 3)
Filters: English, 2015-present

Retrieval strategy — PubMed esearch caps at 9,999 records per call.
Work-around: date-range chunking.
  Phase 1 — iterate year/month windows; each window runs esearch to collect PMIDs
  Phase 2 — POST-based efetch in batches of 200 using direct PMID lists (no WebEnv cap)
"""

import requests
import time
import calendar
import xml.etree.ElementTree as ET
import pandas as pd
import json
import sys
import os
from datetime import datetime, timezone

# ---------------------------------------------------------------------------
# Search terms (locked Version B — no date filter here; added per-chunk below)
# ---------------------------------------------------------------------------

G1 = (
    '("precision medicine"[tiab] OR "personalized medicine"[tiab] OR '
    '"personalised medicine"[tiab] OR "genomic medicine"[tiab] OR '
    'genomic*[tiab] OR pharmacogenom*[tiab] OR pharmacogenetic*[tiab] OR '
    '"precision health"[tiab] OR "precision oncology"[tiab] OR '
    '"Precision Medicine"[Mesh] OR "Pharmacogenetics"[Mesh] OR "Genomics"[Mesh])'
)

G2 = (
    '(implement*[tiab] OR adopt*[tiab] OR integrat*[tiab] OR '
    '"organizational readiness"[tiab] OR "organisational readiness"[tiab] OR '
    'readiness[tiab] OR "change management"[tiab] OR "healthcare delivery"[tiab] OR '
    '"health care delivery"[tiab] OR "service delivery"[tiab] OR '
    '"clinical workflow"[tiab] OR uptake[tiab] OR rollout[tiab] OR '
    '"scale up"[tiab] OR barrier*[tiab] OR facilitat*[tiab] OR enabler*[tiab])'
)

G3 = (
    '(governance[tiab] OR policy[tiab] OR policies[tiab] OR leadership[tiab] OR '
    'workforce[tiab] OR "human resources"[tiab] OR "digital infrastructure"[tiab] OR '
    'interoperab*[tiab] OR "decision support"[tiab] OR financ*[tiab] OR '
    'reimburs*[tiab] OR "cost-effectiveness"[tiab] OR equity[tiab] OR '
    'ethic*[tiab] OR sustainab*[tiab])'
)

# Base query without date filter (added per date-window chunk)
QUERY_BASE = f'{G1} AND ({G2} OR {G3}) AND (english[Language])'

# Full query with date filter (used only for the initial count)
QUERY_VERSION_B = (
    f'{G1} AND ({G2} OR {G3}) AND '
    f'("2015/01/01"[Date - Publication] : "3000"[Date - Publication]) AND '
    f'(english[Language])'
)

BASE_URL       = 'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/'
FETCH_BATCH    = 200    # records per efetch call
MAX_ESEARCH    = 9000   # conservative PubMed esearch ceiling (hard limit is 9,999)
RATE_DELAY     = 0.4    # ≤3 requests/sec without API key
CHECKPOINT     = 'pmid_checkpoint.json'   # resume file

RUN_DATE = datetime.now(timezone.utc).isoformat()

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _request(method: str, endpoint: str, *, params=None, data=None, timeout=60) -> requests.Response:
    """HTTP call with exponential-backoff retry on transient errors (5xx, timeout, connection)."""
    url = BASE_URL + endpoint
    for attempt in range(5):
        try:
            r = requests.request(method, url, params=params, data=data, timeout=timeout)
            if r.status_code in (429, 500, 502, 503, 504):
                wait = 2 ** attempt * 2
                print(f"  HTTP {r.status_code} — retrying in {wait}s (attempt {attempt + 1}/5) …",
                      file=sys.stderr)
                time.sleep(wait)
                continue
            r.raise_for_status()
            return r
        except (requests.exceptions.ConnectionError,
                requests.exceptions.Timeout) as e:
            wait = 2 ** attempt * 2
            print(f"  {type(e).__name__} — retrying in {wait}s (attempt {attempt + 1}/5) …",
                  file=sys.stderr)
            time.sleep(wait)
    raise RuntimeError(f"All 5 retries failed for {url}")


def _post(endpoint: str, data: dict, timeout: int = 60) -> requests.Response:
    return _request('POST', endpoint, data=data, timeout=timeout)


def _get(endpoint: str, params: dict, timeout: int = 60) -> requests.Response:
    return _request('GET', endpoint, params=params, timeout=timeout)


# ---------------------------------------------------------------------------
# Phase 0: initial count (for the log + summary comparison)
# ---------------------------------------------------------------------------

def get_count(query: str) -> int:
    print("Getting overall count …")
    r = _post('esearch.fcgi', {
        'db':      'pubmed',
        'term':    query,
        'retmax':  0,
        'retmode': 'json',
    })
    count = int(r.json()['esearchresult']['count'])
    print(f"  Raw hit count: {count:,}")
    print(f"  Run date UTC:  {RUN_DATE}")
    return count


# ---------------------------------------------------------------------------
# Phase 1: collect PMIDs via date-window chunking
# PubMed esearch limit = 9,999 records per call.
# Strategy: iterate year → if year count > MAX_ESEARCH, iterate month.
# ---------------------------------------------------------------------------

def _esearch_pmids(term: str) -> tuple[int, list[str]]:
    """Run one esearch POST; return (count, pmid_list)."""
    r = _post('esearch.fcgi', {
        'db':      'pubmed',
        'term':    term,
        'retmax':  MAX_ESEARCH,
        'retmode': 'json',
    })
    data = r.json()['esearchresult']
    if 'ERROR' in data:
        raise RuntimeError(f"NCBI esearch error: {data['ERROR']}")
    return int(data['count']), data['idlist']


def _year_term(year: int) -> str:
    return f'{QUERY_BASE} AND ("{year}/01/01"[Date - Publication] : "{year}/12/31"[Date - Publication])'


def _month_term(year: int, month: int) -> str:
    last_day = calendar.monthrange(year, month)[1]
    return (
        f'{QUERY_BASE} AND '
        f'("{year}/{month:02d}/01"[Date - Publication] : '
        f'"{year}/{month:02d}/{last_day}"[Date - Publication])'
    )


def collect_pmids_chunked(start_year: int = 2015, end_year: int = 2026) -> list[str]:
    """Collect all PMIDs by splitting into date windows that each stay under the cap.

    Writes a checkpoint file after each window so the run can resume if interrupted.
    On startup, if a checkpoint exists, already-processed windows are skipped.
    """
    # Load checkpoint
    checkpoint: dict = {}
    if os.path.exists(CHECKPOINT):
        with open(CHECKPOINT) as f:
            checkpoint = json.load(f)
        print(f"  Resuming from checkpoint ({len(checkpoint.get('pmids', []))} PMIDs so far)")

    all_pmids: set[str] = set(checkpoint.get('pmids', []))
    done_windows: set[str] = set(checkpoint.get('done', []))

    def _save_checkpoint():
        with open(CHECKPOINT, 'w') as f:
            json.dump({'pmids': list(all_pmids), 'done': list(done_windows)}, f)

    for year in range(start_year, end_year + 1):
        year_key = str(year)
        if year_key in done_windows:
            print(f"  {year}: already done (checkpoint) — skipping")
            continue

        year_term  = _year_term(year)
        year_count, year_pmids = _esearch_pmids(year_term)
        print(f"  {year}: {year_count:,} records", end="")
        time.sleep(RATE_DELAY)

        if year_count <= MAX_ESEARCH:
            all_pmids.update(year_pmids)
            done_windows.add(year_key)
            _save_checkpoint()
            print(f" → {len(year_pmids)} PMIDs collected")
        else:
            print(f" → too large, splitting by month …")
            for month in range(1, 13):
                month_key = f"{year}/{month:02d}"
                if month_key in done_windows:
                    print(f"    {month_key}: already done — skipping")
                    continue
                m_term = _month_term(year, month)
                m_count, m_pmids = _esearch_pmids(m_term)
                print(f"    {month_key}: {m_count:,} records → {len(m_pmids)} PMIDs")
                if m_count > MAX_ESEARCH:
                    print(f"    WARNING: {month_key} exceeds esearch cap ({m_count:,}). "
                          f"Only first {MAX_ESEARCH:,} PMIDs captured for this window.",
                          file=sys.stderr)
                all_pmids.update(m_pmids)
                done_windows.add(month_key)
                _save_checkpoint()
                time.sleep(RATE_DELAY)
            done_windows.add(year_key)
            _save_checkpoint()

    result = list(all_pmids)
    print(f"\nTotal unique PMIDs collected: {len(result):,}")
    return result


# ---------------------------------------------------------------------------
# Phase 2: efetch full records via POST — no WebEnv, no 10k cap
# ---------------------------------------------------------------------------

def _text(element, tag: str) -> str:
    node = element.find('.//' + tag)
    return (node.text or '').strip() if node is not None else ''


def _parse_article(node) -> dict:
    rec: dict = {}

    pmid_node = node.find('.//PMID')
    rec['pmid'] = pmid_node.text.strip() if pmid_node is not None else ''

    rec['title'] = _text(node, 'ArticleTitle')

    abstract_parts = node.findall('.//AbstractText')
    rec['abstract'] = ' '.join((p.text or '') for p in abstract_parts if p.text).strip()

    authors = []
    for author in node.findall('.//Author'):
        last  = _text(author, 'LastName')
        first = _text(author, 'ForeName')
        if last:
            authors.append(f"{last} {first}".strip())
    rec['authors'] = '; '.join(authors)

    year = _text(node, 'Year')
    if not year:
        md = _text(node, 'MedlineDate')
        year = md[:4] if md else ''
    rec['year'] = year

    rec['journal'] = _text(node, 'Title')
    return rec


def fetch_records_by_pmids(pmids: list[str]) -> list[dict]:
    n_batches = (len(pmids) + FETCH_BATCH - 1) // FETCH_BATCH
    print(f"\nFetching full records — {len(pmids):,} PMIDs, {n_batches} batches …")
    all_records: list[dict] = []

    for i in range(n_batches):
        batch = pmids[i * FETCH_BATCH:(i + 1) * FETCH_BATCH]
        pct   = (i / n_batches) * 100
        print(f"  Batch {i + 1}/{n_batches}  [{pct:.1f}%]  "
              f"({len(all_records):,} records so far)")

        try:
            r = _post('efetch.fcgi', {
                'db':      'pubmed',
                'id':      ','.join(batch),
                'rettype': 'xml',
                'retmode': 'xml',
            }, timeout=120)
            root = ET.fromstring(r.content)
            for article in root.findall('.//PubmedArticle'):
                try:
                    all_records.append(_parse_article(article))
                except Exception as e:
                    print(f"  Warning: skipped record — {e}", file=sys.stderr)
        except Exception as e:
            print(f"  ERROR on batch {i + 1}: {e}", file=sys.stderr)
            print("  Records in this batch skipped.", file=sys.stderr)

        time.sleep(RATE_DELAY)

    return all_records


# ---------------------------------------------------------------------------
# Phase 3: de-duplicate, add decision column, save CSV
# ---------------------------------------------------------------------------

def build_csv(records: list[dict], out_path: str) -> pd.DataFrame:
    df = pd.DataFrame(records, columns=['pmid', 'title', 'abstract', 'authors', 'year', 'journal'])
    before = len(df)
    df.drop_duplicates(subset='pmid', keep='first', inplace=True)
    after  = len(df)
    diff   = before - after
    if diff:
        print(f"\nDe-duplicated: {before:,} → {after:,} ({diff:,} duplicates removed)")
    else:
        print(f"\nNo duplicates ({after:,} records).")
    df['decision'] = 'pending'
    df.to_csv(out_path, index=False, encoding='utf-8-sig')
    print(f"Saved: {out_path}")
    return df


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

if __name__ == '__main__':
    today      = datetime.now().strftime('%Y%m%d')
    OUTPUT_CSV = f'pubmed_results_{today}.csv'
    LOG_FILE   = f'pubmed_run_log_{today}.json'

    # 0. Total count (informational)
    raw_count = get_count(QUERY_VERSION_B)

    # 1. Collect PMIDs via date-window chunking
    print("\n--- Phase 1: PMID collection ---")
    pmids = collect_pmids_chunked(start_year=2015, end_year=2026)

    # 2. Fetch records
    print("\n--- Phase 2: Full record retrieval ---")
    records = fetch_records_by_pmids(pmids)

    # 3. Save
    print("\n--- Phase 3: CSV export ---")
    df = build_csv(records, OUTPUT_CSV)

    # 4. Audit log
    log = {
        'run_date_utc':       RUN_DATE,
        'query_version':      'Version B',
        'database':           'PubMed/MEDLINE',
        'filters':            'English, 2015-present',
        'raw_hit_count':      raw_count,
        'pmids_collected':    len(pmids),
        'retrieved_count':    len(records),
        'deduplicated_count': int(len(df)),
        'output_file':        OUTPUT_CSV,
        'query_string':       QUERY_VERSION_B,
        'retrieval_method':   'date-window esearch + POST efetch (bypasses 9999/10000 caps)',
    }
    with open(LOG_FILE, 'w') as f:
        json.dump(log, f, indent=2)
    print(f"Run log: {LOG_FILE}")

    # 5. Human-readable summary
    print("\n" + "=" * 60)
    print("SUMMARY")
    print(f"  Raw API count (esearch, no limit):  {raw_count:,}")
    print(f"  PMIDs collected (chunked esearch):  {len(pmids):,}")
    print(f"  Retrieved records (efetch):         {len(records):,}")
    print(f"  After de-duplication:               {int(len(df)):,}")
    print(f"  Output CSV:                         {OUTPUT_CSV}")
    print("=" * 60)
