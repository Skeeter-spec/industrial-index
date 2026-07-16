# The catalog schema

`catalog.csv` is the product. Everything else in this repo is either a checker that keeps it honest
or a note that adds something a link cannot.

One row per document. Sixteen columns, all required, empty allowed only where stated.

| Column | Meaning | Empty allowed |
|---|---|---|
| `id` | Stable slug, `vendor-docnumber-rev`. Never reused, never renumbered. Other files cite this. | no |
| `title` | The document's own title, transcribed, not paraphrased. | no |
| `vendor` | Publisher. `modbus.org`, `Rockwell Automation`, `NIST`. | no |
| `doc_number` | The publisher's number: `1756-UM001`, `SP 800-82r3`. `n/a` if genuinely none. | no |
| `revision` | The revision this row describes. `n/a` if unversioned. | no |
| `revision_date` | ISO date of that revision. Empty if the document does not state one. | yes |
| `category` | One of the `domains/` slugs. | no |
| `url` | Canonical publisher URL. Not a mirror, not a reseller, not a search result. | no |
| `archive_url` | Wayback snapshot. **The row is not done without this.** See below. | no |
| `license` | The terms the publisher actually grants. `unknown` is a real and common answer. | no |
| `redistributable` | `yes` or `no`. **Defaults to no.** `yes` requires a named license. | no |
| `license_basis` | How the licence is known: `DOCUMENT`, `STATUTE`, `UNVERIFIED`. Vocabulary below. | no |
| `local_path` | Path under `mirrors/`. Empty unless `redistributable=yes`. | yes |
| `sha256` | Hash of the mirrored file. Empty unless `local_path` is set. | yes |
| `verified_level` | How far this row was actually checked. Vocabulary below. | no |
| `verified_date` | ISO date of that check. | no |
| `notes` | Why a field tech would open this, or what is wrong with it. | yes |

## `verified_level`, and why it is copied from the toolbox

`power-service-toolbox/tools/check_sources.py` already worked out that "I checked" is worthless
without saying how far. That repo's problem was citations in prose. This repo's problem is the same
thing at a thousand times the volume, so the vocabulary carries over unchanged:

| Level | Means |
|---|---|
| `TRACED` | Fetched, read, and specific content confirmed to be what the row claims. |
| `READ IN FULL` | Fetched and read end to end. |
| `FETCHED, NOT READ` | Have the file, skimmed it. Do not build on details. |
| `LOCATED ONLY` | URL confirmed reachable. **Content UNVERIFIED.** |
| `CITED, UNREAD` | Named by number only, never opened. The honest level for a paid standard. |
| `GATED, UNREAD` | Paywalled or login walled. Cannot access. No content used. |

A new row starts at `LOCATED ONLY` and earns its way up. Nothing forbids a `LOCATED ONLY` row. What
is forbidden is a `LOCATED ONLY` row that reads like a `TRACED` one, which is exactly what a
confident bullet with a link looks like, and exactly what a research agent produces by default.

**The failure mode this column exists to catch is specific and it is not laziness.** It is citing
revision C while linking revision A. The document is real, the link works, the number is wrong, and
nothing about the row looks broken. Only someone who opened it knows.

## `archive_url`, and why it is required rather than nice to have

Vendor literature libraries delete things. Rockwell retires documents when a product goes obsolete,
which is precisely when a field tech needs the manual, because the obsolete equipment is still
racked and still running. A catalog of dead links is worse than no catalog: it is a promise that
wastes the reader's time at the moment they are least able to spare it.

So the snapshot is not a backup of the row. It **is** the row's durability, and a row without one is
not finished. `tools/check_links.py` reports canonical rot and snapshot presence separately, because
a rotted canonical with a live snapshot is a working row, and the opposite is a time bomb.

## `redistributable`, and why it defaults to no

Most of what belongs in this catalog is free to download and not free to republish. Those are
different rights and vendors are clear about the difference even when readers are not.

`yes` is a legal claim. It requires `license` to name actual terms (`CC BY-SA 4.0`, `public domain`,
`Apache 2.0`), never `unknown` and never `free to download`, which is not a license. The gate
enforces this rather than trusting anyone to remember it at 1am, which is the only time this repo
gets worked on.

## `license_basis`, and why naming the terms was not enough

`license` says WHAT the terms are. `license_basis` says HOW ANYONE KNOWS. Naming a licence is not
reading one, and for thirteen rows the answer to "how do you know" turned out to be "we assumed it
from the publisher's domain name."

| Basis | Means |
|---|---|
| `DOCUMENT` | The document grants it **in its own words**. `notes` carries the quote. |
| `STATUTE` | The document is **silent**. The claim rests on law: 17 USC 105, or the edicts doctrine. |
| `UNVERIFIED` | Nobody has checked. The default, and an **error** under `redistributable=yes`. |

`tools/check_license.py` reads a row's document at the publisher and reports which of these it earns.
It never edits the catalog and it does not rule on copyright: a regex has no business doing that.

**This is a different axis from `verified_level`, and conflating them is what went wrong.** Until
2026-07-16 the gate used `verified_level` as a proxy for whether the licence was known, flagging
`redistributable=yes` at `LOCATED ONLY` as "a legal claim on a document nobody has opened." That
proxy is wrong in both directions. You can read a manual end to end and never open its copyright
page. You can read only the copyright page and know the licence exactly while the content stays
unread, which is the true state of every row here that now says `DOCUMENT`. When those thirteen were
finally read, three carried an explicit written grant: the proxy had been nagging about rows that
were provably fine while saying nothing about the ones that were merely assumed.

It is the same bug the toolbox hit with provenance, where `TRACED` recorded how far a document was
read and said nothing about **whose copy**, and the fix there was the same: a machine checked column,
because the rule had already been written down and broken anyway.

**`STATUTE` is not a defect and the gate does not treat it as one.** Most public domain federal works
say nothing at all about their own terms, so demanding a written grant would delete good rows, which
is the direction a checker's findings always fall. It is worth attention rather than alarm: 17 USC
105 reaches works of federal **employees**, and does not reach a contractor's manuscript or a
copyrighted table reprinted by permission inside an otherwise public domain report. TM 5-811-14 is a
public domain Army document **except** the asterisked paragraph reprinting IEEE 242, and the
asterisked paragraph is always the one someone wants. A licence is not uniform across a document.

**`UNVERIFIED` under a `yes` is an error, not a warning, and that is the whole point of the column.**
This repo has already shipped a row whose own note said "verify this licence before trusting
redistributable=yes" with the yes still in it, and the yes was wrong. A gate line reading
"unfinished" beside a published legal claim is that same note wearing a checker's uniform. A recorded
doubt is not a check. It is the alibi that lets the claim ship.
