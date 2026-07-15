#!/usr/bin/env python3
"""Snapshot every EXPOSED row to the Wayback Machine and write archive_url back to the catalog.

    ./tools/archive.py --dry-run       # say what would be submitted
    ./tools/archive.py                 # submit, then write the catalog back
    ./tools/archive.py --category protocols

This is the highest leverage script in the repo and it is also the most boring one, which is why it
has to be a command rather than a good intention. A vendor deletes a manual the week the product
goes obsolete, which is the exact week a field tech starts needing it. The snapshot has to exist
BEFORE that, and "before that" has no warning.

WRITE SAFETY. This rewrites catalog.csv, the one irreplaceable file here. It re reads the catalog
immediately before writing rather than trusting the copy it loaded minutes ago, because a snapshot
run takes a while and another session may have edited the catalog meanwhile. It writes to a temp
file and renames, so an interrupted run cannot leave a truncated catalog.
"""
import argparse
import csv
import os
import pathlib
import sys
import urllib.error
import urllib.request

ROOT = pathlib.Path(__file__).resolve().parent.parent
CATALOG = ROOT / "catalog" / "catalog.csv"
SAVE = "https://web.archive.org/save/"
UA = "industrial-index archiver (+https://github.com/Skeeter-spec/industrial-index)"

COLUMNS = [
    "id", "title", "vendor", "doc_number", "revision", "revision_date", "category",
    "url", "archive_url", "license", "redistributable", "local_path", "sha256",
    "verified_level", "verified_date", "notes",
]


def submit(url, timeout):
    """Ask the Wayback Machine to snapshot url. Returns the snapshot URL or None.

    The save endpoint redirects to the created snapshot, so the final URL after redirects is the
    answer. A 429 means rate limited, not failed: back off and rerun rather than recording nothing.
    """
    req = urllib.request.Request(SAVE + url, headers={"User-Agent": UA})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            final = resp.geturl()
            return final if "/web/" in final else None
    except urllib.error.HTTPError as e:
        if e.code == 429:
            print("    rate limited (429). Stop here and rerun later.")
            return "RATELIMIT"
        return None
    except Exception:
        return None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--category")
    ap.add_argument("--timeout", type=int, default=90)
    args = ap.parse_args()

    with CATALOG.open(newline="", encoding="utf-8") as fh:
        rows = list(csv.DictReader(fh))

    targets = [
        r for r in rows
        if not (r.get("archive_url") or "").strip()
        and (r.get("url") or "").strip()
        and (not args.category or r["category"] == args.category)
    ]

    if not targets:
        print("  nothing exposed. Every row with a url has a snapshot.")
        return 0

    print(f"  {len(targets)} row(s) exposed:")
    for r in targets:
        print(f"    {r['id']}")
    if args.dry_run:
        print("  --dry-run, nothing submitted")
        return 0

    got = {}
    for r in targets:
        print(f"  submitting {r['id']} ..")
        snap = submit(r["url"], args.timeout)
        if snap == "RATELIMIT":
            break
        if snap:
            got[r["id"]] = snap
            print(f"    ok {snap}")
        else:
            print("    no snapshot returned (leaving the row exposed rather than guessing)")

    if not got:
        print("  no snapshots taken, catalog untouched")
        return 1

    # Re read before writing. Another session may own this file now.
    with CATALOG.open(newline="", encoding="utf-8") as fh:
        fresh = list(csv.DictReader(fh))
    n = 0
    for r in fresh:
        if r["id"] in got and not (r.get("archive_url") or "").strip():
            r["archive_url"] = got[r["id"]]
            n += 1

    tmp = CATALOG.with_suffix(".csv.tmp")
    with tmp.open("w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=COLUMNS)
        w.writeheader()
        w.writerows(fresh)
    os.replace(tmp, CATALOG)
    print(f"  wrote {n} archive_url value(s) into the catalog")
    return 0


if __name__ == "__main__":
    sys.exit(main())
