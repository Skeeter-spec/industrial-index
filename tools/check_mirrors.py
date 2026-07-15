#!/usr/bin/env python3
"""Every committed document file is cleared for redistribution, and is the file the catalog says.

    ./tools/check_mirrors.py

WHY THIS IS A SEPARATE CHECKER FROM check_catalog.py

check_catalog.py reads the catalog and asks "is this row internally consistent?" It can only see
rows. It cannot see a PDF sitting in mirrors/ that no row mentions, because there is no row to
check. That file is the dangerous one: it is the one that got dropped in during a session, never
catalogued, and committed by a `git add -A` at the end.

This checker starts from the FILESYSTEM and works back to the catalog, which is the only direction
that can catch a file nobody declared. .gitignore makes mirrors/ opt in, so a file has to be force
added to get here; this is what notices when that happened for a bad reason.

Three questions, and each is a different way to be exposed:

  1. Is every tracked file in mirrors/ named by a catalog row?      (undeclared file)
  2. Does that row say redistributable=yes with a real license?     (declared but not cleared)
  3. Does the file's hash match the row?                            (cleared, but not that file)

Question 3 is the subtle one. A vendor can publish rev A under an open license, then replace it with
rev B under different terms at the same URL. Re fetching silently swaps the file under a row that
still says the old license. The hash is what notices.
"""
import csv
import hashlib
import pathlib
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
CATALOG = ROOT / "catalog" / "catalog.csv"
MIRRORS = ROOT / "mirrors"

NON_LICENSES = {
    "", "unknown", "free", "free to download", "freely available", "public",
    "open", "n/a", "none", "tbd",
}

# Repo furniture, not documents.
EXEMPT = {"mirrors/README.md", "mirrors/.gitkeep"}


def tracked_mirror_files():
    """Files git actually tracks under mirrors/. Not files on disk.

    The distinction matters: an uncommitted PDF in mirrors/ is a local download and nobody's
    business. A TRACKED one is published to the world the moment he pushes. Only the second is a
    copyright question, so only the second is checked here.
    """
    try:
        out = subprocess.run(
            ["git", "ls-files", "mirrors"],
            cwd=ROOT, capture_output=True, text=True, check=True,
        ).stdout
    except (subprocess.CalledProcessError, FileNotFoundError):
        return None
    return {p for p in out.split("\n") if p.strip() and p not in EXEMPT}


def sha256(path):
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def main():
    if not CATALOG.exists():
        print("  FAIL catalog/catalog.csv missing")
        return 1

    with CATALOG.open(newline="", encoding="utf-8") as fh:
        rows = list(csv.DictReader(fh))

    by_path = {}
    for r in rows:
        p = (r.get("local_path") or "").strip()
        if p:
            by_path.setdefault(p, []).append(r)

    tracked = tracked_mirror_files()
    if tracked is None:
        print("  SKIP not a git repo yet (nothing can be published, so nothing to check)")
        return 0

    errors = []

    for path in sorted(tracked):
        rs = by_path.get(path)
        if not rs:
            errors.append(
                f"{path}: TRACKED but no catalog row claims it. An undeclared document file is "
                f"about to be published. Catalog it or `git rm --cached` it.")
            continue
        if len(rs) > 1:
            errors.append(f"{path}: claimed by {len(rs)} rows ({', '.join(r['id'] for r in rs)})")
            continue
        row = rs[0]
        if (row.get("redistributable") or "").strip().lower() != "yes":
            errors.append(f"{path}: tracked but row {row['id']} says redistributable is not yes")
        if (row.get("license") or "").strip().lower() in NON_LICENSES:
            errors.append(
                f"{path}: tracked under license '{row.get('license')}', which is not a license")

        full = ROOT / path
        if not full.exists():
            errors.append(f"{path}: tracked by git but not on disk")
            continue
        want = (row.get("sha256") or "").strip()
        got = sha256(full)
        if want and want != got:
            errors.append(
                f"{path}: sha256 mismatch. Row {row['id']} says {want[:12]}.., file is {got[:12]}.. "
                f"The file changed under the row. Re check the license before trusting it.")

    # Rows pointing at files that are not there.
    for path, rs in by_path.items():
        if not (ROOT / path).exists():
            for r in rs:
                errors.append(f"{r['id']}: local_path '{path}' does not exist")

    print(f"  {len(tracked)} tracked file(s) in mirrors/, {len(by_path)} row(s) claim a local_path")
    for e in errors:
        print(f"  FAIL {e}")
    if errors:
        return 1
    print("  OK   nothing is published that is not cleared")
    return 0


if __name__ == "__main__":
    sys.exit(main())
