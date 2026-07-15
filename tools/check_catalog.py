#!/usr/bin/env python3
"""Validate catalog.csv against catalog/SCHEMA.md.

    ./tools/check_catalog.py

TWO TIERS, AND THE SPLIT IS THE WHOLE DESIGN.

  ERRORS   exit 1. The row makes a claim that is WRONG. A bad license clearance, a hash that does
           not match, a level outside the vocabulary, a duplicate id.
  UNFINISHED  exit 0, counted and printed. The row has not made the claim YET. No snapshot, still
           LOCATED ONLY, no revision recorded.

power-service-toolbox's gate fails hard on everything, and that is right for it: there are ten
projects and a project either reproduces its worked example or it does not. This catalog will have
hundreds of rows and most of them will be half done most of the time. A gate that goes red on day
one and stays red is not a gate, it is a light nobody looks at, and the first thing it teaches is
that red means nothing here.

So: wrong is fatal, incomplete is visible. Incomplete work is the normal state of a catalog.
Incorrect work is the one thing this repo cannot survive, because the entire value proposition is
that the row is true.
"""
import csv
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
CATALOG = ROOT / "catalog" / "catalog.csv"
DOMAINS = ROOT / "domains"

COLUMNS = [
    "id", "title", "vendor", "doc_number", "revision", "revision_date", "category",
    "url", "archive_url", "license", "redistributable", "local_path", "sha256",
    "verified_level", "verified_date", "notes",
]

REQUIRED = [
    "id", "title", "vendor", "doc_number", "revision", "category", "url",
    "license", "redistributable", "verified_level", "verified_date",
]

LEVELS = {
    "TRACED", "READ IN FULL", "FETCHED, NOT READ",
    "LOCATED ONLY", "CITED, UNREAD", "GATED, UNREAD",
}

# A level that means the content was never confirmed. A row at one of these cannot also claim to
# have been mirrored: you cannot have the file and not have fetched it.
UNOPENED = {"LOCATED ONLY", "CITED, UNREAD", "GATED, UNREAD"}

ID_RE = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
SHA_RE = re.compile(r"^[a-f0-9]{64}$")

# "free" is not a license. Neither is "free to download", which is the single most common way a
# redistribution mistake gets made: the reader conflates the price with the grant. If a vendor
# genuinely grants redistribution they say so in words you can quote, so require quotable words.
NON_LICENSES = {
    "", "unknown", "free", "free to download", "freely available", "public",
    "open", "n/a", "none", "tbd",
}


def domains():
    if not DOMAINS.is_dir():
        return set()
    return {p.name for p in DOMAINS.iterdir() if p.is_dir()}


def main():
    if not CATALOG.exists():
        print(f"  FAIL catalog/catalog.csv missing. Run ./tools/seed_catalog.py")
        return 1

    with CATALOG.open(newline="", encoding="utf-8") as fh:
        reader = csv.DictReader(fh)
        if reader.fieldnames != COLUMNS:
            print("  FAIL header does not match SCHEMA.md")
            print(f"       expected: {COLUMNS}")
            print(f"       found:    {reader.fieldnames}")
            return 1
        rows = list(reader)

    known = domains()
    errors, unfinished = [], []
    seen_ids = {}

    for n, row in enumerate(rows, start=2):  # header is line 1
        rid = (row.get("id") or "").strip()
        where = f"line {n} ({rid or 'no id'})"

        for col in REQUIRED:
            if not (row.get(col) or "").strip():
                errors.append(f"{where}: required column '{col}' is empty")

        if rid and not ID_RE.match(rid):
            errors.append(f"{where}: id is not a lowercase slug")
        if rid in seen_ids:
            errors.append(f"{where}: duplicate id, first seen at line {seen_ids[rid]}")
        elif rid:
            seen_ids[rid] = n

        cat = (row.get("category") or "").strip()
        if cat and known and cat not in known:
            errors.append(f"{where}: category '{cat}' is not a directory under domains/")

        level = (row.get("verified_level") or "").strip()
        if level and level not in LEVELS:
            errors.append(f"{where}: verified_level '{level}' is not in the vocabulary")

        url = (row.get("url") or "").strip()
        if url and not url.startswith(("http://", "https://")):
            errors.append(f"{where}: url is not http(s)")

        for col in ("revision_date", "verified_date"):
            v = (row.get(col) or "").strip()
            if v and not DATE_RE.match(v):
                errors.append(f"{where}: {col} '{v}' is not an ISO date")

        redist = (row.get("redistributable") or "").strip().lower()
        if redist not in ("yes", "no"):
            errors.append(f"{where}: redistributable must be yes or no, found '{redist}'")

        lic = (row.get("license") or "").strip().lower()
        local = (row.get("local_path") or "").strip()
        sha = (row.get("sha256") or "").strip()

        # The legal invariants. These are the reason this checker exists at all.
        if redist == "yes" and lic in NON_LICENSES:
            errors.append(
                f"{where}: redistributable=yes but license is '{row.get('license')}'. "
                f"Name the terms or set it to no.")
        if local and redist != "yes":
            errors.append(
                f"{where}: local_path is set but redistributable is not yes. "
                f"That file must not be committed.")
        if local and not local.startswith("mirrors/"):
            errors.append(f"{where}: local_path must be under mirrors/")
        if local and not sha:
            errors.append(f"{where}: local_path set but sha256 empty")
        if sha and not SHA_RE.match(sha):
            errors.append(f"{where}: sha256 is not a 64 char hex digest")
        if sha and not local:
            errors.append(f"{where}: sha256 set but local_path empty")
        if local and level in UNOPENED:
            errors.append(
                f"{where}: mirrored at level '{level}'. You have the file; that is at least "
                f"FETCHED, NOT READ.")

        # Unfinished. Not wrong, just not done.
        if not (row.get("archive_url") or "").strip():
            unfinished.append(f"{rid}: no archive_url")
        if level == "LOCATED ONLY":
            unfinished.append(f"{rid}: content still unverified")

    print(f"  {len(rows)} rows, {len(seen_ids)} unique ids")

    for e in errors:
        print(f"  FAIL {e}")

    if unfinished:
        print(f"  {len(unfinished)} unfinished (not a failure, just not done):")
        for u in unfinished[:8]:
            print(f"       .. {u}")
        if len(unfinished) > 8:
            print(f"       .. and {len(unfinished) - 8} more")

    if errors:
        print(f"  {len(errors)} ERRORS. A row is claiming something untrue.")
        return 1
    print("  OK   no row claims anything it has not earned")
    return 0


if __name__ == "__main__":
    sys.exit(main())
