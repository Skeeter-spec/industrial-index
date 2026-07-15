#!/usr/bin/env python3
"""Link rot report. Canonical URLs and snapshots, counted separately.

    ./tools/check_links.py                  # every row
    ./tools/check_links.py --category protocols
    ./tools/check_links.py --timeout 20

DELIBERATELY NOT IN gate.sh. The gate must run offline, in a second, on a plane, and give the same
answer twice. A network check gives a different answer depending on the wifi, and a check that
flakes is a check that gets bypassed, and a gate with a habitual bypass is worse than no gate:
everyone still believes the repo is checked.

So this runs on a schedule and files issues. It reports, it does not gate.

THE FOUR STATES, WHICH ARE NOT DEGREES OF THE SAME THING:

  OK        canonical live, snapshot present.  Nothing to do.
  ROTTED    canonical dead, snapshot present.  The row still WORKS. This is the system succeeding,
            not failing, and it is why archive_url is mandatory.
  EXPOSED   canonical live, snapshot missing.  The only urgent state. The document is reachable
            right now and unprotected. Run ./tools/archive.py.
  LOST      canonical dead, snapshot missing.  Too late. Find another copy or drop the row.

Sorting by "how many links are broken" hides all of this. EXPOSED rows have working links, which is
exactly why they look fine and are the ones that will hurt.
"""
import argparse
import csv
import pathlib
import sys
import urllib.error
import urllib.request

ROOT = pathlib.Path(__file__).resolve().parent.parent
CATALOG = ROOT / "catalog" / "catalog.csv"

UA = "factory-index link checker (+https://github.com/Skeeter-spec/factory-index)"


def reachable(url, timeout):
    """True if the URL serves something. A HEAD is only ever believed when it SUCCEEDS.

    MEASURED 2026-07-15, and this function is written the way it is because of it.

    Both www.modbus.org and nvlpubs.nist.gov return **HTTP 404 to a HEAD and 200 to a GET on the
    exact same URL**. The user agent makes no difference; it is the method. Isolated with a four
    cell matrix (HEAD/GET against bot UA/browser UA) before touching this code, because the obvious
    suspect was bot blocking and the obvious suspect was wrong.

    The first version of this function retried GET only on 403, 405, and 501, on the theory that
    those are how a server says "no HEAD here." That theory is too generous. A server can refuse a
    HEAD with any status it likes, and 404 is the dangerous one precisely because 404 does not look
    like a refusal. It looks like proof the document is gone. That version reported four live
    documents as LOST and would have had a human delete them.

    So: a failing HEAD proves nothing at all and is always retried with GET. The only claim a HEAD
    is trusted for is success. A false LOST is far more expensive than a wasted GET, because the
    wasted GET costs bandwidth and the false LOST costs a document that this repo existed to keep.
    """
    req = urllib.request.Request(url, method="HEAD", headers={"User-Agent": UA})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            if 200 <= resp.status < 400:
                return True, resp.status
    except Exception:
        pass  # Proves nothing. Fall through to GET, which is the measurement that counts.

    req = urllib.request.Request(url, method="GET", headers={"User-Agent": UA})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return 200 <= resp.status < 400, resp.status
    except urllib.error.HTTPError as e:
        return False, e.code
    except Exception as e:
        return False, type(e).__name__


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--category")
    ap.add_argument("--timeout", type=int, default=15)
    args = ap.parse_args()

    with CATALOG.open(newline="", encoding="utf-8") as fh:
        rows = list(csv.DictReader(fh))
    if args.category:
        rows = [r for r in rows if r["category"] == args.category]

    buckets = {"OK": [], "ROTTED": [], "EXPOSED": [], "LOST": []}

    for r in rows:
        url = (r.get("url") or "").strip()
        snap = (r.get("archive_url") or "").strip()
        live, code = reachable(url, args.timeout) if url else (False, "no url")
        has_snap = bool(snap)
        if live and has_snap:
            state = "OK"
        elif not live and has_snap:
            state = "ROTTED"
        elif live and not has_snap:
            state = "EXPOSED"
        else:
            state = "LOST"
        buckets[state].append((r["id"], code))
        print(f"  {state:<8} {r['id']}  [{code}]")

    print()
    print(f"  OK      {len(buckets['OK']):>4}  live and snapshotted")
    print(f"  ROTTED  {len(buckets['ROTTED']):>4}  canonical dead, snapshot holds. Row still works.")
    print(f"  EXPOSED {len(buckets['EXPOSED']):>4}  live but unsnapshotted. Run ./tools/archive.py.")
    print(f"  LOST    {len(buckets['LOST']):>4}  dead and unsnapshotted. Re source or drop.")

    if buckets["LOST"]:
        print()
        print("  LOST rows are the only ones that need a human:")
        for rid, code in buckets["LOST"]:
            print(f"    .. {rid} [{code}]")
    return 0


if __name__ == "__main__":
    sys.exit(main())
