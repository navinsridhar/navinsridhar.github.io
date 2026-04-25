#!/usr/bin/env python3
"""
sync_ads_library.py
-------------------
Pull the BibTeX export of a public NASA ADS library and append any
*new* entries to ``_bibliography/papers.bib`` so we never miss a paper
appearing on ADS.

Design choices
==============

* We do not overwrite curated entries. The existing file uses custom
  bib keys (e.g. ``sridhar2025corona``), custom journal macros
  (``apj``, ``mnras``, ...), and a ``category = {first|secondthird|nth|
  books|atel}`` field per entry that drives the publications page.
  Overwriting from ADS would destroy all of that.

* Instead, we fingerprint each entry by its 19-character ADS bibcode.
  Existing entries already record the bibcode either in the
  ``html = {https://ui.adsabs.harvard.edu/abs/<BIBCODE>}`` field or as
  the entry key. We diff the ADS library against that set; truly-new
  bibcodes get appended to the bottom of ``papers.bib`` under a
  ``Pending categorization`` separator with ``category = {pending}``.

* ``category = {pending}`` is intentionally not rendered by
  ``_pages/publications.md`` (which only queries first/secondthird/nth/
  books/atel). The user can then move the entry into the correct
  section by hand.

Usage
=====

    ADS_API_TOKEN=... python scripts/sync_ads_library.py \\
        --library-id AspXr7NhTAaWjzQzWm-Kuw \\
        --bib _bibliography/papers.bib

If there is nothing new the script exits 0 with no changes. If there
*are* new entries, it writes them in-place and prints the new bibcodes
to stdout. The wrapping GitHub Actions workflow is in charge of
deciding whether to commit / open a PR.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
import time
import urllib.error
import urllib.request
from typing import Iterable

ADS_API_BASE = "https://api.adsabs.harvard.edu/v1"

# 19-char ADS bibcode, e.g. 2025ApJ...979..199S, 2021MNRAS.507.5625S
BIBCODE_RE = re.compile(r"\b(\d{4}[A-Za-z\.&]{5}[\dA-Z\.]{9}[A-Z])\b")


def http_request(
    url: str,
    *,
    token: str,
    method: str = "GET",
    payload: dict | None = None,
    timeout: int = 60,
) -> dict:
    """Tiny wrapper around urllib that raises on non-2xx and returns JSON."""

    data = None
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
        "Accept": "application/json",
    }
    if payload is not None:
        data = json.dumps(payload).encode("utf-8")

    req = urllib.request.Request(url, data=data, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            body = resp.read().decode("utf-8")
    except urllib.error.HTTPError as exc:
        body = exc.read().decode("utf-8", errors="replace")
        raise RuntimeError(
            f"HTTP {exc.code} from {url}\n{body[:2000]}"
        ) from exc
    return json.loads(body)


def fetch_library_bibcodes(library_id: str, token: str) -> list[str]:
    """Page through the library and return the full list of bibcodes."""

    bibcodes: list[str] = []
    start = 0
    rows = 1000
    while True:
        url = (
            f"{ADS_API_BASE}/biblib/libraries/{library_id}"
            f"?start={start}&rows={rows}"
        )
        payload = http_request(url, token=token)
        # The library endpoint returns either {"documents": [...]} or
        # {"solr": {"response": {"docs": [...]}}} depending on the call;
        # be permissive.
        page: list[str] = []
        if isinstance(payload.get("documents"), list):
            page = list(payload["documents"])
        elif isinstance(payload.get("solr"), dict):
            docs = payload["solr"].get("response", {}).get("docs", [])
            page = [d.get("bibcode") for d in docs if d.get("bibcode")]
        if not page:
            break
        bibcodes.extend(page)
        if len(page) < rows:
            break
        start += rows
        # Be polite to ADS rate limits.
        time.sleep(0.3)
    # Deduplicate while preserving order.
    seen: set[str] = set()
    ordered: list[str] = []
    for b in bibcodes:
        if b not in seen:
            seen.add(b)
            ordered.append(b)
    return ordered


def export_bibtex(bibcodes: list[str], token: str) -> str:
    """Ask ADS to format the given bibcodes as BibTeX."""

    if not bibcodes:
        return ""
    # ADS allows up to ~2000 bibcodes per /export/bibtex call.
    out_chunks: list[str] = []
    chunk_size = 500
    for i in range(0, len(bibcodes), chunk_size):
        chunk = bibcodes[i : i + chunk_size]
        url = f"{ADS_API_BASE}/export/bibtex"
        payload = http_request(
            url,
            token=token,
            method="POST",
            payload={"bibcode": chunk, "sort": "date desc"},
        )
        export = payload.get("export") or ""
        if export:
            out_chunks.append(export)
        time.sleep(0.3)
    return "\n\n".join(out_chunks)


def split_bibtex_entries(text: str) -> list[str]:
    """Split a BibTeX blob into individual ``@type{...}`` entries."""

    entries: list[str] = []
    depth = 0
    start: int | None = None
    for i, ch in enumerate(text):
        if ch == "@" and depth == 0 and (i == 0 or text[i - 1] in "\n\r"):
            start = i
        if start is None:
            continue
        if ch == "{":
            depth += 1
        elif ch == "}":
            depth -= 1
            if depth == 0:
                entries.append(text[start : i + 1])
                start = None
    return entries


def existing_bibcodes(bib_text: str) -> set[str]:
    """Pull every ADS bibcode that already appears in ``papers.bib``."""

    return set(BIBCODE_RE.findall(bib_text))


def annotate_entry(entry: str) -> str:
    """Add ``category = {pending}`` to a fresh ADS entry if missing."""

    if re.search(r"\bcategory\s*=", entry):
        return entry
    # Insert category just before the closing brace of the entry.
    # Find the last '}' which closes the @article{...}.
    last_brace = entry.rfind("}")
    if last_brace == -1:
        return entry
    head = entry[:last_brace].rstrip()
    if not head.endswith(","):
        head = head + ","
    return head + "\n  category = {pending}\n}"


def append_pending_entries(bib_path: str, new_entries: Iterable[str]) -> int:
    """Append entries to ``papers.bib`` under a Pending separator. Returns count."""

    new_entries = list(new_entries)
    if not new_entries:
        return 0

    with open(bib_path, "r", encoding="utf-8") as fh:
        current = fh.read()

    block_marker = "% Pending categorization (auto-added from ADS library)"
    addition = "\n\n".join(annotate_entry(e.strip()) for e in new_entries)

    if block_marker in current:
        # Append below the existing pending block, before EOF.
        new_text = current.rstrip() + "\n\n" + addition + "\n"
    else:
        new_text = (
            current.rstrip()
            + "\n\n"
            + "% ============================================================\n"
            + block_marker + "\n"
            + "% Move each entry into the appropriate section above and\n"
            + "% replace category={pending} with first/secondthird/nth/books/atel.\n"
            + "% ============================================================\n\n"
            + addition
            + "\n"
        )
    with open(bib_path, "w", encoding="utf-8") as fh:
        fh.write(new_text)
    return len(new_entries)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--library-id", required=True, help="ADS public library id")
    parser.add_argument("--bib", required=True, help="Path to papers.bib")
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print what would be added without writing the file.",
    )
    args = parser.parse_args()

    token = os.environ.get("ADS_API_TOKEN", "").strip()
    if not token:
        print(
            "ERROR: ADS_API_TOKEN env var is empty. Generate one at "
            "https://ui.adsabs.harvard.edu/user/settings/token and add it as "
            "a repository secret.",
            file=sys.stderr,
        )
        return 2

    print(f"Fetching bibcodes for ADS library {args.library_id} …")
    library_bibcodes = fetch_library_bibcodes(args.library_id, token)
    print(f"  library reports {len(library_bibcodes)} entries")

    with open(args.bib, "r", encoding="utf-8") as fh:
        bib_text = fh.read()
    have = existing_bibcodes(bib_text)
    print(f"  papers.bib already references {len(have)} bibcodes")

    new_codes = [b for b in library_bibcodes if b not in have]
    if not new_codes:
        print("Nothing new — exiting.")
        return 0

    print(f"  {len(new_codes)} new bibcode(s) to fetch:")
    for b in new_codes:
        print(f"    - {b}")

    bibtex = export_bibtex(new_codes, token)
    entries = split_bibtex_entries(bibtex)
    if not entries:
        print(
            "WARN: ADS export returned no entries despite reporting new bibcodes.",
            file=sys.stderr,
        )
        return 0

    if args.dry_run:
        print("\n--- dry run; would append ---\n")
        for e in entries:
            print(annotate_entry(e.strip()))
            print()
        return 0

    n = append_pending_entries(args.bib, entries)
    print(f"Appended {n} entr{'y' if n == 1 else 'ies'} under a "
          "'Pending categorization' block.")
    # Emit machine-readable counts for the wrapping workflow.
    gh_out = os.environ.get("GITHUB_OUTPUT")
    if gh_out:
        with open(gh_out, "a", encoding="utf-8") as fh:
            fh.write(f"new_count={n}\n")
            fh.write("new_bibcodes<<EOF\n")
            for b in new_codes:
                fh.write(b + "\n")
            fh.write("EOF\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
