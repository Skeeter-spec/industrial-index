#!/usr/bin/env python3
"""Does each row's URL actually serve the document the row NAMES?

    ./tools/check_titles.py                   # every row
    ./tools/check_titles.py --category protocols
    ./tools/check_titles.py --id foo-bar

DELIBERATELY NOT IN gate.sh, for the same reason as check_links.py: it needs the network and it
downloads real documents, some of which are 40MB. The gate stays offline and one second long. A check
that flakes is a check that gets bypassed, and a bypassed gate is worse than no gate.

WHY THIS EXISTS, AND IT IS NOT THE SAME CHECK AS check_links.py.

check_links asks "is this URL alive". merge_candidates asks "did it fetch". Neither asks the question
that actually matters: **is the thing on the other end the document this row claims?** Reachability
is not identity. A live URL serving the WRONG document is the cites-rev-C-links-rev-A case, and it
looks perfect from the outside: green link, confident row, wrong file.

MEASURED 2026-07-15, which is why this is a tool and not a good intention. Of 17 power-distribution
rows sourced in one pass, TWELVE named a page that was not the document: nine se.com landing pages
and two Siemens product pages. The rows looked immaculate. The se.com pages then started answering
403 from Akamai's edge, so those rows would have failed for a READER, not merely for a checker.

THE SUBTLE ONE, and the reason this prints the missing words instead of only a verdict. Two Siemens
rows PASSED a 60 percent title match, because a product page for the SENTRON naturally repeats most
of the words in the SENTRON manual's title. What gave them away was the MOST SPECIFIC word being the
missing one: no "sentron", no "rts30na". A threshold cannot see that. A person reading the missing
words can. So this tool reports and a human decides; it never edits the catalog.

FOUR BUGS THIS FILE IS BUILT AROUND, all of them mine, all found on 2026-07-15, all of them failing
in the "everything is broken" direction:
  1. A 4MB read cap truncated big PDFs, the parser opened them happily, and eleven GOOD documents
     came back 0%. The ControlLogix manual is 43.5MB. Trusting that run would have deleted eleven
     correct rows. There is no cap here.
  2. The rewrite never passed the URL to curl, so it fetched nothing, and the "it worked" check was
     reading a STALE FILE from a previous run. Every fetch here deletes its target first.
  3. tempfile.mkdtemp() lands in /var/folders, which the sandbox blocks, so curl could not open its
     output file and failed before printing anything. The empty error string was the only tell.
  4. urllib got a bare HTTPError from hosts that answer curl fine, which reads exactly like "gone"
     and is a user agent check. This shells out to curl, which already solves certificates,
     redirects and user agents.
Every one of those produced a confident red. A red is a claim too, and it gets checked like any other.
"""
import argparse
import csv
import os
import pathlib
import re
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
CATALOG = ROOT / "catalog" / "catalog.csv"
WORK = ROOT / ".check_titles_tmp"

UA = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/120.0 Safari/537.36")

# Words too common in document titles to carry any signal. Matching on "user" or "manual" tells you
# nothing; matching on "rts30na" tells you everything.
STOP = {
    "the", "a", "an", "and", "or", "of", "for", "to", "in", "on", "with", "user", "manual",
    "guide", "system", "series", "module", "unit", "hardware", "reference", "controllers",
    "controller", "programming", "instructions", "instruction", "cpu", "program", "users",
    "specification", "implementation", "document", "documentation", "note", "application",
}


def words(s):
    return {w for w in re.findall(r"[a-z0-9]+", (s or "").lower()) if len(w) > 2 and w not in STOP}


def fetch(url, path):
    if path.exists():
        path.unlink()          # never let a previous run's file answer for this one
    r = subprocess.run(
        ["curl", "-sS", "--max-time", "180", "-L", "-A", UA, "-o", str(path),
         "-w", "%{http_code} %{content_type} %{size_download}", url],
        capture_output=True, text=True)
    if r.returncode != 0:
        return None, f"curl rc={r.returncode} {r.stderr.strip()[:80]}"
    if not path.exists() or path.stat().st_size == 0:
        return None, f"empty ({r.stdout.strip()})"
    return r.stdout.strip(), None


def text_of(path):
    head = path.open("rb").read(4)
    if head == b"%PDF":
        try:
            import fitz
        except ImportError:
            return None, 0, "PyMuPDF not installed (try ~/.venvs/pptx/bin/python3)"
        d = fitz.open(str(path))
        n = min(3, d.page_count)
        return " ".join(d[i].get_text() for i in range(n)), d.page_count, None
    raw = path.open("rb").read().decode("utf-8", "ignore")
    raw = re.sub(r"<script.*?</script>|<style.*?</style>", " ", raw, flags=re.S | re.I)
    return re.sub(r"<[^>]+>", " ", raw)[:40000], 0, None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--category")
    ap.add_argument("--id")
    ap.add_argument("--thin", type=float, default=0.5)
    args = ap.parse_args()

    with CATALOG.open(newline="", encoding="utf-8") as fh:
        rows = list(csv.DictReader(fh))
    if args.category:
        rows = [r for r in rows if r["category"] == args.category]
    if args.id:
        rows = [r for r in rows if r["id"] == args.id]

    WORK.mkdir(exist_ok=True)
    target = WORK / "f.bin"
    flagged = []

    for r in rows:
        title = r["title"]
        # A ROTTED row's canonical is gone by definition, so ask its snapshot instead. Checking the
        # dead URL would report a 404 page as a title mismatch, which is true and useless.
        url = (r["url"] or "").strip()
        via = ""
        meta, err = fetch(url, target)
        if err and (r.get("archive_url") or "").strip():
            meta, err = fetch(r["archive_url"].strip(), target)
            via = " (via snapshot)"
        if err:
            print(f"  FETCH-FAIL {r['id'][:44]:44s} {err}")
            flagged.append((r, "fetch failed", err))
            continue

        text, pages, perr = text_of(target)
        if perr:
            print(f"  PARSE-FAIL {r['id'][:44]:44s} {perr}")
            flagged.append((r, "parse failed", perr))
            continue

        want = words(title)
        hit = want & words(text)
        frac = len(hit) / max(1, len(want))
        verdict = "OK  " if frac >= args.thin else ("THIN" if frac >= args.thin / 2 else "MISS")
        missing = sorted(want - words(text))
        print(f"  {verdict} {frac:4.0%} p{pages:<4d} {r['id'][:40]:40s}{via} missing={missing[:3]}")
        if verdict != "OK  ":
            flagged.append((r, verdict, f"{frac:.0%}, missing={missing}"))

    if target.exists():
        target.unlink()
    try:
        WORK.rmdir()
    except OSError:
        pass

    print()
    print(f"  {len(rows)} row(s) checked, {len(flagged)} flagged")
    if flagged:
        print("\n  A HUMAN reads these. This tool never edits the catalog, because the interesting")
        print("  failures pass a threshold and are caught by noticing WHICH word is missing:")
        for r, v, why in flagged:
            print(f"    {v} {r['id']}")
            print(f"        {r['url'][:96]}")
            print(f"        {why[:140]}")
    else:
        print("  Every row's URL serves a document that says its own name.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
