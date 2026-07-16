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
    "url", "archive_url", "license", "redistributable", "license_basis", "local_path", "sha256",
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

# `license_basis`: WHY this row believes its licence. An INDEPENDENT AXIS from verified_level.
#
# verified_level answers "how far did someone read the CONTENT". It cannot answer "does anyone know
# the LICENCE", and until 2026-07-16 this checker used it as a proxy for exactly that: it flagged
# redistributable=yes at LOCATED ONLY as "a legal claim on a document nobody has opened". That proxy
# is wrong in both directions. You can read a manual end to end and never look at its copyright page.
# You can read ONLY the copyright page and know the licence exactly while the content stays unread,
# which is the true state of thirteen rows here.
#
# This is the toolbox's provenance bug, exactly: `TRACED` recorded how far a document was read and
# said nothing about WHOSE COPY was read, and the fix was a machine checked column rather than a
# better intention. Same shape, same fix.
BASES = {
    # The document grants it, in its own words. `notes` carries the quote. The strongest basis there
    # is, and the only one that is a quotation rather than a legal conclusion.
    "DOCUMENT",
    # The claim rests on law, not on the document, and the document is SILENT about its own terms.
    # 17 USC 105 for a federal work, or the government edicts doctrine for regulatory text. Usually
    # right and NOT a defect. It is a conclusion someone drew, and the row should say so, because
    # 17 USC 105 reaches works of federal EMPLOYEES and does not reach a contractor's manuscript or
    # a copyrighted table reprinted by permission inside an otherwise public domain report.
    "STATUTE",
    # Nobody has checked. The honest default, and the only value that is a defect under a yes.
    "UNVERIFIED",
}

ID_RE = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
SHA_RE = re.compile(r"^[a-f0-9]{64}$")

# A Wayback URL carries the URL it snapshotted inside itself, after the timestamp. That is what
# lets this be an OFFLINE check: the row already contains the answer, nobody has to fetch anything.
WAYBACK_RE = re.compile(r"^https://web\.archive\.org/web/[0-9a-z_]+/(.+)$")

# "free" is not a license. Neither is "free to download", which is the single most common way a
# redistribution mistake gets made: the reader conflates the price with the grant. If a vendor
# genuinely grants redistribution they say so in words you can quote, so require quotable words.
NON_LICENSES = {
    "", "unknown", "free", "free to download", "freely available", "public",
    "open", "n/a", "none", "tbd",
}


def _norm(u):
    """Reduce a URL to the part worth comparing.

    Scheme and a trailing slash are not a move. Reporting them as one trains the reader to skim
    this list, and the whole point of the unfinished tier is that somebody actually reads it.
    """
    u = u.strip().lower()
    for p in ("https://", "http://"):
        if u.startswith(p):
            u = u[len(p):]
            break
    return u.rstrip("/")


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

        # Empty is not a fourth state. It reads as "no opinion" and would let a yes through the
        # invariant below by saying nothing, which is the exact move this column exists to stop.
        basis = (row.get("license_basis") or "").strip() or "UNVERIFIED"
        if basis not in BASES:
            errors.append(f"{where}: license_basis '{basis}' is not in the vocabulary "
                          f"({', '.join(sorted(BASES))})")

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
        snap = (row.get("archive_url") or "").strip()
        if not snap:
            unfinished.append(f"{rid}: no archive_url")
        if level == "LOCATED ONLY":
            unfinished.append(f"{rid}: content still unverified")

        # A LEGAL claim resting on a document nobody opened. Visible, never fatal.
        #
        # MEASURED 2026-07-16, and this check is named after the row that taught it. The RP2040
        # datasheet row said `license=CC BY-SA 4.0, redistributable=yes` at LOCATED ONLY. The
        # schema already required that `yes` name actual terms, and it did name actual terms, and
        # they were THE WRONG TERMS: the colophon says CC BY-ND, NoDerivatives, the opposite
        # obligation. Naming a licence is not reading one. Nothing caught it, because the rule
        # tested the SHAPE of the value and never asked whether anyone had looked.
        #
        # It is deliberately not fatal. "public domain (US government work)" is usually right, and
        # a gate that goes red on 13 probably-fine rows teaches that red means nothing here. But it
        # is also not free: TM 5-811-14 is a public domain Army document EXCEPT the asterisked
        # paragraph reprinting IEEE 242 by permission. A licence is not uniform across a document,
        # so "the publisher is the US government" is a hypothesis about a file nobody has opened.
        # WAS: `redist == "yes" and level in UNOPENED` -> "a legal claim on a document nobody has
        # opened", reported as unfinished. Retired 2026-07-16 for being wrong twice over.
        #
        # It asked the wrong column. verified_level is about the CONTENT, and a licence lives on the
        # copyright page: reading it does not raise the level, and raising the level does not mean
        # anyone read it. Thirteen rows sat under that warning, and when they were finally read at
        # the publisher, ten were resting on a statutory inference and THREE CARRIED AN EXPLICIT
        # WRITTEN GRANT. The proxy had been nagging about rows that were provably fine while having
        # nothing to say about the ones that were merely assumed.
        #
        # And it was unfinished, not an error, which is the deeper bug. This repo has already shipped
        # a row whose own note said "verify this licence before trusting redistributable=yes" WITH
        # the yes still in it, and the yes was wrong. A gate line reading "unfinished" next to a
        # published legal claim is that same note wearing a checker's uniform. A recorded doubt is
        # not a check; it is the alibi that lets the claim ship. So this one is an ERROR.
        if redist == "yes" and basis == "UNVERIFIED":
            errors.append(
                f"{where}: redistributable=yes with license_basis=UNVERIFIED. This row is telling a "
                f"reader they may lawfully republish a document on the strength of nobody having "
                f"checked. Read it (tools/check_license.py --id {rid}), then say what the yes rests "
                f"on: DOCUMENT if it grants in its own words, STATUTE if it is silent and the claim "
                f"rests on 17 USC 105 or the edicts doctrine.")

        # A STATUTE basis is not a defect and this is deliberately not an error. Most public domain
        # federal works say nothing at all, so demanding a written grant would delete good rows,
        # which is the direction a checker's findings always fall. It IS worth a reader's attention:
        # 17 USC 105 is a conclusion about a file, and TM 5-811-14 is a public domain Army document
        # EXCEPT the asterisked paragraph reprinting IEEE 242 by permission. A licence is not uniform
        # across a document, and the asterisked paragraph is always the one someone wants.
        if redist == "yes" and basis == "STATUTE":
            unfinished.append(
                f"{rid}: redistributable=yes rests on statute, not on the document. The document is "
                f"silent about its own terms. Correct as far as anyone knows, and worth re-reading "
                f"before anything is mirrored on the strength of it.")

        # The snapshot is of somewhere else. Visible, never fatal, and the distinction matters.
        #
        # MEASURED 2026-07-15. archive.py asks Wayback to save the row's url, and Wayback follows
        # the redirect and snapshots wherever it lands. Four rows came back holding a snapshot of a
        # URL the row never names. Every one of those snapshots is genuine and is of the right
        # document, which is exactly why this is not an error: nothing here is WRONG.
        #
        # It is a fact the row is throwing away, and the fact is worth money. datasheets.raspberrypi
        # .com/rp2040/rp2040-datasheet.pdf lands on a file called RP-008371-DS-1-rp2040-datasheet
        # .pdf. That row says doc_number n/a and revision n/a. The publisher plainly has both and
        # the redirect was carrying them the whole time. A stable url that hides a versioned one is
        # the Modbus problem wearing a different hat: the link cannot rot, so nothing looks broken,
        # and the revision moves underneath it in silence.
        m = WAYBACK_RE.match(snap) if snap else None
        if m and _norm(m.group(1)) != _norm(url):
            unfinished.append(f"{rid}: snapshot is of {m.group(1)}, not the url this row names")

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
