#!/usr/bin/env python3
"""Generate every domain INDEX.md and the README status block from catalog.csv.

    ./tools/build_indexes.py           # write them
    ./tools/build_indexes.py --check   # fail if they have drifted (this is what gate.sh runs)

WHY GENERATED RATHER THAN WRITTEN

power-service-toolbox's README said "no tool is live yet" for a while after 01 went live, because a
status typed into prose is a copy, and a copy rots. That cost that repo a build_readme.py.

Here the same problem is multiplied by every domain: a hand written index of protocol documents is
a second catalog that disagrees with the first one. Two files describing the same state is how they
drift, and then a reader trusts the wrong one. The catalog is the single source. The indexes are a
rendering, and gate.sh fails if the rendering is stale.

The hand written part of each domain is ABOVE the generated marker and is never touched by this
script. That is deliberate: the notes are the reason to visit, the table is just the manifest.
"""
import argparse
import csv
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
CATALOG = ROOT / "catalog" / "catalog.csv"
DOMAINS = ROOT / "domains"
README = ROOT / "README.md"

BEGIN = "<!-- BEGIN GENERATED: {} Do not hand edit. Regenerate: ./tools/build_indexes.py -->"
END = "<!-- END GENERATED: {} -->"

LEVEL_ORDER = [
    "TRACED", "READ IN FULL", "FETCHED, NOT READ",
    "LOCATED ONLY", "CITED, UNREAD", "GATED, UNREAD",
]


def load():
    with CATALOG.open(newline="", encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


def splice(text, key, body):
    """Replace the region between the markers for `key`, appending it if absent."""
    b, e = BEGIN.format(key), END.format(key)
    block = f"{b}\n\n{body}\n\n{e}"
    if b in text and e in text:
        head = text.split(b)[0]
        tail = text.split(e, 1)[1]
        return head + block + tail
    return text.rstrip() + "\n\n" + block + "\n"


def domain_table(rows):
    if not rows:
        return ("No documents catalogued in this domain yet. That is a real state and it is written\n"
                "here rather than hidden behind an empty table.")
    out = ["| Document | Vendor | Rev | Verified | Mirror |", "|---|---|---|---|---|"]
    for r in sorted(rows, key=lambda r: (r["vendor"].lower(), r["title"].lower())):
        link = f"[{r['title']}]({r['url']})"
        if (r.get("archive_url") or "").strip():
            link += f" ([snapshot]({r['archive_url']}))"
        mirror = f"`{r['local_path']}`" if (r.get("local_path") or "").strip() else "link only"
        rev = r["revision"] if r["revision"] != "n/a" else ""
        out.append(f"| {link} | {r['vendor']} | {rev} | `{r['verified_level']}` | {mirror} |")
    return "\n".join(out)


def readme_status(rows):
    by_level = {lv: 0 for lv in LEVEL_ORDER}
    for r in rows:
        lv = r["verified_level"]
        if lv in by_level:
            by_level[lv] += 1

    opened = sum(by_level[lv] for lv in ("TRACED", "READ IN FULL", "FETCHED, NOT READ"))
    snap = sum(1 for r in rows if (r.get("archive_url") or "").strip())
    mirrored = sum(1 for r in rows if (r.get("local_path") or "").strip())
    total = len(rows)

    lines = [
        f"**{total} documents catalogued. {opened} of them have actually been opened by a human.**",
        "",
        "That second number is the honest one, and it is generated from the catalog rather than "
        "claimed in prose, so it cannot flatter itself.",
        "",
        "| | Count |",
        "|---|---|",
    ]
    for lv in LEVEL_ORDER:
        lines.append(f"| `{lv}` | {by_level[lv]} |")
    lines += [
        f"| **snapshotted against link rot** | **{snap} of {total}** |",
        f"| **mirrored locally (license cleared)** | **{mirrored}** |",
        "",
        "By domain:",
        "",
        "| Domain | Documents |",
        "|---|---|",
    ]
    counts = {}
    for r in rows:
        counts[r["category"]] = counts.get(r["category"], 0) + 1
    for d in sorted(p.name for p in DOMAINS.iterdir() if p.is_dir()):
        n = counts.get(d, 0)
        cell = str(n) if n else "_none yet_"
        lines.append(f"| [{d}](domains/{d}/INDEX.md) | {cell} |")
    return "\n".join(lines)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true")
    args = ap.parse_args()

    rows = load()
    drift = []

    for d in sorted(p for p in DOMAINS.iterdir() if p.is_dir()):
        idx = d / "INDEX.md"
        mine = [r for r in rows if r["category"] == d.name]
        if idx.exists():
            text = idx.read_text(encoding="utf-8")
        else:
            text = f"# {d.name}\n\n_Notes for this domain go above the table. The table is generated._\n"
        new = splice(text, "catalog.", domain_table(mine))
        if args.check:
            if not idx.exists() or idx.read_text(encoding="utf-8") != new:
                drift.append(str(idx.relative_to(ROOT)))
        else:
            idx.write_text(new, encoding="utf-8")

    if README.exists():
        text = README.read_text(encoding="utf-8")
        new = splice(text, "status.", readme_status(rows))
        if args.check:
            if text != new:
                drift.append("README.md")
        else:
            README.write_text(new, encoding="utf-8")

    if args.check:
        for f in drift:
            print(f"  FAIL {f} is stale. Run ./tools/build_indexes.py")
        if drift:
            return 1
        print("  OK   every index matches the catalog")
        return 0

    print(f"  regenerated indexes for {len(list(p for p in DOMAINS.iterdir() if p.is_dir()))} "
          f"domains and the README status block")
    return 0


if __name__ == "__main__":
    sys.exit(main())
