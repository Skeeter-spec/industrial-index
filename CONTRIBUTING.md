# Contributing

The useful contribution here is **a row that is true**, or a note that took you a bad afternoon to
learn. Volume is not the goal and never was: this catalog is competing with a search engine, and it
loses that fight on breadth and wins it on trust.

## Adding a document

1. Add a row to `catalog/catalog.csv`. Every column, per [`catalog/SCHEMA.md`](catalog/SCHEMA.md).
2. Set `verified_level` to **what you actually did**. If you found the URL and did not open the file,
   that is `LOCATED ONLY`, and it is a welcome row. Nothing here is embarrassed by `LOCATED ONLY`.
3. Run `./tools/archive.py` so the row has a snapshot. A row without one is not finished.
4. Run `./tools/gate.sh`. It must pass.

The one unforgivable thing is a row claiming a level it did not earn. Everything else is fixable by
the next person; that one is not, because it is invisible. A `LOCATED ONLY` row marked `TRACED` looks
exactly like a good row, forever, until it costs someone standing in front of the equipment.

Do not paste in a list of documents you have not verified. Put it in [`BACKLOG.md`](BACKLOG.md),
which exists for exactly that and is honest about what it is.

### If an LLM helped you produce the row

Say so in the PR, and set the level to what **you** checked, not what it told you.

A language model's failure mode here is not a wrong answer, it is a confident, correctly formatted,
entirely fabricated citation with a plausible document number and a URL that looks right. That
artifact is undetectable downstream and it is lethal to this repo specifically, because trust is the
only thing the catalog sells. If neither you nor the model opened it, the level is `LOCATED ONLY`
at best, and if the URL was never fetched, the row does not go in at all.

## Clearing a document for mirroring

Read [`mirrors/README.md`](mirrors/README.md) first. Short version: `redistributable=yes` is a legal
claim, it needs terms you can quote, and "free to download" is not a license. In practice the answer
is almost always no, and the catalog row serves the reader nearly as well.

## Adding a note

See [`notes/README.md`](notes/README.md). Write it longhand from understanding. Do not reproduce
copyrighted text, and do not reproduce standards tables, paraphrased or otherwise.

If a note can be replaced by a link, make it a link.

## Requesting a document

Open an issue titled `DOC REQUEST: <what you need>`. Say what equipment, what you are trying to do,
and what you already tried. A request that names the problem is more useful than one that names a
document, because the document you asked for is often not the one that answers it, and that gap is
the most interesting content this repo has.

## Reporting a bad row

Open an issue. Wrong revision, wrong document number, dead link with no snapshot, a level that looks
inflated. **A row that overclaims is a bug of the highest severity here**, and reporting one is the
single most valuable thing you can do for this repo.

## Style

Prose here does not use the `-` character: no em dashes, no hyphenated compounds. Identifiers, URLs,
document numbers, and code are exempt, so `1756-UM001`, `IEC 61131-3`, and `4-20 mA` are correct as
written. This is a house style, and it is applied to the writing, not to the facts.
