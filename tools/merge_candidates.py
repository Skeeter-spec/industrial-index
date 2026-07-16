#!/usr/bin/env python3
"""Turn proposed candidate documents into catalog rows, but only the ones that survive a fetch.

    ./tools/merge_candidates.py --dry-run          # say what would land and what would be rejected
    ./tools/merge_candidates.py                    # fetch, filter, write the survivors into the catalog
    ./tools/merge_candidates.py --staging DIR      # default: catalog/_incoming/

Input is a directory of JSON files, each an array of candidate objects. Where they came from is not
this script's business: a research agent, a vendor's index page, an afternoon of bookmarks. What
matters is that a candidate is a CLAIM and a row is a RECORD, and the only thing standing between
them should be a measurement rather than a good mood.

WHY THIS EXISTS, and it is not tidiness.

This repo measured its own seed data. Twelve rows were written from memory by someone who knew the
subject, every one of them plausible, and FOUR WERE 404. Not obscure documents, not typos: one
publisher had restructured its site and the other failures were the checker itself lying. A third of
confident recall was wrong, and none of it looked wrong.

So the rule this file enforces is the whole repo in one line: **a URL nobody fetched does not become
a row.** Not a row with a caveat, not a row at a lower level. Not a row.

That is also what makes it safe to source candidates in bulk from something that can be confidently
wrong. Let the proposer propose. Nothing it says about reachability is load bearing, because this
script does not believe any of it: it re fetches every URL itself and the fetch is the only vote
that counts. A rejected candidate costs nothing. A bad row costs the reader's trust in every other
row, which is the only asset here.

WHAT IT WILL NOT DO

Everything lands at LOCATED ONLY, which means exactly what the schema says: the URL is confirmed
reachable and the CONTENT IS UNVERIFIED. A machine fetched a file. Nobody read it. Promoting a row
above LOCATED ONLY is a human act and this script must never do it, because the moment a level can
be earned automatically it stops being a claim about knowledge and starts being a claim about
plumbing, and then the one column this repo runs on means nothing.

Rejects are written out with their reason. They are not failures, they are the system working, and
they are worth reading: a 404 in this file is usually a publisher having moved something.
"""
import argparse
import csv
import datetime
import importlib.util
import json
import os
import pathlib
import re
import sys
import urllib.parse
import urllib.request

WAYBACK_API = "https://archive.org/wayback/available?url="
# archive.org answers a bare urllib request with an HTTPError. That reads exactly like "no snapshot
# exists" and is not: it is a user agent check. Measured 2026-07-15, after it nearly cost two real
# documents.
BROWSER_UA = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
              "(KHTML, like Gecko) Chrome/120.0 Safari/537.36")


def wayback(url, timeout=30):
    """The closest Wayback snapshot of url, or None.

    A dead canonical is not automatically a dead row. `check_links.py` already names the state:
    ROTTED means the publisher deleted it and the snapshot holds, and it calls that the system
    SUCCEEDING, because the whole reason archive_url is mandatory is the day the vendor deletes the
    manual for the obsolete equipment that is still racked and still running.

    So a candidate whose URL 404s gets one more question asked of it before rejection: did this
    document ever exist? A snapshot is evidence that it did. This does NOT soften the gate. A URL
    somebody hallucinated was never live, so nothing ever archived it, and it still gets rejected.
    """
    req = urllib.request.Request(WAYBACK_API + urllib.parse.quote(url, safe=""),
                                 headers={"User-Agent": BROWSER_UA})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            data = json.loads(r.read())
    except Exception:
        return None
    snap = (data.get("archived_snapshots") or {}).get("closest") or {}
    if snap.get("available") and str(snap.get("status")) == "200" and snap.get("url"):
        return snap["url"].replace("http://web.archive.org", "https://web.archive.org")
    return None

ROOT = pathlib.Path(__file__).resolve().parent.parent
CATALOG = ROOT / "catalog" / "catalog.csv"
STAGING = ROOT / "catalog" / "_incoming"

COLUMNS = [
    "id", "title", "vendor", "doc_number", "revision", "revision_date", "category",
    "url", "archive_url", "license", "redistributable", "license_basis", "local_path", "sha256",
    "verified_level", "verified_date", "notes",
]

NON_LICENSES = {
    "", "unknown", "free", "free to download", "freely available", "public",
    "open", "n/a", "none", "tbd",
}


def _load_reachable():
    """Borrow check_links.reachable rather than writing a second one.

    Two functions that decide "is this URL alive" is two functions that will disagree, and the one
    that is wrong will be the one nobody is looking at. That function also already carries a
    measured lesson this one would otherwise have to learn again the hard way: modbus.org and
    nvlpubs.nist.gov both answer a HEAD with 404 and a GET with 200 on the identical URL, so a
    failing HEAD proves nothing and is always retried with a GET.
    """
    spec = importlib.util.spec_from_file_location("check_links", ROOT / "tools" / "check_links.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod.reachable


def slug(s):
    s = re.sub(r"[^a-z0-9]+", "-", (s or "").lower())
    return re.sub(r"-+", "-", s).strip("-")


def make_id(c, taken):
    """vendor-docnumber-rev, per the schema. Falls back to the title when there is no number."""
    vendor = slug(c.get("vendor"))
    num = slug(c.get("doc_number"))
    rev = slug(c.get("revision"))
    parts = [p for p in (vendor, num if num not in ("", "n-a") else "", rev if rev not in ("", "n-a") else "") if p]
    if len(parts) < 2:
        # Strip AFTER the truncation, not before: cutting a slug at a fixed width lands on a
        # separator often enough, and "...-configurations-" is not a lowercase slug. The gate
        # caught this on the first row that had no doc number and a long title.
        parts = [p for p in (vendor, slug(c.get("title"))[:60].strip("-")) if p]
    base = "-".join(parts) or "row"
    rid, n = base, 2
    while rid in taken:            # never reuse, never renumber an existing one
        rid = f"{base}-{n}"
        n += 1
    return rid


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--staging", default=str(STAGING))
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--timeout", type=int, default=30)
    args = ap.parse_args()

    reachable = _load_reachable()
    today = datetime.date.today().isoformat()

    staging = pathlib.Path(args.staging)
    files = sorted(staging.glob("*.json")) if staging.is_dir() else []
    if not files:
        print(f"  no candidate files in {staging}")
        return 0

    with CATALOG.open(newline="", encoding="utf-8") as fh:
        existing = list(csv.DictReader(fh))
    taken = {r["id"] for r in existing}
    # Normalize for dedupe: the same document reached by http and https is the same document.
    seen_urls = {re.sub(r"^https?://", "", (r["url"] or "").strip().rstrip("/").lower()) for r in existing}

    candidates = []
    for f in files:
        try:
            data = json.loads(f.read_text())
        except Exception as e:
            print(f"  SKIP {f.name}: not readable JSON ({e})")
            continue
        if not isinstance(data, list):
            print(f"  SKIP {f.name}: expected a JSON array")
            continue
        for c in data:
            c["_src"] = f.stem
            candidates.append(c)
    print(f"  {len(candidates)} candidate(s) from {len(files)} file(s)\n")

    landed, rejects = [], []
    for c in candidates:
        url = (c.get("url") or "").strip()
        title = (c.get("title") or "").strip()
        cat = (c.get("category") or c.get("_src") or "").strip()
        why = None

        if not url or not title:
            why = "missing url or title"
        elif not url.startswith(("http://", "https://")):
            why = "url is not http(s)"
        elif not (ROOT / "domains" / cat).is_dir():
            why = f"category '{cat}' is not a domain"
        else:
            key = re.sub(r"^https?://", "", url.rstrip("/").lower())
            if key in seen_urls:
                why = "already in the catalog"

        if why:
            rejects.append((c, why, ""))
            print(f"  reject  {title[:52]:52s} {why}")
            continue

        live, code = reachable(url, args.timeout)     # the only vote that counts
        snap = ""
        if not live:
            # Dead canonical. Ask the one question that separates a deleted document from an
            # invented one, and let the answer decide.
            snap = wayback(url) or ""
            if not snap:
                rejects.append((c, "did not fetch", code))
                print(f"  DEAD    {title[:52]:52s} [{code}]  <- proposed, not real")
                continue
            print(f"  ROTTED  {title[:52]:52s} [{code}] canonical gone, snapshot holds")

        note = (c.get("notes") or "").strip()

        # `redistributable` is a two value column and a candidate will hand you an essay. Measured
        # 2026-07-16: a batch arrived with "yes (per apache-2.0 terms; standard attribution/notice
        # conditions apply)" and "conditional -- cc by-nc-nd 4.0 permits sharing the unmodified work
        # with attribution for non-commercial purposes only; no derivatives". Both are BETTER
        # thinking than a bare yes, and both are unusable as a value: the old code lowercased the
        # essay and compared it to "yes", which never matched, so the NON_LICENSES guard below could
        # not fire and the essay went into the column. The gate caught it. The gate should not have
        # had to.
        #
        # Take the leading token and keep the reasoning in notes, because the reasoning is the part
        # worth having. Anything that does not START with yes becomes no, which is the schema's
        # default and the safe direction: "conditional" is not a yes.
        redist_raw = (c.get("redistributable") or "no").strip()
        redist = "yes" if redist_raw.lower().startswith("yes") else "no"
        if redist_raw.lower() not in ("yes", "no"):
            note = f"{note} Candidate stated redistributable as: {redist_raw}".strip()
        lic = (c.get("license") or "unknown").strip()
        # A named license is the only thing that buys redistributable=yes. Same rule as the gate;
        # applied here too so a bad candidate is stopped at the door rather than at the gate.
        if redist == "yes" and lic.lower() in NON_LICENSES:
            redist = "no"

        # `revision_date` wants a full ISO date and the schema says empty when the document does not
        # state one. Candidates supply what the document actually says, which is very often a month
        # ("2019-09"), sometimes a year, and sometimes two dates ("2023-06 (published); 2025-08
        # (last modified)"). None of those are ISO dates and the gate rejects all of them.
        #
        # Whether YYYY-MM should be allowed is an OPEN QUESTION recorded in BACKLOG.md and it is not
        # this script's to decide. So do what the catalog already does for PI-MBUS-300's June 1996
        # and the Moxa guide's April 2021: empty the field, keep the real date in notes. Honest, and
        # it loses the field, which is exactly the cost the backlog is weighing.
        rd = (c.get("revision_date") or "").strip()
        if rd and not re.fullmatch(r"\d{4}-\d{2}-\d{2}", rd):
            note = f"{note} The document states its date as: {rd}.".strip()
            rd = ""

        rid = make_id(c, taken)
        taken.add(rid)
        key = re.sub(r"^https?://", "", url.rstrip("/").lower())
        seen_urls.add(key)
        landed.append({
            "id": rid,
            "title": title,
            "vendor": (c.get("vendor") or "").strip() or "n/a",
            "doc_number": (c.get("doc_number") or "").strip() or "n/a",
            "revision": (c.get("revision") or "").strip() or "n/a",
            "revision_date": rd,
            "category": cat,
            "url": url,
            "archive_url": snap,   # set only for a ROTTED row; archive.py fills the rest
            "license": lic or "unknown",
            "redistributable": redist,
            # Say it, do not leave it blank for someone else to interpret. This column was added
            # after this script was written, so the row dict simply had no key for it and
            # csv.DictWriter filled the gap with "" without raising: a schema that says "empty not
            # allowed" quietly getting empties, from the one tool that writes rows in bulk. The gate
            # coerces "" to UNVERIFIED and so nothing unsafe shipped, but a value that only means
            # the right thing because a READER fixes it up is not recorded, it is inferred.
            # UNVERIFIED is also the only honest basis available here: this script fetches, it does
            # not read a copyright page, and check_license.py is what promotes a row off UNVERIFIED.
            "license_basis": "UNVERIFIED",
            "local_path": "",
            "sha256": "",
            "verified_level": "LOCATED ONLY",   # never anything else. See the module docstring.
            "verified_date": today,
            "notes": note,
        })
        print(f"  land    {title[:52]:52s} [{code}] {rid}")

    print()
    print(f"  {len(landed)} would land, {len(rejects)} rejected")
    dead = [r for r in rejects if r[1] == "did not fetch"]
    if dead:
        print(f"  {len(dead)} of the rejects were PROPOSED BUT NOT REAL. That is this script's whole job:")
        for c, _, code in dead:
            print(f"    .. [{code}] {(c.get('url') or '')[:90]}")

    if args.dry_run:
        print("\n  --dry-run, catalog untouched")
        return 0
    if not landed:
        print("\n  nothing survived, catalog untouched")
        return 0

    # Re read before writing. Another session may own this file now.
    with CATALOG.open(newline="", encoding="utf-8") as fh:
        fresh = list(csv.DictReader(fh))
    fresh_ids = {r["id"] for r in fresh}
    add = [r for r in landed if r["id"] not in fresh_ids]

    tmp = CATALOG.with_suffix(".csv.tmp")
    with tmp.open("w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=COLUMNS)
        w.writeheader()
        w.writerows(fresh + add)
    os.replace(tmp, CATALOG)
    print(f"\n  wrote {len(add)} new row(s), all at LOCATED ONLY")

    if rejects:
        rp = staging / "_rejected.json"
        rp.write_text(json.dumps(
            [{"why": w, "code": str(code), **{k: v for k, v in c.items()}} for c, w, code in rejects],
            indent=2))
        print(f"  rejects written to {rp.relative_to(ROOT)}")
    print("\n  Next: ./tools/archive.py to snapshot them, then ./tools/build_indexes.py")
    return 0


if __name__ == "__main__":
    sys.exit(main())
