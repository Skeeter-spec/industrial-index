# mirrors/

License cleared documents only. **This directory is gitignored by default.**

That is not tidiness, it is the copyright boundary. A file lands here two ways: someone downloads
something to read, or someone intends to publish it. Only the second is a legal question, and git is
the line between them. Ignoring the directory means the first case can never accidentally become the
second, which is exactly what a `git add -A` at the end of a long session would otherwise do.

## Adding a document here

1. Read the publisher's actual license. Not the download page, not the price, the license.
   "Free to download" is not permission to republish.
2. Add or update its catalog row: `redistributable=yes` and `license` naming quotable terms.
3. Record `local_path` and `sha256` on that row.
4. `./tools/check_mirrors.py` must pass.
5. `git add -f mirrors/<path>` on purpose.

The gate fails on any tracked file here that no catalog row has cleared, so step 5 without steps 1
through 4 does not survive `./tools/gate.sh`.

## What actually belongs here

In practice, almost nothing:

- US government works: NIST, OSHA, DOE, NREL. Public domain, mirror freely.
- Openly licensed vendor documentation. Rare, but real (Raspberry Pi publishes under CC BY-SA).
- Open source project documentation under a permissive or copyleft license.

Vendor manuals, chip datasheets, and sold standards do not belong here, and the catalog handles them
better anyway: a row with a canonical link, a snapshot, and a note about what the document is good
for gives the reader everything except a copy they were never entitled to.

## The sha256 column, which looks like paranoia and is not

A publisher can replace revision A with revision B at the same URL under different terms. Re fetch
and the file silently changes underneath a row still asserting the old license. Nothing about that
looks broken from the catalog's side. The hash is the only thing that notices, and by then the repo
would have been republishing content under a license that no longer applied.
