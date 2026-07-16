# Industrial Index

A catalogued, verified, snapshot backed index of the technical documentation behind automation and
industrial power: PLCs, drives, protocols, microcontrollers, boards, instrumentation, switchgear,
UPS and transfer gear, and the standards that govern all of it. Factory floor, data center, and the
gear that does not care which building it is in.

Built in public by a field service engineer who has to find these documents anyway.

## The rule this repo runs on

**Every row says how far it was actually checked, and no row claims more than that.**

That is the whole point of the repo, so it goes first. There are two ways to describe a document you
have never opened. One of them is `LOCATED ONLY`, and the other is a confident bullet with a working
link. They look identical to a reader and they are worth wildly different amounts, and the second one
is what a search engine, a forum post, and a language model all produce by default.

So the level is a required column, checked by machine, using the same vocabulary as
`power-service-toolbox`:

| Level | Means |
|---|---|
| `TRACED` | Fetched, read, and specific content confirmed to be what the row claims. |
| `READ IN FULL` | Fetched and read end to end. |
| `FETCHED, NOT READ` | Have the file, skimmed it. Do not build on details. |
| `LOCATED ONLY` | URL confirmed reachable. **Content UNVERIFIED.** |
| `CITED, UNREAD` | Named by number only, never opened. The honest level for a paid standard. |
| `GATED, UNREAD` | Paywalled or login walled. Cannot access. No content used. |

A `LOCATED ONLY` row is welcome here. A `LOCATED ONLY` row dressed as a `TRACED` one is the thing
this repo exists to not be.

**The failure this guards against is not laziness, and that is worth being precise about.** It is a
row citing revision C while linking revision A. Real document, working link, wrong number, and
nothing about the row looks broken. The person who finds out is a tech standing in front of the
equipment, and by then the catalog has already cost them the thing it promised to save.

## What this is

A bookmark folder is not a source of truth. Neither is a pile of PDFs.

This is a **catalog**: one row per document, with the publisher's own document number and revision,
the canonical URL, a Wayback snapshot so the row survives the vendor deleting the file, the license
terms that actually apply, and a stated verification level. Around it sit notes that a link cannot
give you: which document you actually need, what is wrong with it, and what the vendor's manual does
not say.

**The links are the commodity. The notes are the repo.** Anyone can bookmark a Rockwell manual. The
value is knowing that the answer to most "RS485 will not talk" problems is in the serial line spec's
timing and biasing section rather than in the device manual, and that the manual for the obsolete
drive still running in your plant was deleted from the vendor's library the year it went obsolete,
which is why the snapshot column is mandatory here.

## Copyright, stated plainly

**This repo does not host other people's documents, with narrow and deliberate exceptions.**

Almost everything worth cataloguing here is free to download and not free to republish. Those are
different rights, and vendors are clear about the difference even when readers are not. "Free to
download" is not a license, and treating it as one is the single most common way a documentation
repo becomes a legal problem.

So `redistributable` defaults to `no` and is machine enforced. Setting it to `yes` requires naming
actual terms you can quote (`CC BY-SA 4.0`, `public domain`, `Apache 2.0`). `mirrors/` is gitignored
by default so a document file has to be force added on purpose, and `tools/check_mirrors.py` fails
the gate on any tracked file that no catalog row has cleared. What gets mirrored is US government
work, openly licensed vendor documentation, and nothing else.

Standards bodies stay where they belong. IEC, ISO, IEEE, UL, and NFPA documents are copyrighted and
sold. This repo cites them by number, links the free access viewers where they exist, describes their
scope, and paraphrases structure. **It does not reproduce their tables.** That is the same line
`power-service-toolbox` draws around NFPA 70E and the NETA acceptance testing specification, and it
is drawn in the same place for the same reason.

If you own something here and want it gone, see [POLICY.md](POLICY.md). It comes down without an
argument.

## Status

<!-- BEGIN GENERATED: status. Do not hand edit. Regenerate: ./tools/build_indexes.py -->

**86 documents catalogued. 6 of them have actually been opened by a human.**

That second number is the honest one, and it is generated from the catalog rather than claimed in prose, so it cannot flatter itself.

| | Count |
|---|---|
| `TRACED` | 6 |
| `READ IN FULL` | 0 |
| `FETCHED, NOT READ` | 0 |
| `LOCATED ONLY` | 78 |
| `CITED, UNREAD` | 0 |
| `GATED, UNREAD` | 2 |
| **snapshotted against link rot** | **17 of 86** |
| **mirrored locally (license cleared)** | **0** |

By domain:

| Domain | Documents |
|---|---|
| [instrumentation](domains/instrumentation/INDEX.md) | _none yet_ |
| [maintenance](domains/maintenance/INDEX.md) | _none yet_ |
| [plc-control](domains/plc-control/INDEX.md) | 17 |
| [power-distribution](domains/power-distribution/INDEX.md) | 17 |
| [protocols](domains/protocols/INDEX.md) | 28 |
| [robotics-motion](domains/robotics-motion/INDEX.md) | _none yet_ |
| [safety](domains/safety/INDEX.md) | 9 |
| [silicon](domains/silicon/INDEX.md) | 3 |
| [software-scada](domains/software-scada/INDEX.md) | _none yet_ |
| [standards](domains/standards/INDEX.md) | 12 |

<!-- END GENERATED: status. -->

## Scope, and the order of work

The backlog in [BACKLOG.md](BACKLOG.md) is long on purpose and it is a **wishlist, not a claim**. It
lives in a separate file from the catalog for exactly that reason: a catalog seeded with six hundred
empty rows reads as an abandoned project, because that is what it would be. A row enters the catalog
when it has a real URL and a real verification level, and not before.

Work goes depth first, one domain at a time, starting where the author has ground truth to check the
documents against rather than only the documents themselves. Breadth is what makes this a link dump.
Depth is what makes it a source of truth.

## Layout

    catalog/
      catalog.csv        THE PRODUCT. One row per document.
      SCHEMA.md          What each column means and why it is required.
    domains/<slug>/
      INDEX.md           Hand written notes on top, generated table underneath.
    notes/               Original content. Cheat sheets, decision trees, retrofit playbooks.
    mirrors/             License cleared documents only. Gitignored by default.
    tools/
      gate.sh            The three offline checks. This is the rule, as a command.
      check_catalog.py   No row claims more than it earned.
      check_mirrors.py   Nothing published that is not cleared.
      build_indexes.py   Renders every index from the catalog, so no index can drift.
      check_links.py     Which URLs rotted, which rows are unprotected. Network, not in the gate.
      archive.py         Snapshots exposed rows before the vendor deletes them.
      seed_catalog.py    Wrote the initial rows. Kept as a worked example of the schema.

## Checking it yourself

    ./tools/gate.sh

Three checks, offline, in about a second:

| Check | Because |
|---|---|
| catalog | a row that claims more than it earned is the one failure this repo cannot survive |
| mirrors | an undeclared PDF is a copyright problem that a `git add -A` creates silently |
| indexes | a status typed into prose is a copy, and a copy rots |

Incomplete rows do not fail the gate. Incorrect rows do. A catalog is incomplete by nature and always
will be, and a gate that goes red on day one and stays red teaches exactly one lesson, which is that
red means nothing here.

Link checking is deliberately outside the gate, because a check that needs the network flakes, and a
check that flakes gets bypassed, and a bypassed gate is worse than no gate: everyone still believes
the repo is checked.

## License

Split, because the two halves are different kinds of thing:

- **Catalog and notes**: CC BY-SA 4.0. Use them, build on them, share alike.
- **Tools**: AGPL 3.0, matching the author's other repos.
- **Mirrored documents**: whatever their own license says. See the `license` column. They are not
  the author's to relicense and this repo makes no claim over them.

Copyright in the original content is held by the author.
