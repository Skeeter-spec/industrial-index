#!/usr/bin/env python3
"""Does the document itself support the licence this row claims?

    ./tools/check_license.py                  # every redistributable=yes row
    ./tools/check_license.py --all            # every row that names a licence
    ./tools/check_license.py --id foo-bar
    ./tools/check_license.py --selftest       # prove it can still tell the states apart

WHY THIS EXISTS.

`redistributable` is the only column in this catalog that is a LEGAL claim. Every other column is a
statement about a document. This one is a statement about what a reader may lawfully DO with it, and
a reader who mirrors a file on the strength of a yes is relying on it. Thirteen rows carried yes at
level LOCATED ONLY: a legal claim on a document nobody had opened.

The gate already flags that pair and calls it unfinished. That was not enough, and the reason is the
sharper lesson here: A RECORDED DOUBT IS NOT A CHECK. This repo has already shipped a row whose own
note said "verify this licence before trusting redistributable=yes" WITH the yes still in it, and the
yes was wrong. The note did not prevent the claim. The note is what let it ship, because writing the
doubt down feels like handling it. So does a gate line that says "unfinished" while the yes sits
published. If a claim rests on something unverified, the claim gets DOWNGRADED, not annotated.

WHAT IT ACTUALLY CHECKS, and what it deliberately does not.

It reads the document at the publisher and reports the verbatim licence language it finds. It does
not decide. Same contract as check_titles.py: the tool reports, a person decides, the catalog is
edited by hand. A regex has no business ruling on copyright.

The finding worth the whole file is the THIRD PARTY notice inside a government document.
TM 5-811-14 is a public domain Army work EXCEPT the asterisked paragraph reprinting IEEE 242 by
permission. A LICENCE IS NOT UNIFORM ACROSS A DOCUMENT. "The publisher is the US government" is a
hypothesis about the file, and 17 USC 105 covers works of federal EMPLOYEES: it does not reach
contractor authored material, and it does not reach a copyrighted table a federal author reprinted
with permission. So a hit on "reprinted with permission" inside a public domain claim is not noise.
It is the entire point.

FOUR STATES, AND THE FOURTH ONE WAS EARNED THE HARD WAY.

A bool cannot say "I could not tell", so every failure to OBSERVE silently becomes a claim about the
world, and it always lands on the destructive side. That much was known. This file shipped its first
draft with three states and it was STILL wrong, because UNKNOWN was doing two incompatible jobs:

    SUPPORTED    the document grants it, in its own words, quoted below
    CONFLICT     the document carries language that contradicts or narrows the claim
    SILENT       read end to end. It says nothing about its own licence, either way.
    UNREADABLE   could not fetch it, could not parse it. No evidence of any kind.

SILENT AND UNREADABLE ARE NOT THE SAME ANSWER and collapsing them is `http=0 is not a 404` repeating
itself one layer up. "I read 45 pages and there is no grant in them" is EVIDENCE. "I never got the
file" is the ABSENCE of evidence. They point opposite directions: the first says the yes rests on
something other than the document, the second says go and look again. A reader who cannot tell them
apart cannot act on either.

MEASURED 2026-07-16, and this is why the state exists rather than being a nice idea. OSHA 3120 is 45
pages and 64,840 characters and contains ZERO occurrences of copyright, public domain, reproduce or
permission. The grant this catalog claims for it is not in it. That is a real finding about a real
document, and the first draft of this tool reported it with the same word it used for a 404.

NONE OF SUPPORTED, SILENT OR UNREADABLE IS A PASS. The absence of a copyright notice is not evidence
of public domain: most public domain federal works say nothing at all. SILENT does not mean the row
is wrong. It means the yes rests on 17 USC 105 as an INFERENCE FROM THE PUBLISHER, which is a legal
judgement about the file rather than a quotation from it, and the row should say so.

No size cap. A 4MB cap once truncated eleven good documents into a confident 0 percent, and a
truncated file must never be scored: a 49MB document read through a 40MB window is indistinguishable
from a fabrication. RAISING THE CAP IS NOT THE FIX. Not having one is.
"""
import argparse
import csv
import pathlib
import re
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
CATALOG = ROOT / "catalog" / "catalog.csv"
WORK = ROOT / ".check_license_tmp"          # inside the repo: /var/folders is sandbox blocked

UA = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/120.0 Safari/537.36")

SUPPORTED, CONFLICT, SILENT, UNREADABLE = "SUPPORTED", "CONFLICT", "SILENT", "UNREADABLE"

# Language that GRANTS. Quoted back verbatim so a person can read what was actually said.
GRANT = [
    r"(?:is |are )?in the public domain[^.]{0,120}",
    r"may be reproduced[^.]{0,120}",
    r"may be (?:freely )?(?:copied|distributed|reproduced)[^.]{0,120}",
    r"not subject to copyright[^.]{0,120}",
    r"no copyright[^.]{0,80}",
    r"distribution statement a[^.]{0,120}",
    r"approved for public release[^.]{0,80}",
    r"distribution (?:is )?unlimited[^.]{0,60}",
]

# Language that NARROWS or CONTRADICTS. A hit here inside a "public domain" row is the TM 5-811-14
# case and it is the reason this tool exists.
NARROW = [
    r"reprinted (?:by|with) permission[^.]{0,120}",
    r"used (?:by|with) permission[^.]{0,120}",
    r"with (?:the )?permission of[^.]{0,120}",
    r"all rights reserved[^.]{0,80}",
    r"copyright ©[^.]{0,100}",
    r"© ?(?:19|20)\d\d[^.]{0,100}",
    r"copyright (?:19|20)\d\d[^.]{0,100}",
    r"may not be reproduced[^.]{0,120}",
    r"distribution statement [b-f][^.]{0,120}",
    r"prior written (?:permission|consent)[^.]{0,100}",
    r"is a (?:registered )?trademark[^.]{0,80}",
]


def fetch(url, path):
    """Returns (meta, err). Shells out to curl: it already solves certificates, redirects and the
    user agent checks that hand urllib a bare HTTPError that reads exactly like 'gone'."""
    if path.exists():
        path.unlink()          # never let a previous run's file answer for this one
    r = subprocess.run(
        ["curl", "-sS", "--max-time", "180", "-L", "-A", UA, "-o", str(path),
         "-w", "%{http_code} %{size_download}", url],
        capture_output=True, text=True)
    if r.returncode != 0:
        return None, f"curl rc={r.returncode} {r.stderr.strip()[:80]}"
    if not path.exists() or path.stat().st_size == 0:
        return None, f"empty ({r.stdout.strip()})"
    code = r.stdout.strip().split()[0]
    if code.startswith(("4", "5")):
        return None, f"http {code}"
    return r.stdout.strip(), None


def text_of(path):
    """Whole document, every page. Returns (text, npages, err). err is never a verdict.

    The de-hyphenation is not cosmetic. OSHA's booklets are Acrobat Paper Capture OCR of a scan, and
    a line broken across "pub- lic domain" makes a literal search for the grant return zero hits: you
    conclude the document is silent when the notice is sitting right there. That is a false SILENT,
    which is the most expensive verdict this tool can produce, because SILENT is the one that says
    "the row's yes has nothing behind it".
    """
    head = path.open("rb").read(4)
    if head == b"%PDF":
        try:
            import fitz
        except ImportError:
            return None, 0, "PyMuPDF not installed (try ~/.venvs/pptx/bin/python3)"
        try:
            d = fitz.open(str(path))
        except Exception as e:
            return None, 0, f"pdf would not open: {type(e).__name__}"
        if d.page_count == 0:
            return None, 0, "pdf has zero pages"
        t = " ".join(p.get_text() for p in d)
        if not t.strip():
            # A scan with no OCR layer. There is nothing to read, so there is nothing to be silent
            # about: this is UNREADABLE wearing a PDF costume, and it must not score as SILENT.
            return None, d.page_count, f"{d.page_count}p pdf with no text layer (scan, not OCRd)"
        return re.sub(r"(\w)-\s+(\w)", r"\1\2", t), d.page_count, None
    raw = path.open("rb").read().decode("utf-8", "ignore")
    if not raw.strip():
        return None, 0, "empty body"
    raw = re.sub(r"<script.*?</script>|<style.*?</style>", " ", raw, flags=re.S | re.I)
    return re.sub(r"(\w)-\s+(\w)", r"\1\2", re.sub(r"<[^>]+>", " ", raw)), 0, None


def scan(text):
    """Returns (grants, narrows) as verbatim snippets, deduped, order preserved."""
    flat = re.sub(r"\s+", " ", text)
    out = []
    for pats in (GRANT, NARROW):
        found, seen = [], set()
        for p in pats:
            for m in re.finditer(p, flat, re.I):
                s = re.sub(r"\s+", " ", m.group(0)).strip()
                k = s.lower()[:60]
                if k not in seen:
                    seen.add(k)
                    found.append(s)
        out.append(found)
    return out[0], out[1]


def verdict(grants, narrows):
    if narrows:
        return CONFLICT
    if grants:
        return SUPPORTED
    return SILENT           # read it, found nothing. Silence is not consent. It is also not a 404.


def check(url, target):
    """Returns (state, grants, narrows, err, npages). A fetch or parse failure can only ever produce
    UNREADABLE: this function is structurally incapable of turning a failure to look into a finding
    about the document."""
    meta, err = fetch(url, target)
    if err:
        return UNREADABLE, [], [], err, 0
    text, npages, err = text_of(target)
    if err:
        return UNREADABLE, [], [], err, npages
    g, n = scan(text)
    return verdict(g, n), g, n, None, npages


# EVERY FIXTURE HERE IS A REAL DOCUMENT THAT REALLY SAYS THIS, MEASURED 2026-07-16. None are invented.
#
# This is not ceremony. A sibling guard in this system shipped with "2 controls fire, 4 negatives
# silent" written in its own docs while sitting SILENT on both false claims that were live in this
# repo's BACKLOG.md the whole time, because its fixtures had been written to match its own regex. It
# tested that a regex matches itself, passed, and the pass got quoted back as proof.
#
# So when a document is found saying something in the wild, PASTE THE REAL URL IN HERE.
# The first fixture written here was "osha3120.pdf -> SUPPORTED, an OSHA booklet states its own
# public domain grant in its front matter." That was INVENTED. It came from what I assumed OSHA
# booklets say, not from reading one, and the selftest failed on it within a minute of being written.
# The document is silent. The tool was right and the fixture was the lie, which is the entire reason
# the expectations live here as measurements instead of as intentions.
SELFTEST = [
    ("https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-82r3.pdf",
     SUPPORTED,
     'POSITIVE CONTROL, 316p: says in its own words "is not subject to copyright in the United '
     'States. Attribution would, however, be appreciated by NIST." If this stops reading SUPPORTED '
     'the grant patterns have gone blind.'),
    ("https://www.energy.gov/sites/default/files/2026-04/DOE-HDBK-1011-92_VOL1.pdf",
     SUPPORTED,
     'POSITIVE CONTROL, 166p: "Distribution Statement A. Approved for public release; distribution '
     'is unlimited." on the title page. A DIFFERENT grant dialect from NIST, deliberately: one '
     'positive control only proves the one pattern that matched it.'),
    ("https://www.osha.gov/sites/default/files/publications/osha3120.pdf",
     SILENT,
     "THE FINDING THIS FILE EXISTS TO REPORT, and it broke this selftest's original fixture. 45 "
     "pages, 64,840 chars, Acrobat Paper Capture OCR, and ZERO occurrences of copyright, public "
     "domain, reproduce or permission. The catalog claims public domain + redistributable=yes for "
     "it. That claim is not in the document. SILENT, never UNREADABLE: the file downloads and parses "
     "perfectly, and 'lockout' appears 105 times in it, so the reader demonstrably works."),
    ("https://www.iemfg.com/technical/switchgear-commissioning-handbook-9th-ed.pdf",
     UNREADABLE,
     "NEGATIVE CONTROL: a url invented on purpose, it 404s. It MUST come back UNREADABLE and never "
     "SILENT or SUPPORTED. This is the whole rule in one row: a document that does not exist must "
     "not be able to grant a licence by staying quiet, and 'I could not fetch it' must never be "
     "reportable as 'it contains no restrictions'."),
]


def selftest():
    """Prove the three states are still distinguishable, against documents from the wild."""
    WORK.mkdir(exist_ok=True)
    target = WORK / "selftest.bin"
    print("  check_license selftest, real documents, measured in the wild\n")
    ok = True
    for url, expect, why in SELFTEST:
        got, g, n, err, _ = check(url, target)
        hit = got == expect
        ok &= hit
        print(f"  {'PASS' if hit else 'FAIL'}  expected {expect:<9} got {got:<9} {err or ''}")
        print(f"        {url[:92]}")
        print(f"        {why}")
        if g:
            print(f"        grants : {g[0][:88]}")
        if n:
            print(f"        narrows: {n[0][:88]}")
        print()
    print("  ALL PASS" if ok else "  *** FAILED, do not trust a report from this checker ***")
    return 0 if ok else 1


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--id")
    ap.add_argument("--all", action="store_true",
                    help="every row naming a licence, not only redistributable=yes")
    ap.add_argument("--selftest", action="store_true")
    args = ap.parse_args()

    if args.selftest:
        return selftest()

    with CATALOG.open(newline="", encoding="utf-8") as fh:
        rows = list(csv.DictReader(fh))
    if args.id:
        rows = [r for r in rows if r["id"] == args.id]
    elif not args.all:
        rows = [r for r in rows if r["redistributable"] == "yes"]

    WORK.mkdir(exist_ok=True)
    target = WORK / "f.bin"
    tally = {SUPPORTED: 0, CONFLICT: 0, SILENT: 0, UNREADABLE: 0}

    print(f"  reading {len(rows)} document(s) at the publisher\n")
    for r in rows:
        got, g, n, err, npages = check(r["url"], target)
        tally[got] += 1
        pg = f" {npages}p" if npages else ""
        print(f"  {got:<10} {r['id']}{pg}")
        print(f"             claims: {r['license']} | redistributable={r['redistributable']} "
              f"| {r['verified_level']}")
        if err:
            print(f"             no evidence either way: {err}")
        for s in g[:3]:
            print(f"             grants : \"{s[:100]}\"")
        for s in n[:4]:
            print(f"             narrows: \"{s[:100]}\"")
        if got == CONFLICT:
            print("             ^ the licence may not be uniform across this document. Read it.")
        if got == SILENT:
            print("             ^ the grant this row claims is not in the document. The yes rests on")
            print("               17 USC 105 inferred from the publisher, not on anything it says.")
        print()

    print(f"  {tally[SUPPORTED]} supported, {tally[CONFLICT]} conflict, "
          f"{tally[SILENT]} silent, {tally[UNREADABLE]} unreadable")
    print("\n  This tool reports. It does not edit the catalog, and it does not rule on copyright.")
    print("  SILENT is not a pass: a document that says nothing has granted nothing in writing.")
    print("  SILENT is not a failure either: most public domain federal works say nothing at all.")
    print("  It means the row is resting on a legal inference, and should say which one.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
